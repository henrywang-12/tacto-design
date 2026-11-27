#!/usr/bin/env python3
"""inline.py - turn your HTML into one self-contained, branded file.

    python3 scripts/inline.py in.html out.html
    python3 scripts/inline.py in.html out.html --no-brand
    python3 scripts/inline.py in.html out.html --allow-missing   (missing images only warn)
    python3 scripts/inline.py in.html out.html --keep-comments   (leave build comments in)

What it does:
1. Inlines tacto.css, with its fonts, and the scripts a page links: tacto.js,
   tacto-scroll.js, tacto-3d.js and three.min.js (found next to the input, in this
   skill's assets/ or in assets/vendor/).
2. Applies the private brand, if this installation has one (brand.local/brand.json):
   every wordmark that carries the brand's name or a template sample name, and
   every <span data-tc-logo></span>, becomes the real logo. Dark and white
   versions are both embedded; tacto.css shows the right one for the background.
   Force one with data-tc-logo="dark" or data-tc-logo="white".
3. Embeds local images (<img src="customer.svg">, url(...) in styles) as data
   URIs, so customer logos travel inside the file. Bare filenames are also
   looked up in ./logos/ and in brand.local/customers/.

4. Removes the build comments (template instructions, the stylesheet's commentary), so the
   file that is handed over says nothing about how it was made.

Then it checks its own work. It exits with code 1, and says why, when the
result would be broken once sent: tacto.css still linked, a logo placeholder left
unfilled, an image that could not be found. HTML comments are left untouched.

Nothing is fetched at view time: Aspekta, Geist Mono and (for product screens)
Inter are embedded from assets/fonts/, all open source. Only the icons a file
uses stay in its stylesheet.
"""
import base64
import html as htmllib
import json
import mimetypes
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
BRAND_DIR = ROOT / "brand.local"
PLACEHOLDER_NAMES = {"northdesk", "your company", "yourcompany"}
COMMENT = re.compile(r"(<!--.*?-->)", re.S)


def outside_comments(text: str, fn) -> str:
    """Apply fn to the parts of the document that are not inside HTML comments."""
    parts = COMMENT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = fn(parts[i])
    return "".join(parts)


def find(ref: str, base: Path) -> Path:
    ref = ref.split("?")[0].split("#")[0]
    for candidate in (base / ref, ASSETS / Path(ref).name, ASSETS / "vendor" / Path(ref).name):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"cannot find {ref} (looked next to the input and in {ASSETS})")


def load_brand():
    cfg = BRAND_DIR / "brand.json"
    if not cfg.is_file():
        return None
    brand = json.loads(cfg.read_text(encoding="utf-8"))
    dark = BRAND_DIR / brand.get("logo", "logo.svg")
    white = BRAND_DIR / brand.get("logo_white", "logo-white.svg")
    if not dark.is_file():
        return None
    brand["_dark"] = dark.read_text(encoding="utf-8")
    brand["_white"] = white.read_text(encoding="utf-8") if white.is_file() else None
    return brand


def prep_svg(svg: str, cls: str, uid: str, recolour: bool) -> str:
    svg = re.sub(r"<\?xml.*?\?>|<!DOCTYPE.*?>|<!--.*?-->", "", svg, flags=re.S).strip()
    head = re.match(r"<svg\b[^>]*>", svg)
    if not head:
        return ""
    tag = re.sub(r'\s(?:width|height|class)="[^"]*"', "", head.group(0))
    tag = tag[:-1] + f' class="{cls}" aria-hidden="true">'
    body = svg[head.end():]
    if recolour:  # a single-colour logo follows the text colour (ink on white)
        body = re.sub(r'fill="#(?:000|000000|030712)"', 'fill="currentColor"', body, flags=re.I)
    for ident in set(re.findall(r'\bid="([^"]+)"', body)):  # keep ids unique when the logo repeats
        body = body.replace(f'id="{ident}"', f'id="{ident}-{uid}"').replace(f"url(#{ident})", f"url(#{ident}-{uid})")
    return tag + body


