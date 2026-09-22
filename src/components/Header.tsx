import Link from "next/link";
import { nav, site } from "@/content/site";

export default function Header() {
  return (
    <header className="border-b border-brand-dark bg-brand/95 backdrop-blur sticky top-0 z-40 text-paper">
      <div className="container-page flex items-center justify-between py-4">
        <Link href="/" className="flex items-center gap-3 group">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-paper text-brand font-serif text-sm">
            M
          </span>
          <span className="flex flex-col leading-tight">
            <span className="font-serif text-base text-paper group-hover:text-tint transition-colors">
              {site.name}
            </span>
            <span className="text-xs text-tint/80 tracking-wide uppercase">{site.title}</span>
          </span>
        </Link>
        <nav className="hidden md:flex items-center gap-8 text-sm">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-tint/90 hover:text-paper transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <details className="md:hidden group">
          <summary className="list-none cursor-pointer text-tint/90 hover:text-paper transition-colors">
            Menu
          </summary>
          <nav className="absolute inset-x-0 top-full flex flex-col gap-1 border-b border-brand-dark bg-brand-dark px-6 py-4 text-sm shadow-sm">
            {nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="py-2 text-tint/90 hover:text-paper transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </details>
      </div>
    </header>
  );
}
