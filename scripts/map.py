#!/usr/bin/env python3
"""map.py - draw the grey supplier map of the product screen.

    python3 scripts/map.py --region europe --dot 9.99,53.55,Hamburg --dot 13.40,52.52 > map.svg
    python3 scripts/map.py --center 8,53 --span 62 --size 1184x380 --labels > map.svg
    python3 scripts/map.py --region dach --size 800x420 --dot 11.58,48.14,Munich > map.svg

  --region   europe | dach | uk | nordics | north-america | asia | world
  --center   lon,lat of the middle of the picture     (instead of --region)
  --span     degrees of longitude across the picture  (instead of --region)
  --size     WxH in px of the panel it goes into (default 1184x380)
  --dot      lon,lat[,title]: a supplier dot; repeat it
  --labels   write country names on the larger countries
  --inline   print markup to paste into the page (styled by tacto.css) instead of a file

Then, in the page:  <div class="tc-app__map"><img src="map.svg" alt=""></div>
scripts/inline.py embeds the file. The sea is the panel's own background.

Data: Natural Earth 1:50m (public domain) as packaged by world-atlas (ISC),
in assets/maps/. Mercator projection. Standard library only.
"""
import json
import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "assets" / "maps" / "countries-50m.json"
REGIONS = {"europe": (8, 53, 62), "dach": (10.5, 50, 20), "uk": (-3, 54.5, 22), "nordics": (16, 62.5, 44),
           "north-america": (-98, 44, 96), "asia": (105, 30, 110), "world": (10, 25, 340)}
# the same values as the --tca tokens in assets/tacto.css (a standalone picture cannot read them)
LAND, BORDER, DOT, LABEL = "#fdfdfd", "#d4d4d4", "#2563eb", "#a3a3a3"


def merc(lat):
    lat = max(-85.0, min(85.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


def load():
    topo = json.loads(DATA.read_text(encoding="utf-8"))
    (sx, sy), (tx, ty) = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(pts[1:] if out else pts)
        return out

    countries = []
    for g in topo["objects"]["countries"]["geometries"]:
        polys = [g["arcs"]] if g["type"] == "Polygon" else g.get("arcs", []) if g["type"] == "MultiPolygon" else []
        countries.append((g.get("properties", {}).get("name", ""), [ring(r) for poly in polys for r in poly]))
    return countries


def clip(pts, x0, y0, x1, y1):
    """Sutherland-Hodgman against a rectangle."""
    def cut(pts, inside, cross):
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(cross(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cross(prev, cur))
        return out

    def at_x(x):
        return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / ((b[0] - a[0]) or 1e-9))

    def at_y(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / ((b[1] - a[1]) or 1e-9), y)

    for inside, cross in ((lambda p: p[0] >= x0, at_x(x0)), (lambda p: p[0] <= x1, at_x(x1)),
                          (lambda p: p[1] >= y0, at_y(y0)), (lambda p: p[1] <= y1, at_y(y1))):
        pts = cut(pts, inside, cross)
        if len(pts) < 3:
            return []
    return pts


def simplify(pts, eps):
    """Douglas-Peucker, without recursion."""
    if len(pts) < 5:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy) or 1e-9
        far, idx = 0.0, -1
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - ax) - dx * (pts[i][1] - ay)) / norm
            if d > far:
                far, idx = d, i
        if far > eps and idx > 0:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, keep) if k]


def area(pts):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2


def num(v):
    return f"{v:.1f}".removesuffix(".0")


def main() -> int:
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return 2

    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args and len(args) > args.index(name) + 1 else default

    try:
        w, h = (float(v) for v in opt("--size", "1184x380").lower().split("x"))
        if opt("--region"):
            clon, clat, span = REGIONS[opt("--region")]
        else:
            clon, clat = (float(v) for v in opt("--center", "8,53").split(","))
            span = float(opt("--span", "62"))
    except (ValueError, KeyError):
        print("map.py: use --region " + " | ".join(REGIONS) + ", or --center lon,lat --span degrees; --size WxH", file=sys.stderr)
        return 2
    if not DATA.is_file():
        print(f"map.py: missing {DATA}", file=sys.stderr)
        return 2
    inline = "--inline" in args
    k = w / span                               # px per degree of longitude
    cy = merc(clat)

    def project(lon, lat):
        return ((lon - clon) * k + w / 2, (cy - merc(lat)) * k + h / 2)

    pad = 12
    shapes, labels = [], []
    for name, rings in load():
        d, best = [], (0, None)
        for r in rings:
            lons = [p[0] for p in r]
            if max(lons) < clon - span or min(lons) > clon + span:
                continue
            pts = clip([project(*p) for p in r], -pad, -pad, w + pad, h + pad)
            if len(pts) < 3:
                continue
            half = len(pts) // 2      # a ring is closed: simplify it as two open halves
            slim = simplify(pts[:half + 1], 0.7)[:-1] + simplify(pts[half:] + pts[:1], 0.7)[:-1]
            a = area(slim)
            if len(slim) < 3 or a < 6:
                continue
            d.append("M" + "L".join(f"{num(x)},{num(y)}" for x, y in slim) + "Z")
            if a > best[0]:
                seen = [p for p in slim if 0 <= p[0] <= w and 0 <= p[1] <= h]
                if seen:
                    best = (a, (sum(p[0] for p in seen) / len(seen), sum(p[1] for p in seen) / len(seen)))
        if d:
            shapes.append("".join(d))
            if "--labels" in args and best[0] > w * h / 90 and best[1]:
                labels.append((best[1][0], best[1][1], name))
    dots = []
    for i, a in enumerate(args):
        if a == "--dot" and i + 1 < len(args):
            bits = args[i + 1].split(",")
            try:
                x, y = project(float(bits[0]), float(bits[1]))
            except (ValueError, IndexError):
                print(f"map.py: bad --dot {args[i + 1]!r} (use lon,lat[,title])", file=sys.stderr)
                return 2
            dots.append((x, y, ",".join(bits[2:]).strip()))

    out = []
    if inline:
        out.append(f'<svg viewBox="0 0 {w:g} {h:g}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Supplier map">')
        out.append(f'<path class="land" d="{"".join(shapes)}"/>')
        out += [f'<text x="{x:.0f}" y="{y:.0f}">{escape(n)}</text>' for x, y, n in labels]
        out += [f'<circle class="dot" cx="{num(x)}" cy="{num(y)}" r="5">' + (f"<title>{escape(t)}</title>" if t else "") + "</circle>" for x, y, t in dots]
    else:
        out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" preserveAspectRatio="xMidYMid slice">')
        out.append(f'<path fill="{LAND}" stroke="{BORDER}" stroke-width="0.6" stroke-linejoin="round" d="{"".join(shapes)}"/>')
        if labels:
            out.append(f'<g font-family="Inter, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="500" fill="{LABEL}" text-anchor="middle">'
                       + "".join(f'<text x="{x:.0f}" y="{y:.0f}">{escape(n)}</text>' for x, y, n in labels) + "</g>")
        if dots:
            out.append(f'<g fill="{DOT}" stroke="#ffffff" stroke-width="2">'
                       + "".join(f'<circle cx="{num(x)}" cy="{num(y)}" r="5"/>' for x, y, _ in dots) + "</g>")
    out.append("</svg>")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
