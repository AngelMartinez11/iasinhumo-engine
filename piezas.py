"""Biblioteca de piezas ilustradas para el motor v4 (estilo explainer 2D plano con contorno).

Cada pieza es una funcion que devuelve (svg, caja) donde:
  svg  = fragmento SVG dibujado en coordenadas locales
  caja = (x0, y0, x1, y1) limites del dibujo en coordenadas locales
El origen (0, 0) es el punto de anclaje: los pies para personas y objetos que
se apoyan en el suelo, y el centro para objetos flotantes.
"""
import math
import random

L = "#1d1d2b"          # tinta del contorno
SW = 7                 # grosor del contorno
FONT = "Poppins"

PIELES = ["#f2c49b", "#e0a878", "#c68a5c", "#8d5a3b", "#f5d0b0"]
PELOS = ["#3a2a1e", "#1f1f1f", "#a16207", "#6b4423", "#c9c9c9"]
CAMISAS = ["#3b82f6", "#f59e0b", "#22c55e", "#ef4444", "#8b5cf6", "#14b8a6", "#ec4899", "#64748b"]


def _esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _txt(x, y, t, size, color=L, peso=800, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{peso}" '
            f'font-size="{size}" fill="{color}" stroke="none" {extra}>{_esc(t)}</text>')


def _g(contenido, sw=SW):
    return (f'<g stroke="{L}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">'
            f'{contenido}</g>')


# ------------------------------------------------------------------ personas

def _cara(cara, piel):
    o = []
    ojos_y = -590
    if cara == "triste":
        o.append(f'<path d="M-44 -628 L-14 -620 M14 -620 L44 -628" fill="none"/>')
    elif cara == "enojado":
        o.append(f'<path d="M-46 -632 L-14 -616 M14 -616 L46 -632" fill="none"/>')
    elif cara == "sorpresa":
        o.append(f'<path d="M-46 -634 Q-30 -644 -14 -636 M14 -636 Q30 -644 46 -634" fill="none"/>')
    else:
        o.append(f'<path d="M-46 -624 L-16 -628 M16 -628 L46 -624" fill="none"/>')
    if cara == "sorpresa":
        o.append(f'<circle cx="-30" cy="{ojos_y}" r="12" fill="#fff"/><circle cx="30" cy="{ojos_y}" r="12" fill="#fff"/>')
        o.append(f'<circle cx="-30" cy="{ojos_y}" r="5" fill="{L}"/><circle cx="30" cy="{ojos_y}" r="5" fill="{L}"/>')
    else:
        o.append(f'<circle cx="-30" cy="{ojos_y}" r="9" fill="{L}" stroke="none"/><circle cx="30" cy="{ojos_y}" r="9" fill="{L}" stroke="none"/>')
    boca = {
        "sorpresa": '<ellipse cx="0" cy="-535" rx="17" ry="22" fill="#7a2e2e"/>',
        "feliz": '<path d="M-30 -550 Q0 -512 30 -550 Z" fill="#7a2e2e"/>',
        "risa": '<path d="M-26 -540 Q6 -528 30 -552" fill="none"/>',
        "triste": '<path d="M-24 -528 Q0 -548 24 -528" fill="none"/>',
        "enojado": '<path d="M-24 -532 L24 -532" fill="none"/>',
        "preocupado": '<path d="M-24 -532 Q-12 -540 0 -532 Q12 -524 24 -532" fill="none"/>',
    }.get(cara, '<path d="M-22 -536 L22 -538" fill="none"/>')
    o.append(boca)
    if cara in ("sorpresa", "preocupado"):
        o.append('<path d="M70 -640 q8 14 0 22 q-8 -8 0 -22 Z" fill="#7dd3fc" stroke-width="4"/>')
    return "".join(o)


