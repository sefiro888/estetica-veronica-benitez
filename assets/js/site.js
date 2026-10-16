/* Estética Verónica Benítez · interacción */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const WA = "34679901866";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- estado abierto/cerrado (hora peninsular) ---------- */
  function ahoraMadrid() {
    const p = new Intl.DateTimeFormat("es-ES", { timeZone: "Europe/Madrid", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false })
      .formatToParts(new Date());
    const dias = { lun: 0, mar: 1, "mié": 2, mie: 2, jue: 3, vie: 4, "sáb": 5, sab: 5, dom: 6 };
    const wd = p.find(x => x.type === "weekday").value.replace(".", "").toLowerCase();
    return { d: dias[wd] ?? new Date().getDay() - 1, m: +p.find(x => x.type === "hour").value % 24 * 60 + +p.find(x => x.type === "minute").value };
  }
  const aMin = t => { const [h, m] = t.split(":"); return +h * 60 + +m; };
  const fmt = t => t.replace(/^0/, "");
  const NOMBRES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"];
  function estado() {
    const H = window.HORARIO || {};
    const { d, m } = ahoraMadrid();
    const hoy = H[d] || [];
    for (const [a, c] of hoy) {
      if (m >= aMin(a) && m < aMin(c)) {
        const quedan = aMin(c) - m;
        return { open: true, txt: quedan <= 45 ? `Abierto · cierra pronto (${fmt(c)})` : `Abierto ahora · hasta las ${fmt(c)}` };
      }
      if (m < aMin(a)) return { open: false, txt: `Cerrado ahora · abrimos hoy a las ${fmt(a)}` };
    }
    for (let i = 1; i <= 7; i++) {
      const nd = (d + i) % 7, f = H[nd] || [];
      if (f.length) return { open: false, txt: `Cerrado · abrimos ${i === 1 ? "mañana" : "el " + NOMBRES[nd]} a las ${fmt(f[0][0])}` };
    }
    return { open: false, txt: "Cerrado" };
  }
  function pintaEstado() {
    const s = estado();
    $$("[data-estado]").forEach(el => {
      el.classList.toggle("is-open", s.open); el.classList.toggle("is-closed", !s.open);
      const t = $(".estado-txt", el); if (t) t.textContent = s.txt;
    });
    const { d } = ahoraMadrid();
    $$(".horario tr[data-dia]").forEach(tr => tr.classList.toggle("is-today", +tr.dataset.dia === d));
  }
  pintaEstado(); setInterval(pintaEstado, 60000);

  /* ---------- cabecera ---------- */
  const header = $("[data-header]");
  let lastY = scrollY, acc = 0, ticking = false;
  const waFloat = $(".wa-float");
  function onScroll() {
    const y = Math.max(0, scrollY), dy = y - lastY;
    header.classList.toggle("is-solid", y > 40);
    acc = (dy > 0) === (acc > 0) ? acc + dy : dy;   // distancia acumulada en el mismo sentido
    const bloqueado = document.body.classList.contains("menu-open") || $(".nav-item.is-open");
    if (y < 300 || bloqueado) header.classList.remove("is-hidden");
    else if (acc > 60) header.classList.add("is-hidden");
    else if (acc < -40) header.classList.remove("is-hidden");
    if (waFloat) waFloat.classList.toggle("is-in", y > 500);
    lastY = y; ticking = false;
  }
  addEventListener("scroll", () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* ---------- mega menú y desplegables ---------- */
  const items = $$(".nav-item");
  const cierra = except => items.forEach(it => { if (it !== except) { it.classList.remove("is-open"); $(".nav-btn", it)?.setAttribute("aria-expanded", "false"); } });
  items.forEach(it => {
    const btn = $(".nav-btn", it); let t;
    const abre = () => { clearTimeout(t); cierra(it); it.classList.add("is-open"); btn.setAttribute("aria-expanded", "true");
      const mega = $(".mega", it); if (mega) mega.style.setProperty("--mega-top", header.getBoundingClientRect().bottom + "px"); };
    const sal = () => { t = setTimeout(() => { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }, 220); };
    it.addEventListener("mouseenter", () => matchMedia("(hover:hover)").matches && abre());
    it.addEventListener("mouseleave", () => matchMedia("(hover:hover)").matches && sal());
    btn.addEventListener("click", () => it.classList.contains("is-open") ? sal() : abre());
    it.addEventListener("focusout", e => { if (!it.contains(e.relatedTarget)) sal(); });
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") { cierra(); cerrarMenu(); cerrarLB(); } });
  // vista previa del mega menú
  const mImg = $(".mega-img"), mTxt = $(".mega-preview-txt strong"), mTag = $(".mega-preview-txt span");
  $$(".mega-link").forEach(a => a.addEventListener("mouseenter", () => {
    if (!mImg) return;
    mImg.style.opacity = 0;
    setTimeout(() => { mImg.src = a.dataset.img; mImg.style.opacity = 1; }, 140);
    mTxt.textContent = $(".mega-name", a).childNodes[0].textContent.trim();
    mTag.textContent = $(".mega-desc", a).textContent;
  }));

  /* ---------- menú móvil ---------- */
  const mm = $("[data-mmenu]"), burger = $("[data-burger]");
  function abrirMenu() { mm.classList.add("is-open"); mm.setAttribute("aria-hidden", "false"); burger.setAttribute("aria-expanded", "true"); document.body.classList.add("menu-open"); setTimeout(() => $("[data-close]", mm).focus(), 300); }
  function cerrarMenu() { if (!mm?.classList.contains("is-open")) return; mm.classList.remove("is-open"); mm.setAttribute("aria-hidden", "true"); burger.setAttribute("aria-expanded", "false"); document.body.classList.remove("menu-open"); }
  burger?.addEventListener("click", abrirMenu);
  $("[data-close]", mm)?.addEventListener("click", cerrarMenu);
  $$("a", mm).forEach(a => a.addEventListener("click", cerrarMenu));

  /* ---------- anclas internas ---------- */
  document.addEventListener("click", e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute("href").length < 2) return;
    const t = document.getElementById(a.getAttribute("href").slice(1));
    if (!t) return;
    e.preventDefault();
    const off = (header.offsetHeight || 70) + ($("[data-toc]")?.offsetHeight || 0) + 12;
    scrollTo({ top: t.getBoundingClientRect().top + scrollY - off, behavior: reduce ? "auto" : "smooth" });
    history.replaceState(null, "", a.getAttribute("href"));
  });

  /* ---------- aparición al hacer scroll ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach((el, i) => { el.style.transitionDelay = (i % 4) * 70 + "ms"; io.observe(el); });
  } else $$(".reveal").forEach(el => el.classList.add("is-in"));

  /* ---------- índice de la página ---------- */
  const toc = $("[data-toc]");
  if (toc && "IntersectionObserver" in window) {
    const links = $$("a", toc);
    const map = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));
    const io2 = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { links.forEach(l => l.classList.remove("is-on")); const l = map.get(e.target.id); if (l) { l.classList.add("is-on"); const bar = l.parentElement; bar.scrollTo({ left: l.offsetLeft - (bar.clientWidth - l.offsetWidth) / 2, behavior: reduce ? "auto" : "smooth" }); } }
    }), { rootMargin: "-40% 0px -55% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io2.observe(s); });
  }

  /* ---------- carrusel ---------- */
  $$("[data-carousel]").forEach(c => {
    const sec = c.closest("section");
    const paso = () => (c.firstElementChild?.getBoundingClientRect().width || 300) + 20;
    $("[data-car-next]", sec)?.addEventListener("click", () => c.scrollBy({ left: paso(), behavior: "smooth" }));
    $("[data-car-prev]", sec)?.addEventListener("click", () => c.scrollBy({ left: -paso(), behavior: "smooth" }));
  });

  /* ---------- filtros ---------- */
  $$("[data-filter]").forEach(f => {
    const destino = f.dataset.target ? $(f.dataset.target) : $("[data-cards]");
    $$(".filter", f).forEach(b => b.addEventListener("click", () => {
      $$(".filter", f).forEach(x => x.classList.toggle("is-on", x === b));
      $$("[data-cat]", destino).forEach(el => el.classList.toggle("is-hidden", b.dataset.f !== "all" && el.dataset.cat !== b.dataset.f));
    }));
  });

  /* ---------- test «¿qué necesita tu pelo?» ---------- */
  const qbox = $("[data-quizbox]"), qout = $("[data-quiz-out]");
  qbox && $$(".chip", qbox).forEach(b => b.addEventListener("click", () => {
    $$(".chip", qbox).forEach(x => x.classList.toggle("is-on", x === b));
    qout.innerHTML = "";
    JSON.parse(b.dataset.quiz).forEach(slug => { const t = $(`template[data-tpl="${slug}"]`); if (t) qout.appendChild(t.content.cloneNode(true)); });
  }));

  /* ---------- asistente de cita ---------- */
  $$("[data-wizard]").forEach(w => {
    const estadoW = { dias: [], franja: "", primera: "" };
    $$("[data-multi]", w).forEach(g => $$(".chip", g).forEach(c => c.addEventListener("click", () => {
      c.classList.toggle("is-on"); estadoW[g.dataset.multi] = $$(".chip.is-on", g).map(x => x.textContent); render();
    })));
    $$("[data-single]", w).forEach(g => $$(".chip", g).forEach(c => c.addEventListener("click", () => {
      const on = !c.classList.contains("is-on");
      $$(".chip", g).forEach(x => x.classList.remove("is-on"));
      if (on) c.classList.add("is-on");
      estadoW[g.dataset.single] = on ? c.textContent : ""; render();
    })));
    w.addEventListener("input", render); w.addEventListener("change", render);
    w.addEventListener("submit", e => e.preventDefault());
    function render() {
      const f = w.elements;
      const l = ["¡Hola Vero! Me gustaría pedir cita en Estética Verónica Benítez."];
      if (f.nombre.value.trim()) l.push(`Me llamo ${f.nombre.value.trim()}.`);
      l.push(f.servicio.value ? `Servicio: ${f.servicio.value}.` : "Aún no sé qué hacerme, me gustaría que me aconsejéis.");
      if (f.extra.checked) l.push("Me gustaría añadir un baño de parafina.");
      if (estadoW.dias.length) l.push(`Días que me vienen bien: ${estadoW.dias.join(", ").toLowerCase()}.`);
      if (estadoW.franja) l.push(`Franja: ${estadoW.franja.toLowerCase()}.`);
      if (estadoW.primera) l.push(estadoW.primera.startsWith("Sí") ? "Es mi primera vez en el centro." : "Ya soy clienta.");
      if (f.notas.value.trim()) l.push(`Nota: ${f.notas.value.trim()}`);
      const txt = l.join("\n");
      $("[data-preview]", w).textContent = txt;
      $("[data-send]", w).href = `https://wa.me/${WA}?text=${encodeURIComponent(txt)}`;
    }
    render();
  });

  /* ---------- lightbox ---------- */
  const lb = $("[data-lightbox]"); let lbList = [], lbI = 0;
  function abrirLB(list, i) { lbList = list; lbI = i; muestra(); lb.hidden = false; document.body.classList.add("menu-open"); $(".lb-close", lb).focus(); }
  function muestra() { $("img", lb).src = lbList[lbI]; $(".lb-cap", lb).textContent = `${lbI + 1} / ${lbList.length} · Estética Verónica Benítez`; }
  function cerrarLB() { if (!lb || lb.hidden) return; lb.hidden = true; document.body.classList.remove("menu-open"); }
  $$("[data-gallery]").forEach(g => g.addEventListener("click", e => {
    const b = e.target.closest("[data-lb]"); if (!b) return;
    const visibles = $$("[data-lb]", g).filter(x => !x.closest(".is-hidden"));
    abrirLB(visibles.map(x => x.dataset.lb), visibles.indexOf(b));
  }));
  if (lb) {
    $(".lb-close", lb).onclick = cerrarLB;
    $(".lb-next", lb).onclick = () => { lbI = (lbI + 1) % lbList.length; muestra(); };
    $(".lb-prev", lb).onclick = () => { lbI = (lbI - 1 + lbList.length) % lbList.length; muestra(); };
    lb.addEventListener("click", e => { if (e.target === lb) cerrarLB(); });
    document.addEventListener("keydown", e => { if (lb.hidden) return; if (e.key === "ArrowRight") $(".lb-next", lb).click(); if (e.key === "ArrowLeft") $(".lb-prev", lb).click(); });
  }

  /* ---------- mapa bajo demanda ---------- */
  $$("[data-map-load]").forEach(b => b.addEventListener("click", () => {
    const m = b.closest("[data-map]");
    m.innerHTML = `<iframe src="${m.dataset.src}" title="Mapa de Estética Verónica Benítez" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>`;
  }));

  /* ---------- copiar dirección ---------- */
  $$("[data-copy]").forEach(b => b.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); const t = b.textContent; b.textContent = "¡Copiada!"; setTimeout(() => b.textContent = t, 1800); } catch (_) { }
  }));
})();

