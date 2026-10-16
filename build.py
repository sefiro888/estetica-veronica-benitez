# -*- coding: utf-8 -*-
"""Genera la web estática de Estética Verónica Benítez.

    python scripts/prepare_assets.py   # (solo si cambian fotos o logo)
    python build.py
"""
import json
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from content import (NEGOCIO as N, HORARIO, DIAS, RESENAS, CATEGORIAS, FRASES,  # noqa: E402
                     SERVICIOS, SERV, FAQ_GENERAL, QUIZ, MODO_DEMO, COMPARA, TITULOS_AD,
                     REELS, VIDEO_SERVICIO, EQUIPO)

LOGO = json.loads((ROOT / "scripts" / "_logo_partes.json").read_text(encoding="utf-8"))
AD = ROOT / "assets" / "img" / "antes-despues"
EQ = ROOT / "assets" / "img" / "equipo"

VERSION = "7"
IA = ROOT / "assets" / "img" / "ia"
e = escape
MSG = "¡Hola Vero! Me gustaría pedir cita."


# ------------------------------------------------------------------ utilidades
def wa(texto: str) -> str:
    return f"https://wa.me/{N['wa']}?text={quote(texto)}"


def foto(nombre, sm=False):
    return f"assets/img/fotos/{'sm/' if sm else ''}{nombre}.webp"


ICONOS = {
    "wa": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3Z" fill="currentColor"/>',
    "tel": '<path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .6 3.6 1 1 0 0 1-.3 1Z" fill="currentColor"/>',
    "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z" fill="currentColor"/>',
    "reloj": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5a.5.5 0 0 1 .5-.5Z" fill="currentColor"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "estrella": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z" fill="currentColor"/>',
    "check": '<path d="m5 12.5 4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "mas": '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "chispa": '<path d="M12 2.5c.6 4.6 2.9 6.9 7.5 7.5-4.6.6-6.9 2.9-7.5 7.5-.6-4.6-2.9-6.9-7.5-7.5 4.6-.6 6.9-2.9 7.5-7.5Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M19 16.5c.2 1.6 1 2.3 2.5 2.5-1.5.2-2.3.9-2.5 2.5-.2-1.6-1-2.3-2.5-2.5 1.5-.2 2.3-.9 2.5-2.5Z" fill="currentColor"/>',
    "corazon": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    "acceso": '<circle cx="12" cy="4.5" r="2" fill="currentColor"/><path d="M5 8.5h14M12 8.5v5l-3.5 7M12 13.5l3.5 7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "persona": '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M4 21a8 8 0 0 1 16 0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "ruta": '<path d="M6 19a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM18 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM8.5 14.5 15.5 9.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "calendario": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "regalo": '<rect x="3.5" y="8.5" width="17" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M5 12.5V20a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7.5M12 8.5V21M12 8.5S10.5 3.5 8 4.2C6 4.8 7 8.5 12 8.5Zm0 0s1.5-5 4-4.3c2 .6 1 4.3-4 4.3Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    "euro": '<path d="M17.5 6.5A7 7 0 1 0 17.5 17.5M4 10.5h9M4 13.5h9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "unas": '<path d="M8 21v-9.5a4 4 0 0 1 8 0V21" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9.5 12a2.5 2.5 0 0 1 5 0v2.5h-5Z" fill="currentColor" opacity=".35"/>',
    "ojo": '<path d="M3 13c2.6-3.2 5.6-4.8 9-4.8s6.4 1.6 9 4.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M5 14.4 3.8 17M8.3 15.6l-.8 2.9M12 16v3M15.7 15.6l.8 2.9M19 14.4l1.2 2.6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "hoja": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15M5 19l8-8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "bano": '<circle cx="8" cy="5" r="1.8" fill="currentColor"/><circle cx="16" cy="5" r="1.8" fill="currentColor"/><path d="M6 21v-6H4.5l1.5-6h4l1.5 6H10v6M14 21v-6.5h-.5V9h5v5.5H18V21M12 3v18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
}


def ico(n, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONOS[n]}</svg>'


def ig_color(cls="ig-color", gid="igG"):
    """Logotipo de Instagram con su degradado de marca."""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><defs>'
            f'<radialGradient id="{gid}" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#fdf497"/>'
            '<stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/>'
            '<stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs>'
            f'<rect x="1" y="1" width="22" height="22" rx="6.5" fill="url(#{gid})"/>'
            '<rect x="5.2" y="5.2" width="13.6" height="13.6" rx="4.2" fill="none" stroke="#fff" stroke-width="1.8"/>'
            '<circle cx="12" cy="12" r="3.3" fill="none" stroke="#fff" stroke-width="1.8"/>'
            '<circle cx="16.5" cy="7.5" r="1.05" fill="#fff"/></svg>')


def nav_carrusel():
    return (f'<div class="car-nav" data-car-nav><button type="button" class="car-nav-btn" data-prev aria-label="Anterior">{ico("flecha", "ico flip")}</button>'
            f'<span class="car-dots" data-dots></span>'
            f'<button type="button" class="car-nav-btn" data-next aria-label="Siguiente">{ico("flecha")}</button></div>')



def estrellas(n=5):
    return '<span class="stars" aria-label="%d de 5 estrellas">%s</span>' % (n, ico("estrella") * n)


def ojo(cls="ojo-deco"):
    return f'<img src="assets/img/brand/ojo-rosa.png" alt="" class="{cls}" loading="lazy" aria-hidden="true">'


def h(t):
    """Franjas de un día como texto."""
    return " y ".join(f"{a.lstrip('0')}–{b.lstrip('0')}" for a, b in t) if t else "Cerrado"


# ------------------------------------------------------------------ cabecera
def nav_mega():
    def col(cat):
        return "".join(
            f'<li><a href="{s["slug"]}.html" class="mega-link" data-img="{foto(s["thumb"], True)}">'
            f'<span class="mega-name">{e(s["nombre"])}{" <em class=tag>Favorito</em>" if s.get("estrella") else ""}</span>'
            f'<span class="mega-desc">{e(s["menu"])}</span></a></li>'
            for s in SERVICIOS if s["cat"] == cat)
    return f"""
<div class="mega" id="mega-servicios" role="region" aria-label="Servicios">
  <div class="mega-inner">
    <div class="mega-col">
      <p class="mega-title">{ico('unas')} {e(CATEGORIAS['unas'][0])}</p>
      <ul class="mega-list">{col('unas')}</ul>
    </div>
    <div class="mega-col">
      <p class="mega-title">{ico('ojo')} {e(CATEGORIAS['mirada'][0])}</p>
      <ul class="mega-list">{col('mirada')}</ul>
      <p class="mega-title mt">{ico('chispa')} {e(CATEGORIAS['depilacion'][0])}</p>
      <ul class="mega-list">{col('depilacion')}</ul>
    </div>
    <div class="mega-col">
      <p class="mega-title">{ico('hoja')} {e(CATEGORIAS['cabina'][0])}</p>
      <ul class="mega-list">{col('cabina')}</ul>
    </div>
    <div class="mega-preview" aria-hidden="true">
      <img src="{foto('unas-placa-logo', True)}" alt="" class="mega-img" loading="lazy">
      <div class="mega-preview-txt"><span>Lo más pedido</span><strong>Manicura semipermanente con diseño</strong></div>
      <a class="mega-all" href="servicios.html">Ver todos los servicios {ico('flecha')}</a>
    </div>
  </div>
</div>"""


def header(activo):
    def a(href, txt, key):
        cur = ' aria-current="page"' if key == activo else ""
        return f'<a href="{href}" class="nav-link"{cur}>{txt}</a>'
    return f"""
<a class="skip" href="#main">Saltar al contenido</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span class="estado" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></span>
    <span class="topbar-mid">Calle Cruz, local 8 · Huelva · Solo con cita previa</span>
    <span class="topbar-right">
      <a href="tel:{N['movil_href']}">{ico('tel')} {N['movil']}</a>
      <a href="{N['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ico('ig')}</a>
      <a href="{N['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ico('fb')}</a>
    </span>
  </div>
</div>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a href="index.html" class="brand" aria-label="Estética Verónica Benítez · inicio">
      {logo_svg("brand-logo")}
    </a>
    <nav class="nav" aria-label="Principal">
      {a('index.html', 'Inicio', 'inicio')}
      <div class="nav-item has-mega">
        <button class="nav-link nav-btn" aria-expanded="false" aria-controls="mega-servicios"{' aria-current="page"' if activo == 'servicios' else ''}>Servicios <span class="chev"></span></button>
        {nav_mega()}
      </div>
      <div class="nav-item has-drop">
        <button class="nav-link nav-btn" aria-expanded="false" aria-controls="drop-centro"{' aria-current="page"' if activo == 'centro' else ''}>El centro <span class="chev"></span></button>
        <div class="drop" id="drop-centro">
          <a href="nosotras.html"><strong>Verónica y su equipo</strong><span>Quién te cuida</span></a>
          <a href="el-centro.html"><strong>Nuestro salón</strong><span>Pequeñito pero muy acogedor</span></a>
          <a href="galeria.html"><strong>Galería de trabajos</strong><span>Uñas, pestañas y cejas reales</span></a>
          <a href="opiniones.html"><strong>Opiniones</strong><span>5,0 ★ en Google</span></a>
          <a href="tarjeta-regalo.html"><strong>Tarjeta regalo</strong><span>Regala un rato para ella</span></a>
        </div>
      </div>
      {a('ubicacion.html', 'Cómo llegar', 'ubicacion')}
      {a('contacto.html', 'Contacto', 'contacto')}
    </nav>
    <a href="contacto.html#cita" class="btn btn-rose btn-sm header-cta">{ico('wa')} Pedir cita</a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu-movil" data-burger>
      <span class="burger-lines"><i></i><i></i><i></i></span><span class="burger-txt">Menú</span>
    </button>
  </div>
</header>
{menu_movil()}"""


def menu_movil():
    grupos = ""
    for cat, (titulo, sub) in CATEGORIAS.items():
        items = "".join(
            f'<a href="{s["slug"]}.html" class="mm-serv"><img src="{foto(s["thumb"], True)}" alt="" loading="lazy">'
            f'<span><strong>{e(s["nombre"])}</strong><small>{e(s["menu"])}</small></span></a>'
            for s in SERVICIOS if s["cat"] == cat)
        grupos += f"""
      <details class="mm-group">
        <summary><span>{e(titulo)}</span><span class="mm-plus">{ico('mas')}</span></summary>
        <div class="mm-servs">{items}</div>
      </details>"""
    return f"""
<div class="mmenu" id="menu-movil" data-mmenu aria-hidden="true">
  <div class="mmenu-bg"></div>
  <div class="mmenu-in">
    <div class="mmenu-top">
      <img src="assets/img/brand/logo-claro.svg" alt="Estética Verónica Benítez" class="mmenu-logo">
      <button class="mmenu-close" data-close aria-label="Cerrar menú">{ico('x')}</button>
    </div>
    <p class="estado estado--menu" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
    <nav class="mm-nav" aria-label="Menú móvil">
      <a href="index.html" class="mm-link"><em>01</em>Inicio</a>
      <a href="servicios.html" class="mm-link"><em>02</em>Todos los servicios</a>
      {grupos}
      <a href="nosotras.html" class="mm-link"><em>03</em>Verónica y su equipo</a>
      <a href="el-centro.html" class="mm-link"><em>04</em>El centro</a>
      <a href="galeria.html" class="mm-link"><em>05</em>Galería</a>
      <a href="opiniones.html" class="mm-link"><em>06</em>Opiniones</a>
      <a href="tarjeta-regalo.html" class="mm-link"><em>07</em>Tarjeta regalo</a>
      <a href="ubicacion.html" class="mm-link"><em>08</em>Cómo llegar</a>
      <a href="contacto.html" class="mm-link"><em>09</em>Contacto y cita</a>
    </nav>
    <div class="mm-actions">
      <a class="btn btn-rose" href="{wa(MSG)}" target="_blank" rel="noopener">{ico('wa')} WhatsApp</a>
      <a class="btn btn-ghost-light" href="tel:{N['movil_href']}">{ico('tel')} Llamar</a>
      <a class="btn btn-ghost-light" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')} Cómo llegar</a>
    </div>
    <div class="mm-social">
      <a href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} @verobenitezc</a>
      <a href="{N['facebook']}" target="_blank" rel="noopener">{ico('fb')} Estética Verónica Benítez</a>
    </div>
    <div class="gold-line" aria-hidden="true"></div>
  </div>
</div>"""


