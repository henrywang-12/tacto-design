#!/usr/bin/env python3
"""tacto_lint.py - find what makes a file look or read off-brand.

    python3 scripts/tacto_lint.py page.html [more files ...]
    python3 scripts/tacto_lint.py --strict deck.html          (warnings fail too)
    python3 scripts/tacto_lint.py --allow-color "#e2001a,#00a0e3" page.html

Checks .html, .css, .svg (styling) and .html, .md, .txt (copy).
Errors are things the design language never does. Warnings are things it
rarely does: read each one and decide. Wrap third-party material (a customer
logo's inline SVG, a quoted source) in
    <!-- tc-lint-off --> ... <!-- tc-lint-on -->
to skip it. Standard library only. Exit code 1 when there are errors.
"""
import bisect
import html as htmllib
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

# --- the palette -------------------------------------------------------------
PALETTE = {
    "black": "000000", "white": "ffffff", "paper": "f5f5f5", "card-grey": "f3f3f3", "fog": "fafafa",
    "line": "e4e2df", "line-soft": "d1d1d1", "grey": "aeaeae", "mid": "767676", "coal": "262626",
    "orange": "ff6414", "orange-hot": "ff4f25", "ember-deep": "5c1c00", "ember-mid": "c2410c",
    "blue": "2170ec", "sea": "2abfc1", "green": "2ed24f", "yellow": "ffcc14",
    # greys the site also uses in small places
    "grey-f7": "f7f7f7", "grey-cb": "cbcbcb", "grey-d0": "d0d0d0", "grey-95": "959595",
    "ink-22": "222222", "ink-11": "111111", "bullet": "252525", "fade-line": "e5e5e5",
}


APP_BLOCK = re.compile(r"/\* app-palette:start \*/(.*?)/\* app-palette:end \*/", re.S)


def load_app_palette():
    """The colours of the product screen (.tc-app): valid inside it, nowhere else."""
    css = SKILL_ROOT / "assets" / "tacto.css"
    pal = {}
    if css.is_file():
        m = APP_BLOCK.search(css.read_text(encoding="utf-8"))
        for t in re.finditer(r"--(tca-[\w-]+)\s*:\s*#([0-9a-fA-F]{6})\b", m.group(1) if m else ""):
            pal[t.group(1)] = t.group(2).lower()
    return pal


def load_palette():
    """Every colour assets/tacto.css uses, plus the product tokens listed above.
    Add a colour to tacto.css and the lint and the render check accept it.
    The product screen's own colours are kept apart: see load_app_palette()."""
    pal = dict(PALETTE)
    css = SKILL_ROOT / "assets" / "tacto.css"
    if css.is_file():
        text = APP_BLOCK.sub("", css.read_text(encoding="utf-8"))
        for m in re.finditer(r"--tc-([\w-]+)\s*:\s*#([0-9a-fA-F]{6})\b", text):
            pal[m.group(1)] = m.group(2).lower()
        known = set(pal.values())
        for m in re.finditer(r"#([0-9a-fA-F]{6})\b", text):
            h = m.group(1).lower()
            if h not in known:
                pal["css-" + h] = h
                known.add(h)
    return pal


PALETTE = load_palette()
APP_PALETTE = load_app_palette()
# the source lint cannot tell where a rule ends up, so it accepts both sets; the render check
# (tacto_check.py) then holds the product screen's colours to the product screen
BY_HEX = {**{v: k for k, v in APP_PALETTE.items()}, **{v: k for k, v in PALETTE.items()}}
# colours that are fine when translucent (overlays, shadows, glass)
ALPHA_OK = {"000000", "ffffff", "ff6414", "2170ec", "2abfc1", "2ed24f", "ffcc14", "d1d1d1", "e5e5e5", "aeaeae", "5c1c00"}

FONT_OK = ("aspekta", "geist mono", "geistmono", "inherit", "var(", "ui-monospace", "monospace", "sfmono", "menlo")
RADIUS_OK = {0, 1, 2, 4, 7, 8, 10, 999, 1000, 9999}
APP_RADIUS_OK = {3, 6, 12}        # the product screen also uses these
NAMED_BAD = ("red|blue|green|purple|violet|indigo|orange|yellow|pink|teal|cyan|magenta|navy|gold|lime|"
             "aqua|fuchsia|maroon|olive|silver|crimson|coral|salmon|tomato|orchid|turquoise|gray|grey")
