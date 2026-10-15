#!/usr/bin/env python3
"""Hyphenate, render and check the newspaper.

Usage:
  python3 render.py <folder_with_index.html> <output.pdf> [--lang pt-BR] [--png]

What it does:
  1. Copies assets/fonts into <folder>/build/fonts, if present (the default
     template embeds its fonts as base64, so this is usually a no-op).
  2. Inserts soft hyphens (&shy;) into the text with pyphen. Chromium on Linux
     doesn't hyphenate Portuguese or Spanish on its own, and narrow justified
     columns end up full of gaps without this.
  3. Renders an A4 PDF with Playwright/Chromium (printBackground, page size and
     margins taken from the template's CSS).
  4. Measures every .col on every .page and warns if content goes past the limit
     (.page has overflow:hidden, so overflowing text silently disappears).
  5. Reports the page count and, with --png, writes PNG previews.
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "assets", "fonts")
LANG_MAP = {"pt": "pt_BR", "pt-br": "pt_BR", "pt-pt": "pt_PT", "en": "en_US",
            "en-us": "en_US", "en-gb": "en_GB", "es": "es", "fr": "fr", "it": "it_IT", "de": "de_DE"}


def ensure(pkg, mod=None):
    try:
        __import__(mod or pkg)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg, "--break-system-packages"], check=False)


def hyphenate(src, dst, lang):
    ensure("pyphen"); ensure("beautifulsoup4", "bs4")
    import pyphen
    from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
    code = LANG_MAP.get(lang.lower(), lang.replace("-", "_"))
    if code not in pyphen.LANGUAGES:
        shutil.copy(src, dst); print(f"[warning] no hyphenation dictionary for {lang}; continuing without it"); return
    d = pyphen.Pyphen(lang=code)
    soup = BeautifulSoup(open(src, encoding="utf-8").read(), "html.parser")
    skip = {"style", "script", "title", "h1", "h2", "h3", "h4", "th"}
    for t in list(soup.find_all(string=True)):
        if isinstance(t, (Comment, Doctype)):
            continue
        if any(p.name in skip for p in t.parents):
            continue
        if any("nameplate" in (p.get("class") or []) or "np" in (p.get("class") or []) for p in t.parents if hasattr(p, "get")):
            continue
        new = re.sub(r"[A-Za-zÀ-ÿ]{7,}", lambda m: d.inserted(m.group(0), hyphen="­"), str(t))
        t.replace_with(NavigableString(new))
    open(dst, "w", encoding="utf-8").write(str(soup))


MEASURE = """() => [...document.querySelectorAll('.page')].map((pg, idx) => {
  const P = pg.getBoundingClientRect();
  const stop = pg.querySelector('.sources') || pg.querySelector('.foot') || pg.querySelector('.pgfoot');
  const limit = stop ? stop.getBoundingClientRect().top - P.top : P.height;
  const cols = [...pg.querySelectorAll('.col')].map(c => {
    let m = 0; c.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height > 0) m = Math.max(m, r.bottom - P.top); });
    return Math.round(m);
  });
  const wide = Math.round(pg.scrollWidth - pg.clientWidth);
  return {page: pg.id || ('p' + (idx + 1)), limit: Math.round(limit), cols, wide};
})"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    work, out = os.path.abspath(args[0]), os.path.abspath(args[1])
    lang = "pt-BR"
    if "--lang" in sys.argv:
        lang = sys.argv[sys.argv.index("--lang") + 1]
        args = [a for a in args if a != lang]
    build = os.path.join(work, "build")
    os.makedirs(build, exist_ok=True)
    if os.path.isdir(FONTS):
        shutil.copytree(FONTS, os.path.join(build, "fonts"), dirs_exist_ok=True)
    hyphenate(os.path.join(work, "index.html"), os.path.join(build, "index.html"), lang)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + os.path.join(build, "index.html"))
        pg.wait_for_timeout(800)
        info = pg.evaluate(MEASURE)
        # The template sets @page{size:A4;margin:0} and pads each .page itself.
        pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True,
               margin=dict(top="0", bottom="0", left="0", right="0"))
        b.close()

    ok = True
    for i in info:
        over = [c - i["limit"] for c in i["cols"]]
        status = ", ".join(f"col{n+1}: {'+' if o > 0 else ''}{o}px" for n, o in enumerate(over))
        print(f"{i['page']}: limit {i['limit']}px | {status}" + (f" | HORIZONTAL OVERFLOW {i['wide']}px" if i["wide"] > 0 else ""))
        if any(o > 0 for o in over) or i["wide"] > 0:
            ok = False
    pages = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
    n = re.search(r"Pages:\s+(\d+)", pages)
    n = int(n.group(1)) if n else -1
    print(f"Pages: {n}")
    if n > 2:
        ok = False
    if "--png" in sys.argv:
        prefix = os.path.join(build, "preview")
        subprocess.run(["pdftoppm", "-r", "80", "-png", out, prefix])
        print("Previews:", ", ".join(sorted(f for f in os.listdir(build) if f.startswith("preview"))))
    print("OK" if ok else "FIX: content overflowing (positive values) or more than 2 pages")


if __name__ == "__main__":
    main()
