#!/usr/bin/env python3
"""IA SinHumo - motor de render de Shorts verticales (1080x1920, 30 fps).

Uso:
    python3 engine.py guion.json salida.mp4 [--voices DIR]

El guion es un JSON con escenas; cada escena tiene un tipo visual y una o
mas lineas de narracion. La voz se genera offline con sherpa-onnx (Piper).
"""
import argparse
import glob
import json
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 22050
GAP = 0.14          # silencio entre lineas (s)
SCENE_GAP = 0.10    # silencio extra al cambiar de escena (s)

C_BG1 = (9, 13, 28)
C_BG2 = (20, 28, 58)
C_PANEL = (20, 29, 60)
C_BORDER = (46, 64, 120)
C_TEXT = (245, 247, 255)
C_MUTED = (150, 163, 205)
C_CYAN = (61, 220, 255)
C_YELLOW = (255, 210, 63)
C_RED = (255, 90, 110)
C_GREEN = (61, 220, 151)

FONT_DIR = "/usr/share/fonts/truetype/google-fonts"
F_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
F_MED = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

PANEL = (60, 230, 1020, 1120)   # x0, y0, x1, y1
MASCOT_Y = 1135
CAPTION_MARGIN_V = 380          # distancia desde abajo para subtitulos

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if fnt.getlength(test) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, path, max_w, max_h, start, minimum, spacing=1.12):
    size = start
    while size > minimum:
        f = font(path, size)
        lines = wrap(text, f, max_w)
        if len(lines) * size * spacing <= max_h:
            return f, lines, size
        size -= 4
    f = font(path, minimum)
    return f, wrap(text, f, max_w), minimum


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- voz

class Voices:
    def __init__(self, voices_dir):
        import sherpa_onnx
        self.engines = {}
        self.sherpa = sherpa_onnx
        self.dir = voices_dir

    def get(self, name):
        if name not in self.engines:
            d = os.path.join(self.dir, name)
            onnx = glob.glob(os.path.join(d, "*.onnx"))[0]
            s = self.sherpa
            cfg = s.OfflineTtsConfig(model=s.OfflineTtsModelConfig(
                vits=s.OfflineTtsVitsModelConfig(
                    model=onnx, tokens=os.path.join(d, "tokens.txt"),
                    data_dir=os.path.join(d, "espeak-ng-data")),
                num_threads=2))
            self.engines[name] = s.OfflineTts(cfg)
        return self.engines[name]

    def say(self, name, text, speed):
        a = self.get(name).generate(text, sid=0, speed=speed)
        x = np.array(a.samples, dtype=np.float32)
        # recorta silencios de los extremos
        idx = np.where(np.abs(x) > 0.01)[0]
        if len(idx):
            x = x[max(0, idx[0] - 200): idx[-1] + 400]
        if a.sample_rate != SR:
            n = int(len(x) * SR / a.sample_rate)
            x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
        return x


# ---------------------------------------------------------------- audio extra

def synth_music(dur):
    t = np.arange(int(dur * SR)) / SR
    bpm = 104
    beat = 60 / bpm
    chords = [(220.0, 277.18, 329.63), (196.0, 246.94, 293.66),
              (174.61, 220.0, 261.63), (196.0, 246.94, 329.63)]
    out = np.zeros_like(t)
    bar = beat * 4
    for i, ch in enumerate(chords * int(dur / (bar * 4) + 2)):
        s0 = i * bar
        if s0 > dur:
            break
        m = (t >= s0) & (t < s0 + bar)
        tt = t[m] - s0
        env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.4)
        for f in ch:
            out[m] += 0.05 * env * np.sin(2 * np.pi * f * tt) * (1 + 0.2 * np.sin(2 * np.pi * 0.5 * tt))
    # bombo suave y hi-hat
    for k in range(int(dur / beat) + 1):
        s0 = k * beat
        n0 = int(s0 * SR)
        n = int(0.18 * SR)
        if n0 + n > len(out):
            break
        tt = np.arange(n) / SR
        kick = 0.35 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18)
        out[n0:n0 + n] += kick
        h0 = int((s0 + beat / 2) * SR)
        hn = int(0.04 * SR)
        if h0 + hn < len(out):
            out[h0:h0 + hn] += 0.04 * np.random.randn(hn) * np.exp(-np.arange(hn) / SR * 80)
    return out.astype(np.float32)


