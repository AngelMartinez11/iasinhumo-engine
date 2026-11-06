#!/usr/bin/env python3
"""Motor de render v4 (multicanal): explainer 2D plano estilo "historias".

Uso:
    python3 engine4.py guion.json salida.mp4 [--voices DIR]

Novedades frente al motor v2:
  - Escenas a pantalla completa armadas con piezas reutilizables (piezas.py).
  - Fondos de rayos con paletas, pantalla dividida, noche u oficina, con suelo.
  - Capas que se quedan entre escenas ("sigue": true) y se quitan por id.
  - Camara con zoom y paneo suave por escena; transicion de empuje entre escenas.
  - Tarjetas de capitulo y de dato (negro y dorado) con numero que cuenta.
  - Subtitulo arriba en banda oscura con efecto karaoke (gris -> blanco).
  - Configuracion por canal en canales/<canal>.json (marca, musica, colores).

Formato del guion: ver MANUAL_V4.md.
"""
import argparse
import io
import json
import math
import os
import random
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import engine as e1
import piezas as P

W, H, FPS = 1080, 1920, 30
SR = e1.SR
GAP = 0.14
ROOT = os.path.dirname(os.path.abspath(__file__))

PALETAS = {
    "lila": ("#d9d2f3", "#cbc1ee", "#d8c7a8"),
    "durazno": ("#f6d5c3", "#f0c3ad", "#d8c7a8"),
    "azul": ("#cfe0f7", "#bdd3f2", "#d3c3a4"),
    "menta": ("#d3efe2", "#c1e6d4", "#d8c7a8"),
    "rojo": ("#f7cfcf", "#f0b9b9", "#d8c7a8"),
    "oro": ("#f7e6b5", "#f0d993", "#d8c7a8"),
    "gris": ("#e4e4ea", "#d6d6de", "#cfc6b4"),
    "cielo": ("#bfe3ff", "#a9d8ff", "#9ccf7a"),
}
ORO = (240, 196, 72)
NEGRO = (20, 20, 30)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ease_io(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ease_bounce(x):
    x = max(0.0, min(1.0, x))
    n1, d1 = 7.5625, 2.75
    if x < 1 / d1:
        return n1 * x * x
    if x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    if x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    x -= 2.625 / d1
    return n1 * x * x + 0.984375


# ------------------------------------------------------------------ canal

def cargar_canal(nombre):
    base = {"marca": "", "musica": "alegre", "acento": "#ffd23f", "barra": "#ffd23f"}
    if nombre:
        ruta = os.path.join(ROOT, "canales", f"{nombre}.json")
        if os.path.exists(ruta):
            base.update(json.load(open(ruta, encoding="utf-8")))
    return base


# ------------------------------------------------------------------ voz de prueba

class VozMuda:
    """Silencio con duracion estimada: sirve para revisar el armado visual sin voz real."""

    def say(self, text, voice=None):
        n = len(text.split())
        return np.zeros(int((0.36 * n + 0.3) * SR), dtype=np.float32) + 1e-3, None


# ------------------------------------------------------------------ fondos

def fondo(spec):
    t = spec.get("tipo", "rayos")
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    suelo = spec.get("suelo")
    if t == "rayos":
        c1, c2, s = PALETAS.get(spec.get("paleta", "lila"), PALETAS["lila"])
        suelo = s if suelo is None else suelo
        d.rectangle((0, 0, W, H), fill=c1)
        cx, cy, r, rays = W / 2, spec.get("cy", 980), 2600, 28
        for i in range(0, rays, 2):
            a0, a1 = 2 * math.pi * i / rays, 2 * math.pi * (i + 1) / rays
            d.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=c2)
    elif t == "split":
        a, b = spec.get("c", ["#cfe0ff", "#ffd6d6"])
        d.rectangle((0, 0, W // 2, H), fill=a)
        d.rectangle((W // 2, 0, W, H), fill=b)
        suelo = "#e9dcc4" if suelo is None else suelo
    elif t == "noche":
        y = np.linspace(0, 1, H)[:, None, None]
        top, bot = np.array(hexrgb("#141a3a")), np.array(hexrgb("#3b2f63"))
        arr = (top * (1 - y) + bot * y).astype(np.uint8)
        img = Image.fromarray(np.repeat(arr, W, axis=1), "RGB")
        d = ImageDraw.Draw(img)
        rnd = random.Random(3)
        for _ in range(120):
            x, yy, rr = rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(1, 3.5)
            d.ellipse((x - rr, yy - rr, x + rr, yy + rr), fill=(255, 255, 255))
        suelo = "#2b2440" if suelo is None else suelo
    elif t == "oficina":
        svg, caja = P.oficina_interior(**spec.get("a", {}))
        img = render_svg(svg, caja, 1.0).convert("RGB")
        suelo = None
    else:
        d.rectangle((0, 0, W, H), fill=spec.get("c", "#e4e4ea"))
        suelo = None if suelo is None else suelo
    if suelo and suelo != "no":
        y0 = spec.get("suelo_y", 1560)
        d = ImageDraw.Draw(img)
        d.rectangle((0, y0, W, H), fill=suelo)
        d.rectangle((0, y0, W, y0 + 9), fill=(43, 43, 58))
    # vineta suave
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-260, -160, W + 260, H + 160), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(200))
    oscuro = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.22)
    return Image.composite(img, oscuro, v).convert("RGBA")


# ------------------------------------------------------------------ piezas

def render_svg(frag, caja, s):
    import cairosvg
    x0, y0, x1, y1 = caja
    w, h = max(1, int((x1 - x0) * s)), max(1, int((y1 - y0) * s))
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" '
           f'width="{w}" height="{h}">{frag}</svg>')
    png = cairosvg.svg2png(bytestring=doc.encode("utf-8"), output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


_cache_piezas = {}


def pieza(it):
    key = json.dumps([it["p"], it.get("a", {}), it.get("s", 1.0), it.get("flip", False)], sort_keys=True)
    if key not in _cache_piezas:
        fn = P.PIEZAS[it["p"]]
        svg, caja = fn(**it.get("a", {}))
        s = float(it.get("s", 1.0))
        img = render_svg(svg, caja, s)
        ox, oy = caja[0] * s, caja[1] * s
        if it.get("flip"):
            img = ImageOps.mirror(img)
            ox = -caja[2] * s
        _cache_piezas[key] = (img, ox, oy)
    return _cache_piezas[key]


# ------------------------------------------------------------------ tarjetas PIL

def tarjeta_dato(valor, texto, ancho=760):
    t1 = 150
    while t1 > 70 and e1.font(e1.F_BOLD, t1).getlength(valor) > 880:
        t1 -= 6
    f1 = e1.font(e1.F_BOLD, t1)
    f2 = e1.font(e1.F_BOLD, 50)
    w = min(1000, max(ancho, int(f1.getlength(valor)) + 120, int(f2.getlength(texto)) + 120))
    h = 330 if texto else 240
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 14, w + 12, h + 14), radius=26, fill=(0, 0, 0, 110))
    d.rounded_rectangle((0, 0, w, h), radius=26, fill=NEGRO + (240,), outline=ORO + (255,), width=8)
    d.text((w / 2, 130), valor, font=f1, fill=ORO + (255,), anchor="mm")
    if texto:
        d.text((w / 2, 262), texto, font=f2, fill=(255, 255, 255, 255), anchor="mm")
    return im


