#!/usr/bin/env python3
"""tacto_check.py - the one command to run before anything is handed over.

    python3 scripts/tacto_check.py out.html
    python3 scripts/tacto_check.py "demo.html?demo=1"      (query strings are kept)
    python3 scripts/tacto_check.py deck.html --strict      (warnings fail too)
    python3 scripts/tacto_check.py out.html --canvases     (only the page/slide fit checks)

It opens the file in headless Chrome and inspects what a reader would actually
see, so content built by scripts is covered too. Exit code 1 when anything is
wrong. It checks:

  fit      A4 pages longer than a page, slides whose content is cut or runs
           into the logo row or footer, text clipped inside any box, sideways
           scrolling, table columns that fall outside the page
  print    for documents and decks: exports a PDF and compares its page count
           with the number of sheets or slides (print lays text out again)
  look     fonts, weights, text and background colours, gradients and text
           shadows as rendered, against the palette in assets/tacto.css
  copy     emoji, exclamation marks, hype words (English and German), template
           sample names, placeholder text - in the rendered text
  brand    a logo that was never filled in, images that did not load, tacto.css
           still linked instead of bundled
  source   everything scripts/tacto_lint.py finds in the markup and CSS

It cannot judge whether the result is good. Look at the screenshot and at the
PDF page pictures yourself (scripts/shoot.sh).
"""
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import tacto_lint  # noqa: E402

CHROMES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/Applications/Chromium.app/Contents/MacOS/Chromium",
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
           "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]

