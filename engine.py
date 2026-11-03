#!/usr/bin/env python3
"""IA SinHumo - motor de render v2 (estilo explainer ilustrado, 1080x1920, 30 fps).
Revision 3: voces Edge (neuronales de Microsoft), ElevenLabs o Kokoro offline.

Uso:
    python3 engine.py guion.json salida.mp4 [--voices DIR]

Cada escena trae una o mas lineas de narracion y capas SVG (ilustraciones
vectoriales) que aparecen animadas al ritmo de la voz. Voz offline con
Kokoro (sherpa-onnx). Subtitulos palabra por palabra dibujados por el motor.
"""
import argparse
import asyncio
import base64
import io
import json
import math
import os
import random
import subprocess
import sys
import tempfile
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 24000
GAP = 0.16
SCENE_GAP = 0.12

C_BG1 = (8, 11, 24)
C_BG2 = (17, 24, 52)
C_TEXT = (245, 247, 255)
C_MUTED = (150, 163, 205)
C_CYAN = (61, 220, 255)
C_YELLOW = (255, 210, 63)

FONT_DIR = "/usr/share/fonts/truetype/google-fonts"
F_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
F_MED = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

ART = (0, 610, 1080, 1582)       # area de ilustracion (viewBox 1000x900 escalado a 1080x972)
CAP_Y = 520                      # centro vertical de los subtitulos

SVG_STYLE = """
<style>
text { font-family: Poppins, sans-serif; font-weight: 700; }
.t { fill: #F5F7FF; } .m { fill: #96A3CD; } .c { fill: #3DDCFF; } .y { fill: #FFD23F; }
.r { fill: #FF5A6E; } .g { fill: #3DDC97; } .p { fill: #1C2A55; } .p2 { fill: #26386E; }
.sc { stroke: #3DDCFF; } .sy { stroke: #FFD23F; } .sr { stroke: #FF5A6E; } .sg { stroke: #3DDC97; } .st { stroke: #F5F7FF; }
</style>
"""

VOICES = {"A": 29, "B": 28}      # Kokoro v1.0: 29 em_alex (narrador), 28 ef_dora, 53 em_santa

_fonts = {}


def font(path, size):
    k = (path, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, size)
    return _fonts[k]


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = max(0.0, min(1.0, x))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


# ---------------------------------------------------------------- voz

class Voice:
    def __init__(self, voices_dir):
        import sherpa_onnx as s
        d = os.path.join(voices_dir, "kokoro-multi-lang-v1_0")
        kc = s.OfflineTtsKokoroModelConfig(
            model=os.path.join(d, "model.onnx"), voices=os.path.join(d, "voices.bin"),
            tokens=os.path.join(d, "tokens.txt"), data_dir=os.path.join(d, "espeak-ng-data"),
            dict_dir=os.path.join(d, "dict"),
            lexicon=os.path.join(d, "lexicon-us-en.txt") + "," + os.path.join(d, "lexicon-zh.txt"))
        kc.lang = "es"
        self.tts = s.OfflineTts(s.OfflineTtsConfig(model=s.OfflineTtsModelConfig(kokoro=kc, num_threads=2)))

    def say(self, text, sid, speed):
        a = self.tts.generate(text, sid=sid, speed=speed)
        x = np.array(a.samples, dtype=np.float32)
        idx = np.where(np.abs(x) > 0.008)[0]
        if len(idx):
            x = x[max(0, idx[0] - 240): idx[-1] + 600]
        if a.sample_rate != SR:
            n = int(len(x) * SR / a.sample_rate)
            x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
        return x