# Calibrated on tacto.ai: the site does say "transform", "unlock", "leading", "frontier" and
# "strong", and never says any of the words below.
HYPE = ["revolutionary", "revolutionise", "revolutionize", "game-changing", "game changer", "cutting-edge",
        "next-generation", "next-gen", "seamless", "seamlessly", "unleash", "supercharge", "empower",
        "elevate", "harness", "reimagine", "best-in-class", "state-of-the-art", "synergy", "robust",
        "delight", "magic", "magical", "blazing", "lightning-fast", "disrupt", "disruptive", "fast-paced",
        "dive in", "deep dive", "we're excited", "we are excited", "thrilled", "incredible", "incredibly",
        "amazing", "stunning", "powerful", "skyrocket", "turbocharge", "10x your", "awesome", "passionate",
        # German
        "nahtlos", "nahtlose", "nahtloser", "revolutionär", "revolutionäre", "bahnbrechend", "bahnbrechende",
        "entfesseln", "entfesselt", "synergie", "synergien", "leistungsstark", "leistungsstarke",
        "disruptiv", "disruptive", "magisch", "begeistert", "wir freuen uns", "tauchen wir ein",
        "schnelllebig", "schnelllebigen", "auf das nächste level", "next level", "spielend leicht",
        "unglaublich", "atemberaubend", "rundum-sorglos", "leidenschaftlich"]
EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000026FF\U00002700-\U00002712\U00002714-\U000027BF\U0000FE0F]")


def nearest(hex6: str) -> str:
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    best = min(PALETTE.items(), key=lambda kv: sum((c - int(kv[1][i:i + 2], 16)) ** 2 for c, i in ((r, 0), (g, 2), (b, 4))))
    return f"--tc-{best[0]} #{best[1]}"


class Report:
    def __init__(self, path, text):
        self.path, self.items = path, []
        self.nl = [m.start() for m in re.finditer("\n", text)]

    def add(self, level, offset, kind, msg):
        line = bisect.bisect_left(self.nl, offset) + 1
        item = (level, line, kind, msg)
        if item not in self.items:
            self.items.append(item)


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def mask_off(text: str) -> str:
    """Blank out tc-lint-off regions, keeping offsets stable."""
    return re.sub(r"<!--\s*tc-lint-off\s*-->.*?<!--\s*tc-lint-on\s*-->", blank, text, flags=re.S)


def lint_scripts(rep, text, allow):
    """Scripts cannot be read as copy, but colours and emoji in them still count."""
    built = 0
    for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", text, flags=re.S | re.I):
        js, base = m.group(1), m.start(1)
        if "tacto.js" in js[:200] or "tacto-design:" in js[:200] or "/* tc-script */" in js[:40] or "Three.js Authors" in js[:200] or not js.strip():
            continue      # the skill's own scripts and the vendored three.js
        for c in re.finditer(r"#([0-9a-fA-F]{6})\b", js):
            check_color(rep, base + c.start(), c.group(1).lower(), 1, c.group(0), allow)
        for c in re.finditer(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})(?:\s*[,/]\s*([\d.]+))?\s*\)", js):
            r, g, b_ = (min(int(c.group(i)), 255) for i in (1, 2, 3))
            check_color(rep, base + c.start(), f"{r:02x}{g:02x}{b_:02x}", float(c.group(4) or 1), c.group(0), allow)
        for c in EMOJI.finditer(js):
            rep.add("error", base + c.start(), "copy", f"emoji {c.group(0)!r} in a script: none, anywhere")
        if re.search(r"innerHTML|textContent|insertAdjacentHTML|createElement|\.map\(", js):
            built += 1
    if built:
        rep.add("note", 0, "scripts", f"{built} script block(s) build content at runtime: this lint cannot read that; scripts/tacto_check.py checks the rendered page")
    for m in re.finditer(r"<script\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)", text, flags=re.I):
        if not re.search(r"(?:tacto(?:-scroll|-3d)?|three\.min)\.js$", m.group(1)):
            rep.add("note", m.start(), "scripts", f"external script {m.group(1)[:50]} is not read by this lint; scripts/tacto_check.py checks the rendered page")


