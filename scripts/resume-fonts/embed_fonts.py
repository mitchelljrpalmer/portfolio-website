#!/usr/bin/env python3
"""
embed_fonts.py — re-embed brand fonts into a copy of the resume .odt
before exporting to .docx/.pdf, so the export renders correctly
regardless of what fonts are installed on the machine doing it.

Why this exists: public/resume/Mitchell-Palmer-Resume.odt is kept
WITHOUT embedded fonts (that's the user's day-to-day editing copy —
embedding fonts there just bloats the file with no benefit, since their
own machine has the real fonts installed). But whatever machine runs
`soffice --convert-to docx/pdf` needs the actual font files, or it
silently substitutes a generic font and the resume loses its look.

This script never touches the source file. It reads whichever fonts
the document's <style:font-face> declarations actually name, embeds
any it has a local copy of (see manifest.json / fonts/), and tries to
fetch any Google Font it doesn't yet have cached from the official
google/fonts GitHub repo (OFL-licensed, safe to cache and re-embed).
Anything it can't resolve (e.g. a proprietary font) is left alone and
reported, exactly like today's un-embedded behavior — never a hard
failure.

Usage:
    python3 embed_fonts.py INPUT.odt OUTPUT.odt
    python3 embed_fonts.py INPUT.odt OUTPUT.odt --to-pdf OUTPUT.pdf --to-docx OUTPUT.docx

Only needs the Python standard library plus `soffice` on PATH if
--to-pdf/--to-docx are used.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"
FONTS_DIR = HERE / "fonts"

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "loext": "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(prefix, local):
    return f"{{{NS[prefix]}}}{local}"


def base_family(name: str) -> str:
    """'Lexend1' / 'Open Sans1' -> 'Lexend' / 'Open Sans' (ODF duplicates
    font-face decls per script type, usually suffixed with a trailing '1')."""
    return re.sub(r"1$", "", name) if name not in ("", None) else name


def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def try_fetch_from_google_fonts(family_entry: dict, family_dir_name: str) -> bool:
    """Best-effort: pull static TTFs for a Google Font family we don't have
    cached yet, from the official google/fonts GitHub repo (OFL/static or
    apache/static dirs). Returns True if it found and cached at least one
    file. Silently returns False on any network/lookup failure — callers
    treat that the same as 'font not available', never a hard error."""
    gf_dir = family_entry.get("google_fonts_dir")
    if not gf_dir:
        return False
    license_dirs = ["ofl", "apache", "ufl"]
    for lic in license_dirs:
        api_url = f"https://api.github.com/repos/google/fonts/contents/{lic}/{gf_dir}/static"
        try:
            with urllib.request.urlopen(api_url, timeout=8) as resp:
                listing = json.loads(resp.read())
        except Exception:
            continue
        if not isinstance(listing, list):
            continue
        fetched_any = False
        dest_dir = FONTS_DIR / family_entry["_display_name"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        for item in listing:
            name = item.get("name", "")
            if not name.lower().endswith(".ttf"):
                continue
            download_url = item.get("download_url")
            if not download_url:
                continue
            try:
                with urllib.request.urlopen(download_url, timeout=15) as r:
                    data = r.read()
                (dest_dir / name).write_bytes(data)
                fetched_any = True
            except Exception:
                continue
        if fetched_any:
            print(f"  fetched {family_entry['_display_name']} static files from google/fonts ({lic}/{gf_dir})")
            return True
    return False


def collect_font_faces(root) -> dict:
    """Map style:name -> element, across every office:font-face-decls block."""
    out = {}
    for ff in root.iter(q("style", "font-face")):
        name = ff.get(q("style", "name"))
        out[name] = ff
    return out


def has_embedded_src(ff_elem) -> bool:
    return ff_elem.find(q("svg", "font-face-src")) is not None


def build_font_face_src(variants, family_key_in_manifest) -> ET.Element:
    src = ET.Element(q("svg", "font-face-src"))
    for v in variants:
        uri = ET.SubElement(src, q("svg", "font-face-uri"))
        uri.set(q("xlink", "href"), f"Fonts/{Path(v['file']).name}")
        uri.set(q("xlink", "type"), "simple")
        uri.set(q("loext", "font-style"), "italic" if v["italic"] else "normal")
        uri.set(q("loext", "font-weight"), v["weight"])
        fmt = ET.SubElement(uri, q("svg", "font-face-format"))
        fmt.set("{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}string", "truetype")
    return src


def process_xml_file(path: Path, manifest: dict, needed_files: set, resolved: set, unresolved: set):
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False
    for name, ff_elem in collect_font_faces(root).items():
        if has_embedded_src(ff_elem):
            continue
        fam = base_family(name)
        skip_notes = manifest.get("skip_no_embed_needed", {})
        if name in skip_notes or fam in skip_notes:
            continue  # deliberately left unembedded -- see manifest.json for why
        entry = manifest["families"].get(name) or manifest["families"].get(fam)
        if entry is None:
            if fam not in manifest.get("known_unused_in_document", []) and name not in manifest.get("known_unused_in_document", []):
                unresolved.add(name)
            continue
        display_name = fam if fam in manifest["families"] else name
        entry = dict(entry)
        entry["_display_name"] = display_name

        # Make sure we actually have the files; try fetching if not.
        missing = [v for v in entry["variants"] if not (FONTS_DIR / v["file"]).exists()]
        if missing and entry.get("source") == "google-fonts":
            try_fetch_from_google_fonts(entry, display_name)
            missing = [v for v in entry["variants"] if not (FONTS_DIR / v["file"]).exists()]
        if missing:
            unresolved.add(name)
            continue

        src_elem = build_font_face_src(entry["variants"], name)
        ff_elem.append(src_elem)
        for v in entry["variants"]:
            needed_files.add(v["file"])
        resolved.add(name)
        changed = True
    if changed:
        tree.write(path, encoding="UTF-8", xml_declaration=True)
    return changed


def set_embed_fonts_flag(settings_path: Path):
    if not settings_path.exists():
        return
    s = settings_path.read_text(encoding="utf-8")
    s2 = s.replace(
        'EmbedFonts" config:type="boolean">false<',
        'EmbedFonts" config:type="boolean">true<',
    )
    if s2 != s:
        settings_path.write_text(s2, encoding="utf-8")


def add_manifest_entries(manifest_xml_path: Path, font_filenames: list):
    s = manifest_xml_path.read_text(encoding="utf-8")
    entries = "".join(
        f'<manifest:file-entry manifest:full-path="Fonts/{fn}" manifest:media-type="application/x-font-ttf"/>'
        for fn in font_filenames
    )
    s = s.replace("</manifest:manifest>", entries + "</manifest:manifest>")
    manifest_xml_path.write_text(s, encoding="utf-8")


def repack_odt(src_dir: Path, out_path: Path):
    if out_path.exists():
        out_path.unlink()
    with zipfile.ZipFile(out_path, "w") as zf:
        # mimetype must be first and stored uncompressed, per ODF spec
        zf.write(src_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(src_dir.rglob("*")):
            if p.is_dir() or p.name == "mimetype":
                continue
            rel = p.relative_to(src_dir).as_posix()
            zf.write(p, rel, compress_type=zipfile.ZIP_DEFLATED)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input_odt", type=Path)
    ap.add_argument("output_odt", type=Path)
    ap.add_argument("--to-pdf", type=Path, help="also export the result to this .pdf path")
    ap.add_argument("--to-docx", type=Path, help="also export the result to this .docx path")
    args = ap.parse_args()

    manifest = load_manifest()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(args.input_odt) as zf:
            zf.extractall(tmp)

        needed_files, resolved, unresolved = set(), set(), set()
        for xml_name in ("content.xml", "styles.xml"):
            p = tmp / xml_name
            if p.exists():
                process_xml_file(p, manifest, needed_files, resolved, unresolved)

        if needed_files:
            dest = tmp / "Fonts"
            dest.mkdir(exist_ok=True)
            filenames = []
            for rel in needed_files:
                src = FONTS_DIR / rel
                dst = dest / Path(rel).name
                shutil.copy2(src, dst)
                filenames.append(Path(rel).name)
            add_manifest_entries(tmp / "META-INF" / "manifest.xml", filenames)
            set_embed_fonts_flag(tmp / "settings.xml")

        repack_odt(tmp, args.output_odt)

    print(f"Wrote {args.output_odt}")
    print(f"  embedded: {sorted(resolved) or '(none needed — already embedded or none declared)'}")
    if unresolved:
        print(f"  COULD NOT RESOLVE: {sorted(unresolved)}  <- these will render with a substitute font")

    if args.to_pdf or args.to_docx:
        for fmt, out in (("pdf", args.to_pdf), ("docx", args.to_docx)):
            if not out:
                continue
            with tempfile.TemporaryDirectory() as outdir:
                subprocess.run(
                    ["soffice", "--headless", "--convert-to", fmt, "--outdir", outdir, str(args.output_odt)],
                    check=True, capture_output=True,
                )
                produced = Path(outdir) / (args.output_odt.stem + f".{fmt}")
                shutil.copy2(produced, out)
            print(f"  exported {out}")


if __name__ == "__main__":
    sys.exit(main())
