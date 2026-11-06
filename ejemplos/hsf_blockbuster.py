"""Genera ejemplos/hsf_blockbuster.json: guion de ejemplo del canal Historias Sin Filtro (motor v4)."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

CEO = {"ropa": "traje", "corbata": "#ef4444", "pelo": "#6b4423", "peinado": "corto"}
REED = {"camisa": "#64748b", "sandalias": True, "pelo": "#3a2a1e"}
MARC = {"camisa": "#14b8a6", "sandalias": True, "pelo": "#a16207", "lentes": True}
TIENDA = {"texto": "BLOCKBUSTER", "letrero": "#1e3a8a", "letra": "#ffffff"}


def L(*txts, pausa=0):
    out = [{"text": t} for t in txts]
    if pausa:
        out[-1]["pausa"] = pausa
    return out


def it(p, x=540, y=1560, s=1.0, at=0, delay=0, anim=None, id=None, **a):
    d = {"p": p, "x": x, "y": y, "s": s, "at": at, "delay": delay, "a": a}
    if anim:
        d["anim"] = anim
    if id:
        d["id"] = id
    return d


def rayos(p):
    return {"tipo": "rayos", "paleta": p}


escenas = [
    # gancho
    {"fondo": rayos("azul"), "lines": L("En el año 2000, a Blockbuster le ofrecieron comprar Netflix por 50 millones de dólares."),
     "items": [it("tienda", 320, 1560, 0.72, id="tienda", anim="crece", **TIENDA),
               it("sobre", 820, 1250, 0.9, delay=1.6, anim="drop", id="sobre", texto="NETFLIX")],
     "dato": {"num": 50, "pre": "$", "suf": " MILLONES", "texto": "EL PRECIO DE NETFLIX", "y": 560, "delay": 2.6},
     "cam": {"z": [1.0, 1.06], "f": [540, 1150]}},
    {"sigue": True, "quita": ["sobre"], "lines": L("Y el director de Blockbuster casi se ríe en su cara."),
     "items": [it("persona", 800, 1560, 0.85, anim="right", id="ceo", cara="risa", brazos="cruzados", **CEO),
               it("etiqueta", 760, 760, 0.9, delay=0.8, texto="¿50 MILLONES?", rot=6)]},
    {"fondo": rayos("rojo"), "lines": L("Hoy Netflix factura más de 30 mil millones de dólares al año."),
     "items": [it("tv", 540, 1000, 1.05, anim="pop", texto="NETFLIX")],
     "dato": {"num": 30000, "pre": "$", "suf": " MILLONES", "texto": "AL AÑO", "y": 1330, "delay": 0.5}},
    {"fondo": {"tipo": "noche"}, "lines": L("Y de Blockbuster queda una sola tienda en todo el planeta.", pausa=0.3),
     "items": [it("tienda", 540, 1560, 0.9, anim="crece", **TIENDA),
               it("etiqueta", 540, 760, 1.0, delay=1.4, texto="1 TIENDA", fondo="#ffd23f")],
     "cam": {"z": [1.18, 1.0], "f": [540, 1250]}},
    {"fondo": rayos("oro"), "lines": L("¿Cómo se pierde un imperio así? Esta es la historia."),
     "items": [it("icono", 540, 1050, 1.7, anim="pop", tipo="pregunta")]},

    {"capitulo": {"t": "EL IMPERIO", "n": 1}, "min_dur": 1.7},
    {"fondo": rayos("azul"), "lines": L("En su mejor momento, en 2004, Blockbuster tenía más de 9 mil tiendas en el mundo."),
     "items": [it("tienda", 190, 1560, 0.42, id="t1", anim="crece", **TIENDA),
               it("tienda", 540, 1560, 0.42, id="t2", delay=0.35, anim="crece", **TIENDA),
               it("tienda", 890, 1560, 0.42, id="t3", delay=0.7, anim="crece", **TIENDA)],
     "dato": {"num": 9094, "texto": "TIENDAS EN 2004", "y": 590, "delay": 1.8}},
    {"sigue": True, "quita": ["t1", "t2", "t3"], "lines": L("Y más de 84 mil empleados."),
     "items": [it("multitud", 540, 1640, 1.0, anim="up", n=27, filas=3, escala=0.36, ancho=960)],
     "dato": {"num": 84300, "texto": "EMPLEADOS", "y": 590, "delay": 0.3}},
    {"fondo": rayos("durazno"), "lines": L("Los viernes en la noche, millones de familias iban a escoger una película."),
     "items": [it("tienda", 540, 1560, 0.72, anim="crece", **TIENDA),
               it("persona", 190, 1600, 0.62, delay=0.6, anim="left", cara="feliz", brazos="saluda", camisa="#f59e0b"),
               it("persona", 890, 1600, 0.62, delay=0.9, anim="right", cara="feliz", brazos="objeto", camisa="#8b5cf6", peinado="largo", pelo="#1f1f1f"),
               it("vhs", 890, 1395, 0.28, delay=1.1, anim="pop", etiqueta="ESTRENO")],
     "cam": {"z": [1.0, 1.07], "f": [540, 1250]}},
    {"fondo": rayos("rojo"), "lines": L("Pero Blockbuster tenía un secreto.", "Buena parte de su dinero venía de castigar a quien devolvía tarde las películas."),
     "items": [it("reloj", 540, 860, 1.1, anim="pop", id="reloj", hora=11),
               it("vhs", 540, 1320, 0.95, at=1, anim="up", id="vhs", etiqueta="DEVOLVER"),
               it("etiqueta", 760, 1110, 1.0, at=1, delay=1.2, id="multa", texto="MULTA", fondo="#ef4444", rot=8)]},
    {"sigue": True, "quita": ["reloj", "vhs", "multa"], "lines": L("Solo en el año 2000, las multas por retraso le dejaron unos 800 millones de dólares."),
     "items": [it("billetes", 330, 1450, 0.9, anim="drop", n=4), it("bolsa_dinero", 760, 1560, 1.0, delay=0.4, anim="drop")],
     "dato": {"num": 800, "pre": "$", "suf": " MILLONES", "texto": "EN MULTAS, AÑO 2000", "y": 590, "delay": 1.6}},

    {"capitulo": {"t": "LA REUNIÓN", "n": 2}, "min_dur": 1.7},
    {"fondo": rayos("menta"), "lines": L("Mientras tanto, en California, una empresa diminuta mandaba películas por correo, en sobres rojos."),
     "items": [it("sobre", 260, 1050, 0.7, delay=1.0, anim="drop"), it("sobre", 540, 1260, 0.7, delay=1.4, anim="drop"),
               it("sobre", 820, 1050, 0.7, delay=1.8, anim="drop")]},
    {"sigue": True, "lines": L("Sin multas. Se llamaba Netflix."),
     "items": [it("etiqueta", 540, 760, 1.05, texto="SIN MULTAS", fondo="#22c55e", rot=-6),
               it("etiqueta", 540, 1520, 1.0, at=0, delay=1.0, texto="NETFLIX", fondo="#ffffff", tinta="#b91c1c", rot=4)]},
    {"fondo": rayos("gris"), "lines": L("Pero perdía dinero. Ese año iba camino de perder unos 50 millones."),
     "items": [it("grafica", 540, 1500, 1.15, anim="crece", tipo="baja")],
     "dato": {"num": 50, "pre": "-$", "suf": " MILLONES", "texto": "PÉRDIDA ESPERADA", "y": 560, "delay": 1.6}},
    {"fondo": rayos("cielo"), "lines": L("Así que sus fundadores, Reed Hastings y Marc Randolph, buscaron una salida: venderle Netflix a Blockbuster."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="preocupado", **REED),
               it("persona", 780, 1560, 0.85, delay=0.3, anim="right", cara="serio", **MARC),
               it("nombre", 300, 690, 0.9, delay=0.6, texto="Reed Hastings", sub="cofundador de Netflix"),
               it("nombre", 780, 850, 0.9, delay=1.4, texto="Marc Randolph", sub="cofundador de Netflix")]},
    {"fondo": rayos("cielo"), "lines": L("Volaron a Dallas, a las oficinas de Blockbuster."),
     "items": [it("edificio", 540, 1560, 0.85, anim="crece", texto="BLOCKBUSTER", pisos=9, ancho=420),
               it("avion", 540, 640, 0.75, anim="left")],
     "cam": {"z": [1.0, 1.12], "f": [540, 1100]}},
    {"fondo": {"tipo": "oficina"}, "lines": L("Llegaron en camiseta y sandalias, a una oficina de traje y corbata."),
     "items": [it("persona", 210, 1640, 0.78, anim="left", cara="serio", **REED),
               it("persona", 450, 1640, 0.78, delay=0.2, anim="left", cara="serio", **MARC),
               it("persona", 850, 1640, 0.82, delay=1.2, anim="right", cara="serio", id="ceo", brazos="cruzados", **CEO),
               it("etiqueta", 330, 850, 0.8, delay=0.6, texto="CAMISETA", rot=-6),
               it("etiqueta", 850, 850, 0.8, delay=1.8, texto="TRAJE", fondo="#ffffff", rot=6)]},
    {"sigue": True, "lines": L("Su propuesta: Blockbuster compraba Netflix, y ellos manejaban el negocio en internet."),
     "items": [it("laptop", 640, 1250, 0.5, anim="pop", id="lap", texto="ONLINE")]},
    {"sigue": True, "quita": ["lap"], "lines": L("Desde Blockbuster les preguntaron cuánto querían."),
     "items": [it("icono", 850, 720, 0.7, anim="pop", id="preg", tipo="pregunta")]},
    {"sigue": True, "quita": ["preg"], "lines": L("Y Hastings dijo: 50 millones.", pausa=0.3),
     "dato": {"num": 50, "pre": "$", "suf": " MILLONES", "y": 600, "delay": 0.9, "cuenta": False},
     "cam": {"z": [1.0, 1.12], "f": [540, 1150]}},
    {"fondo": {"tipo": "oficina"}, "lines": L("Según Randolph, en ese momento el director, John Antioco, tuvo que aguantarse la risa."),
     "items": [it("persona", 540, 1720, 1.25, anim="up", cara="risa", **CEO),
               it("nombre", 540, 680, 1.0, delay=1.6, texto="John Antioco", sub="director de Blockbuster")],
     "cam": {"z": [1.0, 1.18], "f": [540, 1000]}},
    {"sigue": True, "lines": L("La respuesta fue no.", pausa=0.5),
     "items": [it("etiqueta", 540, 1330, 1.15, delay=0.3, texto="NO, GRACIAS", fondo="#ef4444", tinta="#1d1d2b", rot=-4)]},

    {"capitulo": {"t": "EL GIRO", "n": 3}, "min_dur": 1.7},
    {"fondo": rayos("menta"), "lines": L("Netflix no se rindió. En 2002 salió a la bolsa."),
     "items": [it("grafica", 540, 1500, 1.15, anim="crece", tipo="sube", color="#22c55e"),
               it("calendario", 830, 720, 0.6, at=0, delay=1.2, anim="pop", texto="2002")]},
    {"fondo": rayos("rojo"), "lines": L("Y años después cambió los sobres por algo que lo cambió todo: el streaming."),
     "items": [it("tv", 540, 1000, 1.0, anim="pop", texto="STREAMING"),
               it("telefono", 870, 1450, 0.5, delay=1.6, anim="right", play=True, color="#d81f26"),
               it("laptop", 250, 1500, 0.48, delay=1.9, anim="left", texto="PLAY")]},
    {"fondo": rayos("azul"), "lines": L("Blockbuster reaccionó tarde. En 2004 quitó las multas y lanzó su propio servicio en línea."),
     "items": [it("linea_tiempo", 540, 700, 1.0, anim="fade", pasos=["2000", "2004", "2010"], activo=1),
               it("tienda", 540, 1560, 0.68, delay=0.4, anim="crece", **TIENDA)]},
    {"sigue": True, "lines": L("Pero ya iba años por detrás."),
     "items": [it("etiqueta", 790, 1060, 1.0, texto="TARDE", fondo="#ef4444", rot=7)]},
    {"fondo": {"tipo": "noche"}, "lines": L("En 2010, Blockbuster se declaró en bancarrota.", pausa=0.4),
     "items": [it("lapida", 540, 1560, 1.25, anim="crece", texto="QUIEBRA", sub="2010")],
     "cam": {"z": [1.12, 1.0], "f": [540, 1200]}},

    {"capitulo": {"t": "LA ÚLTIMA TIENDA", "n": 4}, "min_dur": 1.7},
    {"fondo": rayos("durazno"), "lines": L("Hoy solo queda una tienda Blockbuster en el mundo: en Bend, Oregón."),
     "items": [it("tienda", 470, 1560, 0.78, anim="crece", **TIENDA),
               it("pin", 860, 900, 0.6, delay=1.6, anim="drop", texto="BEND, OREGÓN")]},
    {"sigue": True, "lines": L("Y la gente viaja hasta allá solo para tomarse una foto."),
     "items": [it("multitud", 540, 1730, 1.0, anim="up", n=9, filas=1, escala=0.36, ancho=1000, cara="feliz")]},
    {"fondo": {"tipo": "noche"}, "lines": L("La empresa que pudo comprar Netflix por 50 millones terminó siendo un recuerdo.", pausa=0.3),
     "items": [it("vhs", 540, 1050, 1.3, anim="pop", etiqueta="2000 - 2010")],
     "cam": {"z": [1.0, 1.12], "f": [540, 1050]}},
    {"sigue": True, "lines": L("¿Tú alcanzaste a rentar en Blockbuster? Te leo en los comentarios."),
     "items": [it("etiqueta", 540, 1460, 1.1, texto="¿Y TÚ?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "Blockbuster pudo comprar Netflix por 50 millones (y casi se ríe)",
    "description": ("En el año 2000, los fundadores de Netflix ofrecieron su empresa a Blockbuster por 50 millones de dólares. "
                    "La respuesta fue no. Esta es la historia de cómo un imperio de más de 9 mil tiendas terminó con una sola.\n"
                    "Fuentes: libro de Marc Randolph 'That Will Never Work'; libro de Reed Hastings 'No Rules Rules'; datos públicos de Blockbuster."),
    "hashtags": ["#HistoriasSinFiltro", "#Blockbuster", "#Netflix", "#historiasreales", "#negocios"],
    "source_url": "https://marketplace.org/2020/09/08/ceo-reed-hastings-on-how-netflix-beat-blockbuster",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_blockbuster.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
print("escenas:", len(escenas))