def css_contexts(text: str, suffix: str):
    """Yield (offset, css_text) for every place styling lives."""
    if suffix in (".css", ".svg"):
        yield 0, text
        if suffix == ".css":
            return
    for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", text, flags=re.S | re.I):
        yield m.start(1), m.group(1)
    for m in re.finditer(r'\bstyle\s*=\s*"([^"]*)"', text, flags=re.I):
        yield m.start(1), m.group(1)
    for m in re.finditer(r'\b(?:fill|stroke|stop-color|flood-color|color)\s*=\s*"([^"]*)"', text, flags=re.I):
        yield m.start(1), "color:" + m.group(1)  # offset is approximate by 6 chars; fine for line numbers


def check_color(rep, off, hex6, alpha, raw, allow):
    if hex6 in allow or hex6 in BY_HEX:
        return
    if alpha < 1 and hex6 in ALPHA_OK:
        return
    rep.add("error", off, "colour", f"{raw} is not in the palette (nearest: {nearest(hex6)})")


def lint_css(rep, base, css, allow, trusted=False, app=False):
    """trusted: this is tacto.css itself, the source of truth for type, weight and radius.
    app: the file holds a product screen (.tc-app), which has its own type and weights."""
    # masks legitimately use black/transparent; blank them out (offsets preserved)
    css = re.sub(r"(?:-webkit-)?mask(?:-image)?\s*:[^;}]*", lambda m: " " * len(m.group(0)), css, flags=re.I)
    # colours: hex
    for m in re.finditer(r"(?<![&\w%])#([0-9a-fA-F]{3,8})\b", css):
        h = m.group(1).lower()
        if len(h) not in (3, 4, 6, 8) or css[max(0, m.start() - 4):m.start()].lower() == "url(":
            continue
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1
        check_color(rep, base + m.start(), h[:6], alpha, m.group(0), allow)
    # colours: rgb()/rgba()
    for m in re.finditer(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})(?:\s*[,/]\s*([\d.]+%?))?\s*\)", css, flags=re.I):
        r, g, b = (min(int(m.group(i)), 255) for i in (1, 2, 3))
        a = m.group(4)
        alpha = 1 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        check_color(rep, base + m.start(), f"{r:02x}{g:02x}{b:02x}", alpha, m.group(0), allow)
    for m in re.finditer(r"\b(hsla?|oklch|oklab|lab|lch|color-mix)\(", css, flags=re.I):
        rep.add("warn", base + m.start(), "colour", f"{m.group(1)}() colour: use a hex token from the palette so it can be checked")
    # colours: named
    for m in re.finditer(rf"(?:^|[;{{\s\"])(?:color|background|background-color|border(?:-[a-z]+)*|fill|stroke|outline)\s*:\s*[^;}}]*?(?<![\w-])({NAMED_BAD})(?![\w-])", css, flags=re.I):
        rep.add("error", base + m.start(1), "colour", f"named colour '{m.group(1)}': use a palette token")
    # fonts
    font_ok = FONT_OK + (("inter",) if app else ())
    heavy = r"bold|bolder|[7-9]00" if app else r"bold|bolder|[5-9]00"
    for m in re.finditer(r"font-family\s*:\s*([^;}]+)", css, flags=re.I):
        first = m.group(1).split(",")[0].strip().strip("'\"").lower()
        if not trusted and not first.startswith(font_ok):
            rep.add("error", base + m.start(), "font", f"font '{first}' is not part of the system (Aspekta, Geist Mono for labels, Inter inside the product screen)")
    for m in re.finditer(rf"font-weight\s*:\s*({heavy})\b", css, flags=re.I):
        if trusted:
            break
        level = "warn" if m.group(1) == "500" else "error"
        rep.add(level, base + m.start(), "weight", f"font-weight {m.group(1)}: " + ("the product screen uses 400, 500 and 600, nothing heavier" if app else
                "everything is light (300); numerals 200; buttons and small UI labels 400. Nothing heavier"))
    for m in re.finditer(r"(?:^|[;{\s\"])font\s*:\s*([^;}]+)", css, flags=re.I):
        if trusted:
            break
        value = m.group(1)
        if re.search(r"\b(bold|bolder|[7-9]00)\b" if app else r"\b(bold|bolder|[6-9]00)\b", value, flags=re.I):
            rep.add("error", base + m.start(1), "weight", f"bold in the font shorthand ({value.strip()[:40]}): headlines are 300, nothing is heavier than 400")
        fam = re.search(r"\d(?:px|rem|em|pt|%)(?:\s*/\s*[\d.]+\w*)?\s+(.+)$", value.strip())
        if fam:
            first = fam.group(1).split(",")[0].strip().strip("'\"").lower()
            if not first.startswith(font_ok):
                rep.add("error", base + m.start(1), "font", f"font '{first}' is not part of the system (Aspekta, Geist Mono for labels, Inter inside the product screen)")
    if not trusted:
        for m in re.finditer(r"\b(?:repeating-)?(?:linear|radial|conic)-gradient\(", css, flags=re.I):
            rep.add("warn", base + m.start(), "effect", "gradient: gradients live in the panels (classes tc-ember, tc-veil, tc-noir, tc-band, tc-cover, tc-slide--ember) and in the tc-powered label")
    for m in re.finditer(r"font-style\s*:\s*italic", css, flags=re.I):
        rep.add("warn", base + m.start(), "type", "italics are not used; emphasise by dimming the rest (class tc-dim) or with orange (class tc-hl)")
    # effects
    for m in re.finditer(r"text-shadow\s*:\s*(?!none)", css, flags=re.I):
        rep.add("error", base + m.start(), "effect", "text-shadow is never used")
    for m in re.finditer(r"(?:-webkit-)?background-clip\s*:\s*text", css, flags=re.I):
        if trusted:
            break
        rep.add("error", base + m.start(), "effect", "gradient text exists once, at label size: the tc-powered label. Headlines are solid black or white")
    for m in re.finditer(r"box-shadow\s*:\s*([^;}]+)", css, flags=re.I):
        if trusted:
            break
        for part in re.split(r",(?![^(]*\))", m.group(1)):
            # every length counts, also a bare 0: offset-x, offset-y, blur, spread
            part = re.sub(r"(?:rgba?|hsla?|oklch|oklab|color|var)\([^)]*\)|#[0-9a-fA-F]{3,8}\b|\binset\b", " ", part)
            nums = [float(v) * (16 if u == "rem" else 1) for v, u in re.findall(r"(-?\d*\.?\d+)(px|rem|em)?(?![\w.%])", part)]
            if len(nums) >= 3 and nums[2] >= 32 and not (len(nums) >= 4 and nums[3] < 0):
                rep.add("warn", base + m.start(), "effect", f"large soft shadow (blur {nums[2]:g}px): the system is flat")
    for m in re.finditer(r"border-radius\s*:\s*([^;}]+)", css, flags=re.I):
        if trusted:
            break
        for v, unit in re.findall(r"(\d*\.?\d+)(px|rem)", m.group(1)):
            px = round(float(v) * (16 if unit == "rem" else 1), 2)
            if px not in RADIUS_OK and px < 100 and not (app and px in APP_RADIUS_OK):
                rep.add("warn", base + m.start(), "radius", f"border-radius {v}{unit} is outside the scale (4 buttons and chips, 8 cards and panels, 10 UI fragments, 1000 pills"
                        + ("; the product screen adds 3, 6 and 12" if app else "") + ")")
    # uppercase only on small labels
    for m in re.finditer(r"[^{}]*\{([^{}]*)\}|^([^{}]+)$", css, flags=re.S):
        block = m.group(1) or m.group(2) or ""
        if re.search(r"text-transform\s*:\s*uppercase", block, flags=re.I):
            size = re.search(r"font-size\s*:\s*(\d*\.?\d+)(px|rem|em)", block)
            px = float(size.group(1)) * (1 if size.group(2) == "px" else 16) if size else 0
            if px > 18 and not trusted:
                rep.add("warn", base + m.start(), "type", f"uppercase at {px:g}px: uppercase is only for mono labels of 10 to 14px (18px on a cover)")
    # motion
    for m in re.finditer(r"cubic-bezier\(\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)", css):
        if float(m.group(2)) > 1.001 or float(m.group(4)) > 1.001 or float(m.group(2)) < 0 or float(m.group(4)) < 0:
            rep.add("warn", base + m.start(), "motion", "overshoot easing: nothing bounces here")
    for m in re.finditer(r"animation(?:-name)?\s*:\s*[^;}]*\b(\w*(?:bounce|shake|wobble|wiggle|flash|float|glow|jello|tada|heartbeat|typing|typewriter)\w*)", css, flags=re.I):
        rep.add("warn", base + m.start(), "motion", f"animation '{m.group(1)}': motion is limited to a short rise-and-fade")
    for m in re.finditer(r"transition\s*:\s*([^;}]+)", css, flags=re.I):
        for d in re.findall(r"(\d*\.?\d+)s\b", m.group(1)):
            if float(d) > 1.0:
                rep.add("warn", base + m.start(), "motion", f"{d}s transition: keep state changes under 0.7s")


