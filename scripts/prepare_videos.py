"""Recorta y comprime los reels de @verobenitezc para usarlos en bucle.

Lee:  _fuentes/reels/<codigo>.mp4  (descargados con yt-dlp)
Crea: assets/video/<nombre>.mp4  (H.264, sin audio, 540 px de ancho, faststart)
      assets/video/<nombre>.webp (imagen de portada)

    python scripts/prepare_videos.py
"""
import subprocess
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_fuentes" / "reels"
OUT = ROOT / "assets" / "video"
FF = imageio_ffmpeg.get_ffmpeg_exe()

# nombre -> (código del reel, inicio s, duración s, recorte ffmpeg o None)
VIDEOS = {
    "reel-semi-azul": ("DTBcQVSiHCM", 1.0, 11, None),
    "reel-lunares-fucsia": ("DZI0KLsRxRx", 0.5, 11, "720:960:0:160"),
    "reel-copos-azul": ("DSTGYL-CKD5", 2.0, 10, None),
    "reel-lunares-verde": ("Da1A8xSx34c", 4.0, 11, "720:960:0:160"),
    "reel-coleccion": ("DcT5NQLoc5z", 6.0, 12, "720:960:0:160"),
    "reel-acry-rosa": ("DTBbz4yCAR_", 1.0, 10, None),
    "salon-entrada": ("Ck8G5CdqDxQ", 0.3, 4.9, None),
    "salon-frases": ("Ck8G5CdqDxQ", 10.8, 6.5, None),
}


def run(*args):
    subprocess.run([FF, "-v", "error", "-y", *args], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for nombre, (codigo, ini, dur, crop) in VIDEOS.items():
        src = SRC / f"{codigo}.mp4"
        vf = (f"crop={crop}," if crop else "") + "scale=540:-2:flags=lanczos,fps=30,format=yuv420p"
        run("-ss", str(ini), "-i", str(src), "-t", str(dur), "-vf", vf, "-an",
            "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-profile:v", "high",
            "-movflags", "+faststart", str(OUT / f"{nombre}.mp4"))
        run("-ss", "0.6", "-i", str(OUT / f"{nombre}.mp4"), "-frames:v", "1", "-q:v", "80", str(OUT / f"{nombre}.webp"))
        print(nombre, round((OUT / f"{nombre}.mp4").stat().st_size / 1024), "KB")


if __name__ == "__main__":
    main()