def _pelo(estilo, color):
    if estilo == "calvo":
        return f'<path d="M-82 -585 Q-86 -620 -70 -628 M82 -585 Q86 -620 70 -628" fill="none" stroke="{color}" stroke-width="16"/>'
    if estilo == "largo":
        return (f'<path d="M-86 -600 Q-96 -705 0 -705 Q96 -705 86 -600 L92 -500 Q70 -490 62 -520 L64 -610 '
                f'Q20 -660 -40 -640 L-64 -610 L-62 -520 Q-70 -490 -92 -500 Z" fill="{color}"/>')
    if estilo == "canoso":
        color = "#d4d4d8"
    if estilo == "gorra":
        return (f'<path d="M-86 -606 Q-88 -700 0 -700 Q88 -700 86 -606 Z" fill="{color}"/>'
                f'<path d="M30 -612 L130 -608 Q132 -592 86 -596 Z" fill="{color}"/>')
    return f'<path d="M-84 -600 Q-90 -702 0 -702 Q95 -702 86 -600 Q60 -655 -10 -640 Q-50 -662 -84 -600 Z" fill="{color}"/>'


_BRAZOS = {
    "abajo": ([(-66, -440), (-90, -290)], [(66, -440), (90, -290)]),
    "arriba": ([(-62, -440), (-150, -560), (-170, -660)], [(62, -440), (150, -560), (170, -660)]),
    "cabeza": ([(-62, -440), (-150, -520), (-96, -640)], [(62, -440), (150, -520), (96, -640)]),
    "senala": ([(-66, -440), (-90, -290)], [(62, -440), (190, -470), (300, -500)]),
    "cruzados": ([(-62, -440), (-70, -360), (50, -380)], [(62, -440), (70, -360), (-50, -380)]),
    "telefono": ([(-66, -440), (-95, -300)], [(62, -440), (110, -360), (40, -330)]),
    "saluda": ([(-66, -440), (-90, -290)], [(62, -440), (150, -540), (150, -650)]),
    "objeto": ([(-62, -440), (-60, -330), (-20, -330)], [(62, -440), (60, -330), (20, -330)]),
}


def persona(camisa="#3b82f6", pelo="#3a2a1e", piel="#f2c49b", pantalon="#2b3a67", cara="serio",
            brazos="abajo", ropa="camiseta", corbata="#ef4444", peinado="corto", lentes=False, sandalias=False):
    """Personaje de cuerpo entero. Origen en los pies. Alto aprox. 710."""
    torso_color = "#2b2f3f" if ropa == "traje" else ("#f8fafc" if ropa == "bata" else camisa)
    if ropa == "traje":
        pantalon = "#2b2f3f"
    g = []
    g.append(f'<rect x="-52" y="-250" width="44" height="240" fill="{pantalon}"/>')
    g.append(f'<rect x="8" y="-250" width="44" height="240" fill="{pantalon}"/>')
    if sandalias:
        g.append(f'<rect x="-64" y="-12" width="58" height="14" rx="6" fill="#a16207"/><rect x="6" y="-12" width="58" height="14" rx="6" fill="#a16207"/>')
    else:
        g.append(f'<rect x="-64" y="-22" width="60" height="26" rx="12" fill="{L}"/><rect x="4" y="-22" width="60" height="26" rx="12" fill="{L}"/>')
    izq, der = _BRAZOS.get(brazos, _BRAZOS["abajo"])
    for brazo in (izq, der):
        pts = " ".join(f"L{x} {y}" for x, y in brazo[1:])
        g.append(f'<path d="M{brazo[0][0]} {brazo[0][1]} {pts}" fill="none" stroke="{L}" stroke-width="{40 + 2 * SW}"/>')
        g.append(f'<path d="M{brazo[0][0]} {brazo[0][1]} {pts}" fill="none" stroke="{torso_color}" stroke-width="40"/>')
    g.append(f'<path d="M-72 -470 Q-80 -260 -60 -240 L60 -240 Q80 -260 72 -470 Q0 -500 -72 -470 Z" fill="{torso_color}"/>')
    if ropa == "traje":
        g.append(f'<path d="M-22 -478 L0 -420 L22 -478 Z" fill="#f8fafc" stroke-width="4"/>')
        g.append(f'<path d="M-8 -470 L8 -470 L12 -330 L0 -310 L-12 -330 Z" fill="{corbata}" stroke-width="4"/>')
    if ropa == "bata":
        g.append(f'<path d="M0 -480 L0 -244" fill="none" stroke-width="4"/>')
    for brazo in (izq, der):
        hx, hy = brazo[-1]
        g.append(f'<circle cx="{hx}" cy="{hy}" r="24" fill="{piel}"/>')
    if brazos == "telefono":
        g.append(f'<rect x="0" y="-410" width="58" height="96" rx="10" fill="#26263a"/><rect x="9" y="-398" width="40" height="66" rx="5" fill="#7dd3fc" stroke="none"/>')
        g.append(f'<circle cx="40" cy="-330" r="24" fill="{piel}"/>')
    g.append(f'<rect x="-20" y="-505" width="40" height="45" fill="{piel}"/>')
    g.append(f'<ellipse cx="0" cy="-590" rx="82" ry="96" fill="{piel}"/>')
    g.append(_pelo(peinado, pelo))
    g.append(_cara(cara, piel))
    if lentes:
        g.append('<circle cx="-30" cy="-590" r="22" fill="none" stroke-width="5"/><circle cx="30" cy="-590" r="22" fill="none" stroke-width="5"/><path d="M-8 -590 L8 -590" stroke-width="5"/>')
    return _g("".join(g)), (-200, -720, 320, 10)