# ------------------------------------------------------------------ hero
def muro_fotos():
    """Cabecera animada: columnas de fotos reales que suben y bajan."""
    cols = [
        ["unas-placa-logo", "lifting-4", "unas-leopardo", "unas-pastel-dorado", "microblading-3"],
        ["unas-arte-turquesa", "unas-celeste-perlas", "lifting-1", "unas-corazones", "unas-french"],
        ["unas-fucsia-ondas", "microblading-2", "unas-lila-motas", "unas-marco-dorado", "lifting-2"],
        ["unas-rayas-pastel", "unas-ombre-rojo", "unas-azul-abstracto", "lifting-5", "unas-fluor"],
    ]
    html = ""
    for i, c in enumerate(cols):
        imgs = "".join(f'<img src="{foto(g, True)}" alt="" decoding="async">' for g in c)
        html += f'<div class="wall-col wall-col--{i}"><div class="wall-track">{imgs}{imgs}</div></div>'
    return f'<div class="wall" aria-hidden="true">{html}</div>'


def hero(clave, eyebrow, h1, intro, ctas="", extra="", alto="", media=None):
    ia = IA / f"hero-{clave}.webp"
    if ia.exists():  # imagen generada por IA añadida más adelante
        src_d = src_l = src_m = f"assets/img/ia/hero-{clave}.webp"
    else:
        src_d, src_l, src_m = (f"assets/img/hero/{clave}-1920.webp", f"assets/img/hero/{clave}.webp",
                               f"assets/img/hero/{clave}-m.webp")
    return f"""
<section class="hero {alto}" data-hero>
  {media or f'''<picture class="hero-media">
    <source media="(max-width: 700px)" srcset="{src_m}">
    <source media="(min-width: 1921px)" srcset="{src_l}">
    <img src="{src_d}" alt="" fetchpriority="high" decoding="async">
  </picture>'''}
  <div class="hero-shade"></div>
  <div class="wrap hero-in">
    <p class="eyebrow eyebrow--light">{e(eyebrow)}</p>
    <h1 class="hero-title">{h1}</h1>
    <p class="hero-intro">{e(intro)}</p>
    <div class="hero-ctas">{ctas}</div>
    {extra}
  </div>
  <a href="#main-c" class="hero-scroll" aria-label="Bajar al contenido"><span></span></a>
</section>
<span id="main-c"></span>"""


def ctas_cita(texto_wa, segundo=("Ver servicios", "servicios.html")):
    return (f'<a class="btn btn-rose" href="{wa(texto_wa)}" target="_blank" rel="noopener">{ico("wa")} Pedir cita por WhatsApp</a>'
            f'<a class="btn btn-ghost-light" href="{segundo[1]}">{segundo[0]} {ico("flecha")}</a>')


# ------------------------------------------------------------------ bloques comunes
def cinta(items=None):
    items = items or ["Manicura semipermanente", "Acrygel", "Nail art a mano alzada", "Lifting de pestañas",
                      "Microblading", "Láser de diodo", "Limpieza de cutis", "Parafina", "Maquillaje de novia"]
    seq = "".join(f"<span>{e(t)}</span><i>{ico('chispa')}</i>" for t in items)
    return f'<div class="cinta" aria-hidden="true"><div class="cinta-track">{seq}{seq}</div></div>'


def tarjeta_servicio(s):
    return f"""
<a href="{s['slug']}.html" class="card-serv" data-cat="{s['cat']}">
  <span class="card-img"><img src="{foto(s['thumb'], True)}" alt="{e(s['nombre'])}" loading="lazy"></span>
  <span class="card-body">
    <span class="card-cat">{e(CATEGORIAS[s['cat']][0])}</span>
    <strong class="card-title">{e(s['nombre'])}</strong>
    <span class="card-txt">{e(s['menu'])}</span>
    <span class="card-more">Descubrir {ico('flecha')}</span>
  </span>
  {"<span class='badge-star'>" + ico('corazon') + " Favorito</span>" if s.get('estrella') else ''}
</a>"""


def resena_card(i):
    autor, fuente, n, txt = RESENAS[i]
    return f"""
<figure class="review">
  {estrellas(n)}
  <blockquote>«{e(txt)}»</blockquote>
  <figcaption><span class="avatar">{e(autor[0])}</span><span><strong>{e(autor)}</strong><small>Reseña en {e(fuente)}</small></span></figcaption>
</figure>"""


def carrusel_resenas(titulo="Lo que dicen nuestras clientas", sub="5,0 ★ en Google con 30 reseñas · 96 % la recomiendan en Facebook"):
    cards = "".join(resena_card(i) for i in range(len(RESENAS)))
    return f"""
<section class="section section--ink reviews-sec" aria-labelledby="t-resenas">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div>
        <p class="eyebrow eyebrow--light">Opiniones reales</p>
        <h2 id="t-resenas" class="h2">{titulo}</h2>
        <p class="lead lead--light">{sub}</p>
      </div>
      <div class="car-ctrl">
        <button class="car-btn" data-car-prev aria-label="Anterior">{ico('flecha', 'ico flip')}</button>
        <button class="car-btn" data-car-next aria-label="Siguiente">{ico('flecha')}</button>
      </div>
    </div>
    <div class="carousel" data-carousel tabindex="0" aria-label="Reseñas de clientas">{cards}</div>
    <p class="center mt-l"><a href="opiniones.html" class="link-light">Leer todas las opiniones {ico('flecha')}</a></p>
  </div>
</section>"""


def faq_list(faqs, abierto=True):
    out = ""
    for i, (q, a) in enumerate(faqs):
        out += f"""
<details class="faq"{' open' if (abierto and i == 0) else ''}>
  <summary><span>{e(q)}</span><span class="faq-ico">{ico('mas')}</span></summary>
  <div class="faq-a"><p>{e(a)}</p></div>
</details>"""
    return out


def horario_tabla():
    filas = ""
    for d in range(7):
        fr = HORARIO[d]
        man = next((f"{a.lstrip('0')} – {b.lstrip('0')}" for a, b in fr if a < "15:00"), "")
        tar = next((f"{a.lstrip('0')} – {b.lstrip('0')}" for a, b in fr if a >= "15:00"), "")
        cer = '<span class="muted">Cerrado</span>'
        if not fr:
            filas += f'<tr data-dia="{d}" class="is-off"><th scope="row">{DIAS[d]}</th><td colspan="2">{cer}</td></tr>'
        else:
            filas += f'<tr data-dia="{d}"><th scope="row">{DIAS[d]}</th><td>{man or cer}</td><td>{tar or cer}</td></tr>'
    return f'<table class="horario"><thead><tr><th></th><th>Mañana</th><th>Tarde</th></tr></thead><tbody>{filas}</tbody></table>'


def bloque_visita(titulo="Ven a vernos"):
    return f"""
<section class="section visit" aria-labelledby="t-visita">
  <div class="wrap visit-grid">
    <div class="visit-info">
      <p class="eyebrow">Dónde y cuándo</p>
      <h2 id="t-visita" class="h2">{titulo}</h2>
      <ul class="info-list">
        <li>{ico('pin')}<span><strong>{e(N['direccion'])}</strong><br>{e(N['referencia'])} · {N['cp']} {N['ciudad']}</span></li>
        <li>{ico('wa')}<span><strong>WhatsApp y reservas</strong><br><a href="{wa(MSG)}" target="_blank" rel="noopener">{N['movil']}</a></span></li>
        <li>{ico('tel')}<span><strong>Teléfono fijo</strong><br><a href="tel:{N['tel_fijo_href']}">{N['tel_fijo']}</a></span></li>
      </ul>
      <h3 class="h4 mt">Horario · con cita previa</h3>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('ruta')} Cómo llegar</a>
        <a class="btn btn-outline" href="ubicacion.html">Ver indicaciones {ico('flecha')}</a>
      </div>
    </div>
    {mapa()}
  </div>
</section>"""


def mapa():
    return f"""
<div class="map" data-map data-src="https://www.google.com/maps?q={N['lat']},{N['lng']}&z=17&output=embed">
  <img src="{foto('local-fachada', True)}" alt="" loading="lazy">
  <div class="map-cover">
    <span class="map-pin">{ico('pin')}</span>
    <strong>Estética Verónica Benítez</strong>
    <span>Calle Cruz, local 8 · Huelva</span>
    <button class="btn btn-rose btn-sm" data-map-load>Cargar mapa interactivo</button>
    <small>Al pulsar se carga Google Maps.</small>
  </div>
</div>"""


def cta_final(texto="¿Te reservamos un ratito?", sub="Escríbenos por WhatsApp y te contestamos en cuanto terminemos con la clienta que está en cabina.", msg=MSG):
    return f"""
<section class="cta-final">
  <div class="cta-bg" style="background-image:url('assets/img/hero/contacto-1920.webp')"></div>
  <div class="wrap cta-in">
    <img src="assets/img/brand/logo-claro.svg" alt="" class="cta-logo" loading="lazy">
    <h2 class="h2">{texto}</h2>
    <p class="lead lead--light">{sub}</p>
    <div class="btn-row center">
      <a class="btn btn-rose btn-lg" href="{wa(msg)}" target="_blank" rel="noopener">{ico('wa')} {N['movil']}</a>
      <a class="btn btn-ghost-light btn-lg" href="tel:{N['tel_fijo_href']}">{ico('tel')} {N['tel_fijo']}</a>
    </div>
  </div>
</section>"""


def footer():
    serv = lambda cat: "".join(f'<li><a href="{s["slug"]}.html">{e(s["nombre"])}</a></li>' for s in SERVICIOS if s["cat"] == cat)
    return f"""
<footer class="footer">
  <div class="gold-line" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="assets/img/brand/logo-claro.svg" alt="Estética Verónica Benítez" class="footer-logo" loading="lazy">
      <p>Salón de estética integral y decorativa en Huelva. Pequeñito pero muy acogedor: uñas, mirada, depilación, faciales y maquillaje con trato cercano y personalizado.</p>
      <div class="footer-social">
        <a href="{N['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ico('ig')}</a>
        <a href="{N['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ico('fb')}</a>
        <a href="{wa('¡Hola Vero!')}" target="_blank" rel="noopener" aria-label="WhatsApp">{ico('wa')}</a>
      </div>
    </div>
    <div><p class="f-title">Manos y pies</p><ul>{serv('unas')}</ul></div>
    <div><p class="f-title">Mirada y depilación</p><ul>{serv('mirada')}{serv('depilacion')}</ul>
      <p class="f-title mt">Cabina</p><ul>{serv('cabina')}</ul></div>
    <div>
      <p class="f-title">Visítanos</p>
      <p>{e(N['direccion'])}<br>{e(N['referencia'])}<br>{N['cp']} {N['ciudad']}</p>
      <p><a href="{wa('¡Hola Vero!')}" target="_blank" rel="noopener">{N['movil']}</a> · <a href="tel:{N['tel_fijo_href']}">{N['tel_fijo']}</a></p>
      <p class="f-hours">L y V · 10–14<br>M y J · 10–14 y 16:30–20:30<br>X · 16:30–20:30<br>S y D · cerrado</p>
      <p class="f-title mt">El centro</p>
      <ul><li><a href="nosotras.html">Verónica y su equipo</a></li><li><a href="el-centro.html">Nuestro salón</a></li><li><a href="galeria.html">Galería</a></li><li><a href="opiniones.html">Opiniones</a></li><li><a href="tarjeta-regalo.html">Tarjeta regalo</a></li></ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© 2026 Estética Verónica Benítez · Huelva</span>
    <span>Web de demostración · Fotos: @verobenitezc</span>
  </div>
</footer>
<nav class="actionbar" aria-label="Acciones rápidas">
  <a href="tel:{N['movil_href']}">{ico('tel')}<span>Llamar</span></a>
  <a href="{wa(MSG)}" target="_blank" rel="noopener" class="ab-main">{ico('wa')}<span>Cita</span></a>
  <a href="{N['instagram']}" target="_blank" rel="noopener" class="ab-ig" aria-label="Instagram de Estética Verónica Benítez">{ig_color(gid="igBar")}<span>Instagram</span></a>
  <a href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')}<span>Llegar</span></a>
</nav>
<a class="ig-float" href="{N['instagram']}" target="_blank" rel="noopener" aria-label="Síguenos en Instagram">{ig_color(gid="igFloat")}<span>@verobenitezc</span></a>
<a class="wa-float" href="{wa(MSG)}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{ico('wa')}<span>¿Te damos cita?</span></a>
<div class="lightbox" data-lightbox hidden><button class="lb-close" aria-label="Cerrar">{ico('x')}</button><button class="lb-prev" aria-label="Anterior">{ico('flecha', 'ico flip')}</button><img alt=""><button class="lb-next" aria-label="Siguiente">{ico('flecha')}</button><p class="lb-cap"></p></div>"""


