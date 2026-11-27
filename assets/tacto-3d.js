/* tacto-design: tacto-3d.js - the 3D part viewer. Load three.js r128 first (assets/vendor/three.min.js).

   <div class="tc-part" data-tc-part="housing"></div>            one part: turns slowly, drag it, throw it
   <div class="tc-part" data-tc-part="station" id="m"></div>     an assembly: hover and click its parts
   <button data-tc-explode="#m">Exploded view</button>           pulls the assembly apart and back
   <div class="tc-part" data-tc-part="unit" data-explode="scroll"></div>   comes apart as the page scrolls

   Two looks, both fixed here, never restyled per page:
   metal    dark gunmetal with a soft studio reflection and no outlines, as in the Geometry card of
            Tacto's product. The default for a part and for an assembly without status colours.
   drawing  light grey solids with dark edge lines. Used when an assembly shows status colours
            (the colours need the pale ground), or with data-look="drawing".

   Attributes: data-tc-part = a name from TcParts.names(), or JSON (see references/3d.md) ·
   data-explode = "scroll" | a number 0..1 · data-explode-range="0.15,0.7" (part of the scene's
   progress over which it comes apart) · data-turn="1.6" (radians it turns across the scene) ·
   data-spin="false" · data-status="false" (no status colours) · data-look="metal" | "drawing" ·
   data-view="-35,22" (where it is seen from at first: turn and tilt in degrees; 0,0 is the front) ·
   data-grid (floor grid) · data-theme="dark" · data-highlight="Housing|Gear" (parts shown in orange;
   with data-explode="scroll" add data-highlight-from="0.75": only from that point of the scene on) ·
   data-dust (fine specks that spread as it comes apart; for one story object on black, nowhere else)
   Script: el.tcPart.explode(0..1 | true | false) · .spin(bool) · .filter('new' | null) ·
   .pick(i | null) · event "tc:pick" with detail { index, name, status }. No other dependencies. */
