"""Monta reel.mp4 (1080x1920, H.264, 30 fps, com faixa de áudio silenciosa) a partir das lâminas.
Uso: python3 ferramentas/artes/montar-reel.py artes/<pasta>
Duração de cada lâmina: campo "segundos" no arte.json (padrão 2.5s).
"""
import json, os, subprocess, sys

pasta = sys.argv[1]
spec = json.load(open(os.path.join(pasta, "arte.json"), encoding="utf-8"))
if spec.get("formato") != "reel":
    sys.exit(0)
lista = os.path.join(pasta, "_lista.txt")
with open(lista, "w") as f:
    lams = spec["laminas"]
    for i, l in enumerate(lams, 1):
        f.write(f"file 'lamina-{i:02d}.jpg'\nduration {float(l.get('segundos', 2.5))}\n")
    f.write(f"file 'lamina-{len(lams):02d}.jpg'\n")  # exigência do concat para a última duração
saida = os.path.join(pasta, "reel.mp4")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lista,
    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
    "-vf", "fps=30,format=yuv420p,scale=1080:1920",
    "-c:v", "libx264", "-profile:v", "high", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", saida,
], check=True)
os.remove(lista)
print("gerado", saida)
