#!/usr/bin/env python3
"""logo.py - find a company's logo and save it locally.

    python3 scripts/logo.py "Auerberg Guss"                      (cache and brand source only)
    python3 scripts/logo.py "Auerberg Guss" auerberg-guss.example            (also look on their website)
    python3 scripts/logo.py "Lindqvist Hydraulik" lindqvist-hydraulik.example --out ./logos

Looks, in this order, and stops at the first hit:
1. Already saved: brand.local/customers/<slug>.* or ./logos/<slug>.*
2. The private brand's own customer-logo source, if brand.local/brand.json
   defines "customer_logo_url" (a URL with {slug} in it).
3. The company's website (when you give the domain): logo images and inline
   SVGs in the page header, then the SVG site icon, then the touch icon.

Prints the saved path and where it came from. ALWAYS look at the result before
using it (scripts/shoot.sh or open the file): a site can serve the wrong mark.
If nothing is found, exit code 1: use the browser, the company's press page, or
ask the user for the file. Never redraw a logo from memory.

Downloaded files are checked: an SVG with scripts or external references is
refused. Standard library only. The only network requests go to the brand's
logo source and to the company's own site.
"""
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "brand.local"
UA = "Mozilla/5.0 (compatible; logo-finder/1.0)"
EXTS = (".svg", ".png", ".webp", ".jpg", ".jpeg")


def slugify(name: str) -> str:
    table = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "é": "e", "è": "e", "å": "a", "ø": "o"})
    return re.sub(r"[^a-z0-9]+", "-", name.lower().translate(table)).strip("-")