def multitud(n=24, filas=3, semilla=1, ancho=900, escala=0.32, cara="serio", camisa=None):
    """Grupo de personas en filas. Origen al centro abajo."""
    rnd = random.Random(semilla)
    por_fila = max(1, math.ceil(n / filas))
    out, k = [], 0
    for f in range(filas):
        s = escala * (0.82 + 0.09 * f)
        y = -((filas - 1 - f) * 70)
        cnt = min(por_fila, n - k)
        for i in range(cnt):
            x = -ancho / 2 + (i + 0.5 + (0.5 if f % 2 else 0)) * ancho / (por_fila + 0.5)
            svg, _ = persona(camisa=camisa or rnd.choice(CAMISAS), pelo=rnd.choice(PELOS), piel=rnd.choice(PIELES),
                             cara=cara, peinado=rnd.choice(["corto", "corto", "largo", "calvo"]))
            out.append(f'<g transform="translate({x:.0f},{y}) scale({s:.3f})">{svg}</g>')
            k += 1
    return "".join(out), (-ancho / 2 - 80, -260 - (filas - 1) * 70, ancho / 2 + 80, 10)


# ------------------------------------------------------------------ edificios

def tienda(texto="TIENDA", letrero="#1e3a8a", letra="#ffd23f", pared="#f1e9da", ancho=620):
    """Fachada de tienda. Origen al centro abajo."""
    w = ancho
    h = 520
    o = [f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="{pared}"/>',
         f'<rect x="{-w / 2 - 20}" y="{-h - 40}" width="{w + 40}" height="140" rx="12" fill="{letrero}"/>',
         _txt(0, -h + 50, texto, min(84, int(w / max(4, len(texto)) * 1.25)), letra),
         f'<rect x="-70" y="-250" width="140" height="250" fill="#94a3b8"/>',
         f'<path d="M0 -250 L0 0" fill="none" stroke-width="5"/>']
    for sx in (-1, 1):
        x0 = sx * (w / 2 - 40) - (170 if sx > 0 else 0)
        o.append(f'<rect x="{x0}" y="-300" width="170" height="210" fill="#bfdbfe"/>')
        for j, c in enumerate(["#ef4444", "#22c55e", "#f59e0b"]):
            o.append(f'<rect x="{x0 + 14 + j * 52}" y="-280" width="42" height="64" fill="{c}" stroke-width="4"/>')
    o.append(f'<path d="M{-w / 2 - 30} -360 L{w / 2 + 30} -360 L{w / 2} -320 L{-w / 2} -320 Z" fill="{letrero}"/>')
    return _g("".join(o)), (-w / 2 - 40, -h - 50, w / 2 + 40, 10)