/* Estética Verónica Benítez · mejoras: intro, parpadeo, antes/después, vídeos y transiciones */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- intro con el logo (solo la primera página de cada visita) ---------- */
  const intro = $("[data-intro]");
  if (intro) {
    let visto = false;
    try { visto = sessionStorage.getItem("vb-intro") === "1"; sessionStorage.setItem("vb-intro", "1"); } catch (_) { visto = true; }
    if (visto || reduce) intro.remove();
    else {
      document.documentElement.classList.add("js-intro");
      setTimeout(() => $(".splash-logo", intro)?.classList.add("parpadea"), 700);
      setTimeout(() => intro.classList.add("is-out"), 1750);
      setTimeout(() => intro.remove(), 2600);
    }
  }

  /* ---------- parpadeo del logo de la cabecera ---------- */
  const marca = $(".brand-logo");
  function parpadea(el) {
    if (!el || reduce) return;
    el.classList.remove("parpadea"); void el.getBoundingClientRect(); el.classList.add("parpadea");
    setTimeout(() => el.classList.remove("parpadea"), 1200);
  }
  setTimeout(() => parpadea(marca), intro && intro.isConnected ? 2300 : 600);
  setInterval(() => { if (!document.hidden) parpadea(marca); }, 9000);

  /* ---------- comparador antes / después ----------
     Arrastre horizontal en cualquier punto (ratón o dedo), toque para saltar,
     y teclado con el input oculto. El scroll vertical del móvil sigue libre. */
  $$("[data-ba]").forEach(ba => {
    const r = $(".ba-range", ba);
    const pon = v => {
      v = Math.max(0, Math.min(100, v));
      ba.style.setProperty("--pos", v + "%");
      r.value = Math.round(v);
    };
    const xa = e => { const b = ba.getBoundingClientRect(); return (e.clientX - b.left) / b.width * 100; };
    let activo = false, decidido = false, x0 = 0, y0 = 0;
    ba.addEventListener("pointerdown", e => {
      if (e.button > 0) return;
      activo = true; x0 = e.clientX; y0 = e.clientY;
      ba.classList.remove("is-hint"); ba.classList.add("is-used");
      decidido = e.pointerType !== "touch";           // con ratón se arrastra al instante
      if (decidido) { ba.setPointerCapture(e.pointerId); ba.classList.add("is-drag"); pon(xa(e)); }
    });
    ba.addEventListener("pointermove", e => {
      if (!activo) return;
      if (!decidido) {
        const dx = Math.abs(e.clientX - x0), dy = Math.abs(e.clientY - y0);
        if (dx < 5 && dy < 5) return;
        if (dy > dx) { activo = false; return; }      // gesto vertical: dejar hacer scroll
        decidido = true; ba.setPointerCapture(e.pointerId); ba.classList.add("is-drag");
      }
      e.preventDefault();
      pon(xa(e));
    });
    const fin = e => {
      if (activo && !decidido && e.type === "pointerup") pon(xa(e));   // toque corto: saltar ahí
      activo = decidido = false; ba.classList.remove("is-drag");
    };
    ba.addEventListener("pointerup", fin);
    ba.addEventListener("pointercancel", fin);
    r.addEventListener("input", () => { ba.classList.remove("is-hint"); pon(+r.value); });
    if ("IntersectionObserver" in window && !reduce) {
      const io = new IntersectionObserver(es => es.forEach(e => {
        if (e.isIntersecting && !ba.classList.contains("is-used")) {
          ba.classList.add("is-hint");
          setTimeout(() => { ba.classList.remove("is-hint"); if (!ba.classList.contains("is-used")) pon(50); }, 2900);
          io.unobserve(ba);
        }
      }), { threshold: .6 });
      io.observe(ba);
    }
  });

  /* ---------- vídeos: reproducir solo cuando se ven ---------- */
  const vids = $$("video[data-autoplay]");
  if ("IntersectionObserver" in window) {
    const iov = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && !reduce) { if (v.preload === "none") v.preload = "auto"; v.play().catch(() => {}); }
      else v.pause();
    }), { threshold: .35 });
    vids.forEach(v => iov.observe(v));
  }

  /* ---------- transición de salida (navegadores sin View Transitions) ---------- */
  if (!("onpagereveal" in window) && !reduce) {
    document.addEventListener("click", e => {
      const a = e.target.closest("a[href]");
      if (!a || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname || !/\.html$|\/$/.test(url.pathname)) return;
      e.preventDefault();
      document.body.classList.add("is-leaving");
      setTimeout(() => { location.href = a.href; }, 220);
    });
    addEventListener("pageshow", () => document.body.classList.remove("is-leaving"));
  }
})();

