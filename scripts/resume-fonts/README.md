# Resume font embedding

`public/resume/Mitchell-Palmer-Resume.odt` is kept **without** embedded
fonts on purpose — that's the editable master, and embedding fonts
there only bloats the file for no benefit (your own machine already has
the real fonts installed).

The problem: exporting that file to `.docx`/`.pdf` on a machine that
*doesn't* have those fonts installed silently substitutes a generic
font, and the resume loses its look. `embed_fonts.py` fixes this at
export time without ever touching the source file.

## Usage

```bash
python3 scripts/resume-fonts/embed_fonts.py \
  public/resume/Mitchell-Palmer-Resume.odt \
  /tmp/embedded.odt \
  --to-pdf public/resume/Mitchell-Palmer-Resume.pdf \
  --to-docx public/resume/Mitchell-Palmer-Resume.docx
```

This reads whichever fonts the `.odt` actually declares, embeds any it
recognizes from the local `fonts/` cache, and tries to fetch any
Google Font it doesn't have yet from the official
[google/fonts](https://github.com/google/fonts) repo (all OFL-licensed,
safe to cache and re-embed). It never fails hard — anything it can't
resolve (e.g. a proprietary font) is reported and left alone, same as
today's unembedded behavior.

Run it again whenever the resume content changes and you need a fresh
`.docx`/`.pdf`.

## What's viable going forward

- **Content and layout changes** (wording, bullets, sections, tables,
  structure) never affect this — the script only cares about which
  *fonts* are declared, not what the document looks like.
- **New open-source (Google) fonts** are handled automatically — the
  script fetches and caches them on first use.
- **New proprietary fonts** (anything not on Google Fonts) are the one
  real limit: the script will report it as unresolved, and either the
  actual font file needs to be supplied, or it renders with the
  substitute LibreOffice picks.

## Files

- `manifest.json` — which fonts are cached, which files, which weights.
- `fonts/<Family>/*.ttf` — the cached static font files themselves.

Currently covers the three fonts actually used in the resume: Lexend
(incl. the ExtraBold weight used in the name header), Merriweather,
and Open Sans. (Trebuchet MS was declared in the original template but
is not actually applied to any visible text, so it's not included.)