def fetch(url: str, limit: int = 3_000_000):
    """GET a URL with certificate checking on. Some Python installs ship without a
    CA bundle, so fall back to the system bundle and then to curl."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    contexts = [None] + [ssl.create_default_context(cafile=c) for c in
                         ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt") if os.path.isfile(c)]
    last = None
    for ctx in contexts:
        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                return r.read(limit), r.headers.get("Content-Type", ""), r.geturl()
        except urllib.error.HTTPError:
            raise
        except urllib.error.URLError as e:
            last = e
            if "CERTIFICATE_VERIFY_FAILED" not in str(e):
                break
    if shutil.which("curl"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        try:
            done = subprocess.run(["curl", "-sSL", "-m", "25", "-A", UA, "--max-filesize", str(limit), "-o", tmp_path,
                                   "-w", "%{http_code}\n%{content_type}\n%{url_effective}", url],
                                  capture_output=True, text=True)
            parts = done.stdout.split("\n")
            if done.returncode == 0 and len(parts) >= 3 and parts[0].startswith("2"):
                with open(tmp_path, "rb") as f:
                    return f.read(limit), parts[1], parts[2]
        finally:
            os.unlink(tmp_path)
    raise last or urllib.error.URLError("fetch failed")


def svg_is_safe(data: bytes) -> bool:
    text = data.decode("utf-8", "replace")
    if "<svg" not in text:
        return False
    return not re.search(r"<script|\son[a-z]+\s*=|<foreignObject|javascript:|<iframe|(?:href|src)\s*=\s*[\"']https?:", text, re.I)


def save(data: bytes, ext: str, out_dir: Path, slug: str, source: str) -> int:
    if ext == ".svg" and not svg_is_safe(data):
        print(f"refused (not a plain SVG): {source}", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}{ext}"
    path.write_bytes(data)
    print(f"{path}\n  source: {source}\n  size: {len(data)} bytes\n  now look at it before you use it")
    return 0


def ext_of(url: str, ctype: str) -> str:
    path = urllib.parse.urlparse(url).path.lower()
    for e in EXTS:
        if path.endswith(e):
            return ".jpg" if e == ".jpeg" else e
    return {"image/svg+xml": ".svg", "image/png": ".png", "image/webp": ".webp", "image/jpeg": ".jpg"}.get(ctype.split(";")[0].strip(), "")


def candidates(html: str, base: str, name: str):
    """Yield (score, kind, value, label) for things in the page that are the logo.
    Deliberately strict: a wrong picture presented as a logo is worse than no logo,
    so anything that is not explicitly marked as a logo is ignored."""
    host = urllib.parse.urlparse(base).netloc.lower().removeprefix("www.")
    # 1. schema.org Organization markup: the site telling us which file is its logo
    for m in re.finditer(r'"logo"\s*:\s*(?:"([^"]+)"|\{[^{}]*?"url"\s*:\s*"([^"]+)")', html):
        url = (m.group(1) or m.group(2)).replace("\\/", "/")
        if not url.lower().endswith((".jpg", ".jpeg")):
            yield 90 + (5 if url.lower().endswith(".svg") else 0), "url", urllib.parse.urljoin(base, url), "logo named in the site's own metadata"
    head = html[:150_000]
    # 2. an <img> that says it is the logo
    for m in re.finditer(r"<img\b[^>]*>", head, flags=re.I):
        tag = m.group(0)
        src = re.search(r'\bsrc\s*=\s*["\']([^"\']+)', tag)
        if not src or src.group(1).startswith("data:"):
            continue
        low = tag.lower()
        path = urllib.parse.urlparse(src.group(1)).path.lower()
        if "logo" not in low or path.endswith((".jpg", ".jpeg")):
            continue
        if re.search(r"partner|client|customer|payment|badge|award|sponsor|press|member|certif|trust|store|app-?store|google-?play", low):
            continue
        score = 60 + (20 if path.endswith(".svg") else 0) + (5 if "logo" in path else 0) - m.start() // 5000
        yield score, "url", urllib.parse.urljoin(base, src.group(1)), "logo image in the page header"
    # 3. an inline SVG inside something called logo, or inside the link to the home page
    wrappers = (r'<(a|div|span|header|h1)\b[^>]*(?:class|id|aria-label|title)\s*=\s*["\'][^"\']*logo[^"\']*["\'][^>]*>\s*(<svg\b.*?</svg>)',
                r'<(a)\b[^>]*href\s*=\s*["\'](?:/|https?://(?:www\.)?' + re.escape(host) + r'/?)["\'][^>]*>\s*(<svg\b.*?</svg>)')
    for i, pattern in enumerate(wrappers):
        for m in re.finditer(pattern, head, flags=re.I | re.S):
            svg = m.group(2)
            if 300 < len(svg) < 200_000 and "<path" in svg:
                if "xmlns" not in svg[:300]:
                    svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
                yield 72 - 8 * i - m.start() // 5000, "svg", svg, "inline SVG in the page header"
    # 4. last resort: the site icon. It is usually the mark alone, not the full logo.
    for m in re.finditer(r"<link\b[^>]*>", head, flags=re.I):
        tag = m.group(0).lower()
        href = re.search(r'\bhref\s*=\s*["\']([^"\']+)', m.group(0))
        if href and "icon" in tag and ".svg" in tag and "mask" not in tag:
            yield 25, "url", urllib.parse.urljoin(base, href.group(1)), "SITE ICON ONLY (the mark, not the full logo): use it in small tiles, or get the real logo"


def main() -> int:
    argv = sys.argv[1:]
    out_dir = None
    if "--out" in argv:
        i = argv.index("--out")
        out_dir = Path(argv[i + 1])
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    name, domain = args[0], (args[1] if len(args) > 1 else "")
    slug = slugify(name)
    brand = {}
    if (BRAND_DIR / "brand.json").is_file():
        brand = json.loads((BRAND_DIR / "brand.json").read_text(encoding="utf-8"))
    if out_dir is None:
        out_dir = BRAND_DIR / "customers" if BRAND_DIR.is_dir() else Path("logos")

    # 1. already saved
    for folder in (out_dir, BRAND_DIR / "customers", Path("logos")):
        for e in EXTS:
            p = folder / f"{slug}{e}"
            if p.is_file():
                print(f"{p}\n  source: already saved")
                return 0

    # 2. the brand's own customer-logo source
    pattern = brand.get("customer_logo_url", "")
    if pattern:
        url = pattern.replace("{slug}", slug)
        try:
            data, ctype, final = fetch(url)
            ext = ext_of(final, ctype)
            if ext and len(data) > 100 and (ext != ".svg" or b"<svg" in data[:2000]):
                return save(data, ext, out_dir, slug, final)
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass

    # 3. the company's own website
    if domain:
        base = domain if domain.startswith("http") else f"https://{domain}"
        try:
            page, _, final = fetch(base, 1_500_000)
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"could not open {base}: {e}", file=sys.stderr)
            page, final = b"", base
        found = sorted(candidates(page.decode("utf-8", "replace"), final, name), key=lambda c: -c[0])
        for _score, kind, value, label in found[:6]:
            if kind == "svg":
                data = value.encode("utf-8")
                if svg_is_safe(data):
                    return save(data, ".svg", out_dir, slug, f"{final} - {label}")
                continue
            try:
                data, ctype, got = fetch(value, 600_000)
            except (urllib.error.URLError, TimeoutError, ValueError):
                continue
            ext = ext_of(got, ctype)
            if ext in (".svg", ".png", ".webp") and 100 < len(data) < 600_000 and save(data, ext, out_dir, slug, f"{got} - {label}") == 0:
                return 0

    print(f"no logo found for '{name}'." + ("" if domain else " Give the company's domain as a second argument to search its website."), file=sys.stderr)
    print("Next: the company's press or brand page in the browser, or ask the user for the file. Until then, set the name as text.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