def pagina(archivo, titulo, desc, activo, cuerpo, og="assets/img/brand/og.jpg", jsonld=None):
    horario_js = json.dumps({str(k): v for k, v in HORARIO.items()})
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#16110f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Estética Verónica Benítez · Huelva">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{N['web']}{'' if archivo == 'index.html' else archivo}">
<meta property="og:image" content="{N['web']}{og}">
<meta property="og:image:secure_url" content="{N['web']}{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo de Estética Verónica Benítez con fotos de uñas, pestañas y cejas">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titulo)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{N['web']}{og}">
<link rel="icon" href="assets/img/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/brand/favicon.png" type="image/png" sizes="64x64">
<link rel="manifest" href="site.webmanifest">
<meta name="view-transition" content="same-origin">
<script>try{{if(sessionStorage.getItem("vb-intro")!=="1"&&!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("js-intro")}}catch(e){{}}</script>
<link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
{ld}
</head>
<body data-page="{activo}">
{intro()}
{header(activo)}
<main id="main">
{cuerpo}
</main>
{footer()}
<script>window.HORARIO={horario_js};</script>
<script src="assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""
    (ROOT / archivo).write_text(html, encoding="utf-8")
    return archivo


JSONLD_NEGOCIO = {
    "@context": "https://schema.org", "@type": "BeautySalon", "name": "Estética Verónica Benítez",
    "image": "assets/img/brand/og.jpg", "telephone": "+34679901866",
    "address": {"@type": "PostalAddress", "streetAddress": "Calle Cruz, local 8",
                "addressLocality": "Huelva", "postalCode": "21006", "addressRegion": "Huelva", "addressCountry": "ES"},
    "geo": {"@type": "GeoCoordinates", "latitude": N["lat"], "longitude": N["lng"]},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "30"},
    "paymentAccepted": "Cash",
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday", "Friday"], "opens": "10:00", "closes": "14:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "16:30", "closes": "20:30"}],
    "sameAs": [N["instagram"], N["facebook"]],
}


# ------------------------------------------------------------------ logo vectorial
def logo_svg(cls="logo-svg", marco=False, ojo_solo=False):
    """Logo original vectorizado, en línea para poder animar el parpadeo."""
    ojo_ = (f'<g class="lg-ceja">{LOGO["ceja"]}</g><g class="lg-parpado">{LOGO["parpado"]}</g>'
            f'<g class="lg-pestanas">{LOGO["pestanas"]}</g>')
    if ojo_solo:
        box, cuerpo = LOGO["ojo_box"], ojo_
    elif marco:
        box, cuerpo = LOGO["full_box"], f'<g class="lg-marco">{LOGO["marco"]}</g><g class="lg-texto">{LOGO["texto"]}</g>{ojo_}'
    else:
        box, cuerpo = LOGO["sin_marco_box"], f'<g class="lg-texto">{LOGO["texto"]}</g>{ojo_}'
    return (f'<svg class="{cls}" viewBox="{" ".join(map(str, box))}" fill="currentColor" role="img" '
            f'aria-label="Estética Verónica Benítez">{cuerpo}</svg>')


def intro():
    return f'<div class="splash" data-intro aria-hidden="true"><div class="splash-in">{logo_svg("splash-logo")}<span class="splash-line"></span></div></div>'


# ------------------------------------------------------------------ antes / después
def pares(prefijo):
    if not AD.exists():
        return []
    out = []
    for a in sorted(AD.glob(f"{prefijo}-*-antes.webp")):
        clave = a.name[:-len("-antes.webp")]
        if (AD / f"{clave}-despues.webp").exists():
            out.append(clave)
    return out


def slider(clave, titulo=""):
    a, d = f"assets/img/antes-despues/{clave}-antes.webp", f"assets/img/antes-despues/{clave}-despues.webp"
    cap = f'<figcaption>{e(titulo)}</figcaption>' if titulo else ''
    return f"""
<figure class="ba-slider reveal" data-ba style="--pos:50%">
  <img src="{d}" alt="Después · {e(titulo)}" loading="lazy" class="ba-img">
  <div class="ba-antes"><img src="{a}" alt="Antes · {e(titulo)}" loading="lazy" class="ba-img"></div>
  <span class="ba-lbl ba-lbl--a">Antes</span><span class="ba-lbl ba-lbl--d">Después</span>
  <span class="ba-handle" aria-hidden="true"><i>{ico('flecha', 'ico flip')}{ico('flecha')}</i></span>
  <input type="range" min="0" max="100" value="50" class="ba-range" aria-label="Desliza para comparar antes y después">
  {cap}
</figure>"""


def hueco_ad(servicio):
    return f"""
<figure class="ba-slot reveal">
  <div class="ba-slot-in">
    <span class="ba-slot-half"><b>Antes</b><small>Tu foto real</small></span>
    <span class="ba-slot-half"><b>Después</b><small>El resultado</small></span>
    <span class="ba-slot-bar"><i>{ico('flecha', 'ico flip')}{ico('flecha')}</i></span>
  </div>
  <figcaption>{ojo('ba-slot-ojo')}Espacio preparado · {e(servicio)}</figcaption>
</figure>"""


def guia_fotos(abierta=False):
    return f"""
<details class="guia"{' open' if abierta else ''}>
  <summary><span class="guia-ico">{ico('chispa')}</span><span><strong>Verónica: este espacio está preparado para tus fotos de antes y después</strong>
  <small>Cuando nos las pases, aparecerán aquí con un deslizador para comparar. Toca para ver cómo hacerlas.</small></span><span class="faq-ico">{ico('mas')}</span></summary>
  <div class="guia-in">
    <ol class="guia-pasos">
      <li><b>Pide permiso por escrito a la clienta.</b> Es obligatorio para publicar su imagen (derecho a la propia imagen y protección de datos). Te preparamos un modelo sencillo de autorización: nombre, servicio, uso en web y redes y firma. Puede retirarlo cuando quiera.</li>
      <li><b>Misma luz, mismo encuadre.</b> Haz el «antes» y el «después» desde la misma posición y distancia, con luz natural o la de cabina, y sin filtros.</li>
      <li><b>Solo la zona, si lo prefiere.</b> Si la clienta no quiere salir entera, encuadra solo ojos, cejas, manos o piel. Con la placa del logo, como haces con las uñas, queda perfecto.</li>
      <li><b>Las dos fotos con el mismo formato.</b> Vertical u horizontal, pero igual en ambas. Mejor con el modo normal de la cámara (no retrato) y la lente limpia.</li>
      <li><b>Envíalas como «documento» por WhatsApp</b> para que no pierdan calidad, indicando el servicio: lifting, cejas, microblading, uñas, facial o láser.</li>
    </ol>
    <p class="guia-nota">{ico('check')} Nosotros las retocamos ligeramente (luz y color, sin alterar el resultado), las igualamos y las publicamos en el servicio correspondiente.</p>
  </div>
</details>"""


def comparador(slug, titulo_sec="Antes y después", sub=""):
    prefijo = COMPARA.get(slug)
    if not prefijo:
        return ""
    reales = pares(prefijo)
    if not reales and not MODO_DEMO:
        return ""
    serv = SERV[slug]["nombre"] if slug in SERV else ""
    items = "".join(slider(c, TITULOS_AD.get(c, "")) for c in reales[:3])
    if MODO_DEMO and not reales:
        items += hueco_ad(serv) + hueco_ad(serv)
    sub = sub or ("Desliza sobre cada foto para comparar. Resultados reales de clientas." if reales
                  else "Aquí verás resultados reales de clientas con un deslizador para comparar el antes y el después.")
    return f"""
<section class="section section--blush" id="antes-despues" aria-labelledby="t-ad-{slug}">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Resultados reales</p><h2 id="t-ad-{slug}" class="h2">{titulo_sec}</h2><p class="lead">{e(sub)}</p></div>
    <div class="ba-grid ba-grid--{len(reales[:3]) or 2}">{items}</div>
    {guia_fotos() if MODO_DEMO else ''}
  </div>
</section>"""


# ------------------------------------------------------------------ fotos de equipo
def foto_equipo(clave):
    for ext in ("webp", "jpg", "png"):
        if (EQ / f"{clave}.{ext}").exists():
            return f"assets/img/equipo/{clave}.{ext}"
    return None


def hueco_retrato(texto="Tu retrato aquí"):
    return f"""
<div class="retrato-slot">
  {logo_svg('retrato-logo', ojo_solo=True)}
  <strong>{e(texto)}</strong>
  <small>Espacio preparado para una foto real</small>
</div>"""


# ------------------------------------------------------------------ vídeos
def video(nombre, cls="vid", caption="", enlace=""):
    pie = ""
    if caption:
        ig = f'<a href="{enlace}" target="_blank" rel="noopener" aria-label="Ver en Instagram">{ico("ig")}</a>' if enlace else ""
        pie = f"<figcaption><span>{e(caption)}</span>{ig}</figcaption>"
    return f"""
<figure class="{cls}">
  <video muted loop playsinline preload="none" poster="assets/video/{nombre}.webp" data-autoplay aria-label="{e(caption or 'Vídeo de Estética Verónica Benítez')}">
    <source src="assets/video/{nombre}.mp4" type="video/mp4">
  </video>
  {pie}
</figure>"""


def seccion_reels():
    vids = "".join(video(n, "reel reveal", c, u) for n, c, u in REELS)
    return f"""
<section class="section section--ink reels-sec" aria-labelledby="t-reels">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div><p class="eyebrow eyebrow--light">En movimiento</p><h2 id="t-reels" class="h2">Así trabajamos, en directo</h2>
      <p class="lead lead--light">Reels de nuestro Instagram: uñas recién terminadas, efectos que solo se aprecian en movimiento y el día a día en cabina.</p></div>
      <a class="btn btn-ghost-light" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} Ver más reels</a>
    </div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p>
    <div class="reels" data-swipe>{vids}</div>
    {nav_carrusel()}
  </div>
</section>"""


