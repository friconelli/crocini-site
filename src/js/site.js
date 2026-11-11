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
    img: stage.getAttribute('data-img'), img2: stage.getAttribute('data-img2')
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
      var asp = lw / lh, pick = (asp > 1.25 && asp < 1.9) ? els.img : els.img2;
      im.setAttributeNS('http://www.w3.org/1999/xlink', 'href', pick); im.setAttribute('href', pick);
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

/* Sezione a scorrimento: il foglio resta fermo e cambia a seconda del passo che sta al centro dello schermo. */
(function () {
  'use strict';
  var scene = document.getElementById('scene');
  if (!scene) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg', PW = 210, PH = 297;
  var presets = JSON.parse(scene.getAttribute('data-presets'));   // [[nome, w, h], …]
  var imgSrc = scene.getAttribute('data-img'), imgTile = scene.getAttribute('data-img2');
  function artFor(w, h) { var a = w / h; return (a > 1.25 && a < 1.9) ? imgSrc : imgTile; }
  var box = document.getElementById('stagebox');
  var labelEl = document.getElementById('sc-label'), nEl = document.getElementById('sc-n'), zoomEl = document.getElementById('sc-zoom');
  var steps = [].slice.call(document.querySelectorAll('.st'));

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e); return e;
  }
  var cam = el('g', { id: 'cam' }, scene);
  el('rect', { x: 0, y: 0, width: PW, height: PH, fill: '#fff' }, cam);
  var cardsG = el('g', {}, cam);
  var marks = el('path', { 'class': 'mk', fill: 'none', stroke: '#141414', 'stroke-width': 0.3 }, cam);

  var cur = { w: 85, h: 55, rot: null, bleed: 3 }, last = null;

  function grid(iw, ih, margin, rotated) {
    var cols = Math.max(0, Math.floor((PW - 2 * margin) / iw + 1e-9)), rows = Math.max(0, Math.floor((PH - 2 * margin) / ih + 1e-9));
    return { cols: cols, rows: rows, count: cols * rows, iw: iw, ih: ih, rotated: rotated, x0: (PW - cols * iw) / 2, y0: (PH - rows * ih) / 2 };
  }
  function layout() {
    var off = Math.max(cur.bleed, 1), len = 4, margin = Math.max(10, off + len + 1);
    var a = grid(cur.w, cur.h, margin, false), b = grid(cur.h, cur.w, margin, true), g;
    if (cur.rot === true) g = b; else if (cur.rot === false) g = a; else g = b.count > a.count ? b : a;
    g.off = off; g.len = len; return g;
  }
  function render() {
    var g = layout(), b = cur.bleed;
    while (cardsG.firstChild) cardsG.removeChild(cardsG.firstChild);
    var i = 0;
    for (var r = 0; r < g.rows; r++) for (var c = 0; c < g.cols; c++, i++) {
      var x = g.x0 + c * g.iw, y = g.y0 + r * g.ih;
      var cell = el('g', { 'class': 'pop', style: '--i:' + i }, cardsG);
      var nest = el('svg', { x: x, y: y, width: g.iw, height: g.ih, viewBox: '0 0 ' + g.iw + ' ' + g.ih, overflow: 'hidden' }, cell);
      var lw = g.rotated ? g.ih : g.iw, lh = g.rotated ? g.iw : g.ih;
      var grp = el('g', { transform: 'translate(' + g.iw / 2 + ' ' + g.ih / 2 + ')' + (g.rotated ? ' rotate(90)' : '') }, nest);
      var im = el('image', { x: -(lw / 2 + b), y: -(lh / 2 + b), width: lw + 2 * b, height: lh + 2 * b, preserveAspectRatio: 'xMidYMid slice' }, grp);
      im.setAttribute('href', artFor(lw, lh));
      // anello dell'abbondanza (tra rifilo e bordo vivo), bordo tratteggiato e rifilo
      el('path', { 'class': 'ring', d: 'M' + (x - b) + ' ' + (y - b) + 'h' + (g.iw + 2 * b) + 'v' + (g.ih + 2 * b) + 'h' + -(g.iw + 2 * b) + 'z M' + x + ' ' + y + 'v' + g.ih + 'h' + g.iw + 'v' + -g.ih + 'h' + -g.iw + 'z' }, cell);
      el('rect', { 'class': 'bd', x: x - b, y: y - b, width: g.iw + 2 * b, height: g.ih + 2 * b, fill: 'none', stroke: '#EC008C', 'stroke-width': 0.25, 'stroke-dasharray': '1.2 .9' }, cell);
      el('rect', { x: x, y: y, width: g.iw, height: g.ih, fill: 'none', stroke: '#00AEEF', 'stroke-width': 0.25 }, cell);
    }
    var d = '', top = g.y0, bot = g.y0 + g.rows * g.ih, left = g.x0, right = g.x0 + g.cols * g.iw;
    for (c = 0; c <= g.cols; c++) { var xx = g.x0 + c * g.iw; d += 'M' + xx + ' ' + (top - g.off) + 'V' + (top - g.off - g.len) + 'M' + xx + ' ' + (bot + g.off) + 'V' + (bot + g.off + g.len); }
    for (r = 0; r <= g.rows; r++) { var yy = g.y0 + r * g.ih; d += 'M' + (left - g.off) + ' ' + yy + 'H' + (left - g.off - g.len) + 'M' + (right + g.off) + ' ' + yy + 'H' + (right + g.off + g.len); }
    marks.setAttribute('d', d);
    nEl.textContent = g.count;
    last = g; return g;
  }
  function camTo(px, py, s) { cam.style.transform = 'translate(' + (PW / 2 - px * s) + 'px,' + (PH / 2 - py * s) + 'px) scale(' + s + ')'; }
  function markStyle(w, col) { marks.style.strokeWidth = w; marks.style.stroke = col; }

  var timer = null, active = -1;
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function every(ms, fn) { fn(0); if (!reduce) { var k = 1; timer = setInterval(function () { fn(k++); }, ms); } }

  function go(i) {
    if (i === active) return;
    active = i; stop();
    steps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
    scene.setAttribute('class', 's' + i); box.setAttribute('data-step', i);
    var chip = steps[i].getAttribute('data-chip');
    markStyle(0.3, '#141414');
    if (i === 0) {                                     // preset: si alternano i formati
      camTo(PW / 2, PH / 2, 1);
      every(2000, function (k) {
        var p = presets[k % presets.length];
        cur.w = p[1]; cur.h = p[2]; cur.rot = null; cur.bleed = 3; render();
        labelEl.textContent = p[0] + ' ' + p[1] + '×' + p[2];
      });
    } else if (i === 1) {                              // abbondanza: zoom sull'angolo del primo biglietto
      cur.w = 85; cur.h = 55; cur.rot = null; cur.bleed = 3; var g = render();
      labelEl.textContent = chip; camTo(g.x0 + 10, g.y0 + 8, 5);
    } else if (i === 2) {                              // crocini: zoom sull'angolo con i segni, che cambiano stile
      cur.w = 85; cur.h = 55; cur.rot = null; cur.bleed = 3; g = render();
      labelEl.textContent = chip; camTo(g.x0 + 12, g.y0 + 9, 3.8);
      var styles = [[0.3, '#141414'], [0.9, '#00AEEF'], [0.5, '#EC008C'], [1.2, '#141414']];
      every(1500, function (k) { var s = styles[k % styles.length]; markStyle(s[0], s[1]); });
    } else if (i === 3) {                              // zoom: entra ed esce dai dettagli
      cur.w = 85; cur.h = 55; cur.rot = null; cur.bleed = 3; render(); labelEl.textContent = chip;
      var frames = [[PW / 2, PH / 2, 1], [PW / 2, 90, 2.2], [150, 60, 3.4], [60, 235, 1.8]];
      every(1900, function (k) { var f = frames[k % frames.length]; camTo(f[0], f[1], f[2]); zoomEl.textContent = Math.round(f[2] * 100) + '%'; });
    } else {                                           // rotazione: da 3 pezzi dritti a 5 ruotati
      camTo(PW / 2, PH / 2, 1); cur.w = 50; cur.h = 150; cur.bleed = 3;
      var name = (presets[4] || ['', 50, 150])[0];
      every(2400, function (k) { cur.rot = (k % 2 === 1) ? null : false; render(); labelEl.textContent = name + ' 50×150'; });
    }
  }

  // stato iniziale (visibile anche senza scorrere) e cambio passo quando uno arriva al centro dello schermo
  cur = { w: presets[0][1], h: presets[0][2], rot: null, bleed: 3 };
  render(); labelEl.textContent = presets[0][0] + ' ' + presets[0][1] + '×' + presets[0][2];
  scene.setAttribute('class', 's0');
  // Il passo attivo è quello il cui centro è più vicino al centro dello schermo; fuori dalla sezione tutto si ferma.
  var ticking = false;
  function pick() {
    ticking = false;
    var sr = scene.getBoundingClientRect(), vh = window.innerHeight || document.documentElement.clientHeight;
    var section = document.querySelector('.scrolly').getBoundingClientRect();
    if (section.bottom < 0 || section.top > vh) { stop(); active = -1; return; }
    var mid = vh / 2, best = 0, bd = 1e9;
    steps.forEach(function (st, k) {
      var r = st.getBoundingClientRect(), d = Math.abs(r.top + r.height / 2 - mid);
      if (d < bd) { bd = d; best = k; }
    });
    go(best);
  }
  function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(pick); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
