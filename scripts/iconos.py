"""Favicon, iconos de app y la imagen para compartir (WhatsApp, redes).

Requiere haber ejecutado antes scripts/logo_svg.py y scripts/prepare_assets.py.

    python scripts/iconos.py
"""
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "assets" / "img" / "brand"
F = ROOT / "assets" / "img" / "fotos"
TINTA, MARFIL, ROSA = (23, 17, 15), (246, 238, 228), (194, 141, 118)


def fuente(nombres, t):
    for n in nombres:
        p = Path("C:/Windows/Fonts") / n
        if p.exists():
            return ImageFont.truetype(str(p), t)
    return ImageFont.load_default()


def favicon_svg():
    ojo = (B / "ojo.svg").read_text(encoding="utf-8")
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', ojo).group(1).split()]
    cuerpo = re.search(r"</title>(.*)</svg>", ojo, re.S).group(1)
    lado = max(vb[2], vb[3]) * 1.32
    x0, y0 = vb[0] - (lado - vb[2]) / 2, vb[1] - (lado - vb[3]) / 2 + vb[3] * .04
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {lado:.0f} {lado:.0f}">'
           f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{lado:.0f}" height="{lado:.0f}" rx="{lado * .22:.0f}" fill="#17110f"/>'
           f'<g fill="#efc8b4">{cuerpo}</g></svg>')
    (B / "favicon.svg").write_text(svg, encoding="utf-8")


def icono(lado, margen=.2, redondo=False):
    ojo = Image.open(B / "ojo-claro-v.png").convert("RGBA")
    im = Image.new("RGBA", (lado, lado), TINTA + (255,))
    # brillo rosado suave
    glow = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((lado * .1, lado * .05, lado * .9, lado * .85), fill=ROSA + (70,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(lado * .12)))
    o = ojo.copy(); o.thumbnail((int(lado * (1 - 2 * margen)), int(lado * (1 - 2 * margen))), Image.LANCZOS)
    im.alpha_composite(o, ((lado - o.width) // 2, (lado - o.height) // 2 + int(lado * .03)))
    if redondo:
        m = Image.new("L", (lado, lado), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, lado - 1, lado - 1), radius=int(lado * .22), fill=255)
        im.putalpha(m)
    return im


def iconos():
    icono(64, .14, True).save(B / "favicon.png")
    icono(180, .2).convert("RGB").save(B / "apple-touch-icon.png")
    icono(192, .2).convert("RGB").save(B / "icon-192.png")
    icono(512, .22).convert("RGB").save(B / "icon-512.png")
    manifest = {
        "name": "Estética Verónica Benítez", "short_name": "Verónica Benítez",
        "description": "Estética integral y decorativa en Huelva", "lang": "es", "start_url": "./index.html",
        "display": "standalone", "background_color": "#17110f", "theme_color": "#17110f",
        "icons": [{"src": "assets/img/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "assets/img/brand/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def og():
    """1200×630 con todo lo importante en el cuadrado central (WhatsApp recorta a veces en cuadrado)."""
    W, H = 1200, 630
    im = Image.new("RGBA", (W, H), TINTA + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((300, -40, 900, 560), fill=ROSA + (55,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))

    def columnas(fotos_cols, ancho):
        capa = Image.new("RGBA", (ancho, 1150), (0, 0, 0, 0))
        for c, fotos in enumerate(fotos_cols):
            y = -60 + (c % 2) * 170
            for f in fotos:
                ph = ImageOps.fit(Image.open(F / "sm" / f"{f}.webp").convert("RGB"), (230, 288), Image.LANCZOS).convert("RGBA")
                m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 229, 287), 20, fill=255)
                ph.putalpha(m)
                capa.alpha_composite(ph, (12 + c * 248, y)); y += 306
        return capa.rotate(7, resample=Image.BICUBIC)

    def funde(capa, hacia_derecha):
        g = Image.linear_gradient("L").rotate(90 if hacia_derecha else -90).resize(capa.size)
        g = g.point(lambda v: max(0, min(255, int((v - 40) * 1.6))))
        capa.putalpha(ImageChops.multiply(capa.getchannel("A"), g))
        return capa

    izq = funde(columnas([["unas-leopardo", "lifting-4", "unas-celeste-perlas"], ["unas-arte-turquesa", "unas-pastel-dorado", "microblading-2"]], 520), False)
    der = funde(columnas([["unas-fucsia-ondas", "microblading-3", "unas-lila-motas"], ["unas-placa-logo", "lifting-1", "unas-corazones"]], 520), True)
    im.alpha_composite(izq, (-150, -260))
    im.alpha_composite(der, (W - 370, -260))

    logo = Image.open(B / "logo-sin-marco-claro.png").convert("RGBA"); logo.thumbnail((430, 300), Image.LANCZOS)
    im.alpha_composite(logo, ((W - logo.width) // 2, 62))
    d = ImageDraw.Draw(im)
    l1, f1 = "Uñas · Pestañas · Cejas · Depilación", fuente(["georgiai.ttf"], 31)
    w1 = d.textlength(l1, font=f1)
    d.text(((W - w1) / 2, 405), l1, font=f1, fill=(239, 200, 180))
    f2, fs = fuente(["segoeui.ttf", "arial.ttf"], 24), fuente(["seguisym.ttf"], 24)
    partes = [("Calle Cruz, 8 · Huelva   ·   5,0 ", f2, (210, 194, 184)), ("★★★★★", fs, (239, 200, 180)), (" en Google", f2, (210, 194, 184))]
    total = sum(d.textlength(t, font=f) for t, f, _ in partes)
    x = (W - total) / 2
    for t, f, c in partes:
        d.text((x, 462), t, font=f, fill=c); x += d.textlength(t, font=f)
    d.rounded_rectangle((W / 2 - 90, 520, W / 2 + 90, 523), 2, fill=ROSA)
    im.convert("RGB").save(B / "og.jpg", quality=88)


if __name__ == "__main__":
    favicon_svg()
    iconos()
    og()
    print("iconos listos")