# ------------------------------------------------------------------ asistente de cita
def asistente(preseleccion=""):
    opts = ""
    for cat, (titulo, _) in CATEGORIAS.items():
        opts += f'<optgroup label="{e(titulo)}">' + "".join(
            f'<option value="{e(s["nombre"])}"{" selected" if s["slug"] == preseleccion else ""}>{e(s["nombre"])}</option>'
            for s in SERVICIOS if s["cat"] == cat) + "</optgroup>"
    return f"""
<form class="wizard" data-wizard id="cita" autocomplete="off">
  <div class="wizard-head">
    {ojo('wizard-ojo')}
    <p class="eyebrow">Reserva guiada</p>
    <h2 class="h3">Prepara tu mensaje de cita</h2>
    <p class="muted">Rellena lo que quieras y abriremos WhatsApp con el mensaje escrito. No guardamos ningún dato.</p>
  </div>
  <label class="field"><span>¿Qué te apetece?</span>
    <select name="servicio"><option value="">Aún no lo sé, quiero que me aconsejéis</option>{opts}</select></label>
  <fieldset class="field"><legend>¿Qué días te vienen bien?</legend>
    <div class="chips" data-multi="dias">
      <button type="button" class="chip">Lunes</button><button type="button" class="chip">Martes</button>
      <button type="button" class="chip">Miércoles</button><button type="button" class="chip">Jueves</button>
      <button type="button" class="chip">Viernes</button><button type="button" class="chip">Lo antes posible</button>
    </div></fieldset>
  <fieldset class="field"><legend>¿Mejor por la mañana o por la tarde?</legend>
    <div class="chips" data-single="franja">
      <button type="button" class="chip">Mañana (10–14)</button><button type="button" class="chip">Tarde (16:30–20:30)</button><button type="button" class="chip">Me da igual</button>
    </div></fieldset>
  <fieldset class="field"><legend>¿Es tu primera vez con nosotras?</legend>
    <div class="chips" data-single="primera"><button type="button" class="chip">Sí, primera vez</button><button type="button" class="chip">Ya soy clienta</button></div></fieldset>
  <label class="check"><input type="checkbox" name="extra"> <span>Añadir un baño de parafina a mi manicura o pedicura</span></label>
  <div class="field-row">
    <label class="field"><span>Tu nombre</span><input name="nombre" type="text" placeholder="Opcional"></label>
    <label class="field"><span>Algo que debamos saber</span><input name="notas" type="text" placeholder="Alergias, ideas, una foto que enviarás…"></label>
  </div>
  <div class="wizard-preview"><span class="muted">Así quedará tu mensaje:</span><p data-preview></p></div>
  <a class="btn btn-rose btn-lg btn-block" data-send href="{wa(MSG)}" target="_blank" rel="noopener">{ico('wa')} Enviar por WhatsApp</a>
</form>"""


