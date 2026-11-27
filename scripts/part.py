#!/usr/bin/env python3
"""part.py - look at a 3D part before you put it on a page.

    python3 scripts/part.py '[["b",120,10,90,0,5,0],["c",12,40,0,30,0,"y"]]' part.png
    python3 scripts/part.py housing part.png            a part that ships
    python3 scripts/part.py my-part.json part.png       the JSON in a file

Writes one picture with four views of the same part: from the front, from above,
from the right, and the usual three-quarter view. Read it: is every solid where
you meant it, does anything stand apart or sit inside something else?
Coordinates: x to the right, y up, z towards the viewer. See references/3d.md.
"""
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    spec, out = args[0], Path(args[1]).resolve()
    if not spec.lstrip().startswith(("[", "{")) and len(spec) < 1024 and Path(spec).is_file():
        spec = Path(spec).read_text(encoding="utf-8").strip()
    if not out.parent.is_dir():
        print(f"part.py: the output folder does not exist: {out.parent}", file=sys.stderr)
        return 2
    views = (("Front", "0,0"), ("From above", "0,83"), ("From the right", "90,0"), ("Three-quarter, as on the page", "-35,22"))
    # the first three views are drawn with edges so the geometry can be read; the last one is the look on the page
    cells = "".join(f'<figure><div class="tc-part" data-spin="false"{"" if "page" in name else chr(32) + chr(100) + "ata-look=" + chr(34) + "drawing" + chr(34)} data-view="{v}" data-tc-part="{html.escape(spec, quote=True)}"></div>'
                    f'<figcaption>{name}</figcaption></figure>' for name, v in views)
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="file://{ROOT}/assets/tacto.css">'
            '<style>body{margin:0;padding:16px;background:#fff;display:grid;grid-template-columns:1fr 1fr;gap:12px}'
            'figure{margin:0;border:1px solid #ebebeb;border-radius:12px;background:#fafafa;position:relative}'
            '.tc-part{--tc-part-h:420px}figcaption{position:absolute;left:14px;top:10px;font:500 13px/20px Inter,Arial,sans-serif;color:#737373}</style></head>'
            f'<body>{cells}<script src="file://{ROOT}/assets/vendor/three.min.js"></script><script src="file://{ROOT}/assets/tacto-3d.js"></script></body></html>')
    tmp = out.parent / f".tc-part-{out.stem}.html"
    try:
        tmp.write_text(page, encoding="utf-8")
        done = subprocess.run(["bash", str(ROOT / "scripts" / "shoot.sh"), str(tmp), str(out), "1200", "900"], capture_output=True, text=True)
    finally:
        tmp.unlink(missing_ok=True)
    if done.returncode != 0 or not out.is_file():
        print("part.py: no picture was written. " + done.stderr.strip()[-300:], file=sys.stderr)
        return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
