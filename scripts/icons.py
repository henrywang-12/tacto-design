#!/usr/bin/env python3
"""icons.py - the icon set of the product screen (Lucide, ISC licence).

    python3 scripts/icons.py                  list every icon name
    python3 scripts/icons.py --find chart     names that contain "chart"
    python3 scripts/icons.py --build          rewrite the icon block in assets/tacto.css

Use an icon with <i data-tc-icon="bell"></i>: it is drawn in the text colour, 16px.

To add one: save the Lucide SVG (lucide.dev, any icon, 24x24, stroke 2) as
assets/icons/<name>.svg and run --build. Do not draw icons by hand and do not
mix in another icon family: Tacto's product uses Lucide throughout.
Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "assets" / "icons"
CSS = ROOT / "assets" / "tacto.css"
START, END = "/* icons:start */", "/* icons:end */"


def names():
    return sorted(p.stem for p in ICONS.glob("*.svg"))


def data_uri(svg: str) -> str:
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    body = re.search(r"<svg\b[^>]*>(.*)</svg>", svg, flags=re.S)
    if not body:
        raise ValueError("not an SVG")
    inner = re.sub(r"\s+", " ", body.group(1)).strip().replace("> <", "><").replace(" />", "/>").replace('"', "'")
    out = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='#000' stroke-width='2' "
           "stroke-linecap='round' stroke-linejoin='round'>" + inner + "</svg>")
    return "data:image/svg+xml," + out.replace("%", "%25").replace("#", "%23").replace("<", "%3C").replace(">", "%3E")


def build() -> int:
    css = CSS.read_text(encoding="utf-8")
    if START not in css or END not in css:
        print(f"icons.py: {CSS} has no {START} ... {END} block", file=sys.stderr)
        return 1
    rules = []
    for name in names():
        try:
            uri = data_uri((ICONS / f"{name}.svg").read_text(encoding="utf-8"))
        except ValueError:
            print(f"icons.py: skipped {name}.svg (not an SVG)", file=sys.stderr)
            continue
        rules.append(f'[data-tc-icon="{name}"] {{ --tc-i: url("{uri}"); }}')
    head, rest = css.split(START, 1)
    tail = rest.split(END, 1)[1]
    CSS.write_text(head + START + "\n" + "\n".join(rules) + "\n" + END + tail, encoding="utf-8")
    print(f"{len(rules)} icons written to {CSS}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if "--build" in args:
        return build()
    found = names()
    if "--find" in args:
        i = args.index("--find")
        word = args[i + 1].lower() if len(args) > i + 1 else ""
        found = [n for n in found if word in n]
    print("\n".join(found) if found else "no icon with that name: see lucide.dev, then add it to assets/icons/ and run --build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