# ------------------------------------------------------------------ páginas de servicio
def pagina_servicio(s):
    cat_t = CATEGORIAS[s["cat"]][0]
    msg = f"¡Hola Vero! Me interesa el servicio de {s['nombre'].lower()}. ¿Me das cita?"
    hero_html = hero(s["hero"], s["eyebrow"], e(s["h1"]), s["intro"], ctas_cita(msg, ("Cómo es la sesión", "#pasos")))
    migas = f'<nav class="crumbs wrap" aria-label="Ruta"><a href="index.html">Inicio</a><span>/</span><a href="servicios.html">Servicios</a><span>/</span><span>{e(cat_t)}</span></nav>'
    toc_items = [("que-es", "Qué es"), ("beneficios", "Beneficios"), ("para-quien", "Para quién"), ("pasos", "La sesión"), ("opciones", "Opciones")]
    if s["galeria"]:
        toc_items.append(("trabajos", "Trabajos"))
    comp = comparador(s["slug"])
    if comp:
        toc_items.append(("antes-despues", "Antes y después"))
    toc_items.append(("cuidados", "Cuidados"))
    if s["mitos"]:
        toc_items.append(("mitos", "Mitos"))
    toc_items += [("preguntas", "Preguntas"), ("reserva", "Cita")]
    toc = "".join(f'<a href="#{i}">{t}</a>' for i, t in toc_items)

    que = "".join(f"<p>{e(p)}</p>" for p in s["que_es"])
    benef = "".join(f'<div class="benef reveal"><span class="benef-n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (t, d) in enumerate(s["beneficios"]))
    quien = "".join(f'<li>{ico("check")}<span>{e(x)}</span></li>' for x in s["para_quien"])
    pasos = "".join(f'<li class="step reveal"><span class="step-n">{i+1}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
                    for i, (t, d) in enumerate(s["pasos"]))
    opciones = "".join(f"""
<article class="opt reveal">
  <h3>{e(n)}</h3><p>{e(d)}</p>
  <a class="opt-link" href="{wa(f'¡Hola Vero! Me interesa: {n}. ¿Me informas de precio y disponibilidad?')}" target="_blank" rel="noopener">{ico('wa')} Consultar esta opción</a>
</article>""" for n, d in s["opciones"])
    gal = ""
    if s["galeria"]:
        figs = "".join(f'<figure class="g-item reveal"><button data-lb="{foto(g)}" aria-label="Ampliar foto"><img src="{foto(g, True)}" alt="Trabajo real de Estética Verónica Benítez" loading="lazy"></button></figure>'
                       for g in s["galeria"])
        gal = f"""
<section class="section section--bone" id="trabajos" aria-labelledby="t-trab">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div><p class="eyebrow">Hecho en cabina</p><h2 id="t-trab" class="h2">Trabajos reales</h2>
      <p class="lead">Fotos de clientas publicadas en <a href="{N['instagram']}" target="_blank" rel="noopener">@verobenitezc</a>. Pulsa para ampliar.</p></div>
      <a class="btn btn-outline" href="galeria.html">Ver galería completa {ico('flecha')}</a>
    </div>
    <div class="g-grid g-grid--{len(s['galeria']) if len(s['galeria']) in (2, 3, 5, 6) else 4}" data-gallery>{figs}</div>
  </div>
</section>"""
    tit_cons, cons = s["consejos"]
    cons_html = "".join(f'<li><span class="tip-n">{i+1}</span><p>{e(c)}</p></li>' for i, c in enumerate(cons))
    mitos = ""
    if s["mitos"]:
        m = "".join(f'<div class="myth reveal"><p class="myth-q"><span>Mito</span>{e(a)}</p><p class="myth-a"><span>Realidad</span>{e(b)}</p></div>'
                    for a, b in s["mitos"])
        mitos = f"""
<section class="section" id="mitos" aria-labelledby="t-mitos">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Hablemos claro</p><h2 id="t-mitos" class="h2">Mitos y realidades</h2></div>
    <div class="myths">{m}</div>
  </div>
</section>"""
    rel = "".join(tarjeta_servicio(SERV[r]) for r in s["relacionados"])
    autor, fuente, n, txt = RESENAS[s["resena"]]
    combo = ""
    if s["slug"] in ("manicura", "pedicura", "acrygel", "nail-art"):
        combo = f"""
<aside class="promo reveal">
  <div class="promo-img"><img src="{foto('unas-pastel-dorado', True)}" alt="" loading="lazy"></div>
  <div class="promo-txt"><p class="eyebrow eyebrow--light">Un mimo más</p>
  <h3 class="h3">Súmale un baño de parafina</h3>
  <p>Hidratación profunda con calor para manos y pies secos. El complemento perfecto de tu cita.</p>
  <a class="btn btn-rose btn-sm" href="parafina.html">Saber más {ico('flecha')}</a></div>
</aside>"""
    img_lat = s["galeria"][0] if s["galeria"] else s["thumb"]
    img_cons = s["galeria"][1] if len(s["galeria"]) > 1 else s["thumb"]
    frase = f'<figure class="quote-card reveal">{ojo()}<blockquote>{e(s["destacado"])}</blockquote><figcaption>Estética Verónica Benítez</figcaption></figure>'
    cuerpo = f"""
{hero_html}
{migas}
<div class="toc-wrap" data-toc><nav class="toc wrap" aria-label="En esta página">{toc}</nav></div>

<section class="section" id="que-es" aria-labelledby="t-que">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">{e(cat_t)}</p>
      <h2 id="t-que" class="h2">¿En qué consiste?</h2>
      {que}
      <blockquote class="pull">{e(s['destacado'])}</blockquote>
    </div>
    <div class="split-media reveal">
      {video(VIDEO_SERVICIO[s["slug"]], "frame frame--video") if s["slug"] in VIDEO_SERVICIO else f'<figure class="frame"><img src="{foto(img_lat)}" alt="{e(s["nombre"])} en Estética Verónica Benítez" loading="lazy"></figure>'}
      <figure class="review review--mini">
        {estrellas(n)}<blockquote>«{e(txt)}»</blockquote><figcaption><strong>{e(autor)}</strong> · <small>Reseña en {e(fuente)}</small></figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section section--ink" id="beneficios" aria-labelledby="t-ben">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Por qué elegirlo</p><h2 id="t-ben" class="h2">Beneficios</h2></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="benefs">{benef}</div>
  </div>
</section>

<section class="section" id="para-quien" aria-labelledby="t-quien">
  <div class="wrap split split--rev">
    <div class="split-txt">
      <p class="eyebrow">¿Es para mí?</p>
      <h2 id="t-quien" class="h2">Para quién es</h2>
      <ul class="ticks">{quien}</ul>
      {combo}
    </div>
    <div class="split-txt" id="pasos">
      <p class="eyebrow">Paso a paso</p>
      <h2 class="h2">Así es tu cita</h2>
      <ol class="steps">{pasos}</ol>
    </div>
  </div>
</section>

<section class="section section--bone" id="opciones" aria-labelledby="t-opc">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Elige</p><h2 id="t-opc" class="h2">Opciones del servicio</h2>
    <p class="lead">Cada opción tiene su botón: abre WhatsApp con el mensaje escrito para que te informemos de precio y disponibilidad.</p></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="opts">{opciones}</div>
  </div>
</section>
{gal}
{comp}
<section class="section" id="cuidados" aria-labelledby="t-cuid">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Consejos de Vero</p>
      <h2 id="t-cuid" class="h2">{e(tit_cons)}</h2>
      <ol class="tips">{cons_html}</ol>
    </div>
    <div class="split-media reveal">
      {f'<figure class="frame frame--tall"><img src="{foto(img_cons)}" alt="" loading="lazy"></figure>' if s["galeria"] else frase}
    </div>
  </div>
</section>
{mitos}
<section class="section section--bone" id="preguntas" aria-labelledby="t-faq">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Dudas frecuentes</p><h2 id="t-faq" class="h2">Preguntas sobre {e(s['nombre'].split(' y ')[0].lower())}</h2>
    <p class="lead">¿No encuentras tu respuesta? Escríbenos y te contestamos encantadas.</p>
    <a class="btn btn-ink" href="{wa(msg)}" target="_blank" rel="noopener">{ico('wa')} Preguntar por WhatsApp</a></div>
    <div class="faqs">{faq_list(s['faqs'])}</div>
  </div>
</section>

<section class="section" id="reserva" aria-labelledby="t-cita">
  <div class="wrap wizard-wrap">
    <div class="wizard-side">
      <p class="eyebrow">Reserva</p>
      <h2 id="t-cita" class="h2">Pide tu cita</h2>
      <p class="lead">Trabajamos solo con cita previa. Mañanas de lunes, martes, jueves y viernes; tardes de martes, miércoles y jueves.</p>
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <ul class="mini-facts">
        <li>{ico('acceso')} Acceso adaptado para sillas de ruedas</li>
        <li>{ico('persona')} Centro unisex</li>
        <li>{ico('euro')} Pago en efectivo en el centro</li>
      </ul>
    </div>
    {asistente(s['slug'])}
  </div>
</section>

<section class="section section--bone" aria-labelledby="t-rel">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Combina bien con</p><h2 id="t-rel" class="h2">Servicios relacionados</h2></div>
    <div class="cards cards--3">{rel}</div>
  </div>
</section>
{cta_final()}"""
    return pagina(f"{s['slug']}.html", f"{s['nombre']} en Huelva · Estética Verónica Benítez", s["meta"],
                  "servicios", cuerpo, jsonld={"@context": "https://schema.org", "@type": "Service", "name": s["nombre"],
                                               "provider": {"@type": "BeautySalon", "name": "Estética Verónica Benítez"},
                                               "areaServed": "Huelva", "description": s["meta"]})


# ------------------------------------------------------------------ portada
def pagina_inicio():
    extra = f"""
<div class="hero-badges">
  <span class="hb">{estrellas()}<b>5,0</b> en Google · 30 reseñas</span>
  <span class="hb">{ico('corazon')} 96 % la recomiendan</span>
  <span class="hb">{ico('acceso')} Local accesible</span>
</div>"""
    h_ = hero("home", "Estética integral y decorativa · Huelva",
              'Verónica Benítez<em>Pequeñito pero muy acogedor. Cuidamos cada detalle de ti.</em>',
              "Uñas pintadas a mano, pestañas y cejas que enmarcan tu mirada, depilación, faciales y maquillaje para tus grandes días. Con todo el cariño, en la calle Cruz.",
              ctas_cita(MSG), extra, "hero--home hero--wall", media=muro_fotos())

    cards = "".join(tarjeta_servicio(s) for s in SERVICIOS)
    quiz = "".join(f'<button type="button" class="chip chip--quiz" data-quiz=\'{json.dumps(v)}\'>{e(k)}</button>' for k, v in QUIZ)
    quiz_cards = "".join(f'<template data-tpl="{s["slug"]}">{tarjeta_servicio(s)}</template>' for s in SERVICIOS)
    galeria = ["unas-leopardo", "unas-arte-turquesa", "lifting-4", "unas-pastel-dorado", "unas-corazones", "unas-celeste-perlas",
               "microblading-3", "unas-fluor", "unas-marco-dorado", "unas-rayas-pastel", "lifting-1", "unas-ombre-rojo"]
    strip = "".join(f'<figure><img src="{foto(g, True)}" alt="Trabajo de Estética Verónica Benítez" loading="lazy"></figure>' for g in galeria)
    galeria2 = ["unas-turquesa", "lifting-3", "unas-magenta", "unas-naranja-marco", "microblading-1", "unas-lima",
                "unas-granate", "unas-verde-rosa", "lifting-5", "unas-cebra-coral", "unas-negro-turquesa", "pedicura"]
    strip2 = "".join(f'<figure><img src="{foto(g, True)}" alt="" loading="lazy"></figure>' for g in galeria2)
    palabras = "".join(f"<span>{p}</span><i>{ico('chispa')}</i>" for p in ["Uñas", "Pestañas", "Cejas", "Piel", "Mirada", "Nail art"])
    mosaico = ["unas-placa-logo", "unas-fucsia-ondas", "unas-lila-motas", "unas-azul-abstracto", "unas-french"]
    mos = "".join(f'<figure class="mo mo--{i}"><button data-lb="{foto(g)}" aria-label="Ampliar"><img src="{foto(g, True)}" alt="Uñas decoradas en Estética Verónica Benítez" loading="lazy"></button></figure>' for i, g in enumerate(mosaico))

    cuerpo = f"""
{h_}
{cinta()}

<section class="section intro" aria-labelledby="t-intro">
  <div class="wrap intro-grid">
    <div class="intro-quote reveal">
      {ojo()}
      <p class="eyebrow">Nuestra filosofía</p>
      <h2 id="t-intro" class="display">«Un salón de estética pequeñito pero muy acogedor, donde ponemos el máximo esfuerzo, profesionalidad y muchas ganas cada día.»</h2>
      <p class="sign">— Verónica Benítez</p>
    </div>
    <div class="intro-stats">
      <div class="stat reveal"><strong>5,0<small>★</small></strong><span>Media en Google · 30 reseñas</span></div>
      <div class="stat reveal"><strong>96<small>%</small></strong><span>Recomendación en Facebook</span></div>
      <div class="stat reveal"><strong>+800</strong><span>Trabajos compartidos en Instagram</span></div>
      <div class="stat reveal"><strong>+10</strong><span>Años con clientas que repiten</span></div>
    </div>
  </div>
</section>

<section class="section section--ink star" aria-labelledby="t-star">
  <div class="wrap star-grid">
    <div class="star-txt">
      <p class="eyebrow eyebrow--light">Nuestro sello · uñas</p>
      <h2 id="t-star" class="h2">Uñas pintadas a mano, una a una</h2>
      <p class="lead lead--light">Manicura tradicional y semipermanente, refuerzo con acrygel y nail art a mano alzada: líneas, flores, leopardo, flúor o glitter. Cada clienta sale con unas uñas que son solo suyas.</p>
      <ul class="ticks ticks--light">
        <li>{ico('check')}<span>Cutícula, limado y forma con todo el cuidado.</span></li>
        <li>{ico('check')}<span>Semipermanente y acrygel para uñas fuertes y brillo de semanas.</span></li>
        <li>{ico('check')}<span>Diseños de temporada que cambian cada mes.</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn-rose" href="nail-art.html">Ver nail art {ico('flecha')}</a><a class="btn btn-ghost-light" href="manicura.html">Manicura</a><a class="btn btn-ghost-light" href="acrygel.html">Acrygel</a></div>
    </div>
    <div class="mosaic" data-gallery>{mos}</div>
  </div>
</section>

{seccion_reels()}

<section class="section mirada" aria-labelledby="t-mir">
  <div class="wrap split split--rev">
    <div class="split-media reveal">
      <div class="ba">
        <img src="{foto('lifting-4')}" alt="Antes y después de un lifting de pestañas" loading="lazy">
        <span class="ba-tag ba-tag--a">Antes</span><span class="ba-tag ba-tag--b">Después</span>
      </div>
    </div>
    <div class="split-txt prose">
      <p class="eyebrow">Mirada</p>
      <h2 id="t-mir" class="h2">Si bajas la mirada, que sea solo para lucir tus pestañas</h2>
      <p>El ojo de nuestro logo no está ahí por casualidad. Lifting y tinte de pestañas, diseño de cejas y microblading pelo a pelo: tratamientos que abren la mirada y se notan desde el primer día, con resultados totalmente naturales.</p>
      <div class="mini-cards">
        <a href="lifting-pestanas.html" class="mini-card"><img src="{foto('lifting-1', True)}" alt="" loading="lazy"><span><strong>Lifting y tinte</strong><small>Efecto rímel durante semanas</small></span></a>
        <a href="microblading.html" class="mini-card"><img src="{foto('microblading-2', True)}" alt="" loading="lazy"><span><strong>Microblading</strong><small>Cejas pelo a pelo</small></span></a>
        <a href="cejas.html" class="mini-card"><img src="{foto('microblading-3', True)}" alt="" loading="lazy"><span><strong>Diseño de cejas</strong><small>La forma que te favorece</small></span></a>
      </div>
    </div>
  </div>
</section>

{comparador("microblading", "Cejas que cambian una mirada", "Microblading pelo a pelo: desliza sobre cada foto para comparar el antes y el después de clientas reales.")}

<section class="section section--bone" id="servicios" aria-labelledby="t-serv">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div><p class="eyebrow">Qué hacemos</p><h2 id="t-serv" class="h2">Estética integral y decorativa</h2>
      <p class="lead">Trece servicios en un mismo salón, con el mismo cariño en cada uno.</p></div>
      <div class="filters" role="tablist" data-filter>
        <button class="filter is-on" data-f="all">Todos</button>
        {''.join(f'<button class="filter" data-f="{k}">{v[0]}</button>' for k, v in CATEGORIAS.items())}
      </div>
    </div>
    <div class="cards" data-cards>{cards}</div>
  </div>
</section>

<section class="section quiz" aria-labelledby="t-quiz">
  <div class="wrap">
    <div class="sec-head center"><p class="eyebrow">Test rápido</p><h2 id="t-quiz" class="h2">¿Qué te apetece hoy?</h2>
    <p class="lead">Toca lo que más se parezca a tu caso y te sugerimos por dónde empezar.</p></div>
    <div class="chips chips--center" data-quizbox>{quiz}</div>
    <div class="quiz-out" data-quiz-out aria-live="polite"></div>
    {quiz_cards}
  </div>
</section>

<section class="section section--blush centro" aria-labelledby="t-centro">
  <div class="wrap split">
    <div class="split-media reveal">
      <div class="duo">
        <img src="{foto('local-pared-mirada')}" alt="Interior del centro con el logo en la pared y el expositor de esmaltes" loading="lazy" class="duo-a">
        <img src="{foto('local-fachada', True)}" alt="Fachada de Estética Verónica Benítez en la calle Cruz" loading="lazy" class="duo-b">
      </div>
    </div>
    <div class="split-txt prose">
      <p class="eyebrow">El centro</p>
      <h2 id="t-centro" class="h2">Pequeñito, acogedor y pensado para ti</h2>
      <p>En la calle Cruz, a dos pasos de José Fariña, nos espera un salón luminoso con el logo en la pared, una pared entera de esmaltes de colores y carteles con frases que nos representan. Un espacio cercano en el que muchas clientas llevan años sintiéndose como en casa.</p>
      <ul class="ticks">
        <li>{ico('acceso')}<span>Acceso totalmente adaptado para sillas de ruedas.</span></li>
        <li>{ico('bano')}<span>Baño de uso neutro.</span></li>
        <li>{ico('persona')}<span>Centro unisex: atendemos a todas las personas.</span></li>
        <li>{ico('calendario')}<span>Trabajamos con cita previa para dedicarte el tiempo que mereces.</span></li>
      </ul>
      <a class="btn btn-ink" href="el-centro.html">Conoce el centro {ico('flecha')}</a>
    </div>
  </div>
</section>

<section class="gift-band" aria-labelledby="t-gift">
  <div class="wrap gift-in">
    <div class="gift-card reveal" aria-hidden="true">
      <img src="assets/img/brand/logo-tinta.svg" alt="">
      <span>Tarjeta regalo</span>
    </div>
    <div>
      <p class="eyebrow eyebrow--light">{ico('regalo')} Tarjeta regalo</p>
      <h2 id="t-gift" class="h2">Regala un ratito para ella</h2>
      <p class="lead lead--light">Una manicura con parafina, un lifting de pestañas, un vale de microblading… Para el Día de la Madre, un cumpleaños o porque sí. También a distancia con Bizum, PayPal o transferencia.</p>
      <a class="btn btn-rose" href="tarjeta-regalo.html">Ver tarjetas regalo {ico('flecha')}</a>
    </div>
  </div>
</section>

<section class="section strip-sec" aria-labelledby="t-strip">
  <div class="wrap sec-head sec-head--row">
    <div><p class="eyebrow">@verobenitezc</p><h2 id="t-strip" class="h2">Recién salidas de cabina</h2></div>
    <div class="btn-row"><a class="btn btn-outline" href="galeria.html">Galería</a><a class="btn btn-ink" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} Síguenos</a></div>
  </div>
  <div class="cross" aria-hidden="true">
    <div class="strip strip--a"><div class="strip-track">{strip}{strip}</div></div>
    <div class="cross-words"><div class="cross-track">{palabras}{palabras}{palabras}{palabras}</div></div>
    <div class="strip strip--b"><div class="strip-track">{strip2}{strip2}</div></div>
  </div>
</section>

{carrusel_resenas()}

<section class="section" aria-labelledby="t-faqh">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Antes de venir</p><h2 id="t-faqh" class="h2">Preguntas frecuentes</h2>
    <p class="lead">Todo lo práctico: cita, horario, pagos y accesibilidad.</p></div>
    <div class="faqs">{faq_list(FAQ_GENERAL)}</div>
  </div>
</section>

{bloque_visita()}
{cta_final()}"""
    return pagina("index.html", "Estética Verónica Benítez · Uñas, pestañas, cejas y depilación en Huelva",
                  "Salón de estética en Huelva (calle Cruz, 8): manicura y pedicura semipermanente, acrygel, nail art, lifting de pestañas, microblading, depilación con cera y láser de diodo, faciales y maquillaje. 5,0 ★ en Google.",
                  "inicio", cuerpo, jsonld=JSONLD_NEGOCIO)


# ------------------------------------------------------------------ servicios
def pagina_servicios():
    h_ = hero("servicios", "Carta de servicios", "Todo lo que podemos hacer por ti",
              "Manos y pies, mirada, depilación, cabina y maquillaje. Estética integral y decorativa con trato cercano y personalizado.",
              ctas_cita("¡Hola Vero! Quería información sobre vuestros servicios.", ("Pedir cita", "contacto.html#cita")))
    bloques = ""
    for i, (cat, (titulo, sub)) in enumerate(CATEGORIAS.items()):
        cs = [s for s in SERVICIOS if s["cat"] == cat]
        lista = "".join(f"""
<a class="serv-row reveal" href="{s['slug']}.html">
  <img src="{foto(s['thumb'], True)}" alt="" loading="lazy">
  <span class="serv-row-txt"><strong>{e(s['nombre'])}{' <em class="tag">Favorito</em>' if s.get('estrella') else ''}</strong><span>{e(s['intro'])}</span></span>
  <span class="serv-row-go">{ico('flecha')}</span>
</a>""" for s in cs)
        bloques += f"""
<section class="section{' section--bone' if i % 2 else ''}" id="{cat}" aria-labelledby="t-{cat}">
  <div class="wrap serv-cat">
    <div class="serv-cat-head"><p class="eyebrow">{len(cs)} {'servicio' if len(cs) == 1 else 'servicios'}</p><h2 id="t-{cat}" class="h2">{e(titulo)}</h2><p class="lead">{e(sub)}</p></div>
    <div class="serv-list">{lista}</div>
  </div>
</section>"""
    extras = f"""
<section class="section section--ink" aria-labelledby="t-extras">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Detalles que importan</p><h2 id="t-extras" class="h2">Cómo trabajamos</h2></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="benefs">
      <div class="benef reveal"><span class="benef-n">{ico('calendario')}</span><h3>Con cita previa</h3><p>Así te dedicamos el tiempo que necesitas, sin esperas ni prisas.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('corazon')}</span><h3>Trato personalizado</h3><p>Te escuchamos y adaptamos cada servicio a ti.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('hoja')}</span><h3>Cosmética profesional</h3><p>Trabajamos con Selvert Thermal en cabina.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('acceso')}</span><h3>Local accesible</h3><p>Acceso adaptado para sillas de ruedas y baño de uso neutro.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('euro')}</span><h3>Pago en efectivo</h3><p>En el centro, los servicios se abonan en efectivo.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('regalo')}</span><h3>Tarjetas regalo</h3><p>Regala cualquier servicio, también a distancia.</p></div>
    </div>
  </div>
</section>"""
    toc = "".join(f'<a href="#{k}">{v[0]}</a>' for k, v in CATEGORIAS.items())
    cuerpo = f"""{h_}
<div class="toc-wrap" data-toc><nav class="toc wrap" aria-label="Categorías">{toc}</nav></div>
{bloques}{extras}{cta_final()}"""
    return pagina("servicios.html", "Servicios · Estética Verónica Benítez · Huelva",
                  "Manicura, pedicura, acrygel, nail art, parafina, lifting de pestañas, cejas, microblading, depilación con cera y láser, faciales, corporales y maquillaje en Huelva.",
                  "servicios", cuerpo)


# ------------------------------------------------------------------ verónica y su equipo
def pagina_equipo():
    h_ = hero("el-centro", "El centro · Quién te cuida", "Verónica y su equipo",
              "Un salón pequeñito con un equipo cercano, detallista y con muchas ganas cada día. Estas son las manos que cuidan de ti.",
              ctas_cita("¡Hola Vero! Me gustaría pedir cita contigo.", ("Conoce el salón", "el-centro.html")))
    v = EQUIPO[0]
    f_v = foto_equipo(v["foto"])
    retrato = (f'<figure class="frame retrato"><img src="{f_v}" alt="{e(v["nombre"])}" loading="lazy"></figure>' if f_v
               else hueco_retrato("Retrato de Verónica") if MODO_DEMO else
               f'<figure class="frame"><img src="{foto("local-pared-mirada")}" alt="" loading="lazy"></figure>')
    pend = '<em class="pendiente">dato pendiente</em>' if MODO_DEMO else ""
    linea = [
        ("La vocación", "Una idea de negocio que nace de la pasión por la profesión: trabajar la estética de cada persona cuidando con esmero cada zona tratada."),
        ("La formación", "Técnica en Estética Integral y Decorativa. Uñas, mirada, depilación, cabina y maquillaje bajo un mismo techo."),
        ("La calle Cruz", f"Abre su salón en el local 8 de la calle Cruz, junto a José Fariña. {pend}"),
        ("Hoy", "Más de 800 trabajos compartidos en Instagram, 5,0 ★ en Google y clientas que llevan casi una década con ella."),
    ]
    tl = "".join(f'<li class="tl-item reveal"><span class="tl-year">{i+1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(linea))
    cards = ""
    for i, m in enumerate(EQUIPO):
        f_m = foto_equipo(m["foto"])
        if not f_m and not MODO_DEMO and i:
            continue
        img = (f'<img src="{f_m}" alt="{e(m["nombre"])}" loading="lazy">' if f_m
               else hueco_retrato("Retrato" if i == 0 else "Foto de tu compañera"))
        nombre = m["nombre"] or ('Nombre de tu compañera' if MODO_DEMO else '')
        tags = "".join(f"<span>{e(t)}</span>" for t in m["tags"]) or ('<span class="pendiente">Especialidades pendientes</span>' if MODO_DEMO else "")
        cards += f"""
<article class="team-card reveal">
  <div class="team-img">{img}</div>
  <div class="team-body"><p class="card-cat">{e(m['puesto'])}</p><h3{' class="is-pend"' if not m['nombre'] else ''}>{e(nombre)}</h3>
  <p>{e(m['texto'])}</p><div class="team-tags">{tags}</div></div>
</article>"""
    guia = f"""
<details class="guia guia--retrato">
  <summary><span class="guia-ico">{ico('persona')}</span><span><strong>Verónica: así hacemos las fotos del equipo</strong>
  <small>Una foto real de quien atiende genera muchísima confianza. Toca para ver cómo hacerlas.</small></span><span class="faq-ico">{ico('mas')}</span></summary>
  <div class="guia-in"><ol class="guia-pasos">
    <li><b>En el salón, con el logo de la pared detrás</b> o junto a la pared de esmaltes: así se reconoce el centro.</li>
    <li><b>Luz natural de frente</b> (cerca de la puerta o el escaparate), nunca a contraluz.</li>
    <li><b>En vertical</b>, de cintura para arriba, con la ropa de trabajo y una sonrisa natural.</li>
    <li><b>Una foto trabajando</b> (haciendo una manicura o diseñando unas cejas) y otra de todo el equipo junto.</li>
    <li><b>Envíalas como «documento» por WhatsApp</b> con el nombre y las especialidades de cada una.</li>
  </ol><p class="guia-nota">{ico('check')} Cada persona debe estar de acuerdo en aparecer en la web.</p></div>
</details>""" if MODO_DEMO else ""
    resenas = "".join(resena_card(i) for i in (2, 4, 14))
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-vero">
  <div class="wrap split">
    <div class="split-media reveal">{retrato}</div>
    <div class="split-txt prose">
      <p class="eyebrow">La fundadora</p>
      <h2 id="t-vero" class="h2">{e(v['nombre'])}</h2>
      <p class="sign">{e(v['puesto'])}</p>
      <p>Verónica es técnica en estética integral y decorativa, y el alma de este salón «pequeñito pero muy acogedor» de la calle Cruz. Su idea fue siempre la misma: ofrecer cada servicio con el máximo esfuerzo, profesionalidad y muchas ganas, con un trato cercano y personalizado.</p>
      <p>Las clientas la llaman Vero. Muchas llevan años con ella —«llevo 9 años con Vero y no hay otro sitio mejor», escribe una— y vuelven por lo mismo: la amabilidad, el cuidado extremo de cada detalle y unas manos que, como dicen otras, «son unas artistas».</p>
      <blockquote class="pull">Ponemos el máximo esfuerzo, profesionalidad y muchas ganas cada día.</blockquote>
      <div class="team-tags">{''.join(f'<span>{e(t)}</span>' for t in v['tags'])}</div>
    </div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-tray">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Trayectoria</p><h2 id="t-tray" class="h2">De la vocación al salón</h2></div>
    <ol class="timeline">{tl}</ol>
  </div>
</section>
<section class="section" aria-labelledby="t-team">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">«Las chicas»</p><h2 id="t-team" class="h2">El equipo</h2>
    <p class="lead">Así nos llaman en las reseñas. Un equipo pequeño en el que cada clienta es conocida por su nombre.</p></div>
    <div class="team">{cards}</div>
    {guia}
  </div>
</section>
<section class="section section--ink salon-vid" aria-labelledby="t-dia">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow eyebrow--light">El día a día</p>
      <h2 id="t-dia" class="h2">Manos a la obra</h2>
      <p class="lead lead--light">Uñas recién terminadas, diseños de temporada y nuestras frases en el mostrador. Lo que compartimos cada semana en Instagram.</p>
      <a class="btn btn-ghost-light" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} @verobenitezc</a>
    </div>
    <div class="vid-duo">{video("reel-copos-azul", "vid vid--a reveal")}{video("salon-entrada", "vid vid--b reveal")}</div>
  </div>
</section>
<section class="section section--blush" aria-labelledby="t-dicen">
  <div class="wrap">
    <div class="sec-head center"><p class="eyebrow">Lo que dicen de ellas</p><h2 id="t-dicen" class="h2">«Vero» y «las chicas»</h2></div>
    <div class="review-wall review-wall--3">{resenas}</div>
  </div>
</section>
{cta_final('¿Te ponemos guapa?', 'Escríbenos y reservamos tu cita con Verónica y su equipo.')}"""
    return pagina("nosotras.html", "Verónica y su equipo · Estética Verónica Benítez · Huelva",
                  "Conoce a Verónica Benítez, técnica en estética integral y decorativa, y al equipo de su salón en la calle Cruz de Huelva.",
                  "centro", cuerpo)


# ------------------------------------------------------------------ el centro
def pagina_centro():
    h_ = hero("el-centro", "El centro · Nuestro salón", "Pequeñito pero muy acogedor",
              "Un salón de estética integral y decorativa en la calle Cruz de Huelva, donde ofrecemos nuestros servicios con el máximo esfuerzo, profesionalidad y muchas ganas cada día.",
              ctas_cita(MSG, ("Ver trabajos", "galeria.html")))
    valores = [
        ("Trato cercano", "Te conocemos por tu nombre y sabemos cómo te gustan las uñas. Muchas clientas llevan con nosotras casi una década."),
        ("Profesionalidad", "Técnica, formación continua y cuidado extremo en cada detalle, de la cutícula a la última pestaña."),
        ("Personalización", "Cada servicio se adapta a ti: tu piel, tu estilo, tu ritmo y tu ocasión."),
        ("Ganas cada día", "Nos encanta lo que hacemos y se nota: en el resultado y en cómo sales de la cabina."),
        ("Un espacio para todas las personas", "Centro unisex, acceso adaptado y baño de uso neutro."),
        ("Creatividad", "El nail art a mano alzada es nuestro sello: diseños nuevos cada temporada."),
    ]
    val = "".join(f'<div class="benef reveal"><span class="benef-n">{i+1:02d}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(valores))
    frases = "".join(f'<figure class="quote-card reveal">{ojo()}<blockquote>{e(f)}</blockquote><figcaption>Cartel de nuestro mostrador</figcaption></figure>' for f in FRASES)
    fotos = [("local-fachada", "La fachada en la calle Cruz"), ("local-pared-mirada", "El logo en la pared y la pared de esmaltes"),
             ("local-mostrador", "Mostrador con cosmética y tarjetas regalo"),
             ("selvert-mascara-led", "Cosmética Selvert Thermal en cabina"), ("unas-placa-logo", "Nuestras placas con el logo, en cada foto")]
    gal = "".join(f'<figure class="m-item"><button data-lb="{foto(g)}" aria-label="Ampliar · {e(t)}"><img src="{foto(g, True)}" alt="{e(t)}" loading="lazy"><span>{e(t)}</span></button></figure>' for g, t in fotos)
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-hist">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">Quiénes somos</p>
      <h2 id="t-hist" class="h2">Estética integral y decorativa, con alma de barrio</h2>
      <p>Detrás de Estética Verónica Benítez está Verónica, técnica en estética integral y decorativa, y un pequeño equipo al que las clientas llaman con cariño «las chicas». Una idea de negocio que nació de la pasión por la profesión y que, año tras año, se ha ganado la confianza de Huelva a base de trabajo bien hecho.</p>
      <p>Nuestro enfoque es sencillo: trabajar la estética de cada persona cuidando con esmero cada zona tratada. Escuchamos, aconsejamos y adaptamos cada servicio, porque no hay dos manos, dos miradas ni dos pieles iguales.</p>
      <p>Las reseñas lo resumen mejor que nosotras: «llevo 9 años con Vero y no hay otro sitio mejor», «son unas artistas», «te sientes muy a gusto en el local».</p>
      <blockquote class="pull">Ponemos el máximo esfuerzo, profesionalidad y muchas ganas cada día.</blockquote>
    </div>
    <div class="split-media reveal">
      <div class="duo">
        <img src="{foto('local-pared-mirada')}" alt="Interior del centro" loading="lazy" class="duo-a">
        <img src="{foto('local-fachada', True)}" alt="Fachada del centro" loading="lazy" class="duo-b">
      </div>
    </div>
  </div>
</section>
<section class="section salon-vid" aria-labelledby="t-tour">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">Pasa, estás en tu casa</p>
      <h2 id="t-tour" class="h2">Un paseo por el salón</h2>
      <p>La puerta roja de la calle Cruz, la mesa de manicura siempre en marcha, el logo en la pared y nuestros carteles. Así es un día cualquiera en Estética Verónica Benítez.</p>
      <a class="btn btn-ink" href="nosotras.html">Conoce al equipo {ico('flecha')}</a>
    </div>
    <div class="vid-duo">{video("salon-entrada", "vid vid--a reveal")}{video("salon-frases", "vid vid--b reveal")}</div>
  </div>
</section>
<section class="section section--ink" aria-labelledby="t-val">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Lo que nos mueve</p><h2 id="t-val" class="h2">Nuestros valores</h2></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="benefs">{val}</div>
  </div>
</section>
<section class="section section--blush" aria-labelledby="t-frases">
  <div class="wrap">
    <div class="sec-head center"><p class="eyebrow">En nuestras paredes</p><h2 id="t-frases" class="h2">Frases que nos representan</h2>
    <p class="lead">Están en los carteles del mostrador y en cada tarjeta regalo.</p></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="quotes">{frases}</div>
  </div>
</section>
<section class="section" aria-labelledby="t-fotos">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Un vistazo</p><h2 id="t-fotos" class="h2">Así es el salón</h2></div>
    <div class="masonry masonry--3" data-gallery>{gal}</div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-acc">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Para todas las personas</p><h2 id="t-acc" class="h2">Accesible, cómodo y sin etiquetas</h2></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="benefs benefs--light">
      <div class="benef reveal"><span class="benef-n">{ico('acceso')}</span><h3>Acceso adaptado</h3><p>El local dispone de acceso totalmente adaptado para personas en silla de ruedas.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('bano')}</span><h3>Baño de uso neutro</h3><p>Un baño unisex, para cualquier persona.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('persona')}</span><h3>Centro unisex</h3><p>Depilación, cejas, faciales, manos y pies para mujeres y hombres.</p></div>
    </div>
  </div>
</section>
{carrusel_resenas('Clientas que se han convertido en amigas')}
{cta_final()}"""
    return pagina("el-centro.html", "El centro · Estética Verónica Benítez · Huelva",
                  "Conoce Estética Verónica Benítez: un salón de estética integral y decorativa en la calle Cruz de Huelva, pequeñito pero muy acogedor, accesible y unisex.",
                  "centro", cuerpo)


# ------------------------------------------------------------------ galería
GAL_CATS = {
    "color": ["unas-fucsia", "unas-magenta", "unas-turquesa", "unas-lila", "unas-granate", "unas-petroleo", "unas-azul-marino", "unas-ombre-rojo", "unas-fluor"],
    "arte": ["unas-arte-turquesa", "unas-rayas-pastel", "unas-corazones", "unas-leopardo-rosa", "unas-leopardo", "unas-azul-abstracto",
             "unas-flores-amarillo", "unas-lila-motas", "unas-fucsia-ondas", "unas-verde-rosa", "unas-negro-turquesa", "unas-cebra-coral",
             "unas-celeste-perlas", "unas-pastel-flores", "unas-lima"],
    "elegantes": ["unas-french", "unas-nude-almendra", "unas-pastel-dorado", "unas-marco-dorado", "unas-naranja-marco", "unas-coral-turquesa", "unas-turquesa-nude", "unas-placa-logo"],
    "pies": ["pedicura"],
    "mirada": ["lifting-1", "lifting-2", "lifting-3", "lifting-4", "lifting-5", "microblading-1", "microblading-2", "microblading-3"],
    "centro": ["local-fachada", "local-pared-mirada", "local-mostrador", "selvert-mascara-led"],
}
GAL_NOMBRES = {"color": "Color liso", "arte": "Nail art", "elegantes": "Elegantes", "pies": "Pedicura", "mirada": "Pestañas y cejas", "centro": "El centro"}


def pagina_galeria():
    h_ = hero("galeria", "El centro · Trabajos reales", "Galería: recién salidas de cabina",
              "Uñas a todo color, nail art, francesas, lifting de pestañas y microblading. Fotos reales de clientas, publicadas en Instagram.",
              ctas_cita("¡Hola Vero! He visto la galería y me encanta. ¿Me das cita?", ("Ver servicios", "servicios.html")))
    filtros = '<button class="filter is-on" data-f="all">Todo</button>' + "".join(
        f'<button class="filter" data-f="{k}">{v}</button>' for k, v in GAL_NOMBRES.items())
    items = ""
    orden = [(k, g) for k, lista in GAL_CATS.items() for g in lista]
    # mezcla suave para que «Todo» no quede por bloques
    mezcla = orden[0::3] + orden[1::3] + orden[2::3]
    for k, g in mezcla:
        items += f'<figure class="m-item" data-cat="{k}"><button data-lb="{foto(g)}" aria-label="Ampliar · {GAL_NOMBRES[k]}"><img src="{foto(g, True)}" alt="{GAL_NOMBRES[k]} · Estética Verónica Benítez" loading="lazy"><span>{GAL_NOMBRES[k]}</span></button></figure>'
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-gal">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="eyebrow">{len(orden)} trabajos seleccionados</p><h2 id="t-gal" class="h2">Filtra por estilo</h2></div>
    <div class="filters" data-filter data-target="[data-masonry]">{filtros}</div></div>
    <div class="masonry" data-masonry data-gallery>{items}</div>
    <p class="center mt-l"><a class="btn btn-ink" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} Más de 800 publicaciones en @verobenitezc</a></p>
  </div>