def formato_num(n, pre="", suf=""):
    if isinstance(n, float) and not n.is_integer():
        s = f"{n:,.1f}"
    else:
        s = f"{int(round(n)):,}"
    return pre + s.replace(",", "X").replace(".", ",").replace("X", ".") + suf


def tarjeta_capitulo(titulo, n=""):
    f1 = e1.font(e1.F_BOLD, 110)
    f2 = e1.font(e1.F_BOLD, 42)
    w = max(760, int(f1.getlength(titulo)) + 140)
    h = 300
    im = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 16, w + 14, h + 16), radius=18, fill=(0, 0, 0, 140))
    d.rounded_rectangle((0, 0, w, h), radius=18, fill=NEGRO + (255,), outline=ORO + (255,), width=8)
    if n:
        d.text((w / 2, 82), f"CAPÍTULO {n}", font=f2, fill=(200, 200, 210, 255), anchor="mm")
    d.text((w / 2, 185 if n else 150), titulo, font=f1, fill=ORO + (255,), anchor="mm")
    return im


def marca_img(texto):
    f = e1.font(e1.F_BOLD, 30)
    tw = sum(f.getlength(ch) + 5 for ch in texto) - 5
    im = Image.new("RGBA", (W, 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = (W - tw) / 2
    d.rounded_rectangle((x - 30, 8, x + tw + 30, 62), radius=27, fill=(20, 20, 30, 150))
    for ch in texto:
        d.text((x, 35), ch, font=f, fill=(255, 255, 255, 235), anchor="lm")
        x += f.getlength(ch) + 5
    return im


# ------------------------------------------------------------------ subtitulo karaoke

def banda():
    im = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    a = np.zeros((260, W), dtype=np.uint8)
    for y in range(260):
        k = min(y / 60, (259 - y) / 60, 1.0)
        a[y, :] = int(190 * k)
    capa = Image.new("RGBA", (W, 260), (24, 24, 36, 255))
    capa.putalpha(Image.fromarray(a))
    im.alpha_composite(capa)
    return im


def karaoke(words, tt):
    f = e1.font(e1.F_BOLD, 68)
    sp = f.getlength(" ")
    lineas, cur, ancho = [], [], 0
    for w, a, b in words:
        lw = f.getlength(w)
        if cur and ancho + sp + lw > W - 120:
            lineas.append(cur)
            cur, ancho = [], 0
        cur.append((w, a, b))
        ancho += (sp if len(cur) > 1 else 0) + lw
    if cur:
        lineas.append(cur)
    im = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 100 - (len(lineas) - 1) * 42
    for ln in lineas:
        total = sum(f.getlength(w) for w, _, _ in ln) + sp * (len(ln) - 1)
        x = (W - total) / 2
        for w, a, b in ln:
            col = (255, 255, 255, 255) if tt >= a else (150, 150, 168, 255)
            d.text((x + 3, y + 3), w, font=f, fill=(0, 0, 0, 120), anchor="lm")
            d.text((x, y), w, font=f, fill=col, anchor="lm")
            x += f.getlength(w) + sp
        y += 84
    return im


# ------------------------------------------------------------------ musica

def musica_intriga(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    bar = 3.2
    progs = [[(110.0, 130.81, 164.81), (87.31, 110.0, 130.81), (130.81, 164.81, 196.0), (98.0, 123.47, 146.83)],
             [(146.83, 174.61, 220.0), (116.54, 146.83, 174.61), (87.31, 110.0, 130.81), (110.0, 138.59, 164.81)]]
    prog = progs[seed % len(progs)]
    out = np.zeros_like(t)
    i = 0
    while i * bar < dur:
        m = (t >= i * bar) & (t < (i + 1) * bar)
        tt = t[m] - i * bar
        env = np.minimum(1, tt / 1.2) * np.minimum(1, (bar - tt) / 1.0)
        for f in prog[i % 4]:
            out[m] += 0.03 * env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 3.01 * tt))
        i += 1
    beat = bar / 4
    k = 0
    while k * beat < dur:
        n0, n = int(k * beat * SR), int(0.35 * SR)
        if n0 + n >= len(out):
            break
        tt = np.arange(n) / SR
        out[n0:n0 + n] += 0.12 * np.sin(2 * np.pi * (45 + 30 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 9)
        k += 1
    return out.astype(np.float32)


def golpe():
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    return (0.5 * np.sin(2 * np.pi * (60 + 90 * np.exp(-tt * 12)) * tt) * np.exp(-tt * 5)).astype(np.float32)


# ------------------------------------------------------------------ render

ANIM_DUR = {"pop": 0.38, "drop": 0.6, "crece": 0.5}


def aparece(img, ox, oy, anim, p):
    """Devuelve (imagen, x, y) para el progreso p (0-1) de la animacion de entrada."""
    e = e1.ease_out(p)
    if anim == "pop":
        sc = max(0.05, 0.45 + 0.55 * e1.ease_back(p))
        w2, h2 = max(1, int(img.width * sc)), max(1, int(img.height * sc))
        im = img.resize((w2, h2), Image.BILINEAR)
        return im, ox + (img.width - w2) / 2, oy + (img.height - h2) / 2, min(1.0, p * 3)
    if anim == "crece":
        h2 = max(1, int(img.height * e))
        im = img.resize((img.width, h2), Image.BILINEAR)
        return im, ox, oy + img.height - h2, 1.0
    if anim == "drop":
        return img, ox, oy - 500 * (1 - ease_bounce(p)), min(1.0, p * 4)
    dx = {"left": -180, "right": 180}.get(anim, 0) * (1 - e)
    dy = (90 if anim == "up" else 0) * (1 - e)
    return img, ox + dx, oy + dy, e


def con_alpha(img, a):
    if a >= 0.999:
        return img
    im = img.copy()
    im.putalpha(im.getchannel("A").point(lambda v, k=a: int(v * k)))
    return im


def render(script_path, out_path, voices_dir):
    spec = json.load(open(script_path, encoding="utf-8"))
    canal = cargar_canal(spec.get("canal", ""))
    if os.environ.get("ISH_TTS") == "mudo":
        tts, voice_b = VozMuda(), None
    else:
        tts, voice_b = e1.make_tts(spec, voices_dir)
    tmp = tempfile.mkdtemp(prefix="ish4_")

    # 1) voz y tiempos
    track, tiempos, chunks = [], [], []
    t = 0.25
    for sc in spec["scenes"]:
        s0, starts = t, []
        for ln in sc.get("lines", []):
            dicho = ln.get("say", ln["text"])
            a, spoken = tts.say(dicho, voice_b if ln.get("spk") == "B" else None)
            if spoken and dicho != ln["text"]:
                spoken = None
            idx = np.where(np.abs(a) > 0.008)[0]
            cut = max(0, idx[0] - 240) if len(idx) else 0
            if len(idx):
                a = a[cut: idx[-1] + 600]
            if spoken:
                spoken = [(w, x - cut / SR, y - cut / SR) for w, x, y in spoken]
            dur = len(a) / SR
            track.append((t, a))
            starts.append(t)
            chunks += e1.word_timing(ln["text"], t, dur, spoken)
            t += dur + GAP + float(ln.get("pausa", 0))
        t = max(t, s0 + float(sc.get("min_dur", 1.6 if sc.get("capitulo") else 1.2)))
        tiempos.append((s0, t, starts))
    total = t + float(spec.get("tail", 0.6))
    n = int(total * SR) + SR
    vo = np.zeros(n, dtype=np.float32)
    for st, a in track:
        i = int(st * SR)
        vo[i:i + len(a)] += a[: n - i]
    vo = vo / (np.max(np.abs(vo)) or 1) * 0.9

    # 2) escenas: fondo, items con tiempos, camara
    escenas = []
    prev_items, prev_fondo, prev_cam = [], None, None
    sfx_pop, sfx_whoosh, sfx_golpe = [], [], []
    for k, (sc, (s0, s1, starts)) in enumerate(zip(spec["scenes"], tiempos)):
        sigue = bool(sc.get("sigue")) and k > 0
        if sc.get("capitulo"):
            fspec = sc.get("fondo", {"tipo": "noche"})
        else:
            fspec = sc.get("fondo") or (prev_fondo if sigue and prev_fondo else {"tipo": "rayos", "paleta": "lila"})
        bg = fondo(fspec)
        items = []
        if sigue:
            quita = set(sc.get("quita", []))
            for it in prev_items:
                it2 = dict(it)
                it2["ya"] = True
                if it.get("id") and it["id"] in quita:
                    it2["sale"] = s0
                if it.get("sale") is not None and it2.get("sale") is None:
                    continue
                items.append(it2)
        for it in sc.get("items", []):
            it2 = dict(it)
            if "t" in it:
                at = s0 + float(it["t"])
            else:
                j = int(it.get("at", 0))
                at = starts[min(j, len(starts) - 1)] if starts else s0
            it2["inicio"] = max(s0, at) + float(it.get("delay", 0))
            it2["ya"] = False
            it2["fase"] = random.Random(len(items) + k * 31).uniform(0, 6.28)
            items.append(it2)
            sfx_pop.append(it2["inicio"])
        dato = None
        if sc.get("dato"):
            dd = dict(sc["dato"])
            j = int(dd.get("at", 0))
            dd["inicio"] = (starts[min(j, len(starts) - 1)] if starts else s0) + float(dd.get("delay", 0.15))
            dato = dd
            sfx_golpe.append(dd["inicio"])
        cap = None
        if sc.get("capitulo"):
            cap = (tarjeta_capitulo(sc["capitulo"].get("t", ""), str(sc["capitulo"].get("n", ""))), s0 + 0.1)
            sfx_golpe.append(s0 + 0.1)
        cam = sc.get("cam") or {}
        zb = float(canal.get("zoom_base", 1.12))
        if cam.get("z"):
            cam = dict(cam, z=[zb * v for v in cam["z"]])
        z = cam.get("z") or ([prev_cam["z"][1]] * 2 if (sigue and prev_cam) else [zb, zb * 1.045])
        cx = cam.get("x") or ([prev_cam["x"][1]] * 2 if (sigue and prev_cam) else [0, 0])
        cy = cam.get("y") or ([prev_cam["y"][1]] * 2 if (sigue and prev_cam) else [0, 0])
        foco = cam.get("f") or (prev_cam["f"] if (sigue and prev_cam) else [540, 600])
        cam_n = {"z": z, "x": cx, "y": cy, "f": foco}
        if k > 0 and not sigue:
            sfx_whoosh.append(s0)
        escenas.append({"s0": s0, "s1": s1, "bg": bg, "items": items, "dato": dato, "cap": cap, "cam": cam_n, "sigue": sigue})
        prev_items, prev_fondo, prev_cam = items, fspec, cam_n

    # 3) audio final
    fx = np.zeros(n, dtype=np.float32)
    wh, pp, gg = e1.synth_whoosh(), e1.synth_pop(), golpe()
    for lista, son, vol in ((sfx_whoosh, wh, 1.0), (sfx_pop, pp, 0.8), (sfx_golpe, gg, 1.0)):
        for st in lista:
            i = max(0, int((st - (0.1 if son is wh else 0)) * SR))
            fx[i:i + len(son)] += vol * son[: n - i]
    if canal.get("musica") == "intriga":
        music = musica_intriga(total + 1, seed=len(spec.get("title", "")))[:n]
    else:
        music = e1.synth_music(total + 1, seed=len(spec.get("title", "")))[:n]
    music = np.pad(music, (0, max(0, n - len(music))))
    env = np.convolve(np.abs(vo), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.6 * np.clip(env * 8, 0, 1)
    mix = vo + 0.5 * music * duck + 0.28 * fx
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.97)
    wav = os.path.join(tmp, "mix.wav")
    e1.write_wav(wav, mix[: int(total * SR)])

    # 4) video
    nf = int(total * FPS)
    BANDA = banda()
    MARCA = marca_img(canal.get("marca", "")) if canal.get("marca") else None
    barra = hexrgb(canal.get("barra", "#ffd23f"))
    spans = [(c[0][1], c[-1][2], ci) for ci, c in enumerate(chunks)]
    cache_dato = {}
    ultimo = {}
    out_tmp = os.path.join(tmp, "video.mp4")
    ff = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_tmp], stdin=subprocess.PIPE)

    def mundo(ei, tt):
        es = escenas[ei]
        img = es["bg"].copy()
        for it in es["items"]:
            base, ox, oy = pieza(it)
            x, y = float(it.get("x", 540)) + ox, float(it.get("y", 1560)) + oy
            if it["p"] == "persona" and it.get("idle", True):
                y += math.sin(tt * 2.4 + it["fase"]) * 5
            alpha = 1.0
            im = base
            if not it["ya"]:
                if tt < it["inicio"]:
                    continue
                anim = it.get("anim", "pop" if it["p"] in ("etiqueta", "icono", "texto", "nombre") else "up")
                p = (tt - it["inicio"]) / ANIM_DUR.get(anim, 0.4)
                if p < 1:
                    im, x, y, alpha = aparece(base, x, y, anim, p)
            if it.get("sale") is not None:
                q = (tt - it["sale"]) / 0.25
                if q >= 1:
                    continue
                alpha *= 1 - q
            img.alpha_composite(con_alpha(im, alpha), (int(x), int(y)))
        # camara: zoom alrededor del punto f (ese punto queda fijo en pantalla)
        c = es["cam"]
        u = ease_io((tt - es["s0"]) / max(0.5, es["s1"] - es["s0"]))
        z = c["z"][0] + (c["z"][1] - c["z"][0]) * u
        px = c["x"][0] + (c["x"][1] - c["x"][0]) * u
        py = c["y"][0] + (c["y"][1] - c["y"][0]) * u
        if abs(z - 1) > 0.002 or abs(px) > 0.5 or abs(py) > 0.5:
            z = max(1.0, z)
            cw, ch = W / z, H / z
            x0 = min(max(0, c["f"][0] - c["f"][0] / z + px), W - cw)
            y0 = min(max(0, c["f"][1] - c["f"][1] / z + py), H - ch)
            img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
        if es["cap"]:
            card, c0 = es["cap"]
            if tt >= c0:
                p = min(1.0, (tt - c0) / 0.45)
                im, x, y, a = aparece(card, (W - card.width) / 2, 820, "pop", p)
                img.alpha_composite(con_alpha(im, a), (int(x), int(y)))
        d = es["dato"]
        if d and tt >= d["inicio"]:
            p = min(1.0, (tt - d["inicio"]) / 0.9)
            num = d.get("num")
            if num is not None and d.get("cuenta", True):
                v = num * e1.ease_out(p)
                valor = formato_num(v if isinstance(num, float) else int(v), d.get("pre", ""), d.get("suf", ""))
            elif num is not None:
                valor = formato_num(num, d.get("pre", ""), d.get("suf", ""))
            else:
                valor = d.get("valor", "")
            key = (valor, d.get("texto", ""))
            if key not in cache_dato:
                cache_dato[key] = tarjeta_dato(valor, d.get("texto", ""))
            card = cache_dato[key]
            pa = min(1.0, (tt - d["inicio"]) / 0.38)
            im, x, y, a = aparece(card, (W - card.width) / 2, float(d.get("y", 1180)), "pop", pa)
            img.alpha_composite(con_alpha(im, a), (int(x), int(y)))
        return img

    ei = 0
    for fi in range(nf):
        tt = fi / FPS
        while ei + 1 < len(escenas) and tt >= escenas[ei + 1]["s0"]:
            ei += 1
        es = escenas[ei]
        frame = mundo(ei, tt)
        lt = tt - es["s0"]
        if ei > 0 and not es["sigue"] and lt < 0.3 and (ei - 1) in ultimo:
            e = e1.ease_out(lt / 0.3)
            prev = ultimo[ei - 1]
            comp = Image.new("RGBA", (W, H))
            comp.alpha_composite(prev, (int(-e * W * 0.6), 0))
            comp.alpha_composite(frame, (int((1 - e) * W), 0))
            frame = comp
        else:
            ultimo[ei] = frame
            ultimo.pop(ei - 2, None)
        # subtitulo
        for a, b, ci in spans:
            if a <= tt < b + 0.2:
                frame.alpha_composite(BANDA, (0, 250))
                frame.alpha_composite(karaoke(chunks[ci], tt), (0, 280))
                break
        if MARCA:
            frame.alpha_composite(MARCA, (0, 110))
        dd = ImageDraw.Draw(frame)
        dd.rectangle((0, 0, W, 8), fill=(30, 30, 44, 255))
        dd.rectangle((0, 0, int(W * tt / total), 8), fill=barra + (255,))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    if ff.returncode != 0:
        sys.exit("ffmpeg fallo")
    os.replace(out_tmp, out_path)
    with open(os.path.splitext(out_path)[0] + "_publicacion.txt", "w", encoding="utf-8") as f:
        f.write("TITULO:\n" + spec.get("title", "") + "\n\n")
        f.write("DESCRIPCION:\n" + spec.get("description", "") + "\n\n")
        f.write("HASHTAGS:\n" + " ".join(spec.get("hashtags", [])) + "\n\n")
        f.write("FUENTE:\n" + spec.get("source_url", "") + "\n")
        f.write(f"\nDURACION: {total:.1f} s\n")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--voices", default=os.environ.get("ISH_VOICES", "/home/claude/tts"))
    a = ap.parse_args()
    print(f"OK {a.out} {render(a.script, a.out, a.voices):.1f}s")


if __name__ == "__main__":
    main()
