"""Genera ejemplos/hsf_newcoke.json: New Coke, el cambio de formula de 1985 (Dato Bomba, canal historias, motor v4, formato largo).

Estructura: gancho -> pregunta -> historia en orden -> datos curiosos -> que paso despues -> cierre con pregunta.
Los bloques se marcan con la narracion y con cambio de fondo (el canal no usa tarjetas de capitulo).
Sin logos reales: las marcas se escriben con texto en etiquetas.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

ROJO = "#d81f26"
AZUL = "#1d4ed8"
GOIZUETA = {"ropa": "traje", "corbata": ROJO, "pelo": "#1f1f1f", "peinado": "corto", "lentes": True}
KEOUGH = {"ropa": "traje", "corbata": "#f0c448", "pelo": "#e5e7eb", "peinado": "canoso"}
MULLINS = {"camisa": "#f59e0b", "pelo": "#c9c9c9", "peinado": "calvo", "lentes": True}
PEMBERTON = {"ropa": "bata", "pelo": "#6b4423", "peinado": "corto"}
JENNINGS = {"ropa": "traje", "corbata": "#1e3a8a", "pelo": "#3a2a1e"}


def L(*txts, pausa=0, say=None):
    out = [{"text": t} for t in txts]
    if say:
        for i, s in say.items():
            out[i]["say"] = s
    if pausa:
        out[-1]["pausa"] = pausa
    return out


def it(p, x=540, y=1560, s=1.0, at=0, delay=0, anim=None, id=None, flip=False, **a):
    d = {"p": p, "x": x, "y": y, "s": s, "at": at, "delay": delay, "a": a}
    if anim:
        d["anim"] = anim
    if id:
        d["id"] = id
    if flip:
        d["flip"] = True
    return d


def rayos(p):
    return {"tipo": "rayos", "paleta": p}


def dato(num, texto, pre="", suf="", y=640, delay=1.0, cuenta=True):
    return {"num": num, "pre": pre, "suf": suf, "texto": texto, "y": y, "delay": delay, "cuenta": cuenta}


def marca(x, y, s, texto, fondo, delay=0, rot=-5, id=None):
    """Nombre de marca escrito en una etiqueta (sin logos)."""
    return it("etiqueta", x, y, s, delay=delay, id=id, texto=texto, fondo=fondo, tinta="#1d1d2b", rot=rot)


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": rayos("rojo"), "lines": L("En 1985, Coca-Cola hizo algo que nadie esperaba: cambió la fórmula de su refresco más famoso."),
     "items": [marca(540, 1170, 1.1, "COCA-COLA", "#ffffff"),
               it("chapa", 540, 720, 1.4, delay=1.0, texto="1985"),
               it("etiqueta", 540, 940, 0.9, delay=3.4, texto="FÓRMULA NUEVA", fondo="#f0c448", rot=4)]},
    {"sigue": True, "lines": L("Antes la habían probado con casi doscientas mil personas."),
     "items": [it("multitud", 540, 1700, 1.0, anim="up", n=16, filas=3, escala=0.45, cara="feliz")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Y aun así, setenta y nueve días después, tuvo que dar marcha atrás."),
     "items": [it("calendario", 540, 1250, 1.1, anim="drop", texto="79")],
     "dato": dato(79, "DÍAS", suf=" DÍAS", delay=1.6),
     "cam": {"z": [1.1, 1.0], "f": [540, 1250]}},
    {"fondo": rayos("oro"), "lines": L("¿Cómo se equivoca tanto una empresa que preguntó a tanta gente?"),
     "items": [it("icono", 540, 1150, 1.3, anim="pop", tipo="pregunta")]},

    # ------------------------------------------------------------ el contexto
    {"fondo": rayos("durazno"), "lines": L("La fórmula original nació en 1886, en Atlanta, creada por el farmacéutico John Pemberton."),
     "items": [it("persona", 320, 1560, 0.95, anim="left", cara="feliz", brazos="objeto", **PEMBERTON),
               it("calendario", 810, 1150, 0.7, delay=0.6, anim="pop", texto="1886"),
               it("nombre", 540, 700, 0.95, delay=2.6, texto="John Pemberton", sub="farmacéutico de Atlanta")]},
    {"sigue": True, "lines": L("Durante noventa y nueve años, nadie la cambió."),
     "items": [it("chapa", 760, 1450, 1.2, texto="99 AÑOS")]},
    {"fondo": rayos("menta"), "lines": L("Después de la Segunda Guerra Mundial, Coca-Cola tenía cerca del sesenta por ciento del mercado de colas en Estados Unidos."),
     "items": [it("grafica", 540, 1520, 1.15, anim="crece", tipo="sube", color=ROJO)],
     "dato": dato(60, "DEL MERCADO EN POSGUERRA", suf=" %", delay=2.0)},
    {"fondo": rayos("gris"), "lines": L("Para 1983 había caído a menos del veinticuatro por ciento."),
     "items": [it("grafica", 540, 1520, 1.15, anim="crece", tipo="baja", color=ROJO),
               it("chapa", 540, 760, 1.45, delay=1.4, texto="< 24 %", sub="en 1983")]},
    {"fondo": rayos("cielo"), "lines": L("Y en 1984, frente a frente con Pepsi, la ventaja era de apenas tres puntos: casi veintidós contra casi diecinueve."),
     "items": [marca(330, 1150, 0.75, "COCA-COLA", "#ffffff", rot=-5),
               marca(770, 1150, 0.75, "PEPSI", "#93c5fd", delay=1.2, rot=5),
               it("chapa", 330, 1400, 1.15, delay=3.4, texto="21.8 %"),
               it("chapa", 770, 1400, 1.15, delay=4.0, texto="18.8 %")]},
    {"fondo": rayos("azul"), "lines": L("Mientras tanto, Pepsi crecía."),
     "items": [marca(540, 1150, 1.0, "PEPSI", "#93c5fd", rot=4),
               it("grafica", 540, 1560, 0.6, delay=0.8, anim="crece", tipo="sube", color=AZUL)]},
    {"sigue": True, "lines": L("Y en 1975, en Texas, lanzó su arma: el Pepsi Challenge."),
     "items": [it("pin", 840, 820, 0.6, delay=0.6, anim="drop", texto="TEXAS", color=AZUL),
               it("etiqueta", 540, 760, 0.85, delay=2.2, texto="PEPSI CHALLENGE", fondo="#f0c448", rot=-4)]},
    {"fondo": rayos("cielo"), "lines": L("Una prueba a ciegas: dos vasos sin marca, uno con la letra M y otro con la Q."),
     "items": [it("mesa", 540, 1560, 1.0, anim="up"),
               it("etiqueta", 380, 1230, 0.9, delay=1.6, texto="M", fondo="#ffffff", rot=-4),
               it("etiqueta", 700, 1230, 0.9, delay=2.4, texto="Q", fondo="#ffffff", rot=4)]},
    {"sigue": True, "lines": L("En los comerciales, la gente elegía la M. Era Pepsi."),
     "items": [it("icono", 380, 950, 0.7, delay=0.8, anim="pop", tipo="check"),
               it("etiqueta", 380, 760, 0.8, delay=2.0, texto="PEPSI", fondo="#93c5fd", rot=-5)]},

    # ------------------------------------------------------------ el plan secreto
    {"fondo": {"tipo": "oficina"}, "lines": L("El director general de la empresa, Roberto Goizueta, decidió actuar."),
     "items": [it("persona", 540, 1640, 0.95, anim="up", id="goi", cara="serio", brazos="cruzados", **GOIZUETA),
               it("nombre", 540, 700, 1.0, delay=1.6, texto="Roberto Goizueta", sub="director general de Coca-Cola")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"sigue": True, "lines": L("En un plan secreto llamado Proyecto Kansas, la empresa desarrolló una fórmula nueva, más dulce."),
     "items": [it("etiqueta", 540, 870, 0.75, delay=1.4, texto="PROYECTO KANSAS", fondo="#f0c448", rot=4)]},
    {"fondo": rayos("durazno"), "lines": L("Era más dulce y menos ácida que la original."),
     "items": [it("chapa", 540, 1000, 1.5, anim="pop", texto="+ DULCE"),
               it("chapa", 540, 1260, 1.5, delay=1.2, texto="- ÁCIDA")]},
    {"fondo": rayos("lila"), "lines": L("La probó con casi doscientos mil consumidores."),
     "items": [it("multitud", 540, 1620, 1.0, anim="up", n=16, filas=3, escala=0.45, cara="feliz", semilla=4)],
     "dato": dato(200000, "PERSONAS EN PRUEBAS", delay=1.0)},
    {"sigue": True, "lines": L("Según la revista Time, en las pruebas a ciegas el cincuenta y cinco por ciento prefirió la nueva."),
     "items": [it("chapa", 540, 1000, 1.45, delay=2.6, texto="55 %", sub="prefirió la nueva")]},
    {"fondo": rayos("oro"), "lines": L("Los números parecían claros. La nueva no iba a convivir con la vieja: la iba a reemplazar."),
     "items": [it("icono", 300, 1150, 1.0, anim="pop", tipo="check"),
               it("flecha", 640, 1150, 0.8, delay=1.8, anim="fade"),
               it("etiqueta", 780, 1400, 0.85, delay=2.6, texto="REEMPLAZO", fondo="#ef4444", rot=5)]},

    # ------------------------------------------------------------ el lanzamiento
    {"fondo": rayos("rojo"), "lines": L("El 23 de abril de 1985, en Nueva York, Coca-Cola anunció el cambio."),
     "items": [it("calendario", 320, 1250, 0.9, anim="pop", texto="1985"),
               it("chapa", 540, 720, 1.3, delay=0.8, texto="23 ABRIL"),
               it("pin", 770, 1350, 0.85, delay=1.6, anim="drop", texto="NUEVA YORK")]},
    {"sigue": True, "lines": L("Era el primer cambio de fórmula en noventa y nueve años."),
     "items": [it("chapa", 540, 930, 1.2, delay=0.6, texto="1.er CAMBIO", sub="en 99 años")]},
    {"fondo": rayos("azul"), "lines": L("Pepsi no perdió tiempo. Publicó anuncios en los periódicos con un mensaje: el otro parpadeó."),
     "items": [it("libro", 540, 1250, 1.1, anim="pop", abierto=True, texto="PEPSI"),
               it("etiqueta", 540, 760, 0.85, delay=3.4, texto="EL OTRO PARPADEÓ", fondo="#93c5fd", rot=-4)]},
    {"sigue": True, "lines": L("Y a los pocos días, le dio el día libre a sus empleados para celebrar."),
     "items": [it("calendario", 860, 1500, 0.55, delay=1.0, anim="pop", texto="LIBRE", color=AZUL)]},

    # ------------------------------------------------------------ la rebelion
    {"fondo": {"tipo": "noche"}, "lines": L("Entonces llegó la reacción del público."),
     "items": [it("multitud", 540, 1700, 1.05, anim="up", n=16, filas=3, escala=0.45, cara="enojado")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1300]}},
    {"fondo": rayos("rojo"), "lines": L("La línea de atención solía recibir unas cuatrocientas llamadas al día."),
     "items": [it("telefono", 540, 1250, 1.0, anim="pop", texto="800-GET-COKE", color=ROJO),
               it("chapa", 540, 760, 1.35, delay=1.6, texto="400", sub="llamadas al día")]},
    {"sigue": True, "lines": L("En junio ya eran mil quinientas diarias, casi todas de queja."),
     "dato": dato(1500, "LLAMADAS AL DÍA", delay=0.6)},
    {"fondo": rayos("gris"), "lines": L("Otros recuentos hablan de hasta ocho mil llamadas en un día, y de unas cuarenta mil cartas."),
     "items": [it("sobre", 250, 1150, 0.7, anim="drop", color="#f8fafc", disco=False),
               it("sobre", 540, 1300, 0.7, delay=0.4, anim="drop", color="#f8fafc", disco=False),
               it("sobre", 830, 1150, 0.7, delay=0.8, anim="drop", color="#f8fafc", disco=False),
               it("chapa", 540, 760, 1.35, delay=3.0, texto="~40.000", sub="cartas")]},
    {"fondo": rayos("durazno"), "lines": L("En Seattle, un jubilado llamado Gay Mullins se puso al frente de la protesta.",
                                          say={0: "En Seattle, un jubilado llamado Guéi Múlins se puso al frente de la protesta."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="mul", cara="enojado", brazos="arriba", **MULLINS),
               it("nombre", 540, 700, 0.95, delay=2.0, texto="Gay Mullins", sub="jubilado de Seattle")]},
    {"sigue": True, "lines": L("Su grupo se llamaba los Antiguos Bebedores de Cola de América."),
     "items": [it("etiqueta", 540, 900, 0.75, delay=0.6, texto="OLD COLA DRINKERS", fondo="#f0c448", rot=-4)],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"fondo": rayos("rojo"), "lines": L("En mayo hubo protestas con carteles en Atlanta, la ciudad donde nació la bebida."),
     "items": [it("multitud", 540, 1700, 1.0, anim="up", n=16, filas=3, escala=0.45, cara="enojado", semilla=7),
               it("etiqueta", 300, 1000, 0.85, delay=1.4, texto="¡LA ORIGINAL!", rot=-6),
               it("pin", 820, 820, 0.6, delay=2.4, anim="drop", texto="ATLANTA")]},
    {"fondo": rayos("gris"), "lines": L("Las pruebas de sabor no habían medido algo: el cariño por la original."),
     "items": [it("icono", 540, 1150, 1.1, anim="pop", tipo="exclamacion")]},
    {"sigue": True, "lines": L("El presidente de la compañía, Donald Keough, lo llamó un apego emocional profundo.",
                               say={0: "El presidente de la compañía, Dónald Kíou, lo llamó un apego emocional profundo."}),
     "items": [it("persona", 280, 1560, 0.85, anim="left", cara="preocupado", **KEOUGH),
               it("nombre", 700, 760, 0.85, delay=1.6, texto="Donald Keough", sub="presidente de la empresa")]},

    # ------------------------------------------------------------ el regreso
    {"fondo": rayos("oro"), "lines": L("El 11 de julio de 1985, Coca-Cola anunció el regreso de la fórmula original."),
     "items": [it("calendario", 540, 1200, 1.0, anim="pop", texto="11 JUL")]},
    {"sigue": True, "lines": L("Con un nombre nuevo: Coca-Cola Classic."),
     "items": [it("etiqueta", 540, 1450, 1.0, delay=0.6, texto="CLASSIC", fondo="#ffffff", rot=-5)]},
    {"sigue": True, "lines": L("Habían pasado setenta y nueve días."),
     "dato": dato(79, "DÍAS DESPUÉS", suf=" DÍAS", delay=0.4)},
    {"fondo": {"tipo": "oficina"}, "lines": L("En la conferencia, Goizueta le dijo al público: los hemos escuchado."),
     "items": [it("persona", 540, 1640, 0.95, anim="up", cara="feliz", brazos="saluda", **GOIZUETA),
               it("etiqueta", 540, 760, 0.9, delay=2.2, texto="«LOS HEMOS ESCUCHADO»", fondo="#ffffff", size=50, rot=-3)]},

    # ------------------------------------------------------------ datos curiosos
    {"fondo": rayos("oro"), "lines": L("Y ahora, cosas que casi nadie sabe."),
     "items": [it("etiqueta", 540, 1150, 1.3, anim="pop", texto="¿SABÍAS?", fondo="#f0c448", rot=-4)],
     "min_dur": 2.0},
    {"fondo": rayos("lila"), "lines": L("Uno. Mucha gente cree que todo fue una estrategia para vender más. La empresa lo niega."),
     "items": [it("icono", 540, 1150, 1.1, anim="pop", tipo="pregunta"),
               it("etiqueta", 540, 1450, 0.85, delay=2.6, texto="¿ESTRATEGIA?", fondo="#ffffff", rot=4)]},
    {"sigue": True, "lines": L("Keough lo resumió así: no somos tan tontos, ni tan listos.",
                               say={0: "Kíou lo resumió así: no somos tan tontos, ni tan listos."}),
     "items": [it("nombre", 540, 760, 0.9, delay=0.4, texto="Donald Keough", sub="presidente de Coca-Cola")]},
    {"fondo": rayos("cielo"), "lines": L("Dos. Un periódico de Seattle le hizo pruebas a ciegas a Gay Mullins, el líder de la protesta.",
                                        say={0: "Dos. Un periódico de Seattle le hizo pruebas a ciegas a Guéi Múlins, el líder de la protesta."}),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="serio", brazos="objeto", **MULLINS),
               it("mesa", 760, 1560, 0.6, delay=1.2, anim="up")]},
    {"sigue": True, "lines": L("No logró distinguir la nueva de la vieja."),
     "items": [it("icono", 760, 1000, 0.85, delay=0.6, anim="pop", tipo="x")]},
    {"fondo": rayos("durazno"), "lines": L("Tres. Goizueta recibió una carta dirigida al Jefe Dodo de Coca-Cola."),
     "items": [it("sobre", 540, 1200, 1.2, anim="drop", color="#f8fafc", disco=False, texto="JEFE DODO")]},
    {"sigue": True, "lines": L("El dodo es un ave extinta."),
     "items": [it("chapa", 540, 760, 1.25, delay=0.4, texto="DODO", sub="ave extinta")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Y cuatro. La noticia del regreso fue tan grande que Peter Jennings, de la cadena ABC, salió al aire de emergencia.",
                                           say={0: "Y cuatro. La noticia del regreso fue tan grande que Píter Yénings, de la cadena A B C, salió al aire de emergencia."}),
     "items": [it("tv", 540, 1200, 1.1, anim="pop", play=False, texto="ÚLTIMA HORA"),
               it("nombre", 540, 760, 0.9, delay=2.6, texto="Peter Jennings", sub="presentador de ABC")]},
    {"sigue": True, "lines": L("Interrumpió la telenovela General Hospital para darla.",
                               say={0: "Interrumpió la telenovela Yéneral Óspital para darla."}),
     "items": [it("etiqueta", 540, 1560, 0.8, delay=0.4, texto="INTERRUMPIDO", fondo="#ef4444", rot=4)]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("gris"), "lines": L("La fórmula nueva siguió a la venta, y a inicios de los noventa cambió de nombre a Coke II.",
                                       say={0: "La fórmula nueva siguió a la venta, y a inicios de los noventa cambió de nombre a Couk tu."}),
     "items": [marca(540, 1150, 1.0, "COKE II", "#e5e7eb"),
               it("chapa", 540, 760, 1.3, delay=2.6, texto="AÑOS 90")]},
    {"sigue": True, "lines": L("Hoy ya no se vende en Estados Unidos."),
     "items": [it("icono", 820, 1350, 0.85, delay=0.4, anim="pop", tipo="x")]},
    {"fondo": rayos("lila"), "lines": L("En 2019 volvió por poco tiempo, en latas de edición limitada, por la tercera temporada de Stranger Things."),
     "items": [it("tv", 540, 1250, 1.0, anim="pop", play=True, color=ROJO),
               it("chapa", 540, 760, 1.35, delay=1.0, texto="2019")]},
    {"sigue": True, "lines": L("Una serie que transcurre justo en el verano de 1985."),
     "items": [it("etiqueta", 540, 1600, 0.85, delay=0.6, texto="VERANO 1985", rot=-4)]},
    {"fondo": rayos("menta"), "lines": L("Desde entonces, la empresa lanza versiones nuevas junto a la original, en vez de reemplazarla."),
     "items": [marca(540, 1000, 1.1, "ORIGINAL", "#ffffff", rot=-5),
               it("etiqueta", 540, 1300, 1.1, delay=1.6, texto="+ NUEVAS", fondo="#f0c448", rot=5)]},

    # ------------------------------------------------------------ cierre
    {"fondo": {"tipo": "noche"}, "lines": L("Casi doscientas mil pruebas dijeron que la nueva sabía mejor. Pero la gente no compraba solo un sabor."),
     "items": [it("chapa", 540, 1000, 1.4, texto="~200.000", sub="pruebas de sabor"),
               it("multitud", 540, 1700, 1.0, delay=2.6, anim="up", n=16, filas=3, escala=0.45, cara="enojado", semilla=9)],
     "cam": {"z": [1.0, 1.08], "f": [540, 1300]}},
    {"fondo": rayos("oro"), "lines": L("¿Y tú? Con dos vasos sin marca, ¿podrías distinguir una cola de otra? Te leo en los comentarios."),
     "items": [it("mesa", 540, 1560, 1.0, anim="up"),
               it("etiqueta", 380, 1230, 0.9, delay=1.0, texto="M", fondo="#ffffff", rot=-4),
               it("etiqueta", 700, 1230, 0.9, delay=1.4, texto="Q", fondo="#ffffff", rot=4),
               it("etiqueta", 540, 800, 1.0, delay=2.4, texto="¿LA TUYA?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "Coca-Cola cambió su fórmula en 1985 y tuvo que dar marcha atrás en 79 días",
    "description": ("La historia de New Coke: cómo Coca-Cola, perdiendo terreno frente a Pepsi y su Pepsi Challenge, probó una fórmula "
                    "más dulce con casi 200.000 personas, la lanzó el 23 de abril de 1985 y tuvo que traer de vuelta la original como "
                    "Coca-Cola Classic el 11 de julio de 1985, 79 días después.\n"
                    "Fuentes: The Coca-Cola Company (historia corporativa); TIME (1985 y artículo de James C. Cobb); HISTORY; Snopes; "
                    "Mental Floss; Fortune; The Boston Globe; Atlanta Journal-Constitution; BevNET; El Cronista."),
    "hashtags": ["#DatoBomba", "#CocaCola", "#NewCoke", "#marketing", "#historiasreales"],
    "source_url": "https://www.coca-colacompany.com/about-us/history/new-coke-the-most-memorable-marketing-blunder-ever",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_newcoke.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55),
      "titulo:", len(guion["title"]))