PROBE = r"""
<script>
window.addEventListener('load', function () { setTimeout(function () {
  var PAL = __PALETTE__, ALPHA_OK = __ALPHA__, out = [], seen = {};
  function add(level, kind, msg) { var k = level + kind + msg; if (seen[k]) { seen[k].n++; return; } seen[k] = { level: level, kind: kind, msg: msg, n: 1 }; out.push(seen[k]); }
  function name(el) { var c = (el.getAttribute && el.getAttribute('class') || '').split(' ')[0]; var t = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42); return '<' + el.tagName.toLowerCase() + (c ? '.' + c : '') + '>' + (t ? ' "' + t + '"' : ''); }
  var cv = document.createElement('canvas'); cv.width = cv.height = 1; var cx = cv.getContext('2d', { willReadFrequently: true }), cache = {};
  function rgba(c) { if (cache[c]) return cache[c]; var mm = /^rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)(?:[,\s\/]+([\d.]+)(%?))?\s*\)$/.exec(c); if (mm) { var hx = [mm[1], mm[2], mm[3]].map(function (v) { return ('0' + Math.min(255, parseInt(v, 10)).toString(16)).slice(-2); }).join(''); return cache[c] = { hex: hx, a: mm[4] === undefined ? 1 : (mm[5] ? parseFloat(mm[4]) / 100 : parseFloat(mm[4])) }; } cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); var d = cx.getImageData(0, 0, 1, 1).data; var hex = [d[0], d[1], d[2]].map(function (v) { return ('0' + v.toString(16)).slice(-2); }).join(''); return cache[c] = { hex: hex, a: d[3] / 255 }; }
  function near(a, b) { for (var i = 0, s = 0; i < 6; i += 2) s += Math.abs(parseInt(a.substr(i, 2), 16) - parseInt(b.substr(i, 2), 16)); return s <= 3; }
  function inPal(c) { if (c.a === 0) return true; if (c.a < 0.999) { for (var j = 0; j < ALPHA_OK.length; j++) if (near(c.hex, ALPHA_OK[j])) return true; } for (var i = 0; i < PAL.length; i++) if (near(c.hex, PAL[i])) return true; return false; }
  function skipped(el) { return !!(el.closest && el.closest('[data-tc-skip], .tc-logo, [class*="tc-shoot"], #tc-check-none')); }
  var vw = document.documentElement.clientWidth;
  /* the text a reader sees, as it was written (innerText would apply CSS uppercase) */
  function visibleText() {
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n, lines = [];
    while ((n = w.nextNode())) {
      var p = n.parentElement; if (!p || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName) || skipped(p)) continue;
      var t = n.nodeValue.replace(/\s+/g, ' ').trim(); if (!t) continue;
      if (!p.getClientRects().length) continue;
      lines.push(t);
    }
    return lines.join('\n');
  }

  /* ---- fit: A4 pages */
  [].forEach.call(document.querySelectorAll('.tc-sheet'), function (s, i) {
    var r = s.getBoundingClientRect(), a4 = r.width * 297 / 210;
    var st = s.querySelector('.tc-sheet__title');
    if (st) { var sl = Math.round(st.getBoundingClientRect().height / parseFloat(getComputedStyle(st).lineHeight)); if (sl > 3) add('warn', 'fit', 'page ' + (i + 1) + ': the title runs to ' + sl + ' lines (2 is the norm)'); }
    if (r.height > a4 + 1.5) add('error', 'fit', 'page ' + (i + 1) + ' is ' + Math.round(r.height - a4) + 'px too long for A4: cut content (pages do not flow into each other)');
  });
  /* ---- fit: slides */
  [].forEach.call(document.querySelectorAll('.tc-slide'), function (s, i) {
    var r = s.getBoundingClientRect(), foot = s.querySelector('.tc-slide__foot'), brand = s.querySelector('.tc-slide__brand');
    var fr = foot ? foot.getBoundingClientRect() : null, br = brand && getComputedStyle(brand).position === 'absolute' ? brand.getBoundingClientRect() : null;
    [].forEach.call(s.querySelectorAll('.tc-slide__title'), function (t) {
      var lines = Math.round(t.getBoundingClientRect().height / parseFloat(getComputedStyle(t).lineHeight));
      if (lines > 3) add('error', 'fit', 'slide ' + (i + 1) + ': the headline runs to ' + lines + ' lines (3 at most): shorten it to one claim');
    });
    [].forEach.call(s.children, function (c) {
      if (c === foot || c === brand || getComputedStyle(c).position === 'absolute') return;
      var cr = c.getBoundingClientRect(); if (!cr.height) return;
      if (cr.bottom > r.bottom + 1) add('error', 'fit', 'slide ' + (i + 1) + ': content is cut off at the bottom by ' + Math.round(cr.bottom - r.bottom) + 'px (' + name(c) + ')');
      else if (fr && cr.bottom > fr.top - 2) add('error', 'fit', 'slide ' + (i + 1) + ': content runs into the footer (' + name(c) + ')');
      if (cr.top < r.top - 1) add('error', 'fit', 'slide ' + (i + 1) + ': content starts above the slide (' + name(c) + ')');
      else if (br && cr.top < br.bottom + 2) add('error', 'fit', 'slide ' + (i + 1) + ': content runs into the logo row (' + name(c) + ')');
      if (cr.right > r.right + 1) add('error', 'fit', 'slide ' + (i + 1) + ': content is cut off at the right (' + name(c) + ')');
    });
  });
  /* ---- fit: covers */
  [].forEach.call(document.querySelectorAll('.tc-cover'), function (c, i) {
    var r = c.getBoundingClientRect();
    [].forEach.call(c.querySelectorAll('.tc-cover__title'), function (t) {
      var lines = Math.round(t.getBoundingClientRect().height / parseFloat(getComputedStyle(t).lineHeight));
      if (lines > 3) add('error', 'fit', 'cover ' + (i + 1) + ': the title runs to ' + lines + ' lines (3 at most)');
    });
    [].forEach.call(c.querySelectorAll('.tc-cover__caption'), function (t) {
      var lh = parseFloat(getComputedStyle(t).lineHeight), lab = t.querySelector('.tc-label'), hh = t.getBoundingClientRect().height - (lab ? lab.getBoundingClientRect().height + 12 : 0);
      if (Math.round(hh / lh) > 2) add('warn', 'fit', 'cover ' + (i + 1) + ': the caption beside the figure runs to ' + Math.round(hh / lh) + ' lines (1 or 2)');
    });
    [].forEach.call(c.querySelectorAll('*'), function (el) {
      if (el.closest('svg')) return;
      var has = false; for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3 && n.nodeValue.trim()) { has = true; break; }
      if (!has) return;
      var cr = el.getBoundingClientRect();
      if (cr.right > r.right - 8 || cr.left < r.left + 8 || cr.bottom > r.bottom - 8 || cr.top < r.top + 8) add('error', 'fit', 'cover ' + (i + 1) + ': text touches or leaves the edge (' + name(el) + ')');
    });
  });
  /* ---- fit: clipped and off-screen content */
  var all = document.body.querySelectorAll('*');
  [].forEach.call(all, function (el) {
    if (skipped(el) || el.closest('svg')) return;
    var cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    var cl = el.getAttribute('class') || '';
    var hidX = /hidden|clip/.test(cs.overflowX), hidY = /hidden|clip/.test(cs.overflowY);
    if ((hidX || hidY) && !/tc-sheet|tc-slide|tc-marquee|tc-numeral/.test(cl) && !el.hasAttribute('data-tc-crop') && el.clientHeight > 0) {
      var dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
      if (cs.textOverflow === 'ellipsis' && dx > 1) add('warn', 'fit', 'label is shortened with "...": ' + name(el));
      else if ((hidY && dy > 3) || (hidX && dx > 3)) add('error', 'fit', 'content is cut inside ' + name(el) + ' (' + Math.max(dy, dx) + 'px hidden)');
    }
    var own = false; for (var tn = el.firstChild; tn; tn = tn.nextSibling) if (tn.nodeType === 3 && tn.nodeValue.trim()) { own = true; break; }
    if (own && cs.overflowX === 'visible' && cs.display.indexOf('inline') !== 0 && el.clientWidth > 0 && el.scrollWidth - el.clientWidth > 2 && !el.closest('.tc-rail, .tc-marquee'))
      add('error', 'fit', 'text is ' + (el.scrollWidth - el.clientWidth) + 'px wider than its box and runs into what is next to it: ' + name(el) + ' (shorten it, or use fewer columns)');
    if (/auto|scroll/.test(cs.overflowX) && el.scrollWidth - el.clientWidth > 4 && !/tc-rail|tc-app__tabs/.test(cl))
      add('warn', 'fit', (el.scrollWidth - el.clientWidth) + 'px of ' + name(el).split('"')[0] + 'is off-screen at ' + vw + 'px: a screenshot or PDF will not show it (fewer columns, or class tc-app__tablewrap--wrap)');
  });
  if (document.documentElement.scrollWidth > vw + 2 && !document.querySelector('.tc-slide, .tc-sheet, .tc-cover')) add('error', 'fit', 'the page scrolls sideways at ' + vw + 'px wide');

  /* ---- look: what is actually rendered */
  [].forEach.call(all, function (el) {
    if (skipped(el)) return;
    var cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    var r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    var inSvg = !!el.closest('svg');
    var ownText = false; for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3 && n.nodeValue.trim()) { ownText = true; break; }
    if (ownText && !inSvg) {
      var fam = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase();
      var mono = /^(geist mono|geistmono|ui-monospace|monospace|sfmono|menlo)/.test(fam);
      if (!mono && !/^aspekta/.test(fam)) add('error', 'look', 'font "' + fam + '" is not part of the system: ' + name(el));
      var w = parseInt(cs.fontWeight, 10), size = parseFloat(cs.fontSize), canvas = !!el.closest('.tc-cover, .tc-slide');
      if (w >= 600) add('error', 'look', 'bold text (weight ' + w + '): everything is light (300), nothing is heavier than 400: ' + name(el));
      else if (w >= 500) add(size >= 20 ? 'error' : 'warn', 'look', 'weight ' + w + ' (text is 300, numerals 200, buttons 400): ' + name(el));
      else if (w >= 400 && size >= 28 && !mono) add('warn', 'look', 'a ' + Math.round(size) + 'px headline at weight 400: headlines are light (300): ' + name(el));
      if (cs.textTransform === 'uppercase' && size > 18.5 && !canvas) add('warn', 'look', 'uppercase at ' + Math.round(size) + 'px (only mono labels of 10 to 14px): ' + name(el));
      if (cs.textTransform === 'uppercase' && !mono) add('warn', 'look', 'uppercase text in the sans face: capitals are always Geist Mono: ' + name(el));
      if (cs.textShadow && cs.textShadow !== 'none') add('error', 'look', 'text-shadow on ' + name(el));
      if (cs.fontStyle === 'italic') add('warn', 'look', 'italic text: ' + name(el));
      var c = rgba(cs.color); if (!inPal(c)) add('error', 'look', 'text colour #' + c.hex + ' is not in the palette: ' + name(el));
    }
    if (!inSvg) {
      var b = rgba(cs.backgroundColor); if (!inPal(b)) add('error', 'look', 'background #' + b.hex + ' is not in the palette: ' + name(el));
      var bi = cs.backgroundImage;
      if (bi && bi.indexOf('gradient') >= 0) {
        var bad = (bi.match(/(rgba?|oklch|oklab|color|hsla?)\([^()]*\)/g) || []).filter(function (x) { return !inPal(rgba(x)); });
        if (bad.length) add('error', 'look', 'gradient with off-palette colours on ' + name(el));
        else if (!el.closest('.tc-ember, .tc-veil, .tc-noir, .tc-band, .tc-cover, .tc-slide--ember, .tc-powered, .tc-photo')) add('warn', 'look', 'gradient outside a panel (ember, veil, noir, band, cover): ' + name(el));
        if (/text/.test(cs.webkitBackgroundClip || cs.backgroundClip || '') && !el.closest('.tc-powered')) add('error', 'look', 'gradient text on ' + name(el) + ' (it exists only in the tc-powered label)');
      }
    } else if (/^(path|rect|circle|ellipse|line|polyline|polygon|text)$/i.test(el.tagName)) {
      ['fill', 'stroke'].forEach(function (p) { var v = cs[p]; if (v && v !== 'none' && v.indexOf('url(') < 0) { var c2 = rgba(v);
        if (p === 'fill' && c2.hex === '000000' && !/^text$/i.test(el.tagName)) return; /* the SVG default on stroke-only shapes */
        if (!inPal(c2)) add('warn', 'look', 'drawing colour #' + c2.hex + ' is not in the palette (wrap a third-party graphic in data-tc-skip)'); } });
    }
  });

  /* ---- brand and assets */
  [].forEach.call(document.querySelectorAll('[data-tc-logo]'), function (el) { if (!el.querySelector('svg')) add('error', 'brand', 'logo placeholder was never filled in: run scripts/inline.py'); });
  [].forEach.call(document.querySelectorAll('img'), function (im) { if (!skipped(im) && im.complete && im.naturalWidth === 0) add('error', 'brand', 'image did not load: ' + (im.getAttribute('src') || '').slice(0, 60)); });
  if (document.querySelector('link[rel="stylesheet"][href*="tacto.css"]')) add('warn', 'brand', 'tacto.css is linked, not bundled: run scripts/inline.py before sending the file');
  var wmNames = []; [].forEach.call(document.querySelectorAll('.tc-wordmark'), function (w) { if (w.querySelector('.tc-wordmark__mark')) wmNames.push((w.textContent || '').replace(/\s+/g, ' ').trim()); });
  var fontOk = false; try { document.fonts.forEach(function (f) { if (/Aspekta/.test(f.family) && f.status === 'loaded') fontOk = true; }); } catch (e) {}
  if (!fontOk) add('warn', 'look', 'Aspekta did not load: the text is set in a fallback font (run scripts/inline.py, which embeds the fonts)');

  var res = { vw: vw, lang: document.documentElement.lang || '', sheets: document.querySelectorAll('.tc-sheet').length, slides: document.querySelectorAll('.tc-slide').length, covers: document.querySelectorAll('.tc-cover').length,
              wordmarks: wmNames, text: visibleText().slice(0, 200000), findings: out };
  document.documentElement.setAttribute('data-tc-check', btoa(unescape(encodeURIComponent(JSON.stringify(res)))));
}, 4500); });
</script>
"""


