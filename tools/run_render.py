#!/usr/bin/env python3
"""Orquestador de render para GitHub Actions.

Modos:
  cola           renderiza los guiones con estado guion_listo de la bitacora (Google Sheet publicada como CSV)
  ejemplo        renderiza ejemplos/v2_estafas.json con la voz indicada
  muestra_voces  genera un mp3 corto por cada voz en espanol para elegir
Todo se sube al release "cola" del repositorio.
"""
import csv
import io
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, ROOT)

VOCES = ["es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-ES-AlvaroNeural", "es-ES-ElviraNeural",
         "es-CO-GonzaloNeural", "es-CO-SalomeNeural", "es-AR-TomasNeural", "es-AR-ElenaNeural",
         "es-US-AlonsoNeural", "es-US-PalomaNeural"]


def sh(*cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def assets_existentes():
    try:
        r = subprocess.run(["gh", "release", "view", "cola", "--json", "assets"], capture_output=True, text=True, check=True)
        return {a["name"] for a in json.loads(r.stdout)["assets"]}
    except Exception:
        return set()


def subir(files):
    if files:
        sh("gh", "release", "upload", "cola", "--clobber", *files)


def render(js, mp4):
    sh("python3", os.path.join(ROOT, "engine.py"), js, mp4)
    return [mp4, os.path.splitext(mp4)[0] + "_publicacion.txt"]


def modo_cola():
    url = os.environ.get("SHEET_CSV_URL", "")
    if not url:
        sys.exit("Falta la variable SHEET_CSV_URL (Settings > Secrets and variables > Actions > Variables)")
    data = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    hechos = assets_existentes()
    files = []
    for r in rows:
        rid = (r.get("id") or "").strip()
        if (r.get("estado") or "").strip() != "guion_listo" or not (r.get("guion_json") or "").strip():
            continue
        if f"{rid}.mp4" in hechos:
            print("ya renderizado:", rid)
            continue
        js = os.path.join(OUT, f"{rid}.json")
        with open(js, "w", encoding="utf-8") as f:
            f.write(r["guion_json"])
        try:
            files += render(js, os.path.join(OUT, f"{rid}.mp4"))
            files.append(js)
        except Exception as e:
            print("FALLO", rid, e, flush=True)
    subir(files)
    print("renderizados:", len(files) // 3)


def modo_ejemplo(voz):
    if voz:
        os.environ["ISH_VOICE"] = voz
    name = "ejemplo_" + (voz or "es-MX-JorgeNeural")
    subir(render(os.path.join(ROOT, "ejemplos", "v2_estafas.json"), os.path.join(OUT, name + ".mp4")))


def modo_muestra():
    import engine
    files = []
    for v in VOCES:
        nombre = v.split("-")[2].replace("Neural", "")
        try:
            a, _ = engine.EdgeVoice(v).say(f"Hola, soy {nombre}. Esto es IA Sin Humo: la inteligencia artificial "
                                           f"explicada sin exageraciones. ¿Humo o real? Te lo cuento en treinta segundos.")
        except Exception as e:
            print("voz no disponible:", v, e)
            continue
        wav = os.path.join(OUT, f"muestra_{v}.wav")
        engine.write_wav(wav, a / (abs(a).max() or 1) * 0.9)
        mp3 = wav[:-4] + ".mp3"
        sh("ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "128k", mp3)
        files.append(mp3)
    subir(files)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    modo = (sys.argv[1] if len(sys.argv) > 1 else "cola") or "cola"
    voz = sys.argv[2] if len(sys.argv) > 2 else ""
    {"cola": modo_cola, "ejemplo": lambda: modo_ejemplo(voz), "muestra_voces": modo_muestra}[modo]()
