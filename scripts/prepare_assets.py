"""Prepara logo, fotos y cabeceras a partir del material original.

Lee:  _fuentes/instagram/NNN_<codigo>.jpg   (publicaciones de @verobenitezc)
      _fuentes/comercio/*.jpg                 (ficha de Comercio Minorista de Huelva)
      _fuentes/carruseles/lifting-*.png       (diapositivas de carruseles de lifting)
      Logotipo de estética Verónica Benítez.png
Crea: assets/img/brand/*, assets/img/fotos/*.webp, assets/img/hero/*.webp

    python scripts/prepare_assets.py
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_fuentes"
OUT = ROOT / "assets" / "img"

# nombre -> (origen, recorte opcional en proporción 0-1: izq, arriba, der, abajo)
FOTOS = {
    # uñas: manicura, semipermanente, acrygel y nail art
    "unas-placa-logo": ("ig:228", None),
    "unas-verde-rosa": ("ig:5", None),
    "unas-rayas-pastel": ("ig:6", None),
    "unas-turquesa": ("ig:7", None),
    "unas-arte-turquesa": ("ig:8", None),
    "unas-coral-turquesa": ("ig:9", None),
    "unas-leopardo-rosa": ("ig:11", None),
    "unas-negro-turquesa": ("ig:12", None),
    "unas-fucsia-ondas": ("ig:13", None),
    "unas-turquesa-nude": ("ig:16", None),
    "unas-fluor": ("ig:17", None),
    "unas-pastel-dorado": ("ig:18", None),
    "unas-lila-motas": ("ig:19", None),
    "unas-leopardo": ("ig:21", None),
    "unas-corazones": ("ig:22", None),
    "unas-azul-abstracto": ("ig:23", None),
    "unas-flores-amarillo": ("ig:25", None),
    "unas-fucsia": ("ig:26", None),
    "unas-magenta": ("ig:28", None),
    "unas-celeste-perlas": ("ig:101", None),
    "unas-granate": ("ig:103", None),
    "unas-french": ("ig:104", None),
    "unas-marco-dorado": ("ig:108", None),
    "unas-lila": ("ig:113", None),
    "unas-naranja-marco": ("ig:116", None),
    "unas-nude-almendra": ("ig:121", None),
    "unas-petroleo": ("ig:122", None),
    "unas-lima": ("ig:125", None),
    "unas-azul-marino": ("ig:127", None),
    "unas-cebra-coral": ("ig:131", None),
    "unas-ombre-rojo": ("ig:166", None),
    "unas-pastel-flores": ("ig:227", None),
    "pedicura": ("ig:332", (0.0, 0.18, 1.0, 1.0)),
    # mirada
    "lifting-1": ("car:lifting-1.png", None),
    "lifting-2": ("car:lifting-2.png", None),
    "lifting-3": ("car:lifting-3.png", None),
    "lifting-4": ("car:lifting-4.png", None),
    "lifting-5": ("car:lifting-5.png", None),
    "microblading-1": ("com:Esteica_Veronica_2.jpeg", None),
    "microblading-2": ("com:Esteica_Veronica_3.jpeg", None),
    "microblading-3": ("com:Esteica_Veronica_4.jpeg", None),
    # el centro
    "local-fachada": ("com:Esteica_Veronica_1.jpg", (0.0, 0.14, 1.0, 0.85)),
    "local-mostrador": ("com:Esteica_Veronica_11.jpeg", (0.037, 0.019, 0.926, 0.471)),
    "local-pared-mirada": ("com:Esteica_Veronica_11.jpeg", (0.025, 0.481, 0.469, 0.931)),
    "local-pared-unas": ("com:Esteica_Veronica_11.jpeg", (0.482, 0.481, 0.926, 0.931)),
    "selvert-mascara-led": ("com:Esteica_Veronica_9.jpeg", (0.22, 0.0, 1.0, 1.0)),
    "tarjeta-regalo": ("com:Esteica_Veronica_7.jpeg", None),
}

# Cabeceras panorámicas: tríptico de fotos reales
HEROES = {
    "home": ["unas-leopardo", "unas-placa-logo", "unas-pastel-dorado"],
    "servicios": ["unas-celeste-perlas", "lifting-4", "unas-fucsia-ondas"],
    "manicura": ["unas-french", "unas-coral-turquesa", "unas-granate"],
    "pedicura": ["unas-turquesa-nude", "pedicura", "unas-pastel-flores"],
    "acrygel": ["unas-nude-almendra", "unas-ombre-rojo", "unas-magenta"],
    "nail-art": ["unas-rayas-pastel", "unas-arte-turquesa", "unas-corazones"],
    "parafina": ["unas-pastel-dorado", "unas-french", "unas-lila"],
    "lifting": ["lifting-1", "lifting-4", "lifting-2"],
    "cejas": ["microblading-1", "lifting-5", "microblading-3"],
    "microblading": ["microblading-2", "microblading-1", "microblading-3"],
    "depilacion-cera": ["local-pared-unas", "local-mostrador", "local-fachada"],
    "depilacion-laser": ["local-fachada", "selvert-mascara-led", "local-pared-mirada"],
    "faciales": ["local-mostrador", "selvert-mascara-led", "local-pared-unas"],
    "corporales": ["local-fachada", "local-pared-mirada", "local-mostrador"],
    "maquillaje": ["lifting-3", "local-pared-mirada", "lifting-5"],
    "el-centro": ["local-pared-mirada", "local-fachada", "local-pared-unas"],
    "galeria": ["unas-fluor", "unas-leopardo-rosa", "unas-lila-motas"],
    "opiniones": ["unas-marco-dorado", "unas-turquesa", "unas-naranja-marco"],
    "regalo": ["unas-pastel-dorado", "unas-placa-logo", "local-mostrador"],
    "ubicacion": ["local-pared-unas", "local-fachada", "local-pared-mirada"],
    "contacto": ["unas-azul-abstracto", "unas-placa-logo", "unas-cebra-coral"],
}


def ruta(origen):
    tipo, nombre = origen.split(":", 1)
    if tipo == "ig":
        return next((SRC / "instagram").glob(f"{int(nombre):03d}_*.jpg"))
    return SRC / {"com": "comercio", "car": "carruseles"}[tipo] / nombre


def retoca(im):
    im = ImageOps.autocontrast(im, cutoff=0.3, preserve_tone=True)
    im = ImageEnhance.Color(im).enhance(1.04)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=3))


# zonas con marca de agua de la cámara (proporción 0-1) que se difuminan
MARCAS = {"car:lifting-1.png": (0.0, 0.40, 0.07, 0.435), "car:lifting-2.png": (0.0, 0.725, 0.26, 0.775), "car:lifting-3.png": (0.0, 0.365, 0.26, 0.42),
          "car:lifting-4.png": (0.0, 0.385, 0.2, 0.43)}


def carga(nombre):
    origen, rec = FOTOS[nombre]
    im = ImageOps.exif_transpose(Image.open(ruta(origen))).convert("RGB")
    if origen in MARCAS:
        w, h = im.size
        l, t, r, b = MARCAS[origen]
        caja = (int(l * w), int(t * h), int(r * w), int(b * h))
        im.paste(im.crop(caja).filter(ImageFilter.GaussianBlur(14)), caja)
    if rec:
        w, h = im.size
        l, t, r, b = rec
        im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    return im


def guarda(im, destino, q=82):
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, "WEBP", quality=q, method=6)


def fotos():
    for nombre in FOTOS:
        im = retoca(carga(nombre))
        if im.width < 1080:
            f = 1080 / im.width
            im = im.resize((1080, int(im.height * f)), Image.LANCZOS).filter(
                ImageFilter.UnsharpMask(radius=2, percent=40, threshold=2))
        guarda(im, OUT / "fotos" / f"{nombre}.webp")
        sm = im.copy(); sm.thumbnail((640, 900), Image.LANCZOS)
        guarda(sm, OUT / "fotos" / "sm" / f"{nombre}.webp", 78)


def ajusta(im, w, h, c=(0.5, 0.45)):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=c)


def heroes():
    W, H = 1080, 1350
    for nombre, piezas in HEROES.items():
        lienzo = Image.new("RGB", (W * 3, H), (20, 17, 15))
        for i, p in enumerate(piezas):
            lienzo.paste(ajusta(retoca(carga(p)), W, H), (i * W, 0))
        pan = ImageOps.fit(lienzo, (3240, 1380), Image.LANCZOS, centering=(0.5, 0.45))
        guarda(pan, OUT / "hero" / f"{nombre}.webp", 80)
        pm = pan.copy(); pm.thumbnail((1920, 1920), Image.LANCZOS)
        guarda(pm, OUT / "hero" / f"{nombre}-1920.webp", 80)
        movil = ajusta(retoca(carga(piezas[1])), 1080, 1440)
        guarda(movil, OUT / "hero" / f"{nombre}-m.webp", 80)


def og():
    d = OUT / "brand"
    base = Image.new("RGB", (1200, 630), (22, 18, 16))
    hero = ImageOps.fit(Image.open(OUT / "hero" / "home-1920.webp").convert("RGB"), (1200, 630), Image.LANCZOS)
    base = Image.blend(base, hero, 0.34)
    logo = Image.open(d / "logo-claro.png"); logo.thumbnail((520, 440), Image.LANCZOS)
    base.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2), logo)
    base.save(d / "og.jpg", quality=86)


if __name__ == "__main__":
    fotos()
    heroes()
    og()
    print("listo")