class Brander:
    WORDMARK = re.compile(
        r"""(<(a|span|div)\b[^>]*\bclass\s*=\s*(["'])[^"']*\btc-wordmark\b[^"']*\3[^>]*>)   # opening tag
            (?:\s|&nbsp;)*<(?:span|i|b)\b[^>]*\btc-wordmark__mark\b[^>]*(?:/>|>\s*</(?:span|i|b)>)   # the neutral mark
            ((?:(?!</\2>).)*?)                                                               # the name
            (</\2>)""", re.S | re.X)
    PLACEHOLDER = re.compile(r"""<(span|div|a)\b[^>]*\bdata-tc-logo\b[^>]*?(?:/>|>\s*</\1>)""", re.S)

    def __init__(self, brand):
        self.brand, self.count = brand, 0
        self.names = PLACEHOLDER_NAMES | {brand.get("name", "").lower()} | {n.lower() for n in brand.get("aliases", [])}

    def logo(self, force: str = "", style: str = "") -> str:
        self.count += 1
        uid = f"tc{self.count}"
        dark = prep_svg(self.brand["_dark"], "tc-logo__dark", uid + "d", True)
        white = prep_svg(self.brand["_white"], "tc-logo__white", uid + "w", False) if self.brand["_white"] else ""
        attr = f' data-tc-logo="{force}"' if force in ("dark", "white") else ""
        if style:
            attr += f' style="{style}"'
        name = htmllib.escape(self.brand.get("name", ""), quote=True)
        return f'<!-- tc-lint-off --><span class="tc-logo"{attr} role="img" aria-label="{name}">{dark}{white}</span><!-- tc-lint-on -->'

    @staticmethod
    def plain(fragment: str) -> str:
        return htmllib.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\xa0", " ").strip()

    def apply(self, text: str) -> str:
        def explicit(m):
            tag = m.group(0)
            force = re.search(r"""data-tc-logo\s*=\s*["'](dark|white)["']""", tag)
            style = re.search(r'\bstyle\s*=\s*"([^"]*)"', tag) or re.search(r"\bstyle\s*=\s*'([^']*)'", tag)
            return self.logo(force.group(1) if force else "", style.group(1) if style else "")

        def wordmark(m):
            if self.plain(m.group(4)).lower() not in self.names:
                return m.group(0)  # someone else's name: leave it alone
            return m.group(1) + self.logo() + m.group(5)

        def run(part):
            part = self.PLACEHOLDER.sub(explicit, part)
            return self.WORDMARK.sub(wordmark, part)
        return outside_comments(text, run)

    def leftovers(self, text: str) -> int:
        """Wordmarks that should have become the logo but did not match the pattern."""
        body = COMMENT.sub("", text)
        left = 0
        for m in re.finditer(r"tc-wordmark__mark\b[^>]*(?:/>|>\s*</(?:span|i|b)>)\s*((?:<[^>]+>|[^<])*?)</(?:a|span|div)>", body, flags=re.S):
            if self.plain(m.group(1)).lower() in self.names:
                left += 1
        return left


def embed_images(text: str, base: Path):
    count, missing = 0, []

    def data_uri(src: str):
        nonlocal count
        if re.match(r"(?:https?:|data:|//|#)", src) or not src.strip():
            return None
        clean = src.split("?")[0].split("#")[0]
        for candidate in (base / clean, base / "logos" / Path(clean).name, BRAND_DIR / "customers" / Path(clean).name):
            if candidate.is_file():
                mime = "image/svg+xml" if candidate.suffix.lower() == ".svg" else (mimetypes.guess_type(candidate.name)[0] or "application/octet-stream")
                count += 1
                return f"data:{mime};base64," + base64.b64encode(candidate.read_bytes()).decode("ascii")
        missing.append(src)
        return None

    def img(m):
        uri = data_uri(m.group(3))
        return f"{m.group(1)}{m.group(2)}{uri}{m.group(2)}" if uri else m.group(0)

    def css_url(m):
        if not re.search(r"\.(?:svg|png|jpe?g|webp|gif)(?:[?#].*)?$", m.group(2), flags=re.I):
            return m.group(0)
        uri = data_uri(m.group(2))
        return f'url("{uri}")' if uri else m.group(0)

    def run(part):
        part = re.sub(r"""(<img\b[^>]*?\bsrc\s*=\s*)(["'])([^"']+)\2""", img, part, flags=re.S)
        return re.sub(r"""url\(\s*(["']?)([^"')]+)\1\s*\)""", css_url, part)

    return outside_comments(text, run), count, missing


def prune_icons(css: str, doc: str) -> str:
    """Keep only the icons the document names (in markup or in a script), so a page does not carry all of them."""
    def keep(m):
        return m.group(0) if re.search(r"""["'=]""" + re.escape(m.group(1)) + r"""["'\s>]""", doc) else ""
    return re.sub(r"""\[data-tc-icon="([\w-]+)"\] \{[^}]*\}\n""", keep, css)


def embed_fonts(css: str, css_dir: Path, app: bool = True) -> str:
    """Aspekta and Geist Mono travel inside the file, so it reads the same offline.
    Inter is the product screen's typeface: it is embedded only when the page has one."""
    if not app:
        css = re.sub(r"""@font-face \{ font-family: "Inter";[^}]*\}\n?""", "", css)
    def font(m):
        f = css_dir / m.group(2)
        if not f.is_file():
            f = ASSETS / m.group(2)   # tacto.css was copied next to the input without its fonts
        if not f.is_file():
            return m.group(0)
        mime = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf"}[f.suffix.lower()]
        return f'url("data:{mime};base64,' + base64.b64encode(f.read_bytes()).decode("ascii") + '")'
    return re.sub(r"""url\(\s*(["']?)(fonts/[^"')]+\.(?:woff2?|ttf|otf))\1\s*\)""", font, css)


