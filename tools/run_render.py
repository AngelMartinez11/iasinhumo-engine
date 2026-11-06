#!/usr/bin/env python3
"""Orquestador de render para GitHub Actions.

Modos:
  cola           renderiza los guiones con estado guion_listo de la bitacora (Google Sheet publicada como CSV)
  ejemplo        renderiza ejemplos/v2_estafas.json con la voz indicada
  archivo        renderiza el guion indicado en el campo "archivo" (motor v2 o v4 segun el guion)
  muestra_voces  genera un mp3 corto por cada voz en espanol para elegir
Todo se sube al release "cola" del repositorio.
"""
import csv
import io
import json
import os
import re
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
    """Usa el motor v4 si el guion trae "motor": 4; si no, el motor v2."""
    try:
        motor = int(json.load(open(js, encoding="utf-8")).get("motor", 2))
    except Exception:
        motor = 2
    sh("python3", os.path.join(ROOT, "engine4.py" if motor >= 4 else "engine.py"), js, mp4)
    return [mp4, os.path.splitext(mp4)[0] + "_publicacion.txt"]


def bajar_csv(url):
    """Descarga la bitacora como CSV. Prueba la exportacion normal y, si Google la rechaza,
    el endpoint gviz (funciona con hojas compartidas por enlace)."""
    m = re.search(r"/d/([A-Za-z0-9_-]+)", url)
    g = re.search(r"gid=(\d+)", url)
    sid, gid = (m.group(1) if m else ""), (g.group(1) if g else "0")
    candidatos = [url,
                  f"https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv&gid={gid}",
                  f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"]
    for u in candidatos:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) iasinhumo-render"})
            data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
            if data.lstrip().startswith("<"):
                print("respuesta HTML (sin acceso) en", u, flush=True)
                continue
            print("bitacora descargada desde", u, flush=True)
            return data
        except Exception as e:
            print("fallo", u, "->", e, flush=True)
    sys.exit("No se pudo leer la bitacora. Revisa que este compartida como 'Cualquier persona con el enlace: Lector'.")


def modo_cola():
    url = os.environ.get("SHEET_CSV_URL", "")
    if not url:
        sys.exit("Falta la variable SHEET_CSV_URL (Settings > Secrets and variables > Actions > Variables)")
    data = bajar_csv(url)
    rows = list(csv.DictReader(io.StringIO(data)))
    print("filas en la bitacora:", len(rows), "| columnas:", list(rows[0].keys()) if rows else [], flush=True)
    hechos = assets_existentes()
    files = []
    for r in rows:
        rid = (r.get("id") or "").strip()
        guion = "".join((r.get(k) or "") for k in ("guion_json", "guion_json2", "guion_json3")).strip()
        if (r.get("estado") or "").strip() != "guion_listo" or not guion:
            continue
        if f"{rid}.mp4" in hechos:
            print("ya renderizado:", rid)
            continue
        js = os.path.join(OUT, f"{rid}.json")
        with open(js, "w", encoding="utf-8") as f:
            f.write(guion)
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


def modo_archivo(ruta):
    """Renderiza un guion del repositorio (por ejemplo ejemplos/hsf_blockbuster.json)."""
    rutas = [r.strip() for r in (ruta or "ejemplos/hsf_blockbuster.json").split(",") if r.strip()]
    files = []
    for r in rutas:
        js = os.path.join(ROOT, r)
        nombre = os.path.splitext(os.path.basename(js))[0]
        try:
            files += render(js, os.path.join(OUT, nombre + ".mp4"))
        except Exception as e:
            print("FALLO", r, e, flush=True)
    subir(files)


VOCES_NARRADOR = ["es-ES-AlvaroNeural", "es-MX-JorgeNeural", "es-US-AlonsoNeural", "es-CO-GonzaloNeural",
                  "en-US-AndrewMultilingualNeural", "en-US-BrianMultilingualNeural", "fr-FR-RemyMultilingualNeural",
                  "it-IT-GiuseppeMultilingualNeural", "de-DE-FlorianMultilingualNeural", "en-US-AvaMultilingualNeural",
                  "en-US-EmmaMultilingualNeural"]

TEXTO_MUESTRA = ("El veinticuatro de noviembre de mil novecientos setenta y uno, un hombre de traje oscuro compra un boleto "
                 "de ida. Paga en efectivo. Se sienta al fondo del avion, pide un cafe, y le entrega una nota a la azafata. "
                 "Ella la guarda sin abrirla. Y el hombre se inclina y le dice: mejor leala. Tengo una bomba.")


def modo_muestra(voces=""):
    """Un mp3 por voz con el mismo texto narrativo. 'voces' (opcional) es una lista separada por comas."""
    import engine
    lista = [v.strip() for v in voces.split(",") if v.strip()] or VOCES_NARRADOR
    files = []
    for v in lista:
        for rate in ("+0%",):
            try:
                a, _ = engine.EdgeVoice(v, rate=rate).say(TEXTO_MUESTRA)
            except Exception as e:
                print("voz no disponible:", v, e)
                continue
            wav = os.path.join(OUT, f"voz_{v}.wav")
            engine.write_wav(wav, a / (abs(a).max() or 1) * 0.9)
            mp3 = wav[:-4] + ".mp3"
            sh("ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "96k", mp3)
            files.append(mp3)
    subir(files)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    modo = (sys.argv[1] if len(sys.argv) > 1 else "cola") or "cola"
    voz = sys.argv[2] if len(sys.argv) > 2 else ""
    archivo = sys.argv[3] if len(sys.argv) > 3 else ""
    {"cola": modo_cola, "ejemplo": lambda: modo_ejemplo(voz), "archivo": lambda: modo_archivo(archivo),
     "muestra_voces": lambda: modo_muestra(voz)}[modo]()