def synth_whoosh():
    n = int(0.3 * SR)
    noise = np.random.randn(n).astype(np.float32)
    # filtro paso bajo que se abre (barrido)
    out = np.zeros(n, dtype=np.float32)
    y = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * (i / n)
        y += a * (noise[i] - y)
        out[i] = y
    env = np.sin(np.pi * np.arange(n) / n) ** 2
    return 0.5 * out * env


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- graficos

def make_background():
    y = np.linspace(0, 1, H)[:, None]
    grad = (np.array(C_BG1)[None, None, :] * (1 - y[..., None]) + np.array(C_BG2)[None, None, :] * y[..., None])
    img = np.repeat(grad, W, axis=1).astype(np.uint8)
    bg = Image.fromarray(img, "RGB")
    d = ImageDraw.Draw(bg)
    for x in range(0, W, 72):
        d.line([(x, 0), (x, H)], fill=(24, 33, 66), width=1)
    for yy in range(0, H, 72):
        d.line([(0, yy), (W, yy)], fill=(24, 33, 66), width=1)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-200, 900, 700, 1800), fill=(20, 60, 110))
    gd.ellipse((600, -100, 1400, 700), fill=(40, 30, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    bg = Image.blend(bg, Image.fromarray(np.clip(np.array(bg, dtype=np.int16) + np.array(glow, dtype=np.int16), 0, 255).astype(np.uint8)), 0.8)
    return bg


def draw_topbar(img, tag, source=""):
    d = ImageDraw.Draw(img)
    if source:
        d.text((W / 2, 207), source, font=font(F_MED, 28), fill=C_MUTED, anchor="mm")
    f = font(F_BOLD, 40)
    label = "IA SIN HUMO"
    tw = f.getlength(label)
    d.rounded_rectangle((60, 110, 60 + tw + 110, 186), radius=38, fill=(16, 24, 50), outline=C_CYAN, width=3)
    d.ellipse((84, 132, 116, 164), fill=C_CYAN)
    d.text((132, 148), label, font=f, fill=C_TEXT, anchor="lm")
    if tag:
        f2 = font(F_BOLD, 34)
        tw2 = f2.getlength(tag)
        x1 = 1020
        d.rounded_rectangle((x1 - tw2 - 60, 116, x1, 180), radius=32, fill=C_YELLOW)
        d.text((x1 - 30 - tw2 / 2, 148), tag, font=f2, fill=(20, 20, 30), anchor="mm")


def make_mascot(mouth, blink, look=0):
    """Mascota original 'Bit': robot redondo con antena. Devuelve RGBA 300x260."""
    im = Image.new("RGBA", (300, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # antena
    d.line([(150, 52), (150, 18)], fill=C_MUTED, width=6)
    d.ellipse((136, 4, 164, 32), fill=C_CYAN)
    # cuerpo
    d.rounded_rectangle((40, 50, 260, 240), radius=70, fill=(232, 238, 255), outline=(120, 140, 200), width=5)
    # pantalla cara
    d.rounded_rectangle((70, 85, 230, 200), radius=45, fill=(14, 20, 44))
    ex = 6 * look
    if blink:
        d.line([(102 + ex, 130), (128 + ex, 130)], fill=C_CYAN, width=7)
        d.line([(172 + ex, 130), (198 + ex, 130)], fill=C_CYAN, width=7)
    else:
        d.ellipse((100 + ex, 112, 130 + ex, 148), fill=C_CYAN)
        d.ellipse((170 + ex, 112, 200 + ex, 148), fill=C_CYAN)
    # boca
    mh = int(4 + mouth * 22)
    d.rounded_rectangle((128, 168 - mh // 2, 172, 168 + mh // 2 + 2), radius=8, fill=C_CYAN)
    # mejillas
    d.ellipse((76, 150, 96, 164), fill=(255, 120, 150))
    d.ellipse((204, 150, 224, 164), fill=(255, 120, 150))
    return im


# --- escenas: cada una produce una lista de elementos (imagen RGBA, x, y, t_aparicion)

def panel_base(accent=C_BORDER):
    x0, y0, x1, y1 = PANEL
    im = Image.new("RGBA", (x1 - x0 + 40, y1 - y0 + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 30, im.width - 20, im.height - 10), radius=56, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    im.alpha_composite(sh)
    ImageDraw.Draw(im).rounded_rectangle((20, 20, im.width - 20, im.height - 20), radius=52, fill=C_PANEL + (255,), outline=accent, width=4)
    return im


def text_block(lines, fnt, color, line_h, align="mm", width=880):
    h = int(line_h * len(lines)) + 20
    im = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        y = int(line_h * i + line_h / 2) + 10
        if align == "mm":
            d.text((width / 2, y), ln, font=fnt, fill=color, anchor="mm")
        else:
            d.text((0, y), ln, font=fnt, fill=color, anchor="lm")
    return im


def highlight_text(text, path, max_w, max_h, start, minimum, color, hl_color):
    """Texto centrado donde las palabras entre *asteriscos* van resaltadas."""
    raw = text.replace("*", "")
    fnt, lines, size = fit_text(raw, path, max_w, max_h, start, minimum)
    marked = set()
    inside = False
    for tok in text.split():
        st = tok.startswith("*")
        if st:
            inside = True
        if inside:
            marked.add(tok.strip("*").strip(".,:;!?¿¡"))
        if tok.endswith("*") or tok.rstrip(".,:;!?").endswith("*"):
            inside = False
    lh = size * 1.14
    im = Image.new("RGBA", (max_w, int(lh * len(lines)) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        y = int(lh * i + lh / 2) + 12
        total = fnt.getlength(ln)
        x = (max_w - total) / 2
        for j, w in enumerate(ln.split()):
            key = w.strip(".,:;!?¿¡")
            ww = fnt.getlength(w)
            if key in marked:
                d.rounded_rectangle((x - 10, y - size * 0.62, x + ww + 10, y + size * 0.58), radius=14, fill=hl_color)
                d.text((x, y), w, font=fnt, fill=(15, 15, 25), anchor="lm")
            else:
                d.text((x, y), w, font=fnt, fill=color, anchor="lm")
            x += ww + fnt.getlength(" ")
    return im


def build_scene(sc, line_starts, dur):
    """Devuelve (accent, elementos). line_starts: tiempos relativos de cada linea."""
    typ = sc.get("type", "title")
    x0, y0, x1, y1 = PANEL
    cx = (x0 + x1) // 2
    inner_w = x1 - x0 - 120
    els = []
    accent = C_BORDER

    def add(img, y, t, x=None):
        els.append((img, cx - img.width // 2 if x is None else x, y, t))

    def t_at(i):
        return line_starts[min(i, len(line_starts) - 1)] if line_starts else 0

    if sc.get("kicker"):
        f = font(F_BOLD, 40)
        add(text_block([sc["kicker"].upper()], f, C_CYAN, 56, width=inner_w), y0 + 50, 0)

    if typ in ("hook", "title", "cta"):
        accent = C_CYAN if typ != "cta" else C_YELLOW
        hl = highlight_text(sc.get("headline", ""), F_BOLD, inner_w, 600, 134, 60, C_TEXT, C_YELLOW)
        add(hl, y0 + 130 + max(0, (560 - hl.height) // 2), 0)
        if sc.get("sub"):
            f = font(F_MED, 44)
            ls = wrap(sc["sub"], f, inner_w)
            add(text_block(ls, f, C_MUTED, 58, width=inner_w), y1 - 90 - 58 * len(ls), t_at(1) if len(line_starts) > 1 else 0.4)
    elif typ == "stat":
        accent = C_CYAN
        f, ls, s = fit_text(sc.get("value", ""), F_BOLD, inner_w, 280, 230, 90)
        add(text_block(ls, f, C_CYAN, s * 1.05, width=inner_w), y0 + 170, 0)
        f2, ls2, s2 = fit_text(sc.get("label", ""), F_BOLD, inner_w, 300, 72, 44)
        add(text_block(ls2, f2, C_TEXT, s2 * 1.18, width=inner_w), y0 + 520, 0.35)
    elif typ == "bullets":
        accent = C_CYAN
        y = y0 + 60
        if sc.get("headline"):
            f, ls, s = fit_text(sc["headline"], F_BOLD, inner_w, 200, 70, 48)
            blk = text_block(ls, f, C_TEXT, s * 1.15, width=inner_w)
            add(blk, y + (60 if sc.get("kicker") else 0), 0)
            y += blk.height + (90 if sc.get("kicker") else 30)
        items = sc.get("items", [])[:4]
        avail = y1 - 50 - y
        step = avail / max(1, len(items))
        for i, it in enumerate(items):
            im = Image.new("RGBA", (inner_w, int(step) - 16), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((0, 0, im.width, im.height), radius=30, fill=(28, 40, 82))
            d.ellipse((24, im.height / 2 - 36, 96, im.height / 2 + 36), fill=C_YELLOW)
            d.text((60, im.height / 2), str(i + 1), font=font(F_BOLD, 44), fill=(20, 20, 30), anchor="mm")
            f, ls, s = fit_text(it, F_BOLD, inner_w - 160, im.height - 20, 58, 34)
            tb = text_block(ls, f, C_TEXT, s * 1.15, align="lm", width=inner_w - 150)
            im.alpha_composite(tb, (126, (im.height - tb.height) // 2))
            when = t_at(i + 1) if len(line_starts) > i + 1 else 0.25 + i * max(0.4, dur / (len(items) + 1))
            add(im, int(y + i * step), when)
    elif typ == "chat":
        accent = C_GREEN
        y = y0 + (130 if sc.get("kicker") else 60)
        msgs = sc.get("messages", [])[:4]
        for i, m in enumerate(msgs):
            user = m.get("role") == "user"
            f, ls, s = fit_text(m.get("text", ""), F_MED, 700, 300, 56, 36)
            tb = text_block(ls, f, (15, 15, 25) if user else C_TEXT, s * 1.2, align="lm", width=720)
            bw = int(max(f.getlength(l) for l in ls)) + 70
            bh = tb.height + 40
            im = Image.new("RGBA", (bw + 10, bh + 50), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.text((10, 18), m.get("name", "Tu" if user else "IA"), font=font(F_BOLD, 28), fill=C_MUTED, anchor="lm")
            d.rounded_rectangle((0, 40, bw, 40 + bh), radius=34, fill=C_CYAN if user else (36, 50, 98))
            im.alpha_composite(tb.crop((0, 0, bw - 40, tb.height)), (35, 60))
            xx = x1 - 50 - im.width if user else x0 + 50
            when = t_at(i) if i < len(line_starts) else 0.3 + i * 0.8
            els.append((im, xx, y, when))
            y += im.height + 24
            if y > y1 - 120:
                break
    elif typ == "versus":
        accent = C_YELLOW
        colw = (inner_w - 40) // 2
        for k, (lab, col, txt) in enumerate([(sc.get("left_label", "HUMO"), C_RED, sc.get("left", "")),
                                             (sc.get("right_label", "REALIDAD"), C_GREEN, sc.get("right", ""))]):
            im = Image.new("RGBA", (colw, 700), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((0, 0, colw, 700), radius=36, fill=(28, 40, 82), outline=col, width=5)
            d.rounded_rectangle((30, 30, colw - 30, 120), radius=26, fill=col)
            d.text((colw / 2, 75), lab, font=font(F_BOLD, 44), fill=(15, 15, 25), anchor="mm")
            f, ls, s = fit_text(txt, F_BOLD, colw - 60, 520, 52, 32)
            tb = text_block(ls, f, C_TEXT, s * 1.2, width=colw - 60)
            im.alpha_composite(tb, (30, 150 + (520 - tb.height) // 2))
            when = 0 if k == 0 else (t_at(1) if len(line_starts) > 1 else 0.8)
            els.append((im, x0 + 60 + k * (colw + 40), y0 + (150 if sc.get("kicker") else 90), when))
    return accent, els


# ---------------------------------------------------------------- subtitulos ASS

def ass_time(t):
    t = max(0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_escape(s):
    return s.replace("{", "(").replace("}", ")").replace("\\", "/")


def build_ass(word_events, path):
    head = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Cap,Poppins,92,&H00FFFFFF,&H00FFFFFF,&H00140A05,&H96000000,-1,0,0,0,100,100,0,0,1,7,3,2,90,90,{CAPTION_MARGIN_V},1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    out = [head]
    for chunk in word_events:
        words = chunk["words"]
        for i, (w, ws, we) in enumerate(words):
            end = words[i + 1][1] if i + 1 < len(words) else chunk["end"]
            parts = []
            for j, (w2, _, _) in enumerate(words):
                if j == i:
                    parts.append("{\\c&H3FD2FF&\\fscx112\\fscy112}" + ass_escape(w2) + "{\\c&HFFFFFF&\\fscx100\\fscy100}")
                else:
                    parts.append(ass_escape(w2))
            txt = " ".join(parts)
            if i == 0:
                txt = "{\\fad(60,0)}" + txt
            out.append(f"Dialogue: 0,{ass_time(ws)},{ass_time(end)},Cap,,0,0,0,,{txt}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out)


def word_timing(text, start, dur):
    words = text.split()
    weights = np.array([len(w.strip(".,;:!?¿¡")) + 2.5 for w in words], dtype=float)
    weights = weights / weights.sum() * dur
    out, t = [], start
    for w, d in zip(words, weights):
        out.append((w, t, t + d))
        t += d
    # agrupa en bloques de max 3 palabras / 20 caracteres, corta tras puntuacion
    chunks, cur = [], []
    for item in out:
        cur.append(item)
        txt = " ".join(x[0] for x in cur)
        if len(cur) >= 3 or len(txt) >= 18 or item[0][-1] in ".,;:!?":
            chunks.append({"words": cur, "end": cur[-1][2]})
            cur = []
    if cur:
        chunks.append({"words": cur, "end": cur[-1][2]})
    return chunks


# ---------------------------------------------------------------- render

def render(script_path, out_path, voices_dir):
    spec = json.load(open(script_path, encoding="utf-8"))
    vmap = spec.get("voices", {"A": "vits-piper-es_MX-claude-high", "B": "vits-piper-es_MX-ald-medium"})
    speed = float(spec.get("speed", 1.12))
    voices = Voices(voices_dir)
    tmp = tempfile.mkdtemp(prefix="ish_")

    # 1) voz y linea de tiempo
    voice_track = []
    t = 0.15
    timeline = []      # por escena: (inicio, fin, [inicios_lineas_relativos])
    word_events = []
    talk_mask = []     # (inicio, fin, speaker)
    for si, sc in enumerate(spec["scenes"]):
        s_start = t
        starts = []
        for ln in sc.get("lines", []):
            spk = ln.get("spk", "A")
            audio = voices.say(vmap.get(spk, vmap["A"]), ln.get("say", ln["text"]), speed)
            d = len(audio) / SR
            voice_track.append((t, audio))
            starts.append(t - s_start)
            word_events += word_timing(ln["text"], t, d)
            talk_mask.append((t, t + d, spk))
            t += d + GAP
        t = max(t, s_start + float(sc.get("min_dur", 1.2)))
        timeline.append((s_start, t, starts))
        t += SCENE_GAP
    total = t + float(spec.get("tail", 0.6))

    n = int(total * SR) + SR
    voice = np.zeros(n, dtype=np.float32)
    for st, a in voice_track:
        i = int(st * SR)
        voice[i:i + len(a)] += a[: n - i]
    peak = np.max(np.abs(voice)) or 1.0
    voice = voice / peak * 0.92

    music = synth_music(total + 1)[:n]
    music = np.pad(music, (0, max(0, n - len(music))))
    # ducking: baja la musica cuando hay voz
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
    duck = 1 - 0.6 * np.clip(env * 8, 0, 1)
    whoosh = synth_whoosh()
    fx = np.zeros(n, dtype=np.float32)
    for (s0, _, _) in timeline[1:]:
        i = max(0, int((s0 - 0.12) * SR))
        fx[i:i + len(whoosh)] += whoosh[: n - i]
    mix = voice + 0.55 * music * duck + 0.35 * fx
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.97)
    wav_path = os.path.join(tmp, "mix.wav")
    write_wav(wav_path, mix[: int(total * SR)])

    # energia de voz por frame para animar la boca
    nf = int(total * FPS)
    hop = SR // FPS
    energy = np.array([np.sqrt(np.mean(voice[i * hop:(i + 1) * hop] ** 2)) for i in range(nf)])
    energy = np.clip(energy / (np.percentile(energy[energy > 0], 90) if np.any(energy > 0) else 1), 0, 1)

    # 2) capas estaticas
    bg = make_background()
    draw_topbar(bg, spec.get("tag", ""), spec.get("source", ""))
    bg = bg.convert("RGBA")
    mascots = {(m, b): make_mascot(m / 3, b) for m in range(4) for b in (0, 1)}
    scenes = []
    for sc, (s0, s1, starts) in zip(spec["scenes"], timeline):
        accent, els = build_scene(sc, starts, s1 - s0)
        scenes.append((s0, s1, panel_base(accent), els))

    ass_path = os.path.join(tmp, "subs.ass")
    build_ass(word_events, ass_path)

    # 3) frames -> ffmpeg
    raw_path = os.path.join(tmp, "video.mp4")
    ff = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", wav_path,
        "-vf", f"ass={ass_path}:fontsdir={FONT_DIR}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", raw_path],
        stdin=subprocess.PIPE)
    fade_cache = {}

    def faded(img, a):
        key = (id(img), int(a * 10))
        if key not in fade_cache:
            im = img.copy()
            al = im.getchannel("A").point(lambda v: int(v * a))
            im.putalpha(al)
            fade_cache[key] = im
        return fade_cache[key]

    blink_frames = set()
    for k in range(int(total / 3.1) + 1):
        f0 = int((1.7 + k * 3.1) * FPS)
        blink_frames.update(range(f0, f0 + 4))

    for fi in range(nf):
        tt = fi / FPS
        frame = bg.copy()
        cur = None
        for s in scenes:
            if s[0] - 0.001 <= tt < s[1] + SCENE_GAP:
                cur = s
        if cur is None:
            cur = scenes[-1]
        s0, s1, pbase, els = cur
        lt = tt - s0
        slide = int((1 - ease_out(lt / 0.28)) * 220)
        px, py = PANEL[0] - 20 + slide, PANEL[1] - 20
        pb = pbase if px + pbase.width <= W else pbase.crop((0, 0, W - px, pbase.height))
        frame.alpha_composite(pb, (px, py))
        for img, ex, ey, et in els:
            if lt < et:
                continue
            p = ease_out((lt - et) / 0.25)
            dy = int((1 - p) * 40)
            im = img if p >= 1 else faded(img, max(0.05, p))
            x = ex + slide
            if x + im.width > W:
                im = im.crop((0, 0, max(1, W - x), im.height))
            frame.alpha_composite(im, (x, ey + dy))
        # mascota
        speaking_a = any(a <= tt <= b and spk == "A" for a, b, spk in talk_mask)
        m = int(round(energy[fi] * 3)) if speaking_a else 0
        mas = mascots[(min(3, m), 1 if fi in blink_frames else 0)]
        bob = int(math.sin(tt * 2 * math.pi * 0.9) * 8)
        frame.alpha_composite(mas, ((W - mas.width) // 2, MASCOT_Y + bob))
        # barra de progreso
        d = ImageDraw.Draw(frame)
        d.rectangle((0, 0, W, 10), fill=(30, 40, 80, 255))
        d.rectangle((0, 0, int(W * tt / total), 10), fill=C_CYAN + (255,))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    if ff.returncode != 0:
        sys.exit("ffmpeg fallo")
    os.replace(raw_path, out_path)
    meta = os.path.splitext(out_path)[0] + "_publicacion.txt"
    with open(meta, "w", encoding="utf-8") as f:
        f.write("TITULO:\n" + spec.get("title", "") + "\n\n")
        f.write("DESCRIPCION:\n" + spec.get("description", "") + "\n\n")
        f.write("HASHTAGS:\n" + " ".join(spec.get("hashtags", [])) + "\n\n")
        f.write("FUENTE:\n" + spec.get("source_url", spec.get("source", "")) + "\n")
        f.write(f"\nDURACION: {total:.1f} s\n")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--voices", default=os.environ.get("ISH_VOICES", "/home/claude/tts"))
    a = ap.parse_args()
    dur = render(a.script, a.out, a.voices)
    print(f"OK {a.out} {dur:.1f}s")


if __name__ == "__main__":
    main()
