#!/usr/bin/env python3
"""Hifeniza, renderiza e confere o jornal.

Uso:
  python3 render.py <pasta_com_index.html> <saida.pdf> [--lang pt-BR] [--png]

O que faz:
  1. Copia as fontes da skill para <pasta>/build/fonts.
  2. Insere hifenização suave (&shy;) no texto com pyphen — o Chromium no
     Linux não hifeniza português sozinho, e sem isso colunas justificadas
     estreitas ficam cheias de buracos.
  3. Gera o PDF A4 com Playwright/Chromium (printBackground, margens 12 mm).
  4. Mede cada .col de cada .page e avisa se o conteúdo passou do limite
     (o .page tem overflow:hidden, então o texto que vaza some calado).
  5. Informa o número de páginas e, com --png, gera prévias PNG.
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
        shutil.copy(src, dst); print(f"[aviso] sem dicionário de hifenização para {lang}; seguindo sem"); return
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


MEASURE = """() => [...document.querySelectorAll('.page')].map(pg => {
  const P = pg.getBoundingClientRect();
  const stop = pg.querySelector('.fontes') || pg.querySelector('.foot');
  const limit = stop ? stop.getBoundingClientRect().top - P.top : P.height;
  const cols = [...pg.querySelectorAll('.col')].map(c => {
    let m = 0; c.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height > 0) m = Math.max(m, r.bottom - P.top); });
    return Math.round(m);
  });
  const wide = Math.round(pg.scrollWidth - pg.clientWidth);
  return {page: pg.id || '?', limit: Math.round(limit), cols, wide};
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
    shutil.copytree(FONTS, os.path.join(build, "fonts"), dirs_exist_ok=True)
    hyphenate(os.path.join(work, "index.html"), os.path.join(build, "index.html"), lang)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + os.path.join(build, "index.html"))
        pg.wait_for_timeout(800)
        info = pg.evaluate(MEASURE)
        pg.pdf(path=out, format="A4", print_background=True,
               margin=dict(top="12mm", bottom="12mm", left="12mm", right="12mm"))
        b.close()

    ok = True
    for i in info:
        over = [c - i["limit"] for c in i["cols"]]
        status = ", ".join(f"col{n+1}: {'+' if o > 0 else ''}{o}px" for n, o in enumerate(over))
        print(f"{i['page']}: limite {i['limit']}px | {status}" + (f" | ESTOURO LATERAL {i['wide']}px" if i["wide"] > 0 else ""))
        if any(o > 0 for o in over) or i["wide"] > 0:
            ok = False
    pages = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
    n = re.search(r"Pages:\s+(\d+)", pages)
    n = int(n.group(1)) if n else -1
    print(f"Páginas: {n}")
    if n > 2:
        ok = False
    if "--png" in sys.argv:
        prefix = os.path.join(build, "preview")
        subprocess.run(["pdftoppm", "-r", "80", "-png", out, prefix])
        print("Prévias:", ", ".join(sorted(f for f in os.listdir(build) if f.startswith("preview"))))
    print("OK" if ok else "AJUSTAR: conteúdo vazando (valores positivos) ou mais de 2 páginas")


if __name__ == "__main__":
    main()
