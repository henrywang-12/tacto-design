/* tacto-design: tacto-scroll.js - scroll scenes. No dependencies.

   A scene is a tall section whose stage stays pinned while its chapters change:

   <section data-tc-scene style="--tc-screens: 4">       four screens of scrolling
     <div class="tc-scene__stage">                        pinned for the whole scene
       <div class="tc-scene__steps">
         <div data-tc-step> chapter 1 </div>               one is shown at a time
         <div data-tc-step> chapter 2 </div>
       </div>
       <div class="tc-part" data-tc-part="unit" data-explode="scroll"></div>   comes apart on the way
     </div>
   </section>

   The script writes two things and CSS does the rest:
   --p  on every [data-tc-scene]     0 at the start of the scene, 1 at its end (eased, not jumpy)
   --p  on every [data-tc-progress]  0 when the element enters the screen from below, 1 when it leaves at the top
   plus .is-active / .is-past on the steps and a "tc:progress" event (detail.p, detail.step) on the scene.

   The page's own scrolling is never taken over: no smooth-scroll hijack, no snapping.
   With reduced motion, or when this script does not run, a scene is an ordinary section and
   its chapters simply follow one another. Build it so that this version reads well too. */
(function () {
  'use strict';
  var root = document.documentElement;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { root.classList.add('tc-still'); return; }
  var scenes = [].map.call(document.querySelectorAll('[data-tc-scene]'), function (el) {
    return { el: el, steps: [].slice.call(el.querySelectorAll('[data-tc-step]')), p: -1, to: 0, step: -2 };
  });
  var tracks = [].map.call(document.querySelectorAll('[data-tc-progress]'), function (el) { return { el: el, p: -1, to: 0 }; });
  if (!scenes.length && !tracks.length) return;
  root.classList.add('tc-moving');           /* only now do scenes pin: CSS waits for this class */

  var raf = 0, SNAP = !!window.TC_SNAP;      /* set by scripts/shoot.sh for a picture: no easing, no transitions */
  if (SNAP) root.classList.add('tc-snap');
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function measure() {
    var vh = window.innerHeight;
    scenes.forEach(function (s) { var b = s.el.getBoundingClientRect(), run = b.height - vh; s.to = run > 0 ? clamp(-b.top / run) : (b.top < 0 ? 1 : 0); });
    tracks.forEach(function (t) { var b = t.el.getBoundingClientRect(); t.to = clamp((vh - b.top) / (vh + b.height)); });
    if (SNAP) frame(performance.now()); else if (!raf) raf = requestAnimationFrame(frame);
  }
  var last = 0;
  function frame(now) {
    raf = 0;
    /* ease by time, not by frame count */
    var f = last ? Math.min(90, Math.max(0.2, (now - last) / 16.67)) : 1, moving = false; last = now;
    function K(rate) { return SNAP ? 1 : 1 - Math.pow(1 - rate, f); }
    scenes.forEach(function (s) {
      var first = s.p < 0;
      s.p = first ? s.to : s.p + (s.to - s.p) * K(0.14);
      if (Math.abs(s.to - s.p) < 0.0004) s.p = s.to; else moving = true;
      s.el.style.setProperty('--p', s.p.toFixed(4));
      var n = s.steps.length, step = n ? Math.min(n - 1, Math.floor(s.p * n)) : -1;
      if (step !== s.step) {
        s.step = step;
        s.steps.forEach(function (el, i) { el.classList.toggle('is-active', i === step); el.classList.toggle('is-past', i < step); });
        s.el.setAttribute('data-step', String(step + 1));
      }
      s.el.dispatchEvent(new CustomEvent('tc:progress', { detail: { p: s.p, step: step } }));
    });
    tracks.forEach(function (t) {
      t.p = t.p < 0 ? t.to : t.p + (t.to - t.p) * K(0.18);
      if (Math.abs(t.to - t.p) < 0.0004) t.p = t.to; else moving = true;
      t.el.style.setProperty('--p', t.p.toFixed(4));
    });
    if (moving) raf = requestAnimationFrame(frame); else last = 0;
  }
  window.addEventListener('scroll', measure, { passive: true });
  window.addEventListener('resize', measure);
  window.addEventListener('load', measure);
  measure();
})();
