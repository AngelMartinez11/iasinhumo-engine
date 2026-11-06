"""Genera tres guiones de ejemplo del motor v4:
  ejemplos/hsf_kodak.json      (Historias Sin Filtro)
  ejemplos/hsf_alcatraz.json   (Historias Sin Filtro)
  ejemplos/ish_synthid.json    (IA SinHumo)
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def L(*txts, pausa=0, say=None):
    out = [{"text": t} for t in txts]
    if pausa:
        out[-1]["pausa"] = pausa
    if say:
        for i, s in say.items():
            out[i]["say"] = s
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


def cap(t, n):
    return {"capitulo": {"t": t, "n": n}, "min_dur": 1.7}


def guardar(nombre, guion):
    with open(os.path.join(AQUI, nombre), "w", encoding="utf-8") as f:
        json.dump(guion, f, ensure_ascii=False, indent=1)
    print(nombre, len(guion["scenes"]), "escenas")


# ------------------------------------------------------------------ Kodak
SASSON = {"ropa": "bata", "lentes": True, "pelo": "#6b4423", "peinado": "corto"}
JEFE = {"ropa": "traje", "corbata": "#facc15", "pelo": "#c9c9c9", "peinado": "canoso"}
KODAK_AMARILLO = "#facc15"

kodak = [
    {"fondo": rayos("oro"), "lines": L("En 1975, un ingeniero de Kodak inventó algo que iba a cambiar el mundo: la cámara digital."),
     "items": [it("camara", 600, 1150, 1.15, anim="pop", id="proto", tipo="prototipo"),
               it("persona", 200, 1600, 0.7, delay=0.6, anim="left", cara="feliz", brazos="arriba", **SASSON)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1200]}},
    {"sigue": True, "lines": L("Y Kodak decidió guardarla en un cajón.", pausa=0.3),
     "items": [it("etiqueta", 640, 820, 1.0, texto="SECRETO", fondo="#ef4444", rot=-6)]},
    {"fondo": {"tipo": "noche"}, "lines": L("Treinta y siete años después, Kodak estaba en bancarrota."),
     "items": [it("lapida", 540, 1560, 1.25, anim="crece", texto="KODAK", sub="2012")],
     "cam": {"z": [1.12, 1.0], "f": [540, 1200]}},
    {"fondo": rayos("oro"), "lines": L("¿Cómo termina destruida por la foto digital la misma empresa que la inventó?"),
     "items": [it("icono", 540, 1080, 1.7, anim="pop", tipo="pregunta")]},

    cap("EL GIGANTE AMARILLO", 1),
    {"fondo": rayos("oro"), "lines": L("Durante casi un siglo, decir foto era decir Kodak."),
     "items": [it("rollo", 380, 1100, 1.0, anim="drop", texto="KODAK", color=KODAK_AMARILLO),
               it("camara", 760, 1420, 0.85, delay=0.6, anim="pop", tipo="antigua")]},
    {"fondo": rayos("durazno"), "lines": L("A finales de los años ochenta, llegó a tener 145 mil empleados."),
     "items": [it("multitud", 540, 1640, 1.0, anim="up", n=27, filas=3, escala=0.36, ancho=960, cara="feliz")],
     "dato": {"num": 145000, "texto": "EMPLEADOS", "y": 590, "delay": 1.4}},
    {"fondo": rayos("oro"), "lines": L("Y en 1996 vendía más de 16 mil millones de dólares al año."),
     "items": [it("edificio", 540, 1560, 0.85, anim="crece", texto="KODAK", pisos=8, ancho=440, letrero="#b45309")],
     "dato": {"num": 16000, "pre": "$", "suf": " MILLONES", "texto": "VENTAS EN 1996", "y": 590, "delay": 1.2}},
    {"fondo": rayos("menta"), "lines": L("Su gran negocio era el rollo: cada foto que tomabas era dinero para Kodak."),
     "items": [it("rollo", 260, 1000, 0.6, anim="drop", color=KODAK_AMARILLO),
               it("rollo", 560, 1150, 0.6, delay=0.3, anim="drop", color=KODAK_AMARILLO),
               it("rollo", 820, 980, 0.6, delay=0.6, anim="drop", color=KODAK_AMARILLO),
               it("billetes", 540, 1500, 0.9, at=0, delay=2.0, anim="up", n=4)]},

    cap("EL INVENTO", 2),
    {"fondo": rayos("azul"), "lines": L("En 1975, un ingeniero de 24 años, Steven Sasson, armó un aparato del tamaño de una tostadora.",
                                         say={0: "En 1975, un ingeniero de 24 años, Stíven Sásson, armó un aparato del tamaño de una tostadora."}),
     "items": [it("persona", 270, 1600, 0.85, anim="left", cara="feliz", brazos="senala", **SASSON),
               it("camara", 760, 1180, 0.95, delay=1.4, anim="pop", id="proto", tipo="prototipo"),
               it("nombre", 300, 700, 0.95, delay=0.8, texto="Steven Sasson", sub="ingeniero de Kodak")]},
    {"sigue": True, "lines": L("Pesaba casi cuatro kilos, y tardaba 23 segundos en guardar una sola foto en un cassette."),
     "dato": {"num": 23, "suf": " SEGUNDOS", "texto": "POR CADA FOTO", "y": 620, "delay": 1.8}},
    {"sigue": True, "lines": L("La foto salía en blanco y negro, de apenas cien por cien pixeles."),
     "items": [it("etiqueta", 760, 1420, 0.85, texto="0,01 MEGAPIXELES", rot=5, size=54)]},
    {"fondo": {"tipo": "oficina"}, "lines": L("Según Sasson, cuando la mostró, la reacción fue: es bonita, pero no se lo digas a nadie."),
     "items": [it("persona", 250, 1680, 0.85, anim="left", cara="feliz", **SASSON),
               it("persona", 820, 1680, 0.9, delay=1.0, anim="right", cara="risa", brazos="cruzados", **JEFE),
               it("etiqueta", 820, 820, 0.95, at=0, delay=3.0, texto="SECRETO", fondo="#ef4444", rot=6)]},
    {"sigue": True, "lines": L("¿Por qué? Porque una cámara sin rollo amenazaba el negocio que les daba de comer."),
     "items": [it("rollo", 540, 1180, 0.6, anim="pop", id="rl", color=KODAK_AMARILLO),
               it("icono", 600, 1180, 0.8, delay=1.6, anim="pop", tipo="x")]},

    cap("LA CAÍDA", 3),
    {"fondo": rayos("azul"), "lines": L("A inicios de los dos mil, las cámaras digitales le ganaron a las de rollo."),
     "items": [it("camara", 300, 1150, 0.8, anim="left", tipo="antigua"),
               it("camara", 780, 1150, 0.8, delay=0.5, anim="right", tipo="digital"),
               it("icono", 300, 1150, 0.8, delay=1.8, anim="pop", tipo="x"),
               it("icono", 780, 900, 0.6, delay=2.1, anim="pop", tipo="check")]},
    {"fondo": rayos("gris"), "lines": L("Después llegaron los teléfonos con cámara, y el rollo dejó de importar."),
     "items": [it("telefono", 330, 1250, 0.85, anim="pop", texto="CÁMARA", color="#6d5dfc"),
               it("grafica", 760, 1500, 0.75, delay=1.4, anim="crece", tipo="baja")]},
    {"fondo": {"tipo": "noche"}, "lines": L("En enero de 2012, Kodak se declaró en bancarrota.", "De 145 mil empleados, le quedaban unos 19 mil."),
     "items": [it("lapida", 540, 1560, 1.15, anim="crece", texto="KODAK", sub="2012")],
     "dato": {"num": 19000, "texto": "EMPLEADOS EN 2012", "y": 620, "at": 1, "delay": 0.6}},

    cap("LA IRONÍA", 4),
    {"fondo": rayos("lila"), "lines": L("Y aquí viene lo más loco.", "Ese mismo año, una app de fotos con solo 13 empleados se vendió por mil millones de dólares."),
     "items": [it("telefono", 540, 1180, 1.0, at=1, anim="pop", texto="APP DE FOTOS", color="#ec4899"),
               it("multitud", 540, 1700, 1.0, at=1, delay=1.6, anim="up", n=13, filas=1, escala=0.3, ancho=1000)],
     "dato": {"num": 1000, "pre": "$", "suf": " MILLONES", "y": 560, "at": 1, "delay": 3.2}},
    {"sigue": True, "lines": L("Se llamaba Instagram, y la compró Facebook."),
     "items": [it("etiqueta", 540, 1520, 1.0, texto="INSTAGRAM", fondo="#ffffff", tinta="#be185d", rot=-4)]},
    {"fondo": {"tipo": "noche"}, "lines": L("Kodak tuvo el futuro en sus manos en 1975, y lo guardó en un cajón.", pausa=0.3),
     "items": [it("camara", 540, 1150, 1.15, anim="pop", tipo="prototipo"),
               it("etiqueta", 540, 820, 0.95, delay=1.2, texto="1975", fondo="#ffffff", rot=-4)],
     "cam": {"z": [1.0, 1.12], "f": [540, 1150]}},
    {"sigue": True, "lines": L("¿Tú todavía tienes fotos en rollo? Te leo en los comentarios."),
     "items": [it("etiqueta", 540, 1480, 1.1, texto="¿Y TÚ?", rot=-5)]},
]

guardar("hsf_kodak.json", {
    "motor": 4, "canal": "historias",
    "title": "Kodak inventó la cámara digital... y la escondió en un cajón",
    "description": ("En 1975 un ingeniero de Kodak, Steven Sasson, inventó la cámara digital. Kodak la guardó para proteger su negocio de rollos. "
                    "En 2012 quebró, el mismo año en que Instagram, con 13 empleados, se vendió por mil millones.\n"
                    "Fuentes: IEEE Milestones (ETHW), NBC News, AFP/VOA sobre la quiebra de Kodak (2012)."),
    "hashtags": ["#HistoriasSinFiltro", "#Kodak", "#historiasreales", "#negocios", "#tecnologia"],
    "source_url": "https://ethw.org/Milestones:Handheld_Digital_Camera,_1975",
    "scenes": kodak,
})

# ------------------------------------------------------------------ Alcatraz
MORRIS = {"camisa": "#94a3b8", "pantalon": "#475569", "pelo": "#1f1f1f"}
JOHN = {"camisa": "#94a3b8", "pantalon": "#475569", "pelo": "#a16207"}
CLARENCE = {"camisa": "#94a3b8", "pantalon": "#475569", "pelo": "#6b4423"}
MAR_NOCHE = {"tipo": "mar"}
MAR_DIA = {"tipo": "mar", "cielo": "#7dd3fc", "horizonte": "#e0f2fe"}

alcatraz = [
    {"fondo": MAR_NOCHE, "lines": L("En 1962, tres presos escaparon de la cárcel más segura de Estados Unidos."),
     "items": [it("isla", 540, 1310, 1.0, anim="up", texto="ALCATRAZ")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1150]}},
    {"sigue": True, "lines": L("Y hasta hoy, nadie sabe si sobrevivieron.", pausa=0.3),
     "items": [it("icono", 540, 760, 1.0, anim="pop", tipo="pregunta")]},
    {"fondo": rayos("gris"), "lines": L("A la mañana siguiente, los guardias solo encontraron cabezas falsas en sus camas."),
     "items": [it("cama", 540, 1500, 1.5, anim="up"),
               it("etiqueta", 380, 900, 0.95, delay=2.0, texto="CABEZA FALSA", fondo="#ef4444", rot=-6)],
     "cam": {"z": [1.0, 1.12], "f": [400, 1150]}},

    cap("LA ROCA", 1),
    {"fondo": MAR_DIA, "lines": L("Alcatraz era una prisión en una isla de la bahía de San Francisco.", "Rodeada de agua helada y corrientes fuertes."),
     "items": [it("isla", 540, 1310, 1.0, anim="up"),
               it("etiqueta", 540, 760, 1.0, at=1, texto="AGUA HELADA", fondo="#7dd3fc", rot=-5)]},
    {"fondo": rayos("gris"), "lines": L("Ahí llegaron tres hombres que ya habían intentado escapar de otras cárceles."),
     "items": [it("persona", 200, 1600, 0.68, anim="left", cara="serio", **MORRIS),
               it("persona", 540, 1600, 0.68, delay=0.3, anim="up", cara="serio", **JOHN),
               it("persona", 880, 1600, 0.68, delay=0.6, anim="right", cara="serio", **CLARENCE),
               it("nombre", 220, 720, 0.8, delay=1.4, texto="Frank Morris"),
               it("nombre", 700, 860, 0.8, delay=2.2, texto="John y Clarence Anglin", sub="hermanos")]},

    cap("EL PLAN", 2),
    {"fondo": rayos("gris"), "lines": L("Durante meses, rasparon la pared detrás de sus celdas con cucharas del comedor."),
     "items": [it("celda", 540, 1560, 1.25, anim="fade"),
               it("cuchara", 540, 1150, 1.2, delay=1.8, anim="pop", id="cuchara"),
               it("etiqueta", 790, 760, 0.9, delay=2.6, texto="CUCHARAS", rot=6)]},
    {"sigue": True, "lines": L("Y hasta armaron un taladro con el motor de una aspiradora."),
     "items": [it("etiqueta", 540, 1420, 0.9, texto="MOTOR DE ASPIRADORA", fondo="#ffffff", rot=-4, size=52)]},
    {"fondo": rayos("azul"), "lines": L("Para que nadie notara su ausencia, fabricaron cabezas falsas con jabón, pasta de dientes y papel higiénico."),
     "items": [it("cama", 540, 1560, 1.35, anim="up"),
               it("etiqueta", 230, 800, 0.8, delay=3.0, texto="JABÓN", rot=-6),
               it("etiqueta", 560, 700, 0.8, delay=3.6, texto="PASTA", fondo="#ffffff", rot=4),
               it("etiqueta", 860, 820, 0.8, delay=4.2, texto="PAPEL", fondo="#7dd3fc", rot=-3)]},
    {"sigue": True, "lines": L("Y les pegaron pelo de verdad, recogido del piso de la barbería."),
     "items": [it("etiqueta", 540, 1000, 1.0, texto="PELO REAL", fondo="#ef4444", rot=6)]},
    {"fondo": rayos("menta"), "lines": L("Con más de 50 impermeables, armaron una balsa inflable y chalecos salvavidas."),
     "items": [it("balsa", 540, 1400, 1.25, anim="pop", personas=0)],
     "dato": {"num": 50, "pre": "+", "texto": "IMPERMEABLES", "y": 600, "delay": 1.2}},

    cap("LA NOCHE", 3),
    {"fondo": {"tipo": "noche"}, "lines": L("La noche del 11 de junio de 1962, dejaron las cabezas falsas en sus camas."),
     "items": [it("cama", 540, 1560, 1.35, anim="fade")],
     "cam": {"z": [1.0, 1.15], "f": [380, 1250]}},
    {"sigue": True, "lines": L("Subieron por los ductos hasta el techo, y bajaron hasta el agua."),
     "items": [it("flecha", 860, 980, 0.9, anim="pop", rot=-90)]},
    {"fondo": rayos("gris"), "lines": L("Un cuarto compañero, Allen West, no logró abrir a tiempo la rejilla de su celda. Se quedó atrás."),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="triste", brazos="cabeza", camisa="#94a3b8", pantalon="#475569"),
               it("celda", 540, 1580, 1.35, delay=0.2, anim="fade"),
               it("nombre", 540, 700, 0.95, delay=0.8, texto="Allen West", sub="se quedó en su celda")]},
    {"fondo": MAR_NOCHE, "lines": L("Los otros tres se perdieron en la oscuridad de la bahía.", pausa=0.4),
     "items": [it("balsa", 600, 1340, 0.9, anim="left", personas=3),
               it("isla", 120, 1310, 0.55, anim="fade")],
     "cam": {"z": [1.0, 1.12], "x": [0, 60], "f": [600, 1200]}},

    cap("EL MISTERIO", 4),
    {"fondo": rayos("azul"), "lines": L("Días después aparecieron en el agua un remo, chalecos salvavidas y una bolsa con fotos de la familia Anglin."),
     "items": [it("olas", 540, 1420, 1.0, anim="up"),
               it("etiqueta", 300, 900, 0.95, delay=2.0, texto="REMO", rot=-6),
               it("etiqueta", 760, 1050, 0.95, delay=2.6, texto="CHALECOS", fondo="#ef4444", rot=5),
               it("etiqueta", 420, 1300, 0.95, delay=3.4, texto="FOTOS", fondo="#ffffff", rot=-3)],
     "items_extra": []},
    {"fondo": rayos("gris"), "lines": L("En 1979, el FBI cerró el caso: dijo que lo más probable es que se ahogaron."),
     "items": [it("calendario", 540, 1120, 1.0, anim="pop", texto="1979"),
               it("etiqueta", 540, 1500, 0.95, delay=2.0, texto="CASO CERRADO", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("lila"), "lines": L("Pero en 2013, la policía de San Francisco recibió una carta firmada como John Anglin.",
                                         "Decía que los tres habían sobrevivido."),
     "items": [it("sobre", 540, 1180, 1.2, anim="drop", color="#f8fafc", texto="", disco=False),
               it("etiqueta", 540, 760, 1.0, at=1, texto="SOBREVIVIMOS", fondo="#22c55e", rot=-5)]},
    {"sigue": True, "lines": L("El FBI la analizó, y no pudo confirmar si era real.", pausa=0.3),
     "items": [it("icono", 800, 1450, 0.8, anim="pop", tipo="pregunta")]},
    {"fondo": MAR_NOCHE, "lines": L("Alcatraz cerró como prisión en 1963. Y para los Marshals de Estados Unidos, el caso sigue abierto.",
                                     say={0: "Alcatraz cerró como prisión en 1963. Y para los Marsals de Estados Unidos, el caso sigue abierto."}),
     "items": [it("isla", 540, 1310, 1.0, anim="fade", texto="ALCATRAZ")],
     "cam": {"z": [1.1, 1.0], "f": [540, 1150]}},
    {"sigue": True, "lines": L("¿Tú crees que lo lograron? Te leo en los comentarios."),
     "items": [it("etiqueta", 540, 760, 1.1, texto="¿LO LOGRARON?", rot=-5)]},
]
for sc in alcatraz:
    sc.pop("items_extra", None)

guardar("hsf_alcatraz.json", {
    "motor": 4, "canal": "historias",
    "title": "Escaparon de Alcatraz con cucharas... y nunca los encontraron",
    "description": ("El 11 de junio de 1962, Frank Morris y los hermanos John y Clarence Anglin escaparon de Alcatraz con cabezas falsas y una balsa de impermeables. "
                    "El FBI cerró el caso en 1979, pero una carta de 2013 reabrió el misterio.\n"
                    "Fuentes: FBI (archivos del caso), Britannica, History.com, WTOP (2025)."),
    "hashtags": ["#HistoriasSinFiltro", "#Alcatraz", "#misterio", "#historiasreales", "#fuga"],
    "source_url": "https://www.britannica.com/event/Alcatraz-escape-of-June-1962",
    "scenes": alcatraz,
})

# ------------------------------------------------------------------ IA SinHumo: SynthID
synthid = [
    {"fondo": rayos("azul"), "lines": L("¿Ese video lo hizo una inteligencia artificial? Google quiere que lo puedas comprobar."),
     "items": [it("robot", 250, 1560, 1.5, anim="left", id="bot"),
               it("telefono", 720, 1230, 0.85, delay=0.8, anim="pop", id="tel", play=True, color="#3b82f6"),
               it("icono", 720, 820, 0.7, delay=2.4, anim="pop", id="preg", tipo="pregunta")]},
    {"sigue": True, "quita": ["preg"], "lines": L("Está ampliando a todo el mundo su detector SynthID.",
                                                    say={0: "Está ampliando a todo el mundo su detector Sinz ai di."}),
     "items": [it("etiqueta", 540, 760, 1.0, texto="SYNTHID DETECTOR", rot=-5, size=58)]},
    {"fondo": rayos("menta"), "lines": L("Le das una imagen, un video o un audio, y revisa si trae la marca de agua invisible que pone la IA."),
     "items": [it("camara", 260, 1000, 0.6, anim="pop", tipo="digital"),
               it("tv", 760, 1000, 0.55, delay=0.4, anim="pop", texto="VIDEO"),
               it("disco", 540, 1380, 0.75, delay=0.8, anim="pop"),
               it("etiqueta", 540, 1650, 0.9, delay=3.0, texto="MARCA INVISIBLE", fondo="#ffffff", rot=-3)]},
    {"fondo": rayos("lila"), "lines": L("Y no solo reconoce lo hecho con Google: también contenido de OpenAI, NVIDIA, Kakao y Apple.",
                                         say={0: "Y no solo reconoce lo hecho con Google: también contenido de Open ei ai, Envidia, Kakao y Apple."}),
     "items": [it("etiqueta", 300, 820, 0.85, delay=2.2, texto="OPENAI", fondo="#ffffff", rot=-6),
               it("etiqueta", 780, 920, 0.85, delay=2.6, texto="NVIDIA", fondo="#86efac", rot=5),
               it("etiqueta", 330, 1180, 0.85, delay=3.0, texto="KAKAO", fondo="#ffd23f", rot=4),
               it("etiqueta", 760, 1300, 0.85, delay=3.4, texto="APPLE", fondo="#e5e7eb", rot=-4),
               it("persona", 540, 1720, 0.75, anim="up", cara="sorpresa", brazos="arriba", camisa="#8b5cf6")]},
    {"fondo": rayos("oro"), "lines": L("Google dice que ya marcó más de 180 mil millones de imágenes y videos."),
     "items": [it("billetes", 540, 1450, 0.01, anim="fade"), it("telefono", 540, 1300, 0.75, anim="up", color="#f59e0b", texto="IMÁGENES")],
     "dato": {"num": 180000, "suf": " MILLONES", "texto": "IMÁGENES Y VIDEOS MARCADOS", "y": 600, "delay": 1.4}},
    {"fondo": rayos("rojo"), "lines": L("Pero ojo: por ahora funciona en inglés, y solo reconoce lo que trae esa marca."),
     "items": [it("icono", 540, 1080, 1.3, anim="pop", tipo="exclamacion"),
               it("etiqueta", 540, 1450, 1.0, delay=1.2, texto="SOLO EN INGLÉS", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("azul"), "lines": L("¿Real o humo? Sirve, pero no es magia.", "¿Lo usarías antes de compartir un video?"),
     "items": [it("robot", 540, 1560, 1.7, anim="pop"),
               it("etiqueta", 540, 780, 1.05, at=1, texto="¿LO USARÍAS?", rot=-5)]},
]
for sc in synthid:
    sc["items"] = [x for x in sc["items"] if x["p"] != "billetes"]

guardar("ish_synthid.json", {
    "motor": 4, "canal": "iasinhumo",
    "title": "¿Ese video es IA? Google ya te deja comprobarlo (con letra pequeña)",
    "description": ("Google está ampliando su detector SynthID: revisa si una imagen, video o audio trae la marca invisible de IA, incluso de OpenAI, NVIDIA, Kakao y Apple. "
                    "Por ahora en inglés.\nFuente: https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026/\n¿Lo usarías?"),
    "hashtags": ["#IASinHumo", "#inteligenciaartificial", "#Google", "#deepfake", "#IA"],
    "source_url": "https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026/",
    "scenes": synthid,
})
