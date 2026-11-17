#!/usr/bin/env python3
"""panel.py - write one of the background panels as a PNG, any size.

    python3 scripts/panel.py out.png 1920 1080              ember: black burning into orange from the lower left
    python3 scripts/panel.py out.png 1920 1080 --right      ember from the lower right
    python3 scripts/panel.py out.png 1920 1080 --streak     a diagonal orange band on black
    python3 scripts/panel.py out.png 1200 1200 --full       solid orange with soft light streaks
    python3 scripts/panel.py out.png 1920 1080 --noir       black with a faint light from the top right
    python3 scripts/panel.py out.png 1920 1080 --veil       page grey with soft orange and blue light
    python3 scripts/panel.py out.png 1600 900 --grain 0     (no grain)

For slides, documents, Figma and image editors, where the CSS version is not
available. Standard library only. The colours and the grain match the classes
tc-ember, tc-noir and tc-veil in assets/tacto.css. A 1920x1080 panel takes a
few seconds.
"""
import math
import os
import struct
import sys
import zlib

BLACK, ORANGE, MID, DEEP = (0, 0, 0), (0xFF, 0x64, 0x14), (0xC2, 0x41, 0x0C), (0x5C, 0x1C, 0x00)
PAPER, LINE, BLUE = (0xF5, 0xF5, 0xF5), (0xE4, 0xE2, 0xDF), (0x21, 0x70, 0xEC)


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def ramp(stops, t):
    """stops: [(pos, rgb), ...] sorted by pos; t in 0..1"""
    if t <= stops[0][0]:
        return stops[0][1]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if t <= p1:
            return lerp(c0, c1, (t - p0) / (p1 - p0) if p1 > p0 else 0)
    return stops[-1][1]


def table(stops, n=512):
    return [ramp(stops, i / (n - 1)) for i in range(n)]


EMBER = table([(0.0, ORANGE), (0.30, ORANGE), (0.48, MID), (0.66, DEEP), (0.90, BLACK), (1.0, BLACK)])
STREAK = table([(0.0, BLACK), (0.18, BLACK), (0.38, DEEP), (0.48, MID), (0.56, ORANGE), (0.64, MID), (0.74, DEEP), (0.92, BLACK), (1.0, BLACK)])


def clamp(v):
    return 0 if v < 0 else 255 if v > 255 else int(v + 0.5)


def main() -> int:
    argv = sys.argv[1:]
    grain = 1.0
    if "--grain" in argv:
        i = argv.index("--grain")
        grain = float(argv[i + 1])
        del argv[i:i + 2]
    mode = next((m for m in ("right", "streak", "full", "noir", "veil") if "--" + m in argv), "ember")
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 3:
        print(__doc__)
        return 2
    out, w, h = args[0], int(args[1]), int(args[2])
    last = len(EMBER) - 1
    # the streak runs at 118 degrees, as in the stylesheet
    ang = math.radians(118)
    dx, dy = math.sin(ang), -math.cos(ang)
    span = abs(w * dx) + abs(h * dy)

    raw = bytearray()
    for y in range(h):
        ty = y / max(h - 1, 1)
        noise, noise2 = os.urandom(w), os.urandom(w)
        row = bytearray(w * 3)
        for x in range(w):
            tx = x / max(w - 1, 1)
            if mode in ("ember", "right"):
                cx = 0.10 if mode == "ember" else 0.90
                d = math.hypot((tx - cx) / 1.30, (ty - 1.05) / 1.00)
                r, g, b = EMBER[min(int(d * last), last)]
                speck = 0.65
            elif mode == "streak":
                t = ((x - w / 2) * dx + (y - h / 2) * dy) / span + 0.5
                r, g, b = STREAK[min(max(int(t * last), 0), last)]
                speck = 0.65
            elif mode == "full":
                s = 0.15 * max(0.0, 1 - abs(tx - 0.34) / 0.2) + 0.10 * max(0.0, 1 - abs(tx - 0.74) / 0.24)
                r, g, b = lerp(ORANGE, (255, 255, 255), s)
                speck = 0.22
            elif mode == "noir":
                d = math.hypot((tx - 0.70) / 0.90, ty / 0.70)
                s = 0.10 * max(0.0, 1 - d)
                r, g, b = (255 * s,) * 3
                speck = 0.0
            else:  # veil
                r, g, b = lerp(LINE, PAPER, ty)
                o = 0.20 * max(0.0, 1 - math.hypot((tx - 0.24) / 0.42, (ty - 0.30) / 0.46))
                bl = 0.15 * max(0.0, 1 - math.hypot((tx - 0.78) / 0.40, (ty - 0.34) / 0.44))
                r, g, b = lerp((r, g, b), ORANGE, o)
                r, g, b = lerp((r, g, b), BLUE, bl)
                speck = 0.07
            if grain:
                # black specks eat into the colour; white specks lift it a little
                a = min(max(1.9 * noise[x] / 255 - 0.62, 0.0), 1.0) * speck * grain
                r, g, b = r * (1 - a), g * (1 - a), b * (1 - a)
                if mode != "veil":
                    lift = min(max(1.6 * noise2[x] / 255 - 0.5, 0.0), 1.0) * 0.10 * grain
                    r, g, b = r + (255 - r) * lift * (r / 255 + 0.08), g + (255 - g) * lift * (g / 255 + 0.08), b + (255 - b) * lift * (b / 255 + 0.08)
            i = x * 3
            row[i], row[i + 1], row[i + 2] = clamp(r), clamp(g), clamp(b)
        raw += b"\x00" + row

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b"")
    with open(out, "wb") as f:
        f.write(png)
    print(f"{out}: {w}x{h} {mode}, {len(png) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