/* Estética Verónica Benítez · flechas y puntos de los carruseles + Instagram flotante */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  $$("[data-swipe]").forEach(sw => {
    const nav = sw.nextElementSibling;
    if (!nav || !nav.matches("[data-car-nav]")) return;
    const items = [...sw.children];
    const dots = $("[data-dots]", nav), prev = $("[data-prev]", nav), next = $("[data-next]", nav);
    dots.innerHTML = items.map(() => "<i></i>").join("");
    const ds = [...dots.children];
    const paso = () => items[0].getBoundingClientRect().width + (parseFloat(getComputedStyle(sw).columnGap) || 12);
    const act = () => {
      const fin = sw.scrollLeft + sw.clientWidth >= sw.scrollWidth - 6;
      const i = fin ? ds.length - 1 : Math.round(sw.scrollLeft / paso());
      ds.forEach((d, k) => d.classList.toggle("is-on", k === i));
      prev.disabled = sw.scrollLeft < 6; next.disabled = fin;
    };
    const actual = () => Math.max(0, ds.findIndex(d => d.classList.contains("is-on")));
    const ir = i => sw.scrollTo({ left: Math.max(0, Math.min(items.length - 1, i)) * paso(), behavior: "smooth" });
    prev.addEventListener("click", () => ir(actual() - 1));
    next.addEventListener("click", () => ir(actual() + 1));
    sw.addEventListener("scroll", () => requestAnimationFrame(act), { passive: true });
    addEventListener("resize", act);
    act();
  });
  const ig = $(".ig-float");
  if (ig) {
    const t = () => ig.classList.toggle("is-in", scrollY > 500);
    addEventListener("scroll", t, { passive: true }); t();
  }
})();