def visible_text(text: str) -> str:
    """HTML with tags, styles and comments blanked, offsets preserved."""
    text = re.sub(r"<style\b.*?</style>", blank, text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"<[^>]+>", blank, text, flags=re.S)
    return text


def lint_copy(rep, text, is_html, check_samples=True, lang=""):
    body = visible_text(text) if is_html else text
    if is_html and not lang:
        m = re.search(r"<html\b[^>]*\blang\s*=\s*[\"']?([A-Za-z-]+)", text)
        lang = m.group(1) if m else ""
    german = lang.lower().startswith("de")       # German capitalises every noun: that is not Title Case
    for m in EMOJI.finditer(body):
        rep.add("error", m.start(), "copy", f"emoji {m.group(0)!r}: none, anywhere")
    for m in re.finditer(r"!", body):
        if not is_html and (body[m.start():m.start() + 2] == "![" or body[max(0, m.start() - 1)] == "<"):
            continue  # markdown image or html comment in a .md file
        ctx = re.sub(r"\s+", " ", body[max(0, m.start() - 28):m.start() + 1]).strip()
        rep.add("error", m.start(), "copy", f"exclamation mark: “…{ctx}”")
    low = body.lower()
    for word in HYPE:
        for m in re.finditer(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", low):
            rep.add("warn", m.start(), "copy", f"hype word '{word}': say what it does, with a number")
    if check_samples:
        for m in re.finditer(r"northdesk(?:\.example)?|hollweg(?: präzision)?|auerberg(?: guss)?|lindqvist|jana petrovic|carla wiesner|brenner zerspanung|feldmark stanztechnik|kessler drehteile|sentec antriebe|your company", low):
            rep.add("error", m.start(), "copy", f"template sample name '{body[m.start():m.end()]}' left in: use the real company, customer and people")
        # the templates' invented figures: long ones cannot be a coincidence, short ones might be
        for m in re.finditer(r"€310,000|€91,754,300|€96,380,000|€1,284,560|€1,083,120|€197,230|€185,770|€108,548|€47,672|€34,800|€9,860|410,000|2,700 drawing parts|3,870 drawing parts", low):
            rep.add("error", m.start(), "copy", f"template sample figure '{body[m.start():m.end()]}' left in: every figure is the customer's own or yours, with its source, or it goes")
        for m in re.finditer(r"€4\.2m|€1\.1m|€1\.2m|€340k|€12b|120\+|(?<![\d.,])3\.4%", low):
            rep.add("warn", m.start(), "copy", f"'{body[m.start():m.end()]}' is also a figure from the templates: keep it only if it is really yours")
    for m in re.finditer(r"iso(?:/iec)?\s?(?:27001|9001|14001)|\bsoc\s?2\b|\btisax\b|gdpr[- ]compliant|dsgvo[- ]konform|\bcertified\b|\bzertifiziert\b|of the year\b|des jahres\b", low):
        rep.add("warn", m.start(), "copy", f"certificate, compliance or award claim “{body[m.start():m.end()]}”: keep it only if the sender really holds it; never invent one")
    if re.search(r"lorem ipsum", low):
        rep.add("error", low.index("lorem ipsum"), "copy", "placeholder text: write real, plausible content")
    for m in re.finditer(r"\b(?:[A-ZÄÖÜ]{2,}[,:]?\s+){3,}[A-ZÄÖÜ]{2,}\b", body):
        rep.add("warn", m.start(), "copy", f"shouted text “{m.group(0)[:40]}”: write labels in normal case and let CSS uppercase the eyebrow")
    if is_html:
        small = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "vs.", "with", "x"}
        for m in re.finditer(r"<h([1-3])\b[^>]*>(.*?)</h\1>", text, flags=re.S | re.I):
            words_ = [w for w in htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(2))).split() if w.lower() not in small and w[0].isalpha()]
            if not german and len(words_) >= 5 and sum(w[0].isupper() for w in words_) / len(words_) > 0.8:
                rep.add("warn", m.start(), "copy", f"Title Case headline “{' '.join(words_)[:48]}”: use sentence case")
        for m in re.finditer(r"fonts\.googleapis\.com/css2?\?([^\"')\s]+)", text):
            for fam in re.findall(r"family=([^:&]+)", m.group(1)):
                if fam.replace("+", " ").lower() not in ("geist mono",):
                    rep.add("error", m.start(), "font", f"web font '{fam.replace('+', ' ')}' is not part of the system")
        if "--tc-black" not in text and not re.search(r"tacto\.css", text):
            rep.add("warn", 0, "setup", "tacto.css is neither linked nor inlined: values are probably hand-copied and may drift")