</section>
{cta_final('¿Quieres ser la siguiente?')}"""
    return pagina("galeria.html", "Galería de trabajos · Estética Verónica Benítez · Huelva",
                  "Galería de trabajos reales: uñas semipermanentes, acrygel, nail art a mano alzada, pedicura, lifting de pestañas y microblading en Huelva.",
                  "centro", cuerpo)


# ------------------------------------------------------------------ opiniones
def pagina_opiniones():
    h_ = hero("opiniones", "El centro · Opiniones", "5,0 ★ y clientas de toda la vida",
              "Reseñas reales de Google y Facebook. Lo que más se repite: profesionalidad, amabilidad y el cuidado extremo que dedicamos a cada detalle.",
              ctas_cita("¡Hola Vero! He leído las opiniones y me gustaría pedir cita."))
    muro = "".join(resena_card(i) for i in range(len(RESENAS)))
    barras = "".join(f'<div class="bar"><span>{n} ★</span><i style="--w:{w}%"></i></div>' for n, w in [(5, 100), (4, 0), (3, 0), (2, 0), (1, 0)])
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-op">
  <div class="wrap rating-grid">
    <div class="rating-box reveal">
      <strong class="rating-big">5,0</strong>{estrellas()}
      <p>30 reseñas en Google</p>
      <div class="bars">{barras}</div>
      <p class="muted small">Y un 96 % de recomendación en Facebook, con 23 opiniones.</p>
      <a class="btn btn-outline btn-sm" href="{N['maps']}" target="_blank" rel="noopener">Ver en Google Maps</a>
    </div>
    <div class="prose">
      <p class="eyebrow">Lo que más se repite</p>
      <h2 id="t-op" class="h2">Profesionales, amables y detallistas</h2>
      <div class="kw">
        <span>«Muy profesionales»</span><span>«Cuidan mucho al cliente»</span><span>«Son unas artistas»</span>
        <span>«Llevo años con ellas»</span><span>«Da gusto ir»</span><span>«Buenos precios»</span><span>«Te sientes muy a gusto»</span>
      </div>
      <p>Nuestras clientas coinciden: llevan años viniendo para hacerse las uñas y las cejas por la amabilidad del equipo, la profesionalidad y el cuidado extremo que dedicamos a cada detalle para que te sientas cómoda.</p>
    </div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-muro">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Muro de opiniones</p><h2 id="t-muro" class="h2">En sus propias palabras</h2></div>
    <div class="review-wall">{muro}</div>
  </div>
</section>
<section class="section center" aria-labelledby="t-tu">
  <div class="wrap">
    {ojo()}
    <p class="eyebrow">¿Ya nos conoces?</p>
    <h2 id="t-tu" class="h2">Cuéntanos qué tal tu experiencia</h2>
    <p class="lead">Tu opinión ayuda a otras personas de Huelva a encontrarnos.</p>
    <div class="btn-row center"><a class="btn btn-ink" href="{N['maps']}" target="_blank" rel="noopener">{estrellas()} Dejar reseña en Google</a></div>
  </div>
</section>
{cta_final()}"""
    return pagina("opiniones.html", "Opiniones · 5,0 ★ en Google · Estética Verónica Benítez",
                  "Opiniones reales de Estética Verónica Benítez en Huelva: 5,0 ★ en Google con 30 reseñas y 96 % de recomendación en Facebook.",
                  "centro", cuerpo)


