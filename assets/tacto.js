/* tacto.js - the behaviours the design language needs. No dependencies.
   1. reveal: .tc-reveal rises and fades in once, staggered inside [data-tc-stagger]
   2. count-up: [data-tc-count="430000"] counts from 0 when it scrolls into view
   3. tabs: [data-tc-tabs] switches .tc-tab buttons and their [data-tc-pane] panels
   4. rail arrows: [data-tc-rail-next="#id"] / [data-tc-rail-prev="#id"] */
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-tc-stagger]").forEach(function (group) {
    var step = parseFloat(group.getAttribute("data-tc-stagger")) || 0.08;
    group.querySelectorAll(".tc-reveal").forEach(function (el, i) {
      el.style.setProperty("--tc-delay", (i * step).toFixed(2) + "s");
    });
  });

  function countUp(el) {
    var raw = el.getAttribute("data-tc-count");
    var target = parseFloat(raw);
    if (isNaN(target)) return;
    var decimals = (raw.split(".")[1] || "").length;
    var prefix = el.getAttribute("data-tc-prefix") || "";
    var suffix = el.getAttribute("data-tc-suffix") || "";
    // numbers follow the page language: 430,000 on an English page, 430.000 on a German one
    var locale = el.getAttribute("data-tc-locale") || document.documentElement.lang || "en";
    var fmt = function (v) {
      var opts = { minimumFractionDigits: decimals, maximumFractionDigits: decimals }, text;
      try { text = v.toLocaleString(locale, opts); } catch (e) { text = v.toLocaleString("en", opts); }
      return prefix + text + suffix;
    };
    // decks, documents and covers are printed and photographed: the final number, at once
    if (reduce || el.closest(".tc-slide, .tc-sheet, .tc-cover")) { el.textContent = fmt(target); return; }
    var start = null, dur = 1200;
    function tick(t) {
      if (start === null) start = t;
      var p = Math.min((t - start) / dur, 1);
      // slow start, slow stop: the same curve as every other movement
      var eased = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      el.textContent = fmt(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  document.querySelectorAll(".tc-slide [data-tc-count], .tc-sheet [data-tc-count], .tc-cover [data-tc-count]").forEach(countUp);
  window.addEventListener("beforeprint", function () { reduce = true; document.querySelectorAll("[data-tc-count]").forEach(countUp); });
  if (!("IntersectionObserver" in window)) {
    document.querySelectorAll(".tc-reveal").forEach(function (el) { el.classList.add("is-in"); });
    document.querySelectorAll("[data-tc-count]").forEach(countUp);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (e.target.classList.contains("tc-reveal")) e.target.classList.add("is-in");
        if (e.target.hasAttribute("data-tc-count")) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".tc-reveal, [data-tc-count]").forEach(function (el) { io.observe(el); });
  }

  document.querySelectorAll("[data-tc-tabs]").forEach(function (group) {
    var tabs = group.querySelectorAll(".tc-tab");
    var scope = document.querySelector(group.getAttribute("data-tc-tabs")) || group.parentElement;
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) { t.classList.toggle("is-active", t === tab); });
        scope.querySelectorAll("[data-tc-pane]").forEach(function (pane, j) { pane.hidden = i !== j; });
      });
    });
  });

  function rail(attr, dir) {
    document.querySelectorAll("[" + attr + "]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var el = document.querySelector(btn.getAttribute(attr));
        if (el) el.scrollBy({ left: dir * el.clientWidth * 0.8, behavior: reduce ? "auto" : "smooth" });
      });
    });
  }
  rail("data-tc-rail-next", 1);
  rail("data-tc-rail-prev", -1);
})();