def lint_file(path: Path, allow) -> Report:
    raw = path.read_text(encoding="utf-8", errors="replace")
    rep = Report(path, raw)
    text = mask_off(raw)
    suffix = path.suffix.lower()
    # the skill's own templates and docs legitimately contain the sample names
    own = SKILL_ROOT not in path.resolve().parents
    if suffix in (".html", ".htm", ".css", ".svg"):
        styled = re.sub(r"<script\b.*?</script>", blank, text, flags=re.S | re.I)
        app = bool(re.search(r"class\s*=\s*[\"'][^\"']*\btc-app\b", text))
        for off, css in css_contexts(styled, suffix):
            trusted = ("tacto.css" in css[:400] and "the Tacto-style design language" in css[:400]) or "/* tc-style */" in css[:40]
            lint_css(rep, off, css, allow, trusted or path.resolve() == SKILL_ROOT / "assets" / "tacto.css", app)
    if suffix in (".html", ".htm"):
        lint_scripts(rep, text, allow)
        text = re.sub(r"<script\b.*?</script>", blank, text, flags=re.S | re.I)
        lint_copy(rep, text, True, own)
    elif suffix in (".md", ".txt", ""):
        lint_copy(rep, text, False, own)
    return rep


def main() -> int:
    args = sys.argv[1:]
    strict = "--strict" in args
    allow = set()
    if "--allow-color" in args:
        i = args.index("--allow-color")
        for c in args[i + 1].split(","):
            c = c.strip().lstrip("#").lower()
            allow.add("".join(ch * 2 for ch in c) if len(c) == 3 else c[:6])
        del args[i:i + 2]
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    errors = warns = 0
    for f in files:
        rep = lint_file(Path(f), allow)
        if rep.items:
            print(f)
            for level, line, kind, msg in sorted(rep.items, key=lambda i: (i[1], i[0])):
                print(f"  {level:<5} L{line:<5} {kind:<7} {msg}")
        errors += sum(1 for i in rep.items if i[0] == "error")
        warns += sum(1 for i in rep.items if i[0] == "warn")
    verdict = "PASS" if errors == 0 and not (strict and warns) else "FAIL"
    print(f"{verdict}: {errors} error(s), {warns} warning(s) in {len(files)} file(s)")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