def find_chrome():
    for c in CHROMES:
        if os.path.isabs(c):
            if os.access(c, os.X_OK):
                return c
        else:
            from shutil import which
            if which(c):
                return which(c)
    return None


def palette():
    """The palette is whatever assets/tacto.css uses: one source of truth."""
    return sorted(tacto_lint.load_palette().values())


def run_probe(chrome, src: Path, query: str, width: int, height: int = 900):
    html = src.read_text(encoding="utf-8", errors="replace")
    probe = PROBE.replace("__PALETTE__", json.dumps(palette())).replace("__ALPHA__", json.dumps(sorted(tacto_lint.ALPHA_OK)))
    html = html.replace("</body>", probe + "</body>") if "</body>" in html else html + probe
    tmp = src.parent / f".tc-check-{os.getpid()}.html"
    try:
        tmp.write_text(html, encoding="utf-8")
        done = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-prefers-reduced-motion",
                               f"--window-size={width},{height}", "--virtual-time-budget=9000", "--dump-dom", f"file://{tmp}{query}"],
                              capture_output=True, text=True, timeout=120)
    finally:
        tmp.unlink(missing_ok=True)
    m = re.search(r'data-tc-check="([A-Za-z0-9+/=]+)"', done.stdout)
    if not m:
        return None
    return json.loads(base64.b64decode(m.group(1)).decode("utf-8"))