def edificio(texto="", pisos=8, color="#cbd5e1", ancho=320, ventana="#fde68a", letrero="#334155"):
    """Edificio de oficinas. Origen al centro abajo."""
    w = ancho
    h = 90 * pisos + 60
    o = [f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="{color}"/>']
    cols = max(2, int(w / 80))
    for p in range(pisos):
        for c in range(cols):
            x = -w / 2 + 22 + c * (w - 44) / cols
            o.append(f'<rect x="{x:.0f}" y="{-h + 70 + p * 90}" width="{(w - 44) / cols - 16:.0f}" height="56" fill="{ventana}" stroke-width="4"/>')
    o.append(f'<rect x="-40" y="-90" width="80" height="90" fill="#64748b"/>')
    if texto:
        o.append(f'<rect x="{-w / 2 + 20}" y="{-h - 70}" width="{w - 40}" height="70" rx="10" fill="{letrero}"/>')
        o.append(_txt(0, -h - 22, texto, min(44, int((w - 60) / max(3, len(texto)) * 1.5)), "#ffffff"))
    return _g("".join(o)), (-w / 2 - 10, -h - 80, w / 2 + 10, 10)


def oficina_interior(pared="#e9d8b8", rayas="#dcc79f", piso="#a47148"):
    """Fondo de oficina para reuniones (dibujado a pantalla completa, origen 0,0 arriba-izquierda)."""
    o = [f'<rect x="0" y="0" width="1080" height="1920" fill="{pared}" stroke="none"/>']
    for i in range(0, 1080, 90):
        o.append(f'<rect x="{i}" y="0" width="45" height="1500" fill="{rayas}" stroke="none"/>')
    o.append(f'<rect x="0" y="1500" width="1080" height="420" fill="{piso}" stroke="none"/>')
    o.append(f'<rect x="700" y="560" width="300" height="420" fill="#bae6fd"/><path d="M850 560 L850 980 M700 770 L1000 770" fill="none"/>')
    return _g("".join(o)), (0, 0, 1080, 1920)


def mesa(ancho=760):
    w = ancho
    o = [f'<rect x="{-w / 2}" y="-230" width="{w}" height="40" rx="10" fill="#7c4a2d"/>',
         f'<rect x="{-w / 2 + 40}" y="-190" width="30" height="190" fill="#5b3420"/>',
         f'<rect x="{w / 2 - 70}" y="-190" width="30" height="190" fill="#5b3420"/>']
    return _g("".join(o)), (-w / 2 - 10, -240, w / 2 + 10, 10)


# ------------------------------------------------------------------ objetos

def sobre(color="#d81f26", texto=""):
    o = [f'<circle cx="40" cy="-60" r="95" fill="#e5e7eb"/><circle cx="40" cy="-60" r="22" fill="#94a3b8"/>',
         f'<rect x="-170" y="-110" width="340" height="220" rx="12" fill="{color}"/>',
         f'<path d="M-170 -100 L0 20 L170 -100" fill="none" stroke="#7f1d1d"/>']
    if texto:
        o.append(_txt(0, 85, texto, 38, "#ffffff"))
    return _g("".join(o)), (-180, -165, 180, 120)


def vhs(etiqueta="", color="#1f2937"):
    o = [f'<rect x="-200" y="-115" width="400" height="230" rx="16" fill="{color}"/>',
         f'<rect x="-150" y="-80" width="300" height="80" rx="8" fill="#f8fafc"/>',
         f'<circle cx="-70" cy="55" r="34" fill="#475569"/><circle cx="70" cy="55" r="34" fill="#475569"/>']
    if etiqueta:
        o.append(_txt(0, -28, etiqueta, 34))
    return _g("".join(o)), (-210, -125, 210, 125)


def disco():
    o = ['<circle r="150" fill="#e2e8f0"/>', '<circle r="150" fill="none" stroke="#a5b4fc" stroke-width="18" opacity=".5"/>',
         '<circle r="34" fill="#94a3b8"/>', '<circle r="12" fill="#f8fafc"/>']
    return _g("".join(o)), (-160, -160, 160, 160)


def billetes(n=3):
    o = []
    for i in range(n):
        y = -i * 28
        o.append(f'<rect x="-190" y="{y - 90}" width="380" height="180" rx="12" fill="#86efac"/>')
        o.append(f'<circle cx="0" cy="{y}" r="50" fill="#bbf7d0"/>')
        o.append(_txt(0, y + 24, "$", 70, "#166534"))
    return _g("".join(o)), (-200, -100 - (n - 1) * 28, 200, 100)


def bolsa_dinero(texto="$"):
    o = ['<path d="M-60 -250 L60 -250 L30 -190 L-30 -190 Z" fill="#d6b88a"/>',
         '<path d="M-30 -190 Q-200 -120 -170 0 L170 0 Q200 -120 30 -190 Z" fill="#e7c98f"/>',
         '<path d="M-40 -195 L40 -195" fill="none" stroke="#7c5a2b" stroke-width="16"/>',
         _txt(0, -40, texto, 120, "#166534")]
    return _g("".join(o)), (-190, -260, 190, 10)


def reloj(hora=3):
    a = math.radians(hora * 30 - 90)
    o = ['<circle r="150" fill="#f8fafc"/>', '<circle r="150" fill="none" stroke="#ef4444" stroke-width="22"/>',
         f'<path d="M0 0 L{70 * math.cos(a):.0f} {70 * math.sin(a):.0f}" fill="none" stroke-width="14"/>',
         '<path d="M0 0 L0 -105" fill="none" stroke-width="10"/>', '<circle r="12" fill="#1d1d2b"/>']
    for k in range(12):
        b = math.radians(k * 30)
        o.append(f'<circle cx="{120 * math.cos(b):.0f}" cy="{120 * math.sin(b):.0f}" r="7" fill="{L}" stroke="none"/>')
    return _g("".join(o)), (-170, -170, 170, 170)


def calendario(texto="2000", color="#ef4444"):
    o = [f'<rect x="-170" y="-150" width="340" height="300" rx="20" fill="#f8fafc"/>',
         f'<rect x="-170" y="-150" width="340" height="80" rx="20" fill="{color}"/>',
         f'<rect x="-170" y="-90" width="340" height="20" fill="{color}" stroke="none"/>',
         '<rect x="-110" y="-175" width="18" height="50" rx="8" fill="#94a3b8"/><rect x="92" y="-175" width="18" height="50" rx="8" fill="#94a3b8"/>',
         _txt(0, 70, texto, 110)]
    return _g("".join(o)), (-180, -185, 180, 160)


def telefono(texto="", color="#6d5dfc", play=False):
    o = ['<rect x="-150" y="-300" width="300" height="600" rx="46" fill="#2a2a3d"/>',
         '<rect x="-128" y="-272" width="256" height="544" rx="30" fill="#f5f3ff" stroke-width="5"/>',
         f'<rect x="-128" y="-272" width="256" height="120" rx="30" fill="{color}" stroke-width="5"/>']
    if texto:
        o.append(_txt(0, -200, texto, 34, "#ffffff"))
    if play:
        o.append('<circle cx="0" cy="40" r="80" fill="#ef4444"/><path d="M-26 0 L44 40 L-26 80 Z" fill="#fff" stroke="none"/>')
    return _g("".join(o)), (-160, -310, 160, 310)


def tv(play=True, color="#d81f26", texto=""):
    o = ['<rect x="-300" y="-200" width="600" height="380" rx="24" fill="#1f2937"/>',
         '<rect x="-270" y="-172" width="540" height="324" rx="12" fill="#0f172a" stroke-width="4"/>',
         '<path d="M-80 180 L-120 250 M80 180 L120 250" fill="none"/>']
    if play:
        o.append(f'<circle cx="0" cy="-10" r="80" fill="{color}"/><path d="M-26 -50 L44 -10 L-26 30 Z" fill="#fff" stroke="none"/>')
    if texto:
        o.append(_txt(0, 120, texto, 40, "#ffffff"))
    return _g("".join(o)), (-310, -210, 310, 260)


def laptop(texto="", color="#d81f26"):
    o = ['<rect x="-260" y="-320" width="520" height="330" rx="20" fill="#334155"/>',
         '<rect x="-235" y="-296" width="470" height="282" rx="8" fill="#0f172a" stroke-width="4"/>',
         '<path d="M-320 10 L320 10 L290 50 L-290 50 Z" fill="#94a3b8"/>']
    if texto:
        o.append(_txt(0, -140, texto, 64, color))
    return _g("".join(o)), (-330, -330, 330, 60)


def avion(color="#f8fafc"):
    o = [f'<path d="M-260 0 Q-260 -50 -200 -50 L200 -50 Q290 -40 300 0 Q290 40 200 50 L-200 50 Q-260 50 -260 0 Z" fill="{color}"/>',
         '<path d="M-40 -40 L60 -190 L120 -190 L80 -40 Z" fill="#cbd5e1"/>',
         '<path d="M-40 40 L60 190 L120 190 L80 40 Z" fill="#cbd5e1"/>',
         '<path d="M-250 -20 L-300 -120 L-240 -120 L-190 -40 Z" fill="#ef4444"/>']
    for k in range(5):
        o.append(f'<circle cx="{-120 + k * 60}" cy="-8" r="14" fill="#7dd3fc"/>')
    return _g("".join(o)), (-310, -200, 310, 200)


def grafica(tipo="baja", color="#ef4444", barras=5):
    o = ['<path d="M-300 -360 L-300 0 L320 0" fill="none" stroke-width="10"/>']
    for i in range(barras):
        frac = (i + 1) / barras if tipo == "sube" else (barras - i) / barras
        h = 60 + 260 * frac
        o.append(f'<rect x="{-270 + i * 118}" y="{-h}" width="90" height="{h}" fill="{color}"/>')
    if tipo == "sube":
        o.append('<path d="M-270 -120 L-60 -200 L100 -180 L280 -380" fill="none" stroke-width="16"/><path d="M280 -380 L230 -370 M280 -380 L276 -330" fill="none" stroke-width="16"/>')
    else:
        o.append('<path d="M-270 -380 L-60 -250 L100 -280 L280 -90" fill="none" stroke-width="16"/><path d="M280 -90 L232 -104 M280 -90 L272 -140" fill="none" stroke-width="16"/>')
    return _g("".join(o)), (-320, -400, 340, 20)


def lapida(texto="RIP", sub=""):
    o = ['<path d="M-170 0 L-170 -300 Q-170 -420 0 -420 Q170 -420 170 -300 L170 0 Z" fill="#cbd5e1"/>',
         '<rect x="-220" y="-20" width="440" height="40" rx="10" fill="#65a30d"/>',
         _txt(0, -280, texto, 70, "#334155")]
    if sub:
        o.append(_txt(0, -190, sub, 48, "#334155"))
    return _g("".join(o)), (-230, -430, 230, 30)


def pin(texto="", color="#ef4444"):
    o = [f'<path d="M0 0 Q-120 -150 -120 -230 A120 120 0 1 1 120 -230 Q120 -150 0 0 Z" fill="{color}"/>',
         '<circle cx="0" cy="-235" r="50" fill="#fff"/>']
    if texto:
        o.append(f'<rect x="-210" y="20" width="420" height="80" rx="16" fill="#fff"/>')
        o.append(_txt(0, 75, texto, 44))
    return _g("".join(o)), (-220, -360, 220, 110)


def globo():
    o = ['<circle r="300" fill="#60a5fa"/>',
         '<path d="M-200 -150 Q-120 -230 -40 -180 Q20 -120 -60 -60 Q-140 -20 -200 -80 Z" fill="#4ade80"/>',
         '<path d="M40 20 Q140 -40 220 30 Q240 140 140 180 Q60 160 40 20 Z" fill="#4ade80"/>',
         '<path d="M-160 120 Q-100 90 -60 150 Q-80 220 -150 200 Z" fill="#4ade80"/>']
    return _g("".join(o)), (-310, -310, 310, 310)


def icono(tipo="x", color=None):
    if tipo == "check":
        c = color or "#22c55e"
        o = [f'<circle r="110" fill="{c}"/>', '<path d="M-50 0 L-12 40 L56 -40" fill="none" stroke="#fff" stroke-width="26"/>']
    elif tipo == "pregunta":
        c = color or "#ffd23f"
        o = [f'<circle r="110" fill="{c}"/>', _txt(0, 50, "?", 150)]
    elif tipo == "exclamacion":
        c = color or "#ef4444"
        o = [f'<path d="M0 -120 L120 100 L-120 100 Z" fill="{c}"/>', _txt(0, 80, "!", 140, "#fff")]
    else:
        c = color or "#ef4444"
        o = [f'<path d="M-110 -80 L-80 -110 L0 -30 L80 -110 L110 -80 L30 0 L110 80 L80 110 L0 30 L-80 110 L-110 80 L-30 0 Z" fill="{c}"/>']
    return _g("".join(o)), (-130, -130, 130, 130)


def flecha(color="#ffd23f", largo=300, rot=0):
    o = [f'<g transform="rotate({rot})"><path d="M{-largo / 2} -30 L{largo / 2 - 70} -30 L{largo / 2 - 70} -80 L{largo / 2} 0 '
         f'L{largo / 2 - 70} 80 L{largo / 2 - 70} 30 L{-largo / 2} 30 Z" fill="{color}"/></g>']
    r = largo / 2 + 20
    return _g("".join(o)), (-r, -r, r, r)


def linea_tiempo(pasos=("2000", "2004", "2010"), activo=0, ancho=760):
    xs = [(-ancho / 2) + i * ancho / max(1, len(pasos) - 1) for i in range(len(pasos))]
    o = [f'<path d="M{xs[0]} 0 L{xs[-1]} 0" fill="none" stroke-width="12"/>']
    for i, (x, t) in enumerate(zip(xs, pasos)):
        fill = "#6d5dfc" if i <= activo else "#ffffff"
        o.append(f'<circle cx="{x}" cy="0" r="36" fill="{fill}" stroke-width="10"/>')
        o.append(_txt(x, 105, t, 54))
    return _g("".join(o)), (xs[0] - 90, -50, xs[-1] + 90, 130)


def robot(color="#e8eeff"):
    """Mascota de IA SinHumo."""
    o = ['<path d="M0 -150 L0 -195" fill="none" stroke-width="8"/><circle cx="0" cy="-205" r="16" fill="#3ddcff"/>',
         f'<rect x="-120" y="-150" width="240" height="210" rx="78" fill="{color}"/>',
         '<rect x="-88" y="-112" width="176" height="126" rx="50" fill="#0e142c"/>',
         '<circle cx="-36" cy="-58" r="18" fill="#3ddcff" stroke="none"/><circle cx="36" cy="-58" r="18" fill="#3ddcff" stroke="none"/>',
         '<rect x="-24" y="-16" width="48" height="12" rx="6" fill="#3ddcff" stroke="none"/>']
    return _g("".join(o)), (-130, -225, 130, 70)


# ------------------------------------------------------------------ textos

def etiqueta(texto="NUEVO", fondo="#ffd23f", tinta=L, size=64, rot=-5):
    w = len(texto) * size * 0.66 + 80
    h = size + 48
    o = (f'<g transform="rotate({rot})">'
         f'<rect x="{-w / 2 + 9}" y="{-h / 2 + 11}" width="{w}" height="{h}" rx="16" fill="{tinta}" stroke="none"/>'
         f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="16" fill="{fondo}" stroke="{tinta}" stroke-width="9"/>'
         + _txt(0, size * 0.36, texto, size, tinta) + "</g>")
    r = math.hypot(w, h) / 2 + 20
    return o, (-r, -r * 0.75, r, r * 0.75)


def nombre(texto="", sub="", fondo="#1d1d2b"):
    """Rotulo tipo 'Vicente Sotelo / electricista'. Origen en el centro."""
    w = max(len(texto) * 30, len(sub) * 18) + 80
    o = [f'<rect x="{-w / 2}" y="-60" width="{w}" height="{120 if sub else 84}" rx="10" fill="{fondo}" stroke="#ffd23f" stroke-width="5"/>',
         _txt(0, -5, texto, 50, "#ffffff")]
    if sub:
        o.append(_txt(0, 42, sub.upper(), 28, "#ffd23f", peso=700))
    return "".join(o), (-w / 2 - 10, -70, w / 2 + 10, 70)


def texto(texto="", size=90, color=L, contorno="#ffffff"):
    w = len(texto) * size * 0.62 + 40
    o = _txt(0, size * 0.36, texto, size, color, extra=f'stroke="{contorno}" stroke-width="{size * 0.16:.0f}" paint-order="stroke"')
    return o, (-w / 2, -size, w / 2, size * 0.7)


PIEZAS = {
    "persona": persona, "multitud": multitud, "tienda": tienda, "edificio": edificio, "mesa": mesa,
    "sobre": sobre, "vhs": vhs, "disco": disco, "billetes": billetes, "bolsa_dinero": bolsa_dinero,
    "reloj": reloj, "calendario": calendario, "telefono": telefono, "tv": tv, "laptop": laptop,
    "avion": avion, "grafica": grafica, "lapida": lapida, "pin": pin, "globo": globo, "icono": icono,
    "flecha": flecha, "linea_tiempo": linea_tiempo, "robot": robot, "etiqueta": etiqueta,
    "nombre": nombre, "texto": texto, "oficina_interior": oficina_interior,
}
