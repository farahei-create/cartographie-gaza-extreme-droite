/* Onrecord — constellation 3D du réseau.
   Rendu canvas original, même projection que le hero. Pas de bibliothèque tierce,
   pas de WebGL : si le contexte 2D manque, l'appelant reste sur vis-network.
   Les positions viennent des nœuds et des liens passés par app.js (data.json). */
(function (global) {
  "use strict";
  var canvas, ctx, opt = {};
  var nodes = [], links = [];
  var running = false, raf = 0, last = 0, bound = false, reduced = false;
  var cssW = 0, cssH = 0;
  var yaw = 0.55, pitch = 0.2, dist = 2.45;
  var hoverId = null, selected = null, neighbors = {};
  var dragging = false, dragMoved = false, holdSpin = 0;
  var pointers = {};
  var pinch = null;
  var sig = "";
  var ro = null;
  var INK = [];
  var LINK_A = [168, 85, 247];
  var LINK_B = [139, 92, 246];
  var LINK_OPP = [249, 168, 212];
  var WHITE = [255, 255, 255];
  var imgs = {};

  function buildInk(rgb) {
    var arr = [], j, a;
    for (j = 0; j <= 40; j++) {
      a = (j / 40).toFixed(3);
      arr.push("rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + "," + a + ")");
    }
    return arr;
  }
  function inkOf(rgb) {
    var k = rgb[0] + "," + rgb[1] + "," + rgb[2];
    if (!INK[k]) INK[k] = buildInk(rgb);
    return INK[k];
  }
  function aix(v) {
    var n = (v * 40 + 0.5) | 0;
    return n < 0 ? 0 : n > 40 ? 40 : n;
  }
  function parseColor(s) {
    s = String(s || "").trim();
    var h = /^#([0-9a-f]{6})$/i.exec(s);
    if (h) return [parseInt(h[1].slice(0, 2), 16), parseInt(h[1].slice(2, 4), 16), parseInt(h[1].slice(4, 6), 16)];
    var m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(s);
    if (m) return [+m[1], +m[2], +m[3]];
    return [216, 199, 255];
  }
  function loadImg(url) {
    if (!url || imgs[url]) return;
    var im = new Image();
    imgs[url] = im;
    im.onload = function () { im._ok = true; };
    im.onerror = function () { im._bad = true; };
    im.src = url;
  }
  function layout(list, edges) {
    var n = list.length, i, j, iter, gold = Math.PI * (3 - Math.sqrt(5));
    if (!n) return;
    var maxDeg = 1;
    for (i = 0; i < n; i++) if (list[i].deg > maxDeg) maxDeg = list[i].deg;
    for (i = 0; i < n; i++) {
      var y = 1 - (i + 0.5) / n * 2;
      var rr = Math.sqrt(Math.max(0, 1 - y * y));
      var th = gold * i;
      var shell = 0.78 + (1 - list[i].deg / maxDeg) * 0.48;
      list[i].x = Math.cos(th) * rr * shell;
      list[i].y = y * shell * 0.9;
      list[i].z = Math.sin(th) * rr * shell;
    }
    var idx = {};
    for (i = 0; i < n; i++) idx[list[i].id] = i;
    var pairs = [];
    for (i = 0; i < edges.length; i++) {
      var a = idx[edges[i].s], b = idx[edges[i].t];
      if (a == null || b == null || a === b) continue;
      pairs.push(a, b);
    }
    var ITER = n > 90 ? 120 : 160;
    for (iter = 0; iter < ITER; iter++) {
      var cool = 0.16 * (1 - iter / ITER);
      var vx = new Float64Array(n), vy = new Float64Array(n), vz = new Float64Array(n);
      for (i = 0; i < n; i++) {
        for (j = i + 1; j < n; j++) {
          var dx = list[i].x - list[j].x;
          var dy = list[i].y - list[j].y;
          var dz = list[i].z - list[j].z;
          var d2 = dx * dx + dy * dy + dz * dz;
          if (d2 < 0.0004) d2 = 0.0004;
          var d = Math.sqrt(d2);
          var f = cool * 0.92 / d2;
          var ux = dx / d, uy = dy / d, uz = dz / d;
          vx[i] += ux * f; vy[i] += uy * f; vz[i] += uz * f;
          vx[j] -= ux * f; vy[j] -= uy * f; vz[j] -= uz * f;
        }
      }
      for (i = 0; i < pairs.length; i += 2) {
        var A = list[pairs[i]], B = list[pairs[i + 1]];
        var dx2 = B.x - A.x, dy2 = B.y - A.y, dz2 = B.z - A.z;
        var d2e = dx2 * dx2 + dy2 * dy2 + dz2 * dz2;
        var de = Math.sqrt(d2e) || 0.001;
        var f2 = (de - 1.05) * cool * 0.28;
        var ux2 = dx2 / de, uy2 = dy2 / de, uz2 = dz2 / de;
        vx[pairs[i]] += ux2 * f2; vy[pairs[i]] += uy2 * f2; vz[pairs[i]] += uz2 * f2;
        vx[pairs[i + 1]] -= ux2 * f2; vy[pairs[i + 1]] -= uy2 * f2; vz[pairs[i + 1]] -= uz2 * f2;
      }
      for (i = 0; i < n; i++) {
        vx[i] -= list[i].x * cool * 0.035;
        vy[i] -= list[i].y * cool * 0.035;
        vz[i] -= list[i].z * cool * 0.035;
        var sp = Math.sqrt(vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i]);
        var cap = 0.07;
        if (sp > cap) { var s = cap / sp; vx[i] *= s; vy[i] *= s; vz[i] *= s; }
        list[i].x += vx[i]; list[i].y += vy[i]; list[i].z += vz[i];
      }
    }
    var maxR = 0.001;
    for (i = 0; i < n; i++) {
      var r = Math.sqrt(list[i].x * list[i].x + list[i].y * list[i].y + list[i].z * list[i].z);
      if (r > maxR) maxR = r;
    }
    var sc = 1.12 / maxR;
    for (i = 0; i < n; i++) { list[i].x *= sc; list[i].y *= sc; list[i].z *= sc; }
  }
  function markNeighbors() {
    neighbors = {};
    if (!selected) return;
    neighbors[selected] = 1;
    var i;
    for (i = 0; i < links.length; i++) {
      if (links[i].s === selected) neighbors[links[i].t] = 1;
      if (links[i].t === selected) neighbors[links[i].s] = 1;
    }
  }
  function resize() {
    if (!canvas || !ctx) return;
    var dpr = Math.min(2, global.devicePixelRatio || 1);
    var w = canvas.clientWidth || 0, h = canvas.clientHeight || 0;
    if (w < 2 || h < 2) { cssW = 0; cssH = 0; return; }
    var bw = Math.round(w * dpr), bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) { canvas.width = bw; canvas.height = bh; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cssW = w; cssH = h;
  }
  function projectAll() {
    var cy = Math.cos(yaw), sy = Math.sin(yaw);
    var cx = Math.cos(pitch), sx = Math.sin(pitch);
    var fov = 1.75;
    var scale = Math.min(cssW, cssH) * 0.58;
    var ox = cssW * 0.5, oy = cssH * 0.46;
    var i, node, x1, z1, y2, z2, den, p;
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];
      x1 = node.x * cy - node.z * sy;
      z1 = node.x * sy + node.z * cy;
      y2 = node.y * cx - z1 * sx;
      z2 = node.y * sx + z1 * cx;
      den = dist - z2;
      if (den < 0.42) den = 0.42;
      p = fov / den;
      node.sx = ox + x1 * p * scale;
      node.sy = oy + y2 * p * scale;
      node.sz = z2;
      node.sp = p;
    }
  }
  function depthOf(z) {
    var t = (z + 1.25) / 2.5;
    return t < 0 ? 0 : t > 1 ? 1 : t;
  }
  function labelSet(now) {
    var show = {}, i, node, front = [];
    if (hoverId) show[hoverId] = 1;
    if (selected) {
      show[selected] = 1;
      for (i = 0; i < nodes.length; i++) if (neighbors[nodes[i].id]) front.push(nodes[i]);
      front.sort(function (a, b) { return b.sz - a.sz; });
      for (i = 0; i < front.length && i < 8; i++) show[front[i].id] = 1;
      return show;
    }
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];
      if (node.dim) continue;
      node._score = node.deg * 1.4 + depthOf(node.sz) * 8;
      if (node.deg >= 4 || depthOf(node.sz) > 0.62) front.push(node);
    }
    front.sort(function (a, b) { return b._score - a._score; });
    var cap = cssW < 520 ? 8 : 14;
    for (i = 0; i < front.length && i < cap; i++) show[front[i].id] = 1;
    return show;
  }
  function shortName(name) {
    name = String(name || "");
    return name.length > 26 ? name.slice(0, 24) + "…" : name;
  }
  function drawDisc(node, rad, alpha, rgb) {
    var col = inkOf(rgb);
    ctx.beginPath();
    ctx.arc(node.sx, node.sy, rad * (2.1 + (1 - depthOf(node.sz)) * 1.6), 0, 6.283185);
    ctx.fillStyle = col[aix(alpha * 0.28)];
    ctx.fill();
    ctx.beginPath();
    ctx.arc(node.sx, node.sy, rad, 0, 6.283185);
    ctx.fillStyle = col[aix(alpha)];
    ctx.fill();
    if (alpha > 0.35) {
      ctx.beginPath();
      ctx.arc(node.sx, node.sy, Math.max(0.8, rad * 0.34), 0, 6.283185);
      ctx.fillStyle = inkOf(WHITE)[aix(0.45 + depthOf(node.sz) * 0.5)];
      ctx.fill();
    }
  }
  function drawPortrait(node, rad) {
    var cx = node.sx, cy = node.sy - rad - 20;
    if (cy < 22) cy = node.sy + rad + 20;
    var r = 15;
    var im = node.img ? imgs[node.img] : null;
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, r + 2, 0, 6.283185);
    ctx.strokeStyle = "rgba(233,213,255,.9)";
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, 6.283185);
    ctx.clip();
    if (im && im._ok) {
      if (node.logo) { ctx.fillStyle = "#fff"; ctx.fillRect(cx - r, cy - r, r * 2, r * 2); }
      var iw = im.naturalWidth || 1, ih = im.naturalHeight || 1;
      var box = node.logo ? r * 1.35 : r * 2;
      var sc = node.logo ? Math.min(box / iw, box / ih) : Math.max((r * 2) / iw, (r * 2) / ih);
      var w = iw * sc, h = ih * sc;
      ctx.drawImage(im, cx - w / 2, cy - h / 2, w, h);
    } else {
      ctx.fillStyle = "rgb(" + node.rgb[0] + "," + node.rgb[1] + "," + node.rgb[2] + ")";
      ctx.fillRect(cx - r, cy - r, r * 2, r * 2);
      ctx.fillStyle = "#1a0828";
      ctx.font = "700 11px " + (opt.font || "system-ui, sans-serif");
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.initials || "·", cx, cy + 0.5);
    }
    ctx.restore();
  }
  function paint(now) {
    if (!cssW) return;
    projectAll();
    ctx.clearRect(0, 0, cssW, cssH);
    var g = ctx.createRadialGradient(cssW * 0.5, cssH * 0.42, 0, cssW * 0.5, cssH * 0.42, Math.min(cssW, cssH) * 0.62);
    g.addColorStop(0, "rgba(124,58,237,0.18)");
    g.addColorStop(1, "rgba(124,58,237,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, cssW, cssH);
    var byId = {}, i, node;
    for (i = 0; i < nodes.length; i++) byId[nodes[i].id] = nodes[i];
    var orderL = [];
    for (i = 0; i < links.length; i++) orderL.push(i);
    orderL.sort(function (ia, ib) {
      var A = byId[links[ia].s], B = byId[links[ia].t], C = byId[links[ib].s], D = byId[links[ib].t];
      var za = ((A ? A.sz : 0) + (B ? B.sz : 0));
      var zb = ((C ? C.sz : 0) + (D ? D.sz : 0));
      return za - zb;
    });
    ctx.lineCap = "round";
    var pulseBase = reduced ? 0.82 : (0.45 + 0.55 * (0.5 + 0.5 * Math.sin(now * 0.0032)));
    for (i = 0; i < orderL.length; i++) {
      var e = links[orderL[i]];
      var a = byId[e.s], b = byId[e.t];
      if (!a || !b) continue;
      var z = (a.sz + b.sz) * 0.5;
      var depthT = depthOf(z);
      var hot = !selected || neighbors[e.s] || neighbors[e.t];
      var alpha = (0.22 + depthT * 0.5) * pulseBase;
      if (e.dim) alpha *= 0.2;
      if (selected && !hot) alpha *= 0.12;
      if (!hot && selected) continue;
      var pulse = reduced ? 1 : (0.72 + 0.28 * Math.sin(now * 0.004 + (orderL[i] % 7)));
      alpha *= pulse;
      if (alpha > 1) alpha = 1;
      var rgb = e.opp ? LINK_OPP : ((e.s.length + e.t.length) % 2 ? LINK_A : LINK_B);
      var col = inkOf(rgb);
      ctx.beginPath();
      ctx.moveTo(a.sx, a.sy);
      ctx.lineTo(b.sx, b.sy);
      ctx.strokeStyle = col[aix(alpha * (0.4 + depthT * 0.3))];
      ctx.lineWidth = (hot && selected ? 2.4 : 1.1) + depthT * 2.2;
      ctx.stroke();
      ctx.strokeStyle = col[aix(Math.min(1, alpha + 0.05))];
      ctx.lineWidth = 0.7 + depthT * 0.8;
      ctx.stroke();
    }
    var orderN = nodes.slice().sort(function (a, b) { return a.sz - b.sz; });
    var labels = labelSet(now);
    for (i = 0; i < orderN.length; i++) {
      node = orderN[i];
      var depthN = depthOf(node.sz);
      var rad = (1.7 + depthN * depthN * 5.2) * (0.62 + Math.min(node.deg, 12) / 12 * 1.05) * (0.85 + Math.min(node.sp, 1.8) * 0.12);
      var alphaN = 0.38 + depthN * 0.62;
      var focus = !selected || neighbors[node.id];
      if (node.dim) alphaN *= 0.16;
      if (!focus) alphaN *= 0.14;
      if (node.id === selected || node.id === hoverId) { alphaN = 1; rad *= 1.18; }
      drawDisc(node, rad, alphaN, node.rgb);
      node.sr = rad;
      node._lab = !!(labels[node.id] && alphaN >= 0.2);
      if (node.id === hoverId || node.id === selected) drawPortrait(node, rad);
    }
    var placed = [];
    ctx.font = "600 12px " + (opt.font || "system-ui, sans-serif");
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (i = orderN.length - 1; i >= 0; i--) {
      node = orderN[i];
      if (!node._lab) continue;
      var ly = node.sy + node.sr + 13;
      var label = shortName(node.name);
      var tw = ctx.measureText(label).width;
      var clash = false, pi;
      for (pi = 0; pi < placed.length; pi++) {
        if (Math.abs(node.sx - placed[pi].x) < (tw + placed[pi].w) * 0.5 + 6 && Math.abs(ly - placed[pi].y) < 16) { clash = true; break; }
      }
      var forceLabel = node.id === selected || node.id === hoverId;
      if (clash && !forceLabel) continue;
      if (!clash) placed.push({ x: node.sx, y: ly, w: tw });
      ctx.lineWidth = 4;
      ctx.strokeStyle = "rgba(7,3,15,.88)";
      ctx.strokeText(label, node.sx, ly);
      ctx.fillStyle = node.dim ? "rgba(216,199,255,.45)" : "#f7f3ff";
      ctx.fillText(label, node.sx, ly);
    }
  }
  function pick(x, y) {
    var best = null, bestD = 26 * 26, i, node, dx, dy, d, hit;
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];
      if (node.sx == null) continue;
      dx = node.sx - x; dy = node.sy - y;
      d = dx * dx + dy * dy;
      hit = Math.max(18, (node.sr || 8) + 10);
      if (d < hit * hit && d < bestD) { bestD = d; best = node; }
    }
    return best;
  }
  function localPoint(e) {
    var r = canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }
  function onDown(e) {
    if (!canvas) return;
    canvas.setPointerCapture && canvas.setPointerCapture(e.pointerId);
    pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(pointers);
    if (ids.length >= 2) {
      var a = pointers[ids[0]], b = pointers[ids[1]];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) || 1, dist: dist };
      dragging = false;
    } else {
      dragging = true;
      dragMoved = false;
      pointers[e.pointerId].ox = e.clientX;
      pointers[e.pointerId].oy = e.clientY;
      pinch = null;
    }
    holdSpin = performance.now() + 900;
    canvas.classList.add("is-drag");
  }
  function onMove(e) {
    if (!pointers[e.pointerId]) {
      if (e.pointerType === "mouse") {
        var p = localPoint(e);
        var hit = pick(p.x, p.y);
        hoverId = hit ? hit.id : null;
        canvas.style.cursor = hit ? "pointer" : "grab";
      }
      return;
    }
    pointers[e.pointerId].x = e.clientX;
    pointers[e.pointerId].y = e.clientY;
    var ids = Object.keys(pointers);
    if (ids.length >= 2 && pinch) {
      var a = pointers[ids[0]], b = pointers[ids[1]];
      var d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
      dist = pinch.dist * (pinch.d / d);
      if (dist < 1.45) dist = 1.45;
      if (dist > 6.2) dist = 6.2;
      dragMoved = true;
      if (e.cancelable) e.preventDefault();
      return;
    }
    if (!dragging) return;
    var dx = e.clientX - pointers[e.pointerId].ox;
    var dy = e.clientY - pointers[e.pointerId].oy;
    if (dx * dx + dy * dy > 36) dragMoved = true;
    yaw += dx * 0.0055;
    pitch += dy * 0.004;
    if (pitch > 1.15) pitch = 1.15;
    if (pitch < -0.85) pitch = -0.85;
    pointers[e.pointerId].ox = e.clientX;
    pointers[e.pointerId].oy = e.clientY;
    holdSpin = performance.now() + 900;
    if (e.cancelable) e.preventDefault();
  }
  function onUp(e) {
    var start = pointers[e.pointerId];
    delete pointers[e.pointerId];
    var wasDrag = dragMoved;
    if (Object.keys(pointers).length < 2) pinch = null;
    if (!Object.keys(pointers).length) {
      dragging = false;
      canvas.classList.remove("is-drag");
    }
    if (!wasDrag && start && e.type !== "pointercancel") {
      var p = localPoint(e);
      var hit = pick(p.x, p.y);
      if (hit) {
        selected = hit.id;
        hoverId = hit.id;
        markNeighbors();
        if (opt.onSelect) opt.onSelect(hit.id);
      }
    }
    holdSpin = performance.now() + 700;
  }
  function onWheel(e) {
    if (!running) return;
    e.preventDefault();
    dist *= Math.exp(e.deltaY * 0.0011);
    if (dist < 1.45) dist = 1.45;
    if (dist > 6.2) dist = 6.2;
  }
  function onVis() { kick(); }
  function frame(t) {
    raf = 0;
    if (!running) return;
    if (document.hidden || !canvas || canvas.hidden || canvas.clientWidth < 2) return;
    var dt = last ? Math.min(40, t - last) : 16;
    last = t;
    if (!reduced && !dragging && t > holdSpin) yaw += dt * 0.00022;
    if (!cssW) resize();
    paint(t);
    global.__r3dReady = true;
    raf = global.requestAnimationFrame(frame);
  }
  function kick() {
    if (running && !raf) { last = 0; raf = global.requestAnimationFrame(frame); }
  }
  function bind() {
    if (bound || !canvas) return;
    bound = true;
    canvas.addEventListener("pointerdown", onDown);
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerup", onUp);
    canvas.addEventListener("pointercancel", onUp);
    canvas.addEventListener("wheel", onWheel, { passive: false });
    document.addEventListener("visibilitychange", onVis);
    if ("ResizeObserver" in global) {
      ro = new ResizeObserver(function () { resize(); kick(); });
      ro.observe(canvas);
    } else {
      global.addEventListener("resize", function () { resize(); kick(); });
    }
  }

  global.Onrecord3D = {
    ok: function () {
      try {
        var c = document.createElement("canvas");
        return !!(c.getContext && c.getContext("2d"));
      } catch (e) { return false; }
    },
    start: function (el, options) {
      canvas = el;
      opt = options || {};
      reduced = !!opt.reduced;
      if (!canvas) return false;
      ctx = canvas.getContext("2d", { alpha: true });
      if (!ctx) return false;
      running = true;
      bind();
      resize();
      kick();
      return true;
    },
    stop: function () {
      running = false;
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
      global.__r3dReady = false;
    },
    setReduced: function (on) { reduced = !!on; },
    resetCam: function () { yaw = 0.55; pitch = 0.2; dist = 2.45; holdSpin = 0; kick(); },
    select: function (id) {
      selected = id || null;
      hoverId = id || null;
      markNeighbors();
      kick();
    },
    setGraph: function (model) {
      model = model || { nodes: [], links: [] };
      var incoming = model.nodes || [];
      var nextSig = incoming.map(function (n) { return n.id; }).join("|");
      var prev = {};
      var i;
      for (i = 0; i < nodes.length; i++) prev[nodes[i].id] = nodes[i];
      var fresh = nextSig !== sig;
      var built = [];
      for (i = 0; i < incoming.length; i++) {
        var src = incoming[i];
        var keep = !fresh && prev[src.id];
        var node = keep ? prev[src.id] : { id: src.id };
        node.name = src.name;
        node.initials = src.initials;
        node.deg = src.deg || 0;
        node.dim = !!src.dim;
        node.img = src.img || "";
        node.logo = !!src.logo;
        node.rgb = parseColor(src.color);
        if (node.img) loadImg(node.img);
        if (!keep) { node.x = node.y = node.z = 0; }
        built.push(node);
      }
      nodes = built;
      links = (model.links || []).map(function (e) { return { s: e.s, t: e.t, dim: !!e.dim, opp: !!e.opp }; });
      if (fresh) {
        sig = nextSig;
        layout(nodes, links);
        var still = false;
        for (i = 0; i < nodes.length; i++) if (nodes[i].id === selected) still = true;
        if (selected && !still) { selected = null; neighbors = {}; }
        else markNeighbors();
      }
      kick();
    }
  };
})(window);