# ------------------------------------------------------------------ tarjeta regalo
def pagina_regalo():
    h_ = hero("regalo", "El centro · Tarjeta regalo", "Regala un ratito para ella",
              "Cualquier servicio de nuestra carta puede convertirse en un regalo: una manicura con parafina, un lifting de pestañas, una limpieza de cutis o un vale de microblading.",
              ctas_cita("¡Hola Vero! Me gustaría regalar una tarjeta regalo.", ("Cómo funciona", "#como")))
    ideas = [
        ("unas-pastel-dorado", "Manos de diez", "Manicura semipermanente con baño de parafina.", "manicura"),
        ("lifting-4", "Mirada de película", "Lifting y tinte de pestañas.", "lifting-pestanas"),
        ("microblading-2", "Vale de microblading", "Cejas pelo a pelo para siempre arregladas.", "microblading"),
        ("selvert-mascara-led", "Piel luminosa", "Limpieza de cutis con cosmética Selvert Thermal.", "tratamientos-faciales"),
        ("pedicura", "Pies de verano", "Pedicura semipermanente con parafina.", "pedicura"),
        ("unas-arte-turquesa", "Capricho de nail art", "Uñas decoradas a mano alzada.", "nail-art"),
    ]
    cards = "".join(f"""
<article class="gift-idea reveal">
  <img src="{foto(f, True)}" alt="" loading="lazy">
  <div><h3>{e(t)}</h3><p>{e(d)}</p>
  <a class="opt-link" href="{wa(f'¡Hola Vero! Me gustaría regalar una tarjeta regalo de: {t} ({d})')}" target="_blank" rel="noopener">{ico('regalo')} Regalar esto</a>
  <a class="link" href="{s}.html">Ver servicio {ico('flecha')}</a></div>
</article>""" for f, t, d, s in ideas)
    pasos = [
        ("Elige el regalo", "Un servicio concreto, una combinación o un importe para que ella elija."),
        ("Escríbenos", "Por WhatsApp o en persona. Te ayudamos a escoger si dudas."),
        ("Paga como prefieras", "En el centro, en efectivo. A distancia, por Bizum, PayPal o transferencia: te pasamos los datos por WhatsApp."),
        ("Entrega", "Recoge la tarjeta impresa en el centro o recíbela en formato digital para enviarla."),
    ]
    p = "".join(f'<li class="step reveal"><span class="step-n">{i+1}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>' for i, (a, b) in enumerate(pasos))
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-ideas">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Ideas para regalar</p><h2 id="t-ideas" class="h2">Seis regalos que siempre aciertan</h2>
    <p class="lead">Perfectos para el Día de la Madre, cumpleaños, aniversarios, Navidad o para darle las gracias a alguien especial.</p></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="gift-ideas">{cards}</div>
  </div>
