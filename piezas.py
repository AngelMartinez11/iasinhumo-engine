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
    trazo = "" if "stroke=" in extra else 'stroke="none" '
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{peso}" '
            f'font-size="{size}" fill="{color}" {trazo}{extra}>{_esc(t)}</text>')


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

def sobre(color="#d81f26", texto="", disco=True):
    o = [f'<circle cx="40" cy="-60" r="95" fill="#e5e7eb"/><circle cx="40" cy="-60" r="22" fill="#94a3b8"/>' if disco else "",
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


# ------------------------------------------------------------------ piezas agregadas (historias)

def camara(tipo="antigua", color="#1f2937", texto=""):
    """tipo: antigua (de rollo), digital (compacta) o prototipo (caja grande con cassette)."""
    if tipo == "prototipo":
        o = ['<rect x="-230" y="-150" width="460" height="300" rx="18" fill="#94a3b8"/>',
             '<rect x="-210" y="-120" width="150" height="110" rx="10" fill="#475569"/>',
             '<circle cx="140" cy="-20" r="70" fill="#1f2937"/><circle cx="140" cy="-20" r="38" fill="#60a5fa"/>',
             '<rect x="-210" y="20" width="200" height="100" rx="8" fill="#1f2937"/>',
             '<circle cx="-160" cy="70" r="22" fill="#94a3b8"/><circle cx="-60" cy="70" r="22" fill="#94a3b8"/>',
             '<rect x="30" y="80" width="170" height="40" rx="6" fill="#64748b"/>']
        if texto:
            o.append(_txt(0, 210, texto, 44))
        return _g("".join(o)), (-240, -160, 240, 230 if texto else 160)
    cuerpo = "#e5e7eb" if tipo == "digital" else color
    o = [f'<rect x="-200" y="-110" width="400" height="230" rx="26" fill="{cuerpo}"/>',
         f'<rect x="-150" y="-150" width="110" height="50" rx="10" fill="{cuerpo}"/>']
    if tipo == "antigua":
        o.append('<rect x="-200" y="-20" width="400" height="40" fill="#a16207" stroke-width="4"/>')
    o += ['<circle cx="20" cy="5" r="88" fill="#334155"/><circle cx="20" cy="5" r="56" fill="#60a5fa"/>',
          '<circle cx="0" cy="-15" r="14" fill="#e0f2fe" stroke="none"/>',
          '<rect x="120" y="-90" width="56" height="30" rx="6" fill="#fde68a"/>']
    if texto:
        o.append(_txt(0, 200, texto, 44))
    return _g("".join(o)), (-210, -160, 210, 230 if texto else 130)


def rollo(texto="", color="#facc15"):
    o = [f'<rect x="-120" y="-150" width="240" height="300" rx="20" fill="{color}"/>',
         '<rect x="-150" y="-100" width="40" height="200" rx="8" fill="#1f2937"/>',
         '<path d="M120 -60 L300 -60 L300 60 L120 60 Z" fill="#7c2d12"/>']
    for k in range(5):
        o.append(f'<rect x="{140 + k * 32}" y="-50" width="18" height="16" fill="#fde68a" stroke-width="3"/>')
        o.append(f'<rect x="{140 + k * 32}" y="34" width="18" height="16" fill="#fde68a" stroke-width="3"/>')
    if texto:
        o.append(_txt(0, 20, texto, 54))
    return _g("".join(o)), (-160, -160, 310, 160)


def celda(ancho=520, alto=640, barrotes=7):
    """Rejas de una celda (transparente por dentro). Origen al centro abajo."""
    w, h = ancho, alto
    o = [f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="none" stroke-width="18"/>',
         f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="none" stroke="#64748b" stroke-width="10"/>']
    for k in range(1, barrotes):
        x = -w / 2 + k * w / barrotes
        o.append(f'<path d="M{x:.0f} {-h} L{x:.0f} 0" fill="none" stroke-width="16"/>')
        o.append(f'<path d="M{x:.0f} {-h} L{x:.0f} 0" fill="none" stroke="#94a3b8" stroke-width="8"/>')
    o.append(f'<path d="M{-w / 2} {-h * 0.55} L{w / 2} {-h * 0.55}" fill="none" stroke-width="16"/>')
    o.append(f'<path d="M{-w / 2} {-h * 0.55} L{w / 2} {-h * 0.55}" fill="none" stroke="#94a3b8" stroke-width="8"/>')
    return _g("".join(o)), (-w / 2 - 15, -h - 15, w / 2 + 15, 15)


def cama(cabeza=True, pelo="#3a2a1e", cobija="#64748b"):
    """Litera de celda con bulto bajo la cobija. Origen al centro abajo."""
    o = ['<rect x="-260" y="-210" width="520" height="40" rx="8" fill="#94a3b8"/>',
         '<rect x="-260" y="-170" width="24" height="170" fill="#64748b"/><rect x="236" y="-170" width="24" height="170" fill="#64748b"/>',
         '<rect x="-250" y="-250" width="120" height="44" rx="18" fill="#f8fafc"/>',
         f'<path d="M-140 -210 Q-120 -290 40 -285 Q220 -280 250 -210 Z" fill="{cobija}"/>']
    if cabeza:
        o.append('<ellipse cx="-175" cy="-280" rx="58" ry="52" fill="#f2c49b"/>')
        o.append(f'<path d="M-232 -285 Q-230 -345 -175 -342 Q-118 -342 -118 -290 Q-150 -318 -232 -285 Z" fill="{pelo}"/>')
        o.append('<path d="M-200 -278 L-180 -278 M-160 -278 L-140 -278" fill="none" stroke-width="5"/>')
    return _g("".join(o)), (-270, -360, 270, 10)


def isla(texto="", edificio=True, faro=True):
    """Isla rocosa con prision y faro. Origen al centro (nivel del agua)."""
    o = ['<path d="M-420 0 Q-380 -120 -220 -150 L220 -160 Q380 -130 430 0 Z" fill="#78716c"/>',
         '<path d="M-300 -140 Q-200 -175 0 -170 Q200 -175 300 -150" fill="none" stroke="#57534e" stroke-width="10"/>']
    if edificio:
        o.append('<rect x="-230" y="-330" width="380" height="180" fill="#e7e5e4"/>')
        for k in range(8):
            o.append(f'<rect x="{-205 + k * 44}" y="-300" width="22" height="40" fill="#334155" stroke-width="3"/>')
            o.append(f'<rect x="{-205 + k * 44}" y="-230" width="22" height="40" fill="#334155" stroke-width="3"/>')
    if faro:
        o.append('<path d="M200 -160 L220 -420 L260 -420 L280 -160 Z" fill="#f5f5f4"/>')
        o.append('<rect x="210" y="-470" width="60" height="50" fill="#fde047"/><path d="M200 -470 L240 -510 L280 -470 Z" fill="#1f2937"/>')
    if texto:
        o.append(_txt(0, 90, texto, 60, "#ffffff"))
    return _g("".join(o)), (-440, -520, 440, 120 if texto else 20)


def balsa(personas=3, color="#facc15"):
    """Balsa inflable de impermeables con personas. Origen al centro (nivel del agua)."""
    o = [f'<path d="M-280 -20 Q-300 -90 -230 -100 L230 -100 Q300 -90 280 -20 Q260 30 0 30 Q-260 30 -280 -20 Z" fill="{color}"/>',
         '<path d="M-200 -60 L200 -60" fill="none" stroke="#a16207" stroke-width="8"/>']
    for k in range(personas):
        x = -150 + k * 150
        o.append(f'<rect x="{x - 32}" y="-200" width="64" height="110" rx="20" fill="#475569"/>')
        o.append(f'<circle cx="{x}" cy="-235" r="38" fill="#f2c49b"/>')
        o.append(f'<path d="M{x - 38} -240 Q{x} -290 {x + 38} -240 Z" fill="#3a2a1e"/>')
    o.append('<path d="M150 -150 L260 -10" fill="none" stroke="#7c4a2d" stroke-width="14"/>')
    return _g("".join(o)), (-310, -290, 310, 40)


def cuchara():
    o = ['<ellipse cx="0" cy="-150" rx="55" ry="80" fill="#cbd5e1"/>',
         '<path d="M-14 -80 L-10 150 Q0 170 10 150 L14 -80 Z" fill="#cbd5e1"/>']
    return _g("".join(o)), (-70, -240, 70, 175)


def olas(ancho=1200, color="#1e3a8a"):
    """Franja de mar en primer plano. Origen arriba al centro."""
    w = ancho
    pts = " ".join(f"Q{-w / 2 + i * 100 + 50} {-30 if i % 2 else 10} {-w / 2 + (i + 1) * 100} 0" for i in range(int(w / 100)))
    o = [f'<path d="M{-w / 2} 0 {pts} L{w / 2} 500 L{-w / 2} 500 Z" fill="{color}"/>',
         f'<path d="M{-w / 2 + 80} 90 q60 -30 120 0 M{-w / 2 + 520} 170 q60 -30 120 0 M{-w / 2 + 900} 110 q60 -30 120 0" fill="none" stroke="#93c5fd" stroke-width="8"/>']
    return _g("".join(o)), (-w / 2 - 10, -40, w / 2 + 10, 510)


PIEZAS.update({"camara": camara, "rollo": rollo, "celda": celda, "cama": cama, "isla": isla,
               "balsa": balsa, "cuchara": cuchara, "olas": olas})


# ------------------------------------------------------------------ piezas agregadas (tecnologia y datos)

def pc_escritorio(texto="", pantalla="#0f172a", tinta="#4ade80", torre=True):
    """Computadora de escritorio de los 80: monitor CRT, teclado y torre. Ancla en la base."""
    o = []
    if torre:
        o += ['<rect x="250" y="-430" width="150" height="430" rx="10" fill="#e7e1cf"/>',
              '<rect x="270" y="-390" width="110" height="20" rx="4" fill="#94a3b8"/>',
              '<rect x="270" y="-350" width="110" height="20" rx="4" fill="#94a3b8"/>',
              '<circle cx="325" cy="-60" r="14" fill="#22c55e"/>']
    o += ['<rect x="-300" y="-560" width="500" height="400" rx="26" fill="#e7e1cf"/>',
          f'<rect x="-262" y="-524" width="424" height="300" rx="30" fill="{pantalla}"/>',
          '<rect x="-150" y="-160" width="200" height="50" fill="#d6cfb8"/>',
          '<rect x="-330" y="-110" width="560" height="110" rx="12" fill="#d6cfb8"/>']
    for f in range(3):
        for c in range(9):
            o.append(f'<rect x="{-310 + c * 58}" y="{-95 + f * 32}" width="46" height="22" rx="4" fill="#f5f1e6" stroke-width="3"/>')
    if texto:
        o.append(_txt(-50, -360, texto, 56, tinta))
    else:
        o.append(f'<rect x="-230" y="-380" width="40" height="40" fill="{tinta}" stroke="none"/>')
    return _g("".join(o)), (-340, -570, 410 if torre else 240, 10)


def maletin_pc(texto="", color="#d6cfb8", pantalla="#0f172a", tinta="#4ade80", abierto=True):
    """Computadora 'portatil' de maletin (Osborne, Compaq Portable): asa, pantallita y teclado al frente."""
    o = ['<path d="M-110 -470 Q-110 -540 0 -540 Q110 -540 110 -470" fill="none" stroke-width="18"/>',
         f'<rect x="-330" y="-470" width="660" height="470" rx="26" fill="{color}"/>',
         '<rect x="-290" y="-420" width="300" height="230" rx="12" fill="#a8a08a"/>',
         f'<rect x="-262" y="-396" width="244" height="182" rx="14" fill="{pantalla}"/>',
         '<rect x="50" y="-420" width="240" height="90" rx="8" fill="#a8a08a"/>',
         '<rect x="70" y="-390" width="200" height="16" rx="4" fill="#1f2937"/>',
         '<rect x="50" y="-310" width="240" height="90" rx="8" fill="#a8a08a"/>',
         '<rect x="70" y="-280" width="200" height="16" rx="4" fill="#1f2937"/>']
    if texto:
        o.append(_txt(-140, -290, texto, 40, tinta))
    if abierto:
        o.append('<path d="M-330 -150 L330 -150 L360 0 L-360 0 Z" fill="#cfc7ae"/>')
        for f in range(3):
            for c in range(12):
                o.append(f'<rect x="{-320 + c * 54}" y="{-135 + f * 42}" width="42" height="28" rx="4" fill="#f5f1e6" stroke-width="3"/>')
    return _g("".join(o)), (-370, -560, 370, 10)


def laptop_moderna(color="#cbd5e1", pantalla="#1e3a8a", texto=""):
    """Laptop delgada y abierta vista de frente. Ancla en la base."""
    o = [f'<path d="M-300 -430 L300 -430 Q316 -430 316 -414 L316 -30 L-316 -30 L-316 -414 Q-316 -430 -300 -430 Z" fill="{color}"/>',
         f'<rect x="-290" y="-406" width="580" height="356" rx="8" fill="{pantalla}"/>',
         f'<path d="M-380 -30 L380 -30 L360 0 L-360 0 Z" fill="{color}"/>',
         '<rect x="-60" y="-30" width="120" height="12" rx="6" fill="#94a3b8" stroke-width="3"/>']
    if texto:
        o.append(_txt(0, -205, texto, 64, "#ffffff"))
    return _g("".join(o)), (-390, -440, 390, 10)


def clamshell(abierto=True, color="#1f2937", tinta="#facc15", texto=""):
    """Laptop de bisagra de los 80 (GRiD Compass): pantalla de texto ambar sobre el teclado."""
    if not abierto:
        o = [f'<rect x="-330" y="-90" width="660" height="90" rx="14" fill="{color}"/>',
             '<path d="M-330 -45 L330 -45" fill="none" stroke-width="5"/>']
        return _g("".join(o)), (-340, -100, 340, 10)
    o = [f'<path d="M-300 -110 L-260 -470 L260 -470 L300 -110 Z" fill="{color}"/>',
         '<path d="M-250 -150 L-222 -430 L222 -430 L250 -150 Z" fill="#111827"/>',
         f'<rect x="-340" y="-110" width="680" height="110" rx="12" fill="{color}"/>']
    for f in range(2):
        for c in range(12):
            o.append(f'<rect x="{-322 + c * 54}" y="{-95 + f * 44}" width="42" height="30" rx="4" fill="#4b5563" stroke-width="3"/>')
    if texto:
        o.append(_txt(0, -280, texto, 46, tinta))
    else:
        for k in range(4):
            o.append(f'<rect x="-190" y="{-400 + k * 55}" width="{300 - k * 50}" height="16" fill="{tinta}" stroke="none"/>')
    return _g("".join(o)), (-350, -480, 350, 10)


def transbordador(color="#f8fafc"):
    """Transbordador espacial de lado, apuntando a la derecha. Origen en el centro."""
    o = [f'<path d="M-330 -40 L200 -40 Q330 -30 360 0 Q330 30 200 40 L-330 40 Z" fill="{color}"/>',
         '<path d="M-200 40 L0 40 L-150 150 L-270 150 Z" fill="#cbd5e1"/>',
         '<path d="M-330 -40 L-300 -170 L-230 -170 L-210 -40 Z" fill="#cbd5e1"/>',
         '<path d="M300 -22 Q330 -10 340 0 L300 0 Z" fill="#1f2937"/>',
         '<rect x="-370" y="-30" width="40" height="60" rx="6" fill="#64748b"/>',
         '<path d="M-370 -20 L-470 0 L-370 20 Z" fill="#fb923c"/>',
         '<path d="M-370 -10 L-430 0 L-370 10 Z" fill="#fde047" stroke-width="3"/>']
    for k in range(4):
        o.append(f'<rect x="{-120 + k * 70}" y="-24" width="40" height="16" rx="4" fill="#e2e8f0" stroke-width="3"/>')
    return _g("".join(o)), (-480, -180, 370, 160)


def bateria(nivel=0.8, color="#22c55e"):
    """Pila horizontal con nivel de carga (0 a 1). Origen en el centro."""
    w = 440 * max(0.05, min(1.0, nivel))
    o = ['<rect x="-250" y="-120" width="480" height="240" rx="30" fill="#ffffff"/>',
         '<rect x="230" y="-50" width="40" height="100" rx="10" fill="#ffffff"/>',
         f'<rect x="-230" y="-100" width="{w}" height="200" rx="18" fill="{color}" stroke-width="4"/>']
    return _g("".join(o)), (-260, -130, 280, 130)


def bascula(texto="", color="#e5e7eb"):
    """Bascula de piso con pantalla. Ancla en la base: el objeto pesado va encima (y - 90)."""
    o = [f'<rect x="-260" y="-90" width="520" height="90" rx="22" fill="{color}"/>',
         '<rect x="-110" y="-74" width="220" height="56" rx="10" fill="#111827"/>']
    if texto:
        o.append(_txt(0, -32, texto, 40, "#facc15"))
    return _g("".join(o)), (-270, -100, 270, 10)


def chapa(texto="", sub="", fondo="#1d1d2b", tinta="#f0c448"):
    """Placa pequena negra y dorada para datos cortos ('11 KG', '1981'). Origen en el centro."""
    size = 72
    w = max(len(texto) * size * 0.62, len(sub) * 17) + 80
    h = 130 if sub else 104
    o = [f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="14" fill="{fondo}" stroke="{tinta}" stroke-width="5"/>',
         _txt(0, (-6 if sub else 24), texto, size, tinta)]
    if sub:
        o.append(_txt(0, 44, sub.upper(), 26, "#ffffff", peso=700))
    return "".join(o), (-w / 2 - 6, -h / 2 - 6, w / 2 + 6, h / 2 + 6)


def libro(texto="", color="#7c3aed", abierto=False):
    """Libro o cuaderno (Dynabook, manuales). Origen en el centro."""
    if abierto:
        o = ['<path d="M0 -150 Q-120 -190 -300 -160 L-300 160 Q-120 130 0 170 Z" fill="#ffffff"/>',
             '<path d="M0 -150 Q120 -190 300 -160 L300 160 Q120 130 0 170 Z" fill="#ffffff"/>']
        for k in range(5):
            o.append(f'<path d="M-250 {-100 + k * 50} L-50 {-90 + k * 50}" fill="none" stroke-width="4"/>')
        if texto:
            o.append(_txt(150, 20, texto, 46))
        return _g("".join(o)), (-310, -200, 310, 180)
    o = [f'<rect x="-200" y="-260" width="400" height="520" rx="18" fill="{color}"/>',
         '<rect x="-200" y="-260" width="50" height="520" rx="10" fill="#1f2937" stroke-width="5"/>']
    if texto:
        o.append(_txt(25, 20, texto, 54, "#ffffff"))
    return _g("".join(o)), (-210, -270, 210, 270)


def nino(camisa="#f59e0b", pelo="#3a2a1e", piel="#f2c49b", cara="feliz", brazos="abajo"):
    """Persona pequena (nino). Ancla en los pies."""
    svg, caja = persona(camisa=camisa, pelo=pelo, piel=piel, cara=cara, brazos=brazos)
    return f'<g transform="scale(0.62)">{svg}</g>', tuple(v * 0.62 for v in caja)


PIEZAS.update({"pc_escritorio": pc_escritorio, "maletin_pc": maletin_pc, "laptop_moderna": laptop_moderna,
               "clamshell": clamshell, "transbordador": transbordador, "bateria": bateria,
               "bascula": bascula, "chapa": chapa, "libro": libro, "nino": nino})