def pdf_pages(chrome, src: Path, query: str):
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "check.pdf"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--force-prefers-reduced-motion", "--virtual-time-budget=9000",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", f"file://{src}{query}"], capture_output=True, timeout=120)
        if not out.is_file():
            return None
        return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", out.read_bytes()))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict, canvases_only = "--strict" in sys.argv, "--canvases" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    raw = args[0][7:] if args[0].startswith("file://") else args[0]
    path_s, _, q = raw.partition("?")
    query = "?" + q if q else ""
    src = Path(path_s).resolve()
    if not src.is_file():
        print(f"tacto_check: no such file: {src}", file=sys.stderr)
        return 2
    chrome = find_chrome()
    if not chrome:
        print("tacto_check: no Chrome, Chromium or Edge found. Only the source lint can run: python3 scripts/tacto_lint.py", file=sys.stderr)
        return 2

    findings = []  # (level, where, kind, msg)

    def take(res, where):
        for f in res["findings"]:
            if canvases_only and f["kind"] != "fit":
                continue
            msg = f["msg"] + (f"  (x{f['n']})" if f["n"] > 1 else "")
            findings.append((f["level"], where, f["kind"], msg))

    first = run_probe(chrome, src, query, 1440)
    if first is None:
        print("tacto_check: the page could not be read in Chrome (script error on the page, or it never finished loading)", file=sys.stderr)
        return 2
    canvases = first["sheets"] + first["slides"]
    covers = first.get("covers", 0) if not canvases else 0
    if first["slides"]:
        res = run_probe(chrome, src, query, 1320)
        take(res, "slides")
    elif covers:
        res = run_probe(chrome, src, query, 1320, 1300)   # a cover is a fixed canvas: no phone check
        take(res, "cover")
    elif first["sheets"]:
        res = run_probe(chrome, src, query, 900)
        take(res, "pages")
    else:
        take(first, "1440px")
        res = first
        if not canvases_only:
            narrow = run_probe(chrome, src, query, 500)
            if narrow:
                for f in narrow["findings"]:
                    if f["kind"] == "fit" and f["level"] == "error":
                        findings.append((f["level"], "500px", "fit", f["msg"]))

    if canvases:
        pages = pdf_pages(chrome, src, query)
        if pages is None:
            findings.append(("error", "print", "print", "the PDF could not be produced"))
        elif pages != canvases:
            findings.append(("error", "print", "print", f"the PDF has {pages} page(s) for {canvases} sheet(s)/slide(s): something is too long in print. Cut content, export again, look at the pages"))

    if not canvases_only:
        # copy, as rendered (covers text that scripts build)
        own = tacto_lint.SKILL_ROOT not in src.parents
        rep = tacto_lint.Report(src, res["text"])
        tacto_lint.lint_copy(rep, res["text"], False, own)
        for level, _line, kind, msg in rep.items:
            findings.append((level, "rendered", kind, msg))
        if res["wordmarks"] and (ROOT / "brand.local" / "brand.json").is_file():
            # Only wordmarks that carry the private brand's own name (or a template sample name) should have
            # become its logo. A wordmark with another sender's name is that sender's, and stays as text.
            cfg = json.loads((ROOT / "brand.local" / "brand.json").read_text(encoding="utf-8"))
            brand = cfg.get("name", "")
            ours = {brand.lower()} | {a.lower() for a in cfg.get("aliases", [])} | {"northdesk", "your company", "yourcompany"}
            left = [w for w in res["wordmarks"] if w.lower() in ours]
            if left:
                findings.append(("error", "rendered", "brand", f"{len(left)} text wordmark(s) left where the {brand} logo belongs: run scripts/inline.py (without --no-brand)"))
        # source
        srep = tacto_lint.lint_file(src, set())
        for level, line, kind, msg in srep.items:
            findings.append((level, f"L{line}", kind, msg))

    seen, uniq = set(), []
    for f in findings:
        key = (f[0], f[2], re.sub(r"\s+\(x\d+\)$", "", f[3]))
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    order = {"error": 0, "warn": 1, "note": 2}
    uniq.sort(key=lambda f: (order.get(f[0], 3), f[2]))
    for level, where, kind, msg in uniq:
        print(f"  {level:<5} {where:<9} {kind:<7} {msg}")
    errors = sum(1 for f in uniq if f[0] == "error")
    warns = sum(1 for f in uniq if f[0] == "warn")
    verdict = "PASS" if errors == 0 and not (strict and warns) else "FAIL"
    kind = (f"{first['slides']} slide(s)" if first["slides"] else f"{first['sheets']} page(s)" if first["sheets"]
            else f"{covers} cover(s)" if covers else "web page, checked at 1440px and 500px")
    print(f"{verdict}: {errors} error(s), {warns} warning(s) - {src.name} ({kind})")
    if verdict == "PASS":
        print("Now look at it: scripts/shoot.sh for the screenshot" + (" and the PDF page pictures." if canvases else "."))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