</section>
<section class="section section--blush" id="como" aria-labelledby="t-como">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Cómo funciona</p>
      <h2 id="t-como" class="h2">Regalar es muy fácil</h2>
      <ol class="steps">{p}</ol>
      <div class="btn-row"><a class="btn btn-rose" href="{wa('¡Hola Vero! Me gustaría regalar una tarjeta regalo.')}" target="_blank" rel="noopener">{ico('wa')} Pedir mi tarjeta regalo</a></div>
    </div>
    <div class="split-media reveal">
      <figure class="frame frame--wide"><img src="{foto('tarjeta-regalo')}" alt="Ejemplo de tarjeta regalo de Estética Verónica Benítez" loading="lazy"></figure>
      <p class="muted small mt">Una de nuestras tarjetas regalo para el Día de la Madre: «Vale por microblading».</p>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="t-faqr">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Dudas</p><h2 id="t-faqr" class="h2">Preguntas sobre la tarjeta regalo</h2></div>
    <div class="faqs">{faq_list([
        ("¿Puedo regalar un importe en lugar de un servicio?", "Sí. Así la persona elige lo que más le apetezca de nuestra carta."),
        ("¿Puedo comprarla sin ir al centro?", "Sí. Pagas por Bizum, PayPal o transferencia y te la enviamos en formato digital. Los datos de pago te los facilitamos por WhatsApp."),
        ("¿Cómo canjea la tarjeta la persona que la recibe?", "Solo tiene que escribirnos por WhatsApp o llamarnos para reservar su cita y traerla (o enseñarla en el móvil)."),
        ("¿Se puede personalizar?", "Claro: dinos el nombre y un mensaje y lo incluimos en la tarjeta."),
    ])}</div>
  </div>
</section>
{cta_final('Un regalo que se nota', 'Escríbenos y preparamos juntas el regalo perfecto.', '¡Hola Vero! Me gustaría regalar una tarjeta regalo.')}"""
    return pagina("tarjeta-regalo.html", "Tarjeta regalo · Estética Verónica Benítez · Huelva",
                  "Regala belleza en Huelva: tarjetas regalo de manicura, pedicura, lifting de pestañas, microblading, faciales y más. También a distancia por Bizum, PayPal o transferencia.",
                  "centro", cuerpo)


# ------------------------------------------------------------------ ubicación
def pagina_ubicacion():
    h_ = hero("ubicacion", "Cómo llegar", "En la calle Cruz, junto a José Fariña",
              "Calle Cruz, local 8 · 21006 Huelva. Es la segunda calle transversal de la calle José Fariña. Acceso adaptado a pie de calle.",
              f'<a class="btn btn-rose" href="{N["maps_dir"]}" target="_blank" rel="noopener">{ico("ruta")} Abrir ruta en Google Maps</a>'
              f'<a class="btn btn-ghost-light" href="tel:{N["movil_href"]}">{ico("tel")} {N["movil"]}</a>')
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-dir">
  <div class="wrap visit-grid">
    <div class="visit-info">
      <p class="eyebrow">Dirección</p>
      <h2 id="t-dir" class="h2">Calle Cruz, local 8</h2>
      <address class="addr">Estética Verónica Benítez<br>{e(N['direccion'])}<br>{N['cp']} {N['ciudad']}</address>
      <ul class="info-list">
        <li>{ico('ruta')}<span><strong>Referencia</strong><br>Segunda calle transversal de la calle José Fariña.</span></li>
        <li>{ico('pin')}<span><strong>Código plus</strong><br>{N['plus']}</span></li>
        <li>{ico('acceso')}<span><strong>Accesible</strong><br>Acceso totalmente adaptado para sillas de ruedas.</span></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-ink" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('ruta')} Cómo llegar</a>
        <button class="btn btn-outline" data-copy="{e(N['direccion'])}, {N['cp']} {N['ciudad']}">Copiar dirección</button>
      </div>
    </div>
    {mapa()}
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-como">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Llegar es fácil</p><h2 id="t-como" class="h2">Elige cómo venir</h2></div>
    <p class="swipe-hint">Desliza {ico('flecha')}</p><div class="opts">
      <article class="opt reveal"><h3>{ico('persona')} Andando</h3><p>Desde la avenida José Fariña, toma la segunda calle transversal: es la calle Cruz. Busca el letrero blanco con el ojo y las pestañas.</p></article>
      <article class="opt reveal"><h3>{ico('ruta')} En coche</h3><p>Usa el botón «Cómo llegar» y Google Maps te guiará hasta la puerta. Te recomendamos venir con unos minutos de margen para aparcar.</p></article>
      <article class="opt reveal"><h3>{ico('acceso')} Accesible</h3><p>El acceso está totalmente adaptado para sillas de ruedas y dentro tenemos un baño de uso neutro.</p></article>
      <article class="opt reveal"><h3>{ico('wa')} ¿Te pierdes?</h3><p>Escríbenos por WhatsApp al {N['movil']} o llama al {N['tel_fijo']} y te guiamos.</p></article>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="t-hor">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Cuándo venir</p>
      <h2 id="t-hor" class="h2">Horario, siempre con cita previa</h2>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <p class="muted">En festivos y vacaciones avisamos de los horarios especiales en Instagram y Facebook.</p>
    </div>
    <div class="split-media reveal"><figure class="frame"><img src="{foto('local-fachada')}" alt="Fachada de Estética Verónica Benítez en la calle Cruz" loading="lazy"></figure></div>
  </div>
</section>
{cta_final('¿Te esperamos?')}"""
    return pagina("ubicacion.html", "Cómo llegar · Estética Verónica Benítez · Calle Cruz, Huelva",
                  "Dirección, mapa, horario y cómo llegar a Estética Verónica Benítez: calle Cruz, local 8, 21006 Huelva, segunda transversal de José Fariña.",
                  "ubicacion", cuerpo, jsonld=JSONLD_NEGOCIO)


# ------------------------------------------------------------------ contacto
def pagina_contacto():
    h_ = hero("contacto", "Contacto y cita", "Hablemos de ti",
              "La forma más rápida de pedir cita es por WhatsApp. Cuéntanos qué te apetece y te respondemos en cuanto terminemos con la clienta que está en cabina.",
              ctas_cita(MSG, ("Reserva guiada", "#cita")))
    canales = f"""
<div class="channels">
  <a class="channel reveal" href="{wa(MSG)}" target="_blank" rel="noopener">{ico('wa')}<strong>WhatsApp</strong><span>{N['movil']}</span><small>Citas y consultas</small></a>
  <a class="channel reveal" href="tel:{N['movil_href']}">{ico('tel')}<strong>Móvil</strong><span>{N['movil']}</span><small>Llamadas y reservas</small></a>
  <a class="channel reveal" href="tel:{N['tel_fijo_href']}">{ico('tel')}<strong>Teléfono fijo</strong><span>{N['tel_fijo']}</span><small>En horario de apertura</small></a>
  <a class="channel reveal" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')}<strong>Instagram</strong><span>@verobenitezc</span><small>Trabajos y novedades</small></a>
  <a class="channel reveal" href="{N['facebook']}" target="_blank" rel="noopener">{ico('fb')}<strong>Facebook</strong><span>Estética Verónica Benítez</span><small>Avisos y sorteos</small></a>
  <a class="channel reveal" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')}<strong>Visítanos</strong><span>Calle Cruz, local 8</span><small>Huelva</small></a>
</div>"""
    cuerpo = f"""{h_}
<section class="section" aria-labelledby="t-can">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Canales</p><h2 id="t-can" class="h2">Elige cómo hablar con nosotras</h2></div>
    {canales}
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-cita">
  <div class="wrap wizard-wrap">
    <div class="wizard-side">
      <p class="eyebrow">Reserva</p>
      <h2 id="t-cita" class="h2">Tu cita en tres toques</h2>
      <p class="lead">Elige servicio, días y franja. Te confirmamos el hueco por WhatsApp.</p>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
    </div>
    {asistente()}
  </div>
</section>
<section class="section" aria-labelledby="t-faqc">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Dudas</p><h2 id="t-faqc" class="h2">Preguntas frecuentes</h2></div>
    <div class="faqs">{faq_list(FAQ_GENERAL)}</div>
  </div>
</section>
{bloque_visita('Te esperamos en la calle Cruz')}"""
    return pagina("contacto.html", "Contacto y cita · Estética Verónica Benítez · Huelva",
                  "Pide cita en Estética Verónica Benítez por WhatsApp (679 90 18 66) o teléfono (959 04 17 00). Calle Cruz, local 8, Huelva.",
                  "contacto", cuerpo, jsonld=JSONLD_NEGOCIO)


def pagina_404():
    cuerpo = f"""
<section class="section notfound">
  <div class="wrap center">
    <img src="assets/img/brand/logo-tinta.svg" alt="" class="nf-logo">
    <h1 class="h2">Esta página se ha ido a hacerse las uñas</h1>
    <p class="lead">No la encontramos, pero todo lo demás sigue en su sitio.</p>
    <div class="btn-row center"><a class="btn btn-ink" href="index.html">Volver al inicio</a><a class="btn btn-outline" href="servicios.html">Ver servicios</a></div>
  </div>
</section>"""
    return pagina("404.html", "Página no encontrada · Estética Verónica Benítez", "Página no encontrada.", "", cuerpo)


if __name__ == "__main__":
    hechas = [pagina_inicio(), pagina_servicios()]
    hechas += [pagina_servicio(s) for s in SERVICIOS]
    hechas += [pagina_equipo(), pagina_centro(), pagina_galeria(), pagina_opiniones(), pagina_regalo(), pagina_ubicacion(), pagina_contacto(), pagina_404()]
    print(f"{len(hechas)} páginas generadas")
