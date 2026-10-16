"""Vectoriza el logotipo original a SVG, separando sus piezas.

Lee:  Logotipo de estética Verónica Benítez.png
Crea: assets/img/brand/logo.svg            (logo completo, con marco)
      assets/img/brand/logo-sin-marco.svg  (arco + ojo + ESTÉTICA)
      assets/img/brand/ojo.svg             (solo el ojo)
      scripts/_logo_partes.json            (piezas para incrustar y animar)

El trazo sale del propio archivo del cliente (vtracer, modo binario): no se
redibuja nada. Cada pieza va en su grupo para poder animarla (parpadeo).

    python scripts/logo_svg.py
"""
import json
import re
import tempfile
from collections import deque
from pathlib import Path

import numpy as np
import vtracer
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Logotipo de estética Verónica Benítez.png"
OUT = ROOT / "assets" / "img" / "brand"
OJO = (340, 410, 910, 800)  # zona del ojo (x0, y0, x1, y1) en el PNG original


def componentes(mask):
    """Etiqueta componentes conexos (8-vecindad) sin SciPy."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1
        lab[y0, x0] = n
        q = deque([(y0, x0)])
        while q:
            y, x = q.popleft()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        q.append((yy, xx))
    return lab, n


def vectoriza(mask):
    """Devuelve los <path> de vtracer para una máscara booleana."""
    img = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8)).convert("RGB")
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "m.png", Path(d) / "m.svg"
        img.save(src)
        vtracer.convert_image_to_svg_py(str(src), str(dst), colormode="binary", mode="spline",
                                        filter_speckle=4, corner_threshold=60, length_threshold=4.0,
                                        splice_threshold=45, path_precision=2)
        svg = dst.read_text()
    paths = re.findall(r"<path[^>]*/>", svg)
    out = []
    for p in paths:
        d_ = re.search(r'd="([^"]+)"', p).group(1)
        tr = re.search(r'transform="([^"]+)"', p)
        out.append(f'<path d="{d_}"{f" transform=\"{tr.group(1)}\"" if tr else ""}/>')
    return "".join(out)


def main():
    g = np.array(Image.open(SRC).convert("L"))
    mask = g < 128
    lab, n = componentes(mask)
    h, w = mask.shape
    marco = np.zeros_like(mask)
    ceja = np.zeros_like(mask); parpado = np.zeros_like(mask); pestanas = np.zeros_like(mask)
    texto = np.zeros_like(mask)
    x0, y0, x1, y1 = OJO
    ojo_partes = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 15:
            continue
        bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
        if bx1 - bx0 > w * 0.85 and by1 - by0 > h * 0.6:
            marco |= lab == i
        elif bx0 >= x0 and bx1 <= x1 and by0 >= y0 and by1 <= y1:
            ojo_partes.append((by0, len(ys), i))
        else:
            texto |= lab == i
    # en el ojo: la ceja es la pieza más alta y grande; el párpado la línea fina;
    # las pestañas, todo lo que queda por debajo
    ojo_partes.sort()
    ceja |= lab == ojo_partes[0][2]
    parpado |= lab == ojo_partes[1][2]
    for _, _, i in ojo_partes[2:]:
        pestanas |= lab == i

    piezas = {k: vectoriza(m) for k, m in
              [("marco", marco), ("texto", texto), ("ceja", ceja), ("parpado", parpado), ("pestanas", pestanas)]}
    ys, xs = np.nonzero(texto | ceja | parpado | pestanas)
    pad = 6
    sin_marco_box = (int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 2 * pad, int(ys.max() - ys.min()) + 2 * pad)
    ys, xs = np.nonzero(ceja | parpado | pestanas)
    ojo_box = (int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 2 * pad, int(ys.max() - ys.min()) + 2 * pad)

    ojo_g = (f'<g class="lg-ceja">{piezas["ceja"]}</g><g class="lg-parpado">{piezas["parpado"]}</g>'
             f'<g class="lg-pestanas">{piezas["pestanas"]}</g>')

    def svg(box, cuerpo, titulo):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, box))}" role="img" '
                f'aria-label="{titulo}" fill="currentColor"><title>{titulo}</title>{cuerpo}</svg>')

    t = "Estética Verónica Benítez"
    (OUT / "logo.svg").write_text(svg((0, 0, w, h), f'<g class="lg-marco">{piezas["marco"]}</g><g class="lg-texto">{piezas["texto"]}</g>{ojo_g}', t), encoding="utf-8")
    (OUT / "logo-sin-marco.svg").write_text(svg(sin_marco_box, f'<g class="lg-texto">{piezas["texto"]}</g>{ojo_g}', t), encoding="utf-8")
    (OUT / "ojo.svg").write_text(svg(ojo_box, ojo_g, t), encoding="utf-8")
    for nombre in ("logo", "logo-sin-marco", "ojo"):
        base = (OUT / f"{nombre}.svg").read_text(encoding="utf-8")
        for sufijo, color in (("claro", "#f6eee4"), ("tinta", "#17110f"), ("rosa", "#c28d76")):
            (OUT / f"{nombre}-{sufijo}.svg").write_text(base.replace('fill="currentColor"', f'fill="{color}"'), encoding="utf-8")
    # PNG sin marco (para la imagen de compartir y los iconos)
    alfa = Image.fromarray(((texto | ceja | parpado | pestanas) * 255).astype(np.uint8))
    bx = sin_marco_box
    alfa = alfa.crop((bx[0], bx[1], bx[0] + bx[2], bx[1] + bx[3]))
    for sufijo, color in (("claro", (246, 238, 228)), ("tinta", (23, 17, 15))):
        im = Image.new("RGBA", alfa.size, color + (255,)); im.putalpha(alfa)
        im.save(OUT / f"logo-sin-marco-{sufijo}.png", optimize=True)
    alfa_o = Image.fromarray(((ceja | parpado | pestanas) * 255).astype(np.uint8))
    bo = ojo_box
    alfa_o = alfa_o.crop((bo[0], bo[1], bo[0] + bo[2], bo[1] + bo[3]))
    im = Image.new("RGBA", alfa_o.size, (246, 238, 228, 255)); im.putalpha(alfa_o); im.save(OUT / "ojo-claro-v.png", optimize=True)
    (ROOT / "scripts" / "_logo_partes.json").write_text(json.dumps(
        {"sin_marco_box": sin_marco_box, "ojo_box": ojo_box, "full_box": [0, 0, w, h], **piezas}), encoding="utf-8")
    print("componentes:", n, "· piezas del ojo:", len(ojo_partes),
          "· tamaños:", {k: len(v) for k, v in piezas.items()})


if __name__ == "__main__":
    main()