(function () {
  'use strict';
  var REDUCE = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var SNAP = !!window.TC_SNAP;          /* set by scripts/shoot.sh for a picture: no easing, the end state at once */
  var INTRO = !REDUCE && !SNAP;         /* parts of an assembly arrive one after another */
  var COL = { part: 0xcfd3d8, raw: 0xe4e6ea, edge: 0x3f3f46, same: 0xd0d3d9, exists: 0x4fc79a, near: 0xf2b755, 'new': 0x6f9ff0, format: 0xffffff, diff: 0xff6414, metal: 0x4b4f57, steel: 0xa9afb8 };
  var SPIN = 0.0028, PI = Math.PI;

  /* ---------- solids. Millimetres. x to the right, y up, z towards the viewer.
     ['b', w, h, d, x, y, z, rx, ry, rz]        box, centre at x y z
     ['c', r, length, x, y, z, axis]            cylinder along 'z' (default), 'x' or 'y'
     ['t', R, r, length, x, y, z, axis, holes]  tube or drilled disc; holes [[x, y, r], ...] in its face
     ['l', a, b, thickness, depth, x, y, z]     angle profile, legs a and b
     ['p', [[x, y], ...], depth, x, y, z, holes, axis]  any outline, extruded along z (or 'x', 'y'), with round holes
     Rotations are in radians. Holes are given in the outline's own coordinates. */
  function turn(geo, axis) { if (axis === 'x') geo.rotateY(PI / 2); else if (axis === 'y') geo.rotateX(-PI / 2); return geo; }
  function solid(d) {
    var T = window.THREE, geo, sh, i;
    if (d[0] === 'b') {
      geo = new T.BoxGeometry(d[1], d[2], d[3]);
      if (d[7]) geo.rotateX(d[7]); if (d[8]) geo.rotateY(d[8]); if (d[9]) geo.rotateZ(d[9]);
      geo.translate(d[4] || 0, d[5] || 0, d[6] || 0);
    } else if (d[0] === 'c') {
      geo = new T.CylinderGeometry(d[1], d[1], d[2], 36); geo.rotateX(PI / 2); turn(geo, d[6]); geo.translate(d[3] || 0, d[4] || 0, d[5] || 0);
    } else if (d[0] === 't') {
      sh = new T.Shape(); sh.absarc(0, 0, d[1], 0, PI * 2, false);
      if (d[2] > 0) hole(sh, 0, 0, d[2]);
      (d[8] || []).forEach(function (h) { hole(sh, h[0], h[1], h[2]); });
      geo = new T.ExtrudeGeometry(sh, { depth: d[3], bevelEnabled: false, curveSegments: 36 }); geo.translate(0, 0, -d[3] / 2);
      turn(geo, d[7]); geo.translate(d[4] || 0, d[5] || 0, d[6] || 0);
    } else if (d[0] === 'l') {
      sh = new T.Shape(); sh.moveTo(0, 0); sh.lineTo(d[1], 0); sh.lineTo(d[1], d[3]); sh.lineTo(d[3], d[3]); sh.lineTo(d[3], d[2]); sh.lineTo(0, d[2]); sh.closePath();
      geo = new T.ExtrudeGeometry(sh, { depth: d[4], bevelEnabled: false }); geo.translate((d[5] || 0) - d[1] / 2, (d[6] || 0) - d[2] / 2, (d[7] || 0) - d[4] / 2);
    } else {
      sh = new T.Shape(); sh.moveTo(d[1][0][0], d[1][0][1]);
      for (i = 1; i < d[1].length; i++) sh.lineTo(d[1][i][0], d[1][i][1]);
      sh.closePath(); (d[6] || []).forEach(function (h) { hole(sh, h[0], h[1], h[2]); });
      geo = new T.ExtrudeGeometry(sh, { depth: d[2], bevelEnabled: false, curveSegments: 28 }); geo.translate(0, 0, -d[2] / 2); turn(geo, d[7]); geo.translate(d[3] || 0, d[4] || 0, d[5] || 0);
    }
    return geo;
  }
  function hole(sh, x, y, r) { var p = new window.THREE.Path(); p.absarc(x, y, r, 0, PI * 2, true); sh.holes.push(p); }
  function ring(n, R, r, phase) { var a = [], i; for (i = 0; i < n; i++) a.push([R * Math.cos(phase + i * 2 * PI / n), R * Math.sin(phase + i * 2 * PI / n), r]); return a; }
  function rect(w, h) { return [[0, 0], [w, 0], [w, h], [0, h]]; }

  /* ---------- the library: single parts, then assemblies (a list of named parts) */
  var LIB = {
    bar: function () { return [['p', rect(150, 22), 12, -75, -11, 0, [[18, 11, 4], [75, 11, 4], [132, 11, 4]]]]; },
    plate: function () { return [['p', rect(140, 84), 5, -70, -42, 0, [[16, 16, 5], [124, 16, 5], [16, 68, 5], [124, 68, 5]]]]; },
    block: function () { return [['p', [[0, 0], [120, 0], [120, 16], [92, 16], [92, 62], [28, 62], [28, 16], [0, 16]], 40, -60, -31, 0, [[60, 40, 13]]]]; },
    angle: function () { return [['p', [[0, 0], [90, 0], [90, 9], [9, 9], [9, 64], [0, 64]], 44, -45, -32, 0]]; },
    gusset: function () { return [['p', [[0, 0], [70, 0], [70, 8], [8, 70], [0, 70]], 6, -30, -30, 0, [[18, 18, 5]]]]; },
    sleeve: function () { return [['t', 20, 11, 46, 0, 0, 0]]; },
    shaft: function () { return [['c', 12, 150, 0, 0, 0, 'x'], ['c', 17, 34, -28, 0, 0, 'x'], ['c', 8, 30, 90, 0, 0, 'x']]; },
    flange: function () { return [['t', 60, 24, 14, 0, 0, -20, 'z', ring(8, 46, 5, 0)], ['t', 34, 24, 40, 0, 0, 7]]; },
    housing: function () { return [['t', 47, 18, 12, 0, 0, -38, 'z', ring(6, 36, 4, PI / 6)], ['t', 32, 18, 46, 0, 0, -9], ['t', 24, 18, 30, 0, 0, 29]]; },
    frame: function () {
      return [['b', 160, 10, 10, 0, -45, 0], ['b', 160, 10, 10, 0, 45, 0], ['b', 10, 80, 10, -75, 0, 0], ['b', 10, 80, 10, 75, 0, 0], ['b', 10, 80, 10, 0, 0, 0],
        ['b', 10, 10, 60, -75, -45, 25], ['b', 10, 10, 60, 75, -45, 25]];
    },
    /* a bearing unit on a base: comes apart along its axis */
    unit: function () {
      var P = [], i, a;
      function p(n, g, s, o) { P.push({ n: n, g: g, s: s, o: o }); }
      var side = [[0, 0], [150, 0], [150, 60], [112, 118], [38, 118], [0, 60]];
      p('Base plate', 'same', [['b', 260, 12, 190, 0, 6, 10]], [0, -60, 0]);
      p('Side plate', 'near', [['p', side, 10, -75, 12, -58, [[75, 70, 31]]]], [0, 0, -150]);
      p('Bearing', 'exists', [['t', 30, 14, 16, 0, 82, -30]], [0, 0, -80]);
      p('Housing', 'new', [['t', 44, 30, 78, 0, 82, 0], ['t', 58, 30, 10, 0, 82, -44, 'z', ring(6, 49, 4, 0)]], [0, 0, 0]);
      p('Shaft', 'same', [['c', 14, 250, 0, 82, 20], ['c', 20, 26, 0, 82, 0]], [0, 70, 0]);
      p('Bearing', 'exists', [['t', 30, 14, 16, 0, 82, 30]], [0, 0, 70]);
      p('Side plate', 'near', [['p', side, 10, -75, 12, 58, [[75, 70, 31]]]], [0, 0, 120]);
      p('Cover', 'new', [['t', 58, 15, 8, 0, 82, 68, 'z', ring(6, 49, 4, 0)]], [0, 0, 170]);
      for (i = 0; i < 6; i++) { a = i * PI / 3; p('Screw', 'same', [['c', 3.4, 30, 49 * Math.cos(a), 82 + 49 * Math.sin(a), 80], ['c', 6, 5, 49 * Math.cos(a), 82 + 49 * Math.sin(a), 97]], [0, 0, 215]); }
      p('Gear', 'near', [['t', 52, 14, 20, 0, 82, 112, 'z', ring(5, 33, 8, PI / 5)]], [0, 0, 270]);
      p('Lock ring', 'same', [['t', 22, 14, 8, 0, 82, 130]], [0, 0, 320]);
      [-1, 1].forEach(function (k) { p('Gusset', 'new', [['p', [[0, 0], [44, 0], [0, 56]], 8, k < 0 ? -122 : 78, 12, 10].concat(k > 0 ? [] : [])], [k * 70, 0, 0]); });
      return P;
    },
    /* a machine station, 148 drawing parts: frame, shafts, rollers, bearings, covers, format parts */
    station: function () {
      var P = [], s = [], i;
      function p(g, n, sol) { P.push({ g: g, n: n, s: sol }); }
      [-520, 520].forEach(function (x) { [-260, 260].forEach(function (z) { p('same', 'Foot', [['b', 90, 10, 90, x, 5, z]]); s.push(['b', 40, 410, 40, x, 215, z]); }); });
      [-260, 260].forEach(function (z) { s.push(['b', 1000, 40, 40, 0, 120, z], ['b', 1080, 40, 40, 0, 440, z]); });
      [-520, 520].forEach(function (x) { s.push(['b', 40, 40, 480, x, 120, 0], ['b', 40, 40, 480, x, 440, 0], ['b', 16, 400, 16, x, 280, 0, 0.9], ['b', 16, 400, 16, x, 280, 0, -0.9]); });
      p('new', 'Base frame', s);
      for (i = 0; i < 6; i++) p('new', 'Chute sheet', [['b', 150, 3, 440, -375 + 150 * i, 300, 0, 0, 0, i % 2 ? 0.3 : -0.3]]);
      [-470, 470].forEach(function (x) { [-238, 238].forEach(function (z) { p('new', 'Gusset', [['b', 60, 60, 4, x, 400, z]]); }); });
      [-498, 498].forEach(function (x) { [-210, 210].forEach(function (z) { p('new', 'Gusset', [['b', 4, 60, 60, x, 400, z]]); }); });
      [-492, 492].forEach(function (x) { p('near', 'Bearing plate', [['b', 10, 150, 220, x, 300, 0]]); });
      [-260, 0, 260].forEach(function (x) { p('new', 'Cross beam', [['b', 50, 40, 470, x, 440, 0], ['b', 70, 80, 10, x, 440, -234], ['b', 70, 80, 10, x, 440, 234]]); });
      for (i = 0; i < 5; i++) p('new', 'Tie bar', [['b', 14, 22, 496, -325 + 130 * i, 510, 0]]);
      [-254, 254].forEach(function (z) { p('new', 'Side wall', [['b', 960, 220, 12, 0, 570, z]]); });
      for (i = 0; i < 7; i++) p('new', 'Shaft', [['c', 11, 590, -390 + 130 * i, 590, 0]]);
      [0, 3, 6].forEach(function (n) { p('same', 'Roller', [['c', 24, 320, -390 + 130 * n, 590, 0]]); });
      [2, 5].forEach(function (n) { p('same', 'Roller', [['c', 24, 180, -390 + 130 * n, 590, 0]]); });
      [1, 2, 4, 5].forEach(function (n) { [-120, 120].forEach(function (z) { p('new', 'Cam disc', [['c', 42, 12, -390 + 130 * n, 590, z]]); }); });
      [0, 1, 2, 3, 4, 5, 6].forEach(function (n) { [-268, 268].forEach(function (z) { var e = n === 1 && z > 0; p(e ? 'exists' : 'new', e ? 'Bearing block' : 'Bearing seat', [['b', 70, 56, 16, -390 + 130 * n, 590, z]]); }); });
      [0, 1, 2, 3, 4, 5, 6].forEach(function (n) { [-286, 286].forEach(function (z) { p(n === 5 && z > 0 ? 'exists' : 'same', 'Sleeve', [['c', 17, 16, -390 + 130 * n, 590, z]]); }); });
      for (i = 0; i < 11; i++) p(i === 6 ? 'exists' : 'same', 'Bracket', [['l', 30, 30, 4, 16, -400 + 80 * i, 476, i % 2 ? -270 : 270]]);
      [-325, 0, 325].forEach(function (x) { [-263, 263].forEach(function (z) { p('new', 'Side sheet', [['b', 44, 56, 3, x, 650, z]]); }); });
      [-200, 200].forEach(function (x) { p('near', 'Sensor bracket', [['l', 46, 46, 5, 30, x, 648, 277]]); });
      [-440, 440].forEach(function (x) { p('near', 'Pin', [['c', 7, 500, x, 650, 0]]); });
      [-265, 265].forEach(function (x) { [-284, 284].forEach(function (z) { p('new', 'Cover', [['b', 470, 290, 3, x, 280, z]]); }); });
      [-546, 546].forEach(function (x) { p('near', 'Guard', [['b', 3, 290, 470, x, 280, 0]]); });
      [-150, 150].forEach(function (z) { p('new', 'Console', [['b', 130, 12, 120, -614, 470, z], ['b', 12, 110, 120, -555, 421, z]]); });
      [-300, 0, 300].forEach(function (x) { p('new', 'Table plate', [['b', 230, 8, 500, x, 686, 0]]); });
      for (i = 0; i < 10; i++) p(i === 4 || i === 7 ? 'near' : 'same', 'Guide rail', [['b', 760, 12, 18, 0, 697, -180 + 40 * i]]);
      p('same', 'Clamp', [['b', 44, 30, 34, -330, 718, 0]]); p('exists', 'Clamp', [['b', 44, 30, 34, 330, 718, 0]]);
      [-475, 475].forEach(function (x) { p('near', 'Hood', [['b', 110, 46, 470, x, 705, 0]]); });
      [0, 1, 2, 3, 4].forEach(function (n) { [-95, 95].forEach(function (z) { p('format', 'Folding finger', [['b', 70, 100, 4, -240 + 120 * n, 778, z, z > 0 ? -0.5 : 0.5]]); }); });
      [-140, -60, 60, 140].forEach(function (z) { p('format', 'Format guide', [['b', 560, 10, 10, 0, 709, z]]); });
      [-275, 275].forEach(function (x) { [-140, 140].forEach(function (z) { p('format', 'Format guide', [['b', 10, 80, 10, x, 754, z]]); }); });
      for (i = 0; i < 5; i++) p('format', 'Pusher', [['b', 50, 36, 70, -200 + 100 * i, 722, 0]]);
      return P;
    }
  };

  /* a spec becomes a list of parts: [{ n, g, s: [solids] }] */
  function parts(spec) {
    if (typeof spec === 'string') {
      var name = spec.trim();
      if (LIB[name]) spec = LIB[name]();
      else { try { spec = JSON.parse(name); } catch (e) { spec = null; } }
    }
    if (!spec || !spec.length) return null;
    if (typeof spec[0][0] === 'string') return [{ n: '', g: '', s: spec }];          /* solids of one part */
    return spec.map(function (p) { return { n: p.n || p.name || '', g: p.g || p.status || '', s: p.s || p.solids || [], o: p.o || p.out || null }; });
  }

  /* ---------- without WebGL: a plain front-view drawing of the same solids */
  function flat(list) {
    var out = [], x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    function box(x, y, w, h) { x0 = Math.min(x0, x); y0 = Math.min(y0, -y - h); x1 = Math.max(x1, x + w); y1 = Math.max(y1, -y); return '<rect x="' + x + '" y="' + (-y - h) + '" width="' + w + '" height="' + h + '"/>'; }
    function circ(x, y, r) { box(x - r, y - r, 2 * r, 2 * r); return '<circle cx="' + x + '" cy="' + (-y) + '" r="' + r + '"/>'; }
    list.forEach(function (p) { p.s.forEach(function (d) {
      if (d[0] === 'b') out.push(box((d[4] || 0) - d[1] / 2, (d[5] || 0) - d[2] / 2, d[1], d[2]));
      else if (d[0] === 'c') out.push(d[6] === 'x' ? box((d[3] || 0) - d[2] / 2, (d[4] || 0) - d[1], d[2], 2 * d[1]) : d[6] === 'y' ? box((d[3] || 0) - d[1], (d[4] || 0) - d[2] / 2, 2 * d[1], d[2]) : circ(d[3] || 0, d[4] || 0, d[1]));
      else if (d[0] === 't') { out.push(circ(d[4] || 0, d[5] || 0, d[1])); if (d[2] > 0) out.push(circ(d[4] || 0, d[5] || 0, d[2])); }
      else if (d[0] === 'l') out.push(box((d[5] || 0) - d[1] / 2, (d[6] || 0) - d[2] / 2, d[1], d[2]));
      else { var xs = d[1].map(function (q) { return q[0]; }), ys = d[1].map(function (q) { return q[1]; }); box((d[3] || 0) + Math.min.apply(0, xs), (d[4] || 0) + Math.min.apply(0, ys), 0, 0); box((d[3] || 0) + Math.max.apply(0, xs), (d[4] || 0) + Math.max.apply(0, ys), 0, 0);
        out.push('<polygon points="' + d[1].map(function (q) { return ((d[3] || 0) + q[0]) + ',' + (-(d[4] || 0) - q[1]); }).join(' ') + '"/>'); }
    }); });
    var m = Math.max(x1 - x0, y1 - y0) * 0.06;
    return '<svg class="tc-part__draw" viewBox="' + (x0 - m) + ' ' + (y0 - m) + ' ' + (x1 - x0 + 2 * m) + ' ' + (y1 - y0 + 2 * m) + '" role="img" aria-label="Front view">' + out.join('') + '</svg>';
  }

  /* ---------- the viewer */
  function Viewer(host) {
    var T = window.THREE, self = this, dark = host.getAttribute('data-theme') === 'dark';
    this.host = host; this.list = parts(host.getAttribute('data-tc-part') || 'housing');
    if (!this.list) { host.setAttribute('data-tc-part-error', 'unknown part'); return; }
    if (!T) { this.fail(); return; }
    try { this.r = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });   /* so screenshots and PDFs show it */ } catch (e) { this.fail(); return; }
    this.r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var scene = this.scene = new T.Scene(), el = this.el = this.r.domElement;
    this.cam = new T.PerspectiveCamera(30, 2, 1, 200000);
    this.root = new T.Group(); scene.add(this.root);
    this.multi = this.list.length > 1;
    this.status = this.multi && host.getAttribute('data-status') !== 'false' && this.list.some(function (p) { return !!p.g; });
    var metal = this.metal = (host.getAttribute('data-look') || (this.status ? 'drawing' : 'metal')) === 'metal';
    if (metal) {            /* a studio to reflect: bright above, dim below, two soft lamps. Without it metal is just dark. */
      this.r.outputEncoding = T.sRGBEncoding; this.r.toneMapping = T.ACESFilmicToneMapping; this.r.toneMappingExposure = dark ? 1.05 : 1.25;
      var ev = document.createElement('canvas'); ev.width = 256; ev.height = 128;
      var e2 = ev.getContext('2d'), sky = e2.createLinearGradient(0, 0, 0, 128);
      sky.addColorStop(0, '#ffffff'); sky.addColorStop(0.45, dark ? '#8d9199' : '#c9ccd2'); sky.addColorStop(0.55, dark ? '#2a2c31' : '#6f737b'); sky.addColorStop(1, dark ? '#0a0a0b' : '#3a3d43');
      e2.fillStyle = sky; e2.fillRect(0, 0, 256, 128);
      e2.fillStyle = '#ffffff'; e2.filter = 'blur(6px)'; e2.fillRect(28, 18, 54, 26); e2.fillRect(150, 26, 40, 20);
      if (dark) { e2.fillStyle = '#ff6414'; e2.globalAlpha = 0.55; e2.fillRect(196, 70, 44, 16); e2.globalAlpha = 1; }   /* a little ember low behind */
      var et = new T.CanvasTexture(ev); et.mapping = T.EquirectangularReflectionMapping; et.encoding = T.sRGBEncoding;
      var pm = new T.PMREMGenerator(this.r); scene.environment = pm.fromEquirectangular(et).texture; et.dispose(); pm.dispose();
    }
    scene.add(new T.HemisphereLight(0xffffff, dark ? 0x4a4e57 : 0xb2b7c0, metal ? 0.35 : (dark ? 0.72 : 0.82)));
    this.sun = new T.DirectionalLight(0xffffff, metal ? 0.9 : 0.72); scene.add(this.sun);
    this.fill = new T.DirectionalLight(dark ? 0xff6414 : 0xffffff, dark ? 0.3 : 0.2); scene.add(this.fill);   /* on black, a little ember from behind */
    this.yaw = -0.62; this.pitch = this.multi ? 0.36 : 0.42; this.vy = 0; this.vp = 0;
    var view = (host.getAttribute('data-view') || '').split(',').map(Number);      /* data-view="yaw,pitch" in degrees: 0,0 is the front view */
    if (view.length === 2 && !isNaN(view[0]) && !isNaN(view[1])) { this.yaw = view[0] * PI / 180; this.pitch = Math.min(1.45, view[1] * PI / 180); }
    this.spinOn = host.getAttribute('data-spin') !== 'false' && !REDUCE;
    this.ex = 0; this.tex = 0; this.hot = null; this.sel = null; this.only = null; this.on = false; this.raf = 0; this.t0 = 0; this.scroll = 0; this.turn = 0;
    this.marks = (host.getAttribute('data-highlight') || '').split('|').map(function (s) { return s.trim(); }).filter(Boolean); this.hl = this.marks.length > 0 && !host.hasAttribute('data-highlight-from');
    this.build(dark);
    var ex = host.getAttribute('data-explode');
    if (ex === 'scroll') this.bindScroll(); else if (ex && !isNaN(+ex)) { this.tex = +ex; this.ex = REDUCE ? +ex : 0; }

    /* drag to turn, let go to throw: the speed of the hand carries on and fades into the slow idle turn */
    var drag = null, moved = false;
    el.addEventListener('pointerdown', function (ev) { drag = { x: ev.clientX, y: ev.clientY, sx: ev.clientX, sy: ev.clientY, t: performance.now() }; moved = false; self.vy = self.vp = 0; try { el.setPointerCapture(ev.pointerId); } catch (e) {} });
    el.addEventListener('pointermove', function (ev) {
      if (!drag) { if (self.multi) self.hover(self.hit(ev), ev); return; }
      if (!moved && Math.abs(ev.clientX - drag.sx) + Math.abs(ev.clientY - drag.sy) > 4) { moved = true; self.hover(null); }
      if (!moved) return;
      var dy = -(ev.clientX - drag.x) * 0.008, dp = (ev.clientY - drag.y) * 0.008;
      self.yaw += dy; self.pitch = Math.max(self.multi ? -0.1 : -1.2, Math.min(1.45, self.pitch + dp));
      var t = performance.now(), per = 16.67 / Math.max(4, t - drag.t);      /* speed per frame, whatever the mouse's rate */
      self.vy = Math.max(-0.3, Math.min(0.3, self.vy * 0.5 + dy * per * 0.5)); self.vp = Math.max(-0.1, Math.min(0.1, self.vp * 0.5 + dp * per * 0.5));
      drag.x = ev.clientX; drag.y = ev.clientY; drag.t = t;
    });
    el.addEventListener('pointerup', function (ev) { var was = moved; if (drag && performance.now() - drag.t > 90) self.vy = self.vp = 0;   /* held still before letting go: no throw */
      drag = null; moved = false; self.dragging = false; if (!was && self.multi) self.pick(self.hit(ev)); });
    el.addEventListener('pointercancel', function () { drag = null; moved = false; });
    el.addEventListener('pointerleave', function () { if (!drag) self.hover(null); });
    Object.defineProperty(this, 'dragging', { get: function () { return !!drag; }, set: function () {} });

    host.appendChild(el);
    this.tip = document.createElement('div'); this.tip.className = 'tc-part__tip'; this.tip.hidden = true; host.appendChild(this.tip);
    if (window.ResizeObserver) new ResizeObserver(function () { self.size(); }).observe(host);
    window.addEventListener('resize', function () { self.size(); });
    if (window.IntersectionObserver) new IntersectionObserver(function (es) { self.on = es[0].isIntersecting; if (self.on) self.start(); }, { rootMargin: '120px' }).observe(host);
    else { this.on = true; }
    this.size(); this.on = true; this.start();
    host.tcPart = { viewer: this, highlight: function (names) { self.marks = names ? [].concat(names) : []; self.hl = self.marks.length > 0; self.start(); }, explode: function (v) { return self.explode(v); }, spin: function (b) { self.spinOn = !!b && !REDUCE; }, filter: function (g) { self.only = g || null; }, pick: function (i) { self.pick(i === undefined ? null : i); } };
  }
  Viewer.prototype.fail = function () { this.host.classList.add('is-flat'); this.host.innerHTML = flat(this.list); };
  Viewer.prototype.build = function (dark) {
    var T = window.THREE, self = this, all = new T.Box3(), units = [], meshes = [];
    this.list.forEach(function (p, i) {
      var geos = p.s.map(solid), bb = new T.Box3(), grp = new T.Group();
      geos.forEach(function (g) { g.computeBoundingBox(); bb.union(g.boundingBox); });
      var home = bb.getCenter(new T.Vector3()); all.union(bb);
      var metal = self.metal, col = metal ? (dark ? COL.steel : COL.metal) : (self.status && COL[p.g] !== undefined ? COL[p.g] : (self.multi ? COL.same : COL.part));
      var mat = new T.MeshStandardMaterial({ color: self.multi && INTRO && !metal ? COL.raw : col, roughness: metal ? 0.3 : 0.6, metalness: metal ? 0.78 : 0.08, transparent: true, opacity: self.multi && INTRO ? 0 : 1 });
      var line = metal ? null : new T.LineBasicMaterial({ color: p.g === 'format' && self.status ? 0x8a8f98 : COL.edge, transparent: true, opacity: 0.5 });
      geos.forEach(function (g) { g.translate(-home.x, -home.y, -home.z); var m = new T.Mesh(g, mat); m.userData.i = i; grp.add(m); meshes.push(m); if (line) grp.add(new T.LineSegments(new T.EdgesGeometry(g, 28), line)); });
      grp.position.copy(home); self.root.add(grp);
      units.push({ grp: grp, mat: mat, line: line, home: home, col: col, box: bb.clone(), vis: self.multi && INTRO ? 0 : 1 });
    });
    var c = this.c = all.getCenter(new T.Vector3()), size = all.getSize(new T.Vector3());
    this.h = size.y; this.rad = size.length() / 2; this.floor = all.min.y;
    /* where each part goes in the exploded view: its own offset, or away from the middle and a little up */
    var apart = new T.Box3();
    units.forEach(function (u, i) {
      var o = self.list[i].o;
      u.out = o ? new T.Vector3(o[0], o[1], o[2]) : new T.Vector3((u.home.x - c.x) * 0.8, (u.home.y - (c.y - 0.3 * size.y)) * 0.85, (u.home.z - c.z) * 0.8);
      apart.union(u.box.clone().translate(u.out));
    });
    this.units = units; this.meshes = meshes;
    this.c2 = apart.getCenter(new T.Vector3()); this.rad2 = apart.getSize(new T.Vector3()).length() / 2;
    this.dist = this.rad / Math.sin(15 * PI / 180) * (this.multi ? 1.0 : 0.94);
    this.dist2 = this.rad2 / Math.sin(15 * PI / 180) * 0.74;
    this.sun.position.set(c.x + this.rad * 0.5, c.y + this.rad * 1.6, c.z + this.rad * 1.1);
    this.fill.position.set(c.x - this.rad * 1.3, c.y + this.rad * 0.4, c.z - this.rad * 0.9);
    if (!dark) {                                   /* a soft shadow on the floor, no hard edge */
      var cv = document.createElement('canvas'); cv.width = cv.height = 128;
      var g2 = cv.getContext('2d'), fade = g2.createRadialGradient(64, 64, 6, 64, 64, 64);
      fade.addColorStop(0, this.metal ? 'rgba(0,0,0,.2)' : 'rgba(0,0,0,.24)'); fade.addColorStop(1, 'rgba(0,0,0,0)'); g2.fillStyle = fade; g2.fillRect(0, 0, 128, 128);
      var shade = new T.Mesh(new T.PlaneGeometry(size.x * 1.9 + size.z, size.z * 1.9 + size.x * 0.6), new T.MeshBasicMaterial({ map: new T.CanvasTexture(cv), transparent: true, depthWrite: false }));
      shade.rotation.x = -PI / 2; shade.position.set(c.x, this.floor - size.y * (this.multi ? 0.002 : 0.16), c.z); this.scene.add(shade);
    }
    if (this.host.hasAttribute('data-dust')) {      /* small square specks, mostly white, a few orange and blue: the "bits" */
      var n = 520, pos = new Float32Array(n * 3), cols = new Float32Array(n * 3), seed = 7, c3 = new T.Color(), i;
      var rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
      for (i = 0; i < n; i++) {
        var a = rnd() * 2 * PI, b = Math.acos(2 * rnd() - 1), rr = this.rad2 * (0.35 + rnd() * 1.05);
        pos[i * 3] = rr * Math.sin(b) * Math.cos(a); pos[i * 3 + 1] = rr * Math.cos(b) * 0.62; pos[i * 3 + 2] = rr * Math.sin(b) * Math.sin(a);
        var pick = rnd(); c3.setHex(pick < 0.16 ? 0xff6414 : pick < 0.21 ? 0x2170ec : 0xffffff); cols[i * 3] = c3.r; cols[i * 3 + 1] = c3.g; cols[i * 3 + 2] = c3.b;
      }
      var dg = new T.BufferGeometry(); dg.setAttribute('position', new T.BufferAttribute(pos, 3)); dg.setAttribute('color', new T.BufferAttribute(cols, 3));
      this.dust = new T.Points(dg, new T.PointsMaterial({ size: this.rad2 * 0.011, vertexColors: true, transparent: true, opacity: 0, depthWrite: false }));
      this.scene.add(this.dust);
    }
    if (this.host.hasAttribute('data-grid')) { var grid = new T.GridHelper(Math.ceil(this.rad * 4 / 100) * 100, 26, dark ? 0x3a3a3a : 0xdcdcdc, dark ? 0x262626 : 0xeaeaea); grid.position.set(c.x, this.floor - 1, c.z); this.scene.add(grid); }
  };
  Viewer.prototype.size = function () {
    if (!this.r) return;
    var w = this.host.clientWidth, h = this.host.clientHeight;
    if (!w || !h || (w === this.w && h === this.hh)) return;
    this.r.setSize(w, h, false); this.cam.aspect = w / h; this.cam.updateProjectionMatrix(); this.w = w; this.hh = h; this.fit = Math.max(1, 1.2 / (w / h));
  };
  Viewer.prototype.hit = function (ev) {
    var T = window.THREE, b = this.el.getBoundingClientRect(), self = this;
    this.ray = this.ray || new T.Raycaster(); this.ndc = this.ndc || new T.Vector2();
    this.ndc.set((ev.clientX - b.left) / b.width * 2 - 1, 1 - (ev.clientY - b.top) / b.height * 2);
    this.ray.setFromCamera(this.ndc, this.cam);
    var h = this.ray.intersectObjects(this.meshes.filter(function (m) { var p = self.list[m.userData.i]; return !self.only || p.g === self.only; }), false);
    return h.length ? h[0].object.userData.i : null;
  };
  Viewer.prototype.hover = function (i, ev) {
    if (i !== this.hot) {
      this.hot = i; this.host.classList.toggle('is-hot', i !== null);
      var p = i !== null ? this.list[i] : null;
      this.tip.hidden = !(p && p.n);
      if (p && p.n) this.tip.innerHTML = (this.status && p.g ? '<i class="tc-part__key tc-part__key--' + p.g + '"></i>' : '') + p.n.replace(/[<>&]/g, '');
    }
    if (i !== null && ev && !this.tip.hidden) {
      var b = this.host.getBoundingClientRect(), x = ev.clientX - b.left + 14, y = ev.clientY - b.top + 14;
      this.tip.style.transform = 'translate(' + Math.max(4, Math.min(x, b.width - this.tip.offsetWidth - 8)) + 'px,' + Math.min(y, b.height - 30) + 'px)';
    }
  };
  Viewer.prototype.pick = function (i) {
    this.sel = i;
    var p = i !== null && i !== undefined ? this.list[i] : null;
    this.host.dispatchEvent(new CustomEvent('tc:pick', { bubbles: true, detail: p ? { index: i, name: p.n, status: p.g } : { index: null } }));
  };
  Viewer.prototype.explode = function (v) {
    this.scrollBound = false;
    this.tex = v === undefined || v === 'toggle' ? (this.tex > 0.5 ? 0 : 1) : (v === true ? 1 : v === false ? 0 : Math.max(0, Math.min(1, +v)));
    this.start(); return this.tex;
  };
  /* comes apart with the page: bound to the scene it sits in (tacto-scroll.js), or to its own way across the screen */
  Viewer.prototype.bindScroll = function () {
    var self = this, host = this.host, scene = host.closest('[data-tc-scene]');
    var range = (host.getAttribute('data-explode-range') || '0.15,0.7').split(',').map(Number), turn = +host.getAttribute('data-turn') || 0, from = host.getAttribute('data-highlight-from');
    this.scrollBound = true;
    if (REDUCE) { this.tex = this.ex = +host.getAttribute('data-rest') || 0.6; this.hl = this.marks.length > 0; return; }
    function apply(p) { if (!self.scrollBound) return; self.tex = Math.max(0, Math.min(1, (p - range[0]) / (range[1] - range[0]))); self.turn = p * turn; if (from !== null) self.hl = self.marks.length > 0 && p >= +from; if (SNAP) { self.on = true; self.frame(performance.now()); } else self.start(); }
    if (scene) scene.addEventListener('tc:progress', function (ev) { apply(ev.detail.p); });
    else {
      var own = function () { var b = host.getBoundingClientRect(), vh = window.innerHeight; apply(Math.max(0, Math.min(1, (vh * 0.85 - (b.top + b.height / 2)) / (vh * 0.5)))); };
      window.addEventListener('scroll', own, { passive: true }); own();
    }
  };
  Viewer.prototype.start = function () { var self = this; if (!this.raf && this.r) this.raf = requestAnimationFrame(function (t) { self.frame(t); }); };
  Viewer.prototype.frame = function (now) {
    var self = this, T = window.THREE; this.raf = 0;
    if (!this.on || !document.body.contains(this.host)) return;
    if (!this.t0) this.t0 = now;
    /* everything eases by time, not by frame count: the same on a slow machine and in a screenshot */
    var f = this.last ? Math.min(90, Math.max(0.2, (now - this.last) / 16.67)) : 1; this.last = now;
    function K(rate) { return REDUCE || SNAP ? 1 : 1 - Math.pow(1 - rate, f); }
    if (!this.dragging) {
      var keep = Math.pow(0.955, f);
      this.yaw += this.vy * f; this.pitch = Math.max(this.multi ? -0.1 : -1.2, Math.min(1.45, this.pitch + this.vp * f));
      this.vy = this.vy * keep + (this.spinOn ? SPIN * (1 - keep) : 0); this.vp *= Math.pow(0.9, f);
    }
    this.ex += (this.tex - this.ex) * K(0.1);
    var k = K(0.16), tmp = this.tmp || (this.tmp = new T.Color());
    this.units.forEach(function (u, i) {
      var p = self.list[i], shown = !INTRO || now - self.t0 > 120 + i * (self.units.length > 40 ? 7 : 40);
      u.vis += ((shown ? 1 : 0) - u.vis) * K(0.2);
      u.grp.visible = u.vis > 0.01; if (!u.grp.visible) return;
      u.grp.scale.setScalar(0.55 + 0.45 * u.vis);
      u.grp.position.set(u.home.x + u.out.x * self.ex, u.home.y + u.out.y * self.ex + (1 - u.vis) * self.h * 0.09, u.home.z + u.out.z * self.ex);
      var dim = self.only && p.g !== self.only, sel = !dim && (i === self.sel || i === self.hot);
      tmp.setHex(self.hl && self.marks.indexOf(p.n) >= 0 ? COL.diff : (u.vis > 0.85 || self.metal ? u.col : COL.raw)); u.mat.color.lerp(tmp, k);
      u.mat.opacity += ((dim ? 0.045 : u.vis) - u.mat.opacity) * k; u.mat.depthWrite = u.mat.opacity > 0.5;
      u.mat.emissive.setHex(sel ? (self.metal ? 0x3a2416 : 0x2a2a2a) : 0x000000);
      if (u.line) { u.line.opacity = dim ? 0.05 : (sel ? 0.95 : 0.46) * u.vis; if (sel) u.line.color.setHex(0x0a0a0a); else u.line.color.setHex(p.g === 'format' && self.status ? 0x8a8f98 : COL.edge); }
    });
    var e = this.ex, d = (this.dist + (this.dist2 - this.dist) * e) * (this.fit || 1), yaw = this.yaw + this.turn, cp = Math.cos(this.pitch);
    var lx = this.c.x + (this.c2.x - this.c.x) * e, ly = this.c.y + (this.c2.y - this.c.y) * e, lz = this.c.z + (this.c2.z - this.c.z) * e;
    this.cam.position.set(lx + d * Math.sin(yaw) * cp, ly + d * Math.sin(this.pitch), lz + d * Math.cos(yaw) * cp);
    this.cam.lookAt(lx, ly, lz);
    if (this.dust) { this.dust.position.set(lx, ly, lz); this.dust.scale.setScalar(0.3 + 0.8 * e); this.dust.rotation.y = now * 0.00004; this.dust.material.opacity = Math.min(1, e * 1.3) * 0.8; }
    this.r.render(this.scene, this.cam);
    var settled = REDUCE || (!this.spinOn && Math.abs(this.vy) < 1e-5 && Math.abs(this.tex - this.ex) < 1e-4 && now - this.t0 > 3000 && !this.dragging);
    if (!settled || this.hot !== null) this.start(); else { var again = function () { self.start(); }; this.el.addEventListener('pointerdown', again, { once: true }); this.el.addEventListener('pointermove', again, { once: true }); }
  };

  function mount(root) {
    [].forEach.call((root || document).querySelectorAll('[data-tc-part]'), function (el) { if (!el.tcPartMounted) { el.tcPartMounted = true; new Viewer(el); } });
  }
  /* buttons anywhere on the page: data-tc-explode="#id" · data-tc-spin="#id" · data-tc-filter="new" data-tc-target="#id" */
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('[data-tc-explode], [data-tc-spin], [data-tc-filter]'); if (!b) return;
    var sel = b.getAttribute('data-tc-explode') || b.getAttribute('data-tc-spin') || b.getAttribute('data-tc-target');
    var host = sel ? document.querySelector(sel) : (b.closest('.tc-app__viewer, .tc-card, section') || document).querySelector('[data-tc-part]');
    if (!host || !host.tcPart) return;
    if (b.hasAttribute('data-tc-explode')) b.setAttribute('aria-pressed', String(host.tcPart.explode('toggle') > 0.5));
    else if (b.hasAttribute('data-tc-spin')) { var on = b.getAttribute('aria-pressed') !== 'true'; host.tcPart.spin(on); b.setAttribute('aria-pressed', String(on)); }
    else { var g = b.getAttribute('aria-pressed') === 'true' ? null : b.getAttribute('data-tc-filter'); host.tcPart.filter(g); [].forEach.call(document.querySelectorAll('[data-tc-filter]'), function (o) { o.setAttribute('aria-pressed', String(o === b && !!g)); }); host.tcPart.viewer.start(); }
  });
  window.TcParts = { mount: mount, names: function () { return Object.keys(LIB); }, add: function (name, make) { LIB[name] = typeof make === 'function' ? make : function () { return make; }; } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { mount(); }); else mount();
})();
