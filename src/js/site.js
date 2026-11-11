(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Rivelazione allo scroll
  var items = [].slice.call(document.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  // Intestazione che prende ombra scorrendo
  var head = document.querySelector('.top');
  function onScroll() { if (head) head.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Copia comando
  [].forEach.call(document.querySelectorAll('[data-copy]'), function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy'), done = b.getAttribute('data-done') || 'OK';
      var label = b.textContent;
      function ok() { b.textContent = done; b.classList.add('ok'); setTimeout(function () { b.textContent = label; b.classList.remove('ok'); }, 1600); }
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });

  // Calcolatore: stesso calcolo dell'app (griglia centrata, rotazione automatica, margine per i segni)
  var NS = 'http://www.w3.org/2000/svg';
  var stage = document.getElementById('sheet');
  if (!stage) return;
  var S = { paper: [210, 297], w: 85, h: 55, bleed: 3, marks: true };
  var els = {
    n: document.getElementById('demo-n'), grid: document.getElementById('demo-grid'),
    w: document.getElementById('demo-w'), h: document.getElementById('demo-h'),
    bleed: document.getElementById('demo-bleed'), marks: document.getElementById('demo-marks'),
    img: stage.getAttribute('data-img')
  };

  function grid(pw, ph, iw, ih, margin, rotated) {
    var cols = Math.max(0, Math.floor((pw - 2 * margin) / iw + 1e-9));
    var rows = Math.max(0, Math.floor((ph - 2 * margin) / ih + 1e-9));
    return { cols: cols, rows: rows, count: cols * rows, iw: iw, ih: ih, rotated: rotated,
             x0: (pw - cols * iw) / 2, y0: (ph - rows * ih) / 2 };
  }
  function layout() {
    var pw = S.paper[0], ph = S.paper[1];
    var off = Math.max(S.bleed, 1), len = 4;
    var margin = S.marks ? Math.max(10, off + len + 1) : 10;
    if (!(S.w > 0 && S.h > 0)) return { cols: 0, rows: 0, count: 0, off: off, len: len };
    var a = grid(pw, ph, S.w, S.h, margin, false), b = grid(pw, ph, S.h, S.w, margin, true);
    var g = b.count > a.count ? b : a; g.off = off; g.len = len; return g;
  }
  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e); return e;
  }
  function render() {
    var pw = S.paper[0], ph = S.paper[1], g = layout();
    while (stage.firstChild) stage.removeChild(stage.firstChild);
    stage.setAttribute('viewBox', '0 0 ' + pw + ' ' + ph);
    el('rect', { x: 0, y: 0, width: pw, height: ph, fill: '#fff' }, stage);
    var i = 0;
    for (var r = 0; r < g.rows; r++) for (var c = 0; c < g.cols; c++, i++) {
      var x = g.x0 + c * g.iw, y = g.y0 + r * g.ih, b = S.bleed;
      var cell = el('g', { 'class': 'pop', style: '--i:' + i }, stage);
      var box = el('svg', { x: x, y: y, width: g.iw, height: g.ih, viewBox: '0 0 ' + g.iw + ' ' + g.ih, overflow: 'hidden' }, cell);
      var lw = g.rotated ? g.ih : g.iw, lh = g.rotated ? g.iw : g.ih;
      var grp = el('g', { transform: 'translate(' + g.iw / 2 + ' ' + g.ih / 2 + ')' + (g.rotated ? ' rotate(90)' : '') }, box);
      var im = el('image', { x: -(lw / 2 + b), y: -(lh / 2 + b), width: lw + 2 * b, height: lh + 2 * b, preserveAspectRatio: 'xMidYMid slice' }, grp);
      im.setAttributeNS('http://www.w3.org/1999/xlink', 'href', els.img); im.setAttribute('href', els.img);
      if (b > 0) el('rect', { x: x - b, y: y - b, width: g.iw + 2 * b, height: g.ih + 2 * b, fill: 'none', stroke: '#EC008C', 'stroke-width': 0.25, 'stroke-dasharray': '1.2 0.9', opacity: 0.7 }, cell);
      el('rect', { x: x, y: y, width: g.iw, height: g.ih, fill: 'none', stroke: '#00AEEF', 'stroke-width': 0.25 }, cell);
    }
    if (S.marks && g.count) {
      var xs = [], ys = [], d = '';
      for (c = 0; c <= g.cols; c++) xs.push(g.x0 + c * g.iw);
      for (r = 0; r <= g.rows; r++) ys.push(g.y0 + r * g.ih);
      var top = g.y0, bot = g.y0 + g.rows * g.ih, left = g.x0, right = g.x0 + g.cols * g.iw;
      xs.forEach(function (x) { d += 'M' + x + ' ' + (top - g.off) + 'V' + (top - g.off - g.len) + 'M' + x + ' ' + (bot + g.off) + 'V' + (bot + g.off + g.len); });
      ys.forEach(function (y) { d += 'M' + (left - g.off) + ' ' + y + 'H' + (left - g.off - g.len) + 'M' + (right + g.off) + ' ' + y + 'H' + (right + g.off + g.len); });
      el('path', { d: d, fill: 'none', stroke: '#000', 'stroke-width': 0.3 }, stage);
    }
    els.n.textContent = g.count;
    els.n.parentNode.classList.toggle('none', g.count === 0);
    els.grid.textContent = g.count ? g.cols + ' × ' + g.rows + (g.rotated ? ' · ' + els.grid.getAttribute('data-rot') : '') : els.grid.getAttribute('data-none');
  }
  function num(v) { v = parseFloat(String(v).replace(',', '.')); return isNaN(v) ? 0 : v; }
  els.w.addEventListener('input', function () { S.w = num(els.w.value); mark(null); render(); });
  els.h.addEventListener('input', function () { S.h = num(els.h.value); mark(null); render(); });
  els.bleed.addEventListener('change', function () { S.bleed = num(els.bleed.value); render(); });
  els.marks.addEventListener('change', function () { S.marks = els.marks.checked; render(); });
  var chips = [].slice.call(document.querySelectorAll('[data-w]'));
  function mark(active) { chips.forEach(function (c) { c.setAttribute('aria-pressed', c === active ? 'true' : 'false'); }); }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      S.w = num(c.getAttribute('data-w')); S.h = num(c.getAttribute('data-h'));
      els.w.value = S.w; els.h.value = S.h; mark(c); render();
    });
  });
  [].forEach.call(document.querySelectorAll('[data-paper]'), function (b) {
    b.addEventListener('click', function () {
      var p = b.getAttribute('data-paper').split('x'); S.paper = [num(p[0]), num(p[1])];
      [].forEach.call(document.querySelectorAll('[data-paper]'), function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      render();
    });
  });
  render();
})();