def decode_audio(data):
    """Decodifica mp3/wav en memoria a float32 mono a SR con ffmpeg."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "pipe:1"],
                       input=data, stdout=subprocess.PIPE, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


class EdgeVoice:
    """Voces neuronales de Microsoft Edge (requiere internet). Devuelve tiempos por palabra."""

    def __init__(self, voice="es-MX-JorgeNeural", rate="+6%", pitch="+0Hz"):
        import edge_tts  # noqa: F401
        self.voice, self.rate, self.pitch = voice, rate, pitch

    async def _run(self, text, voice):
        import edge_tts
        comm = edge_tts.Communicate(text, voice, rate=self.rate, pitch=self.pitch, boundary="WordBoundary")
        audio, words = bytearray(), []
        async for ch in comm.stream():
            if ch["type"] == "audio":
                audio.extend(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7))
        return bytes(audio), words

    def say(self, text, voice=None):
        for intento in range(4):
            try:
                data, words = asyncio.run(self._run(text, voice or self.voice))
                return decode_audio(data), words
            except Exception as e:  # reintento ante cortes de red
                if intento == 3:
                    raise
                print("edge-tts reintento:", e, file=sys.stderr)


class ElevenVoice:
    """ElevenLabs con marcas de tiempo por caracter (requiere ELEVENLABS_API_KEY)."""

    def __init__(self, voice_id, model="eleven_multilingual_v2", stability=0.45, similarity=0.8, style=0.25):
        self.key = os.environ["ELEVENLABS_API_KEY"]
        self.voice_id, self.model = voice_id, model
        self.settings = {"stability": stability, "similarity_boost": similarity, "style": style, "use_speaker_boost": True}

    def say(self, text, voice=None):
        vid = voice or self.voice_id
        body = json.dumps({"text": text, "model_id": self.model, "voice_settings": self.settings}).encode()
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps",
                                     data=body, headers={"xi-api-key": self.key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.loads(r.read())
        audio = decode_audio(base64.b64decode(res["audio_base64"]))
        al = res.get("alignment") or {}
        chars, st, en = al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", [])
        words, cur, ws = [], "", None
        for c, a, b in zip(chars, st, en):
            if c.isspace():
                if cur:
                    words.append((cur, ws, prev))
                cur, ws = "", None
            else:
                if ws is None:
                    ws = a
                cur += c
                prev = b
        if cur:
            words.append((cur, ws, prev))
        return audio, words


class KokoroVoice:
    def __init__(self, voices_dir, sid=29, speed=1.0):
        self.v = Voice(voices_dir)
        self.sid, self.speed = sid, speed

    def say(self, text, voice=None):
        return self.v.say(text, int(voice) if voice is not None else self.sid, self.speed), None


def make_tts(spec, voices_dir):
    cfg = spec.get("tts", {})
    prov = os.environ.get("ISH_TTS", cfg.get("provider", "edge"))
    if prov == "elevenlabs":
        return ElevenVoice(os.environ.get("ELEVENLABS_VOICE_ID", cfg.get("voice_id", ""))), cfg.get("voice_b")
    if prov == "kokoro":
        return KokoroVoice(voices_dir, int(cfg.get("sid", 29)), float(spec.get("speed", 1.0))), cfg.get("sid_b", 28)
    return EdgeVoice(os.environ.get("ISH_VOICE") or cfg.get("voice", "es-MX-JorgeNeural"), cfg.get("rate", "+6%"), cfg.get("pitch", "+0Hz")), cfg.get("voice_b", "es-MX-DaliaNeural")


# ---------------------------------------------------------------- audio

def synth_music(dur, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(dur * SR)) / SR
    bpm = 96
    beat = 60 / bpm
    bar = beat * 4
    progs = [[(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 196.0, 261.63), (196.0, 246.94, 293.66)],
             [(196.0, 246.94, 293.66), (164.81, 196.0, 246.94), (130.81, 164.81, 196.0), (146.83, 185.0, 220.0)]]
    prog = progs[seed % len(progs)]
    out = np.zeros_like(t)
    i = 0
    while i * bar < dur:
        ch = prog[i % 4]
        m = (t >= i * bar) & (t < (i + 1) * bar)
        tt = t[m] - i * bar
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.6)
        for f in ch:
            out[m] += 0.035 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt))
        i += 1
    k = 0
    while k * beat < dur:
        n0 = int(k * beat * SR)
        n = int(0.16 * SR)
        if n0 + n >= len(out):
            break
        tt = np.arange(n) / SR
        out[n0:n0 + n] += 0.22 * np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 20)
        h0 = int((k * beat + beat / 2) * SR)
        hn = int(0.03 * SR)
        if h0 + hn < len(out):
            out[h0:h0 + hn] += 0.025 * rng.standard_normal(hn) * np.exp(-np.arange(hn) / SR * 90)
        k += 1
    return out.astype(np.float32)


def synth_whoosh():
    n = int(0.32 * SR)
    noise = np.random.default_rng(1).standard_normal(n).astype(np.float32)
    out = np.zeros(n, dtype=np.float32)
    y = 0.0
    for i in range(n):
        y += (0.015 + 0.4 * i / n) * (noise[i] - y)
        out[i] = y
    return 0.45 * out * np.sin(np.pi * np.arange(n) / n) ** 2


def synth_pop():
    n = int(0.09 * SR)
    tt = np.arange(n) / SR
    return (0.18 * np.sin(2 * np.pi * (900 - 2500 * tt) * tt) * np.exp(-tt * 45)).astype(np.float32)


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- graficos

def svg_layer(fragment, w, h):
    import cairosvg
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 900" width="{w}" height="{h}">'
           f"{SVG_STYLE}{fragment}</svg>")
    png = cairosvg.svg2png(bytestring=doc.encode("utf-8"), output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def make_background():
    y = np.linspace(0, 1, H)[:, None, None]
    grad = np.array(C_BG1)[None, None] * (1 - y) + np.array(C_BG2)[None, None] * y
    bg = Image.fromarray(np.repeat(grad, W, axis=1).astype(np.uint8), "RGB")
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-250, 900, 650, 1900), fill=(18, 45, 95))
    gd.ellipse((550, 300, 1450, 1200), fill=(34, 26, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    arr = np.clip(np.array(bg, dtype=np.int16) + np.array(glow, dtype=np.int16), 0, 255).astype(np.uint8)
    bg = Image.fromarray(arr)
    # vineta
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-300, -200, W + 300, H + 200), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (4, 6, 14))
    return Image.composite(bg, dark, v)


def draw_header(img, tag, source):
    d = ImageDraw.Draw(img)
    f = font(F_BOLD, 34)
    label = "IA SIN HUMO" + (f"  ·  {tag}" if tag else "")
    tw = f.getlength(label)
    x0 = (W - tw) / 2 - 34
    d.rounded_rectangle((x0, 150, x0 + tw + 68, 212), radius=31, fill=(14, 20, 44), outline=(46, 64, 120), width=2)
    d.text((W / 2, 181), label, font=f, fill=C_MUTED, anchor="mm")
    if source:
        d.text((W / 2, 250), source, font=font(F_MED, 26), fill=(110, 122, 160), anchor="mm")


def make_mascot(mouth, blink):
    im = Image.new("RGBA", (300, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(150, 52), (150, 18)], fill=C_MUTED, width=6)
    d.ellipse((136, 4, 164, 32), fill=C_CYAN)
    d.rounded_rectangle((40, 50, 260, 240), radius=70, fill=(232, 238, 255), outline=(120, 140, 200), width=5)
    d.rounded_rectangle((70, 85, 230, 200), radius=45, fill=(14, 20, 44))
    if blink:
        d.line([(102, 130), (128, 130)], fill=C_CYAN, width=7)
        d.line([(172, 130), (198, 130)], fill=C_CYAN, width=7)
    else:
        d.ellipse((100, 112, 130, 148), fill=C_CYAN)
        d.ellipse((170, 112, 200, 148), fill=C_CYAN)
    mh = int(4 + mouth * 22)
    d.rounded_rectangle((128, 168 - mh // 2, 172, 168 + mh // 2 + 2), radius=8, fill=C_CYAN)
    d.ellipse((76, 150, 96, 164), fill=(255, 120, 150))
    d.ellipse((204, 150, 224, 164), fill=(255, 120, 150))
    return im.resize((210, 182), Image.LANCZOS)


# ---------------------------------------------------------------- subtitulos

def word_timing(text, start, dur, spoken=None):
    words = text.split()
    if spoken and len(spoken) == len(words):
        out = [(w, start + a, start + b) for w, (_, a, b) in zip(words, spoken)]
    else:
        wts = np.array([len(w.strip(".,;:!?¿¡\"")) + 2.2 for w in words], dtype=float)
        wts = wts / wts.sum() * dur
        out, t = [], start
        for w, d in zip(words, wts):
            out.append((w, t, t + d))
            t += d
    chunks, cur = [], []
    for item in out:
        cur.append(item)
        txt = " ".join(x[0] for x in cur)
        if len(cur) >= 4 or len(txt) >= 22 or item[0][-1] in ".,;:!?":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def caption_image(words, hi):
    f = font(F_BOLD, 66)
    sp = f.getlength(" ") + 14
    widths = [f.getlength(w) for w, _, _ in words]
    total = sum(widths) + sp * (len(words) - 1)
    im = Image.new("RGBA", (W, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = (W - total) / 2
    for i, (w, _, _) in enumerate(words):
        if i == hi:
            d.rounded_rectangle((x - 12, 22, x + widths[i] + 12, 108), radius=16,
                                fill=(61, 220, 255, 55), outline=C_CYAN + (255,), width=3)
        d.text((x + 3, 68), w, font=f, fill=(0, 0, 0, 170), anchor="lm")
        d.text((x, 65), w, font=f, fill=C_TEXT + (255,), anchor="lm")
        x += widths[i] + sp
    return im


# ---------------------------------------------------------------- render

def render(script_path, out_path, voices_dir):
    spec = json.load(open(script_path, encoding="utf-8"))
    tts, voice_b = make_tts(spec, voices_dir)
    tmp = tempfile.mkdtemp(prefix="ish_")

    # 1) voz y linea de tiempo
    track, scenes_t, chunks, talk = [], [], [], []
    t = 0.2
    for sc in spec["scenes"]:
        s0 = t
        starts = []
        for ln in sc.get("lines", []):
            spk = ln.get("spk", "A")
            spoken_text = ln.get("say", ln["text"])
            a, spoken = tts.say(spoken_text, voice_b if spk == "B" else None)
            if spoken and spoken_text != ln["text"]:
                spoken = None
            idx = np.where(np.abs(a) > 0.008)[0]
            cut = max(0, idx[0] - 240) if len(idx) else 0
            if len(idx):
                a = a[cut: idx[-1] + 600]
            if spoken:
                spoken = [(w, x - cut / SR, y - cut / SR) for w, x, y in spoken]
            d = len(a) / SR
            track.append((t, a))
            starts.append(t)
            chunks += word_timing(ln["text"], t, d, spoken)
            talk.append((t, t + d))
            t += d + GAP
        t = max(t, s0 + float(sc.get("min_dur", 1.5)))
        scenes_t.append((s0, t, starts))
        t += SCENE_GAP
    total = t + float(spec.get("tail", 0.5))

    n = int(total * SR) + SR
    vo = np.zeros(n, dtype=np.float32)
    for st, a in track:
        i = int(st * SR)
        vo[i:i + len(a)] += a[: n - i]
    vo = vo / (np.max(np.abs(vo)) or 1) * 0.9

    # 2) capas por escena
    scenes = []
    pop_times = []
    aw, ah = ART[2] - ART[0], ART[3] - ART[1]
    for sc, (s0, s1, starts) in zip(spec["scenes"], scenes_t):
        layers = []
        for ly in sc.get("layers", []):
            img = svg_layer(ly["svg"], aw, ah)
            if "t" in ly:
                at = s0 + float(ly["t"])
            else:
                k = int(ly.get("at", 0))
                at = starts[min(k, len(starts) - 1)] if starts else s0
            at = max(s0, at) + float(ly.get("delay", 0))
            layers.append((img, at, ly.get("anim", "up"), bool(ly.get("clear", False))))
            if at > s0 + 0.05:
                pop_times.append(at)
        scenes.append((s0, s1, layers, bool(sc.get("bit", False)), float(sc.get("zoom", 0.05))))

    music = synth_music(total + 1, seed=len(spec.get("title", "")))[:n]
    music = np.pad(music, (0, max(0, n - len(music))))
    env = np.convolve(np.abs(vo), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.65 * np.clip(env * 8, 0, 1)
    fx = np.zeros(n, dtype=np.float32)
    wh, pp = synth_whoosh(), synth_pop()
    for s0, _, _, _, _ in scenes[1:]:
        i = max(0, int((s0 - 0.12) * SR))
        fx[i:i + len(wh)] += wh[: n - i]
    for pt in pop_times:
        i = int(pt * SR)
        fx[i:i + len(pp)] += pp[: n - i]
    mix = vo + 0.5 * music * duck + 0.3 * fx
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.97)
    wav = os.path.join(tmp, "mix.wav")
    write_wav(wav, mix[: int(total * SR)])

    nf = int(total * FPS)
    hop = SR // FPS
    energy = np.array([np.sqrt(np.mean(vo[i * hop:(i + 1) * hop] ** 2)) for i in range(nf)])
    p90 = np.percentile(energy[energy > 0], 90) if np.any(energy > 0) else 1
    energy = np.clip(energy / p90, 0, 1)

    bg = make_background()
    draw_header(bg, spec.get("tag", ""), spec.get("source", ""))
    bg = bg.convert("RGBA")
    mascots = {(m, b): make_mascot(m / 3, b) for m in range(4) for b in (0, 1)}
    rnd = random.Random(7)
    dust = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.2, 0.9), rnd.uniform(1, 3)) for _ in range(70)]
    cap_cache = {}
    chunk_spans = [(c[0][1], c[-1][2], ci) for ci, c in enumerate(chunks)]

    out_tmp = os.path.join(tmp, "video.mp4")
    ff = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_tmp], stdin=subprocess.PIPE)

    for fi in range(nf):
        tt = fi / FPS
        frame = bg.copy()
        d = ImageDraw.Draw(frame)
        for (x, y, sp, r) in dust:
            yy = (y - tt * sp * 25) % H
            d.ellipse((x - r, yy - r, x + r, yy + r), fill=(120, 150, 220, 70))
        cur = scenes[-1]
        for s in scenes:
            if s[0] - 0.001 <= tt:
                cur = s
        s0, s1, layers, bit, zoom = cur
        lt = tt - s0
        canvas = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
        for li, (img, at, anim, _clr) in enumerate(layers):
            if tt < at:
                continue
            hide = [l2[1] for l2 in layers[li + 1:] if l2[3] and l2[1] <= tt]
            if hide:
                q = (tt - min(hide)) / 0.25
                if q >= 1:
                    continue
                im = img.copy()
                im.putalpha(im.getchannel("A").point(lambda v, a=1 - q: int(v * a)))
                canvas.alpha_composite(im)
                continue
            p = (tt - at) / 0.35
            if p >= 1:
                canvas.alpha_composite(img)
                continue
            e = ease_out(p)
            if anim == "pop":
                sc_ = 0.6 + 0.4 * ease_back(p)
                w2, h2 = max(1, int(aw * sc_)), max(1, int(ah * sc_))
                im = img.resize((w2, h2), Image.BILINEAR)
                ox, oy = (aw - w2) // 2, (ah - h2) // 2
            else:
                im = img
                ox = int((1 - e) * (-120 if anim == "left" else 120 if anim == "right" else 0))
                oy = int((1 - e) * (70 if anim == "up" else 0))
            if e < 1:
                im = im.copy()
                im.putalpha(im.getchannel("A").point(lambda v, a=e: int(v * a)))
            tmp_l = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
            tmp_l.paste(im, (ox, oy), im)
            canvas.alpha_composite(tmp_l)
        z = 1 + zoom * min(1.0, lt / max(0.5, s1 - s0))
        if abs(z - 1) > 0.002:
            w2, h2 = int(aw * z), int(ah * z)
            canvas = canvas.resize((w2, h2), Image.BILINEAR).crop(((w2 - aw) // 2, (h2 - ah) // 2, (w2 - aw) // 2 + aw, (h2 - ah) // 2 + ah))
        if lt < 0.25:
            e = ease_out(lt / 0.25)
            canvas.putalpha(canvas.getchannel("A").point(lambda v, a=e: int(v * a)))
            frame.alpha_composite(canvas, (ART[0] + int((1 - e) * 80), ART[1]))
        else:
            frame.alpha_composite(canvas, (ART[0], ART[1]))
        if bit:
            speaking = any(a <= tt <= b for a, b in talk)
            m = int(round(energy[fi] * 3)) if speaking else 0
            blink = (fi % 95) < 4
            mas = mascots[(min(3, m), int(blink))]
            frame.alpha_composite(mas, (40, ART[3] - mas.height + 40 + int(math.sin(tt * 5.5) * 6)))
        for a, b, ci in chunk_spans:
            if a <= tt < b + 0.15:
                words = chunks[ci]
                hi = 0
                for wi, (_, ws, we) in enumerate(words):
                    if tt >= ws:
                        hi = wi
                key = (ci, hi)
                if key not in cap_cache:
                    cap_cache[key] = caption_image(words, hi)
                ci_img = cap_cache[key]
                ap = min(1.0, (tt - a) / 0.08)
                frame.alpha_composite(ci_img, (0, CAP_Y - 65 + int((1 - ap) * 10)))
                break
        d.rectangle((0, 0, W, 8), fill=(24, 32, 66, 255))
        d.rectangle((0, 0, int(W * tt / total), 8), fill=C_CYAN + (255,))
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