def strip_comments(text: str) -> str:
    """The file that is handed over carries no build notes: template instructions, the stylesheet's
    commentary and the scripts' headers stay behind. Kept: the lint markers around a logo, licence
    notices, and one short marker per block so the lint still recognises the system's own code."""
    def style(m):
        body = re.sub(r"/\*.*?\*/", "", m.group(2), flags=re.S)
        body = re.sub(r"\n\s*\n+", "\n", body)
        return m.group(1) + "\n/* tc-style */" + body + m.group(3) if "--tc-black" in body else m.group(0)

    def script(m):
        body = m.group(2)
        if "tacto-design:" in body[:200] or "tacto.js" in body[:200]:
            body = "\n/* tc-script */\n" + re.sub(r"^\s*/\*.*?\*/", "", body, count=1, flags=re.S).lstrip()
        return m.group(1) + body + m.group(3)

    text = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", style, text, flags=re.S)
    text = re.sub(r"(<script\b[^>]*>)(.*?)(</script>)", script, text, flags=re.S)
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", text, flags=re.S)
    for i in range(0, len(parts), 2):          # only between scripts and styles
        parts[i] = re.sub(r"<!--(?!\s*tc-lint-(?:off|on)\b).*?-->\n?", "", parts[i], flags=re.S)
    return "".join(parts)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    src, out = Path(args[0]), Path(args[1])
    if not src.is_file():
        print(f"inline.py: no such file: {src}", file=sys.stderr)
        return 2
    if not out.resolve().parent.is_dir():
        print(f"inline.py: the output folder does not exist: {out.resolve().parent}", file=sys.stderr)
        return 2
    text = src.read_text(encoding="utf-8")
    base = src.resolve().parent
    problems = []
    counts = {"css": 0, "js": 0}

    def swap(kind, open_tag, close_tag):
        def repl(match):
            try:
                found = find(match.group(2), base)
                body = found.read_text(encoding="utf-8")
            except FileNotFoundError as e:
                problems.append(str(e))
                return match.group(0)
            if kind == "css":
                body = prune_icons(body, text)
                body = embed_fonts(body, found.resolve().parent, "tc-app" in text)
            counts[kind] += 1
            return f"{open_tag}\n{body}\n{close_tag}"
        return repl

    def bundle(part):
        part = re.sub(r"""<link\b[^>]*\bhref\s*=\s*(["'])([^"']*\btacto\.css(?:[?#][^"']*)?)\1[^>]*>""", swap("css", "<style>", "</style>"), part)
        return re.sub(r"""<script\b[^>]*\bsrc\s*=\s*(["'])([^"']*\b(?:tacto(?:-scroll|-3d)?|three\.min)\.js(?:[?#][^"']*)?)\1[^>]*>\s*</script>""", swap("js", "<script>", "</script>"), part)
    text = outside_comments(text, bundle)

    brand_note = "no private brand"
    brand = None if "--no-brand" in sys.argv else load_brand()
    if brand:
        brander = Brander(brand)
        text = brander.apply(text)
        brand_note = f"{brand.get('name', 'brand')} logo x{brander.count}"
        left = brander.leftovers(text)
        if left:
            problems.append(f"{left} wordmark(s) with the brand's name were not turned into the logo: write them exactly as "
                            '<span class="tc-wordmark"><span class="tc-wordmark__mark"></span>Name</span>, or use <span data-tc-logo></span>')

    text, n_img, missing = embed_images(text, base)
    visible = COMMENT.sub("", text)
    if re.search(r"<link\b[^>]*\btacto\.css", visible):
        problems.append("tacto.css is still linked, not inlined: the file will be unstyled once it is sent")
    elif "--tc-black" not in visible:
        problems.append('the file has no tacto.css: add <link rel="stylesheet" href="tacto.css"> to its head')
    unfilled = re.sub(r'<span class="tc-logo"[^>]*>', "", visible)
    if re.search(r"<[a-z]+\b[^>]*\bdata-tc-logo\b", unfilled):
        problems.append("a data-tc-logo placeholder was left unfilled" + ("" if brand else
                        ": this installation has no private brand (brand.local/), so write the company name as a text wordmark instead"))
    allow_missing = "--allow-missing" in sys.argv
    for m in missing:
        note = f"image not found: {m} (put it next to the input or in ./logos/, or fetch it with scripts/logo.py)"
        if allow_missing:
            print(f"  warning: {note}", file=sys.stderr)
        else:
            problems.append(note)

    if "--keep-comments" not in sys.argv:
        text = strip_comments(text)
    out.write_text(text, encoding="utf-8")
    print(f"{out}: {counts['css']} stylesheet(s), {counts['js']} script(s), {n_img} image(s) embedded, {brand_note}, {len(text) // 1024} KB")
    if problems:
        for p in problems:
            print(f"  PROBLEM: {p}", file=sys.stderr)
        print(f"inline.py: {len(problems)} problem(s). The file was written but is not ready to send.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
