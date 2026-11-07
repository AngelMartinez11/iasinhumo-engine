"""Genera ejemplos/hsf_armero.json: la tragedia de Armero, 1985 (Dato Bomba, canal historias, motor v4, formato largo).

Estructura: gancho -> pregunta -> historia en orden (pueblo y volcan, senales, el mapa, la noche,
Omayra) -> cosas que casi nadie sabe -> que paso despues -> cierre con pregunta.
Trato respetuoso: no se dibuja a Omayra ni a victimas; se usan simbolos (agua, reloj, camaras, mensajes).
Nota para la biblioteca: no hay pieza de volcan ni de flores; el volcan se arma con islas apiladas.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

CIENT = {"ropa": "bata", "lentes": True, "pelo": "#3a2a1e", "peinado": "corto", "camisa": "#e5e7eb"}
CIENT2 = {"ropa": "bata", "pelo": "#1f1f1f", "peinado": "largo", "camisa": "#e5e7eb", "piel": "#c68a5c"}
FUNC = {"ropa": "traje", "corbata": "#ef4444", "pelo": "#1f1f1f", "peinado": "canoso"}
VECINO = {"camisa": "#f59e0b", "pelo": "#1f1f1f", "piel": "#c68a5c"}
VECINA = {"camisa": "#ec4899", "pelo": "#3a2a1e", "peinado": "largo", "piel": "#e0a878"}
LODO = "#7c5a3a"
AGUA = "#1e3a8a"


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


def volcan(x=540, y=1560, s=1.0, delay=0.0, id="volcan"):
    """Montana armada con islas apiladas (no hay pieza de volcan en la biblioteca)."""
    out, yy = [], y
    for k, f in enumerate([1.25, 0.95, 0.68, 0.42]):
        out.append(it("isla", x, yy, f * s, delay=delay + k * 0.12, anim="crece", id=f"{id}{k}",
                      edificio=False, faro=False))
        yy -= 150 * f * s
    return out


def pueblo(y=1560, delay=0.0, prefijo="casa"):
    return [it("edificio", 200, y, 0.55, delay=delay, anim="crece", id=prefijo + "1", texto="", pisos=3, ancho=300),
            it("tienda", 540, y, 0.5, delay=delay + 0.2, anim="crece", id=prefijo + "2", texto="ARMERO", letrero="#166534", letra="#ffffff"),
            it("edificio", 880, y, 0.55, delay=delay + 0.4, anim="crece", id=prefijo + "3", texto="", pisos=4, ancho=280, color="#fde68a")]


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": {"tipo": "noche"}, "lines": L("Un mes antes de la tragedia ya existía un mapa que marcaba en peligro al valle de Armero."),
     "items": [it("libro", 540, 1250, 1.2, anim="pop", abierto=True, color="#166534", texto="MAPA"),
               it("pin", 640, 1180, 0.45, delay=1.8, anim="drop", color="#ef4444"),
               it("etiqueta", 540, 760, 0.95, delay=2.6, texto="ZONA DE PELIGRO", fondo="#ef4444", rot=-4)],
     "cam": {"z": [1.0, 1.08], "f": [540, 1200]}},
    {"sigue": True, "lines": L("Y aun así, la noche del 13 de noviembre de 1985, nadie evacuó."),
     "items": [it("calendario", 860, 1560, 0.55, anim="pop", texto="1985"),
               it("icono", 230, 1500, 0.8, delay=1.6, anim="pop", tipo="x")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Esa noche, en un solo pueblo, murieron más de veinte mil personas."),
     "items": pueblo(delay=0.0),
     "dato": dato(20000, "MUERTOS SOLO EN ARMERO", pre="+", y=680, delay=1.4),
     "cam": {"z": [1.1, 1.0], "f": [540, 1300]}},
    {"fondo": rayos("oro"), "lines": L("¿Cómo desaparece un pueblo al que avisaron el volcán y los científicos?"),
     "items": volcan(540, 1560, 0.7) + [it("icono", 540, 760, 1.1, delay=2.2, anim="pop", tipo="pregunta")]},

    # ------------------------------------------------------------ el pueblo y el volcan
    {"fondo": rayos("menta"), "lines": L("Armero era un pueblo del Tolima, en Colombia, de unos veintinueve mil habitantes."),
     "items": pueblo(delay=0.0) + [it("chapa", 540, 760, 1.4, delay=1.8, texto="29.000", sub="habitantes")],
     "cam": {"z": [1.0, 1.06], "f": [540, 1300]}},
    {"sigue": True, "lines": L("A menos de cincuenta kilómetros estaba el Nevado del Ruiz."),
     "items": [it("flecha", 540, 1160, 0.8, delay=0.4, anim="fade", rot=0),
               it("etiqueta", 540, 1000, 0.8, delay=1.2, texto="< 50 KM", rot=4)]},
    {"fondo": rayos("cielo"), "lines": L("Un volcán de cinco mil trescientos ochenta y nueve metros, con la cima cubierta de glaciares."),
     "items": volcan(540, 1560, 1.0) + [it("chapa", 540, 780, 1.4, delay=1.6, texto="5.389 M", sub="Nevado del Ruiz")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1350]}},
    {"sigue": True, "lines": L("Llevaba unos ciento cuarenta años sin una erupción grande."),
     "items": [it("etiqueta", 540, 1000, 0.9, delay=0.3, texto="140 AÑOS EN CALMA", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("durazno"), "lines": L("Pero en 1845 un flujo de lodo bajó por el río Lagunillas y mató a cientos de personas."),
     "items": [it("calendario", 540, 900, 0.7, anim="pop", texto="1845", color="#7c5a3a"),
               it("olas", 540, 1380, 1.0, delay=1.4, anim="left", color=LODO)]},
    {"sigue": True, "lines": L("Y Armero creció justo encima de ese lodo."),
     "items": [it("tienda", 540, 1440, 0.45, delay=0.3, anim="crece", texto="ARMERO", letrero="#166534", letra="#ffffff")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1350]}},

    # ------------------------------------------------------------ las senales
    {"fondo": rayos("azul"), "lines": L("En noviembre de 1984 el volcán despertó: empezaron los sismos."),
     "items": volcan(540, 1560, 0.85) + [it("calendario", 860, 780, 0.55, delay=0.8, anim="pop", texto="1984"),
                                          it("icono", 230, 780, 0.8, delay=1.8, anim="pop", tipo="exclamacion")]},
    {"fondo": rayos("lila"), "lines": L("En marzo de 1985, un experto que asesoraba a la UNESCO recomendó dos cosas.", say={0: "En marzo de 1985, un experto que asesoraba a la Unesco recomendó dos cosas."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="tomblin", cara="serio", brazos="senala", **CIENT),
               it("nombre", 540, 720, 1.0, delay=1.4, id="ntom", texto="John Tomblin", sub="vulcanologo, asesor de la UNESCO")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"sigue": True, "quita": ["ntom"], "lines": L("Instalar sismógrafos y hacer un mapa de amenazas."),
     "items": [it("chapa", 290, 760, 1.2, texto="1", sub="sismografos"),
               it("chapa", 790, 760, 1.2, delay=1.0, texto="2", sub="mapa de amenazas")]},
    {"fondo": {"tipo": "noche"}, "lines": L("El 11 de septiembre llegó la primera señal fuerte: una erupción menor que duró siete horas."),
     "items": volcan(540, 1560, 0.85) + [it("chapa", 540, 780, 1.35, delay=1.2, texto="11 SEPT", sub="7 horas de erupcion")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1350]}},
    {"fondo": rayos("cielo"), "lines": L("Días después, un comité asesor pidió con urgencia el mapa de amenaza."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="preocupado", brazos="cruzados", **FUNC),
               it("sobre", 780, 1150, 0.7, delay=1.2, anim="drop", color="#ef4444", texto="URGENTE", disco=False)]},

    # ------------------------------------------------------------ el mapa
    {"fondo": rayos("menta"), "lines": L("Geólogos de Ingeominas, hoy Servicio Geológico Colombiano, trabajaron contrarreloj.", say={0: "Geólogos de Inyeominas, hoy Servicio Geológico Colombiano, trabajaron contrarreloj."}),
     "items": [it("persona", 280, 1560, 0.85, anim="left", cara="preocupado", brazos="objeto", **CIENT),
               it("persona", 800, 1560, 0.85, delay=0.5, anim="right", cara="serio", brazos="senala", flip=True, **CIENT2),
               it("libro", 540, 1160, 0.6, delay=1.6, anim="pop", abierto=True, color="#166534", texto="")]},
    {"fondo": rayos("oro"), "lines": L("El 7 de octubre de 1985 el mapa quedó oficializado."),
     "items": [it("calendario", 540, 1150, 1.0, anim="drop", texto="7 OCT", color="#166534"),
               it("chapa", 540, 760, 1.3, delay=1.4, texto="1985", sub="mapa oficial")]},
    {"sigue": True, "lines": L("Fue uno de los primeros mapas de amenaza volcánica de Colombia."),
     "items": [it("etiqueta", 540, 1450, 0.85, delay=0.4, texto="DE LOS PRIMEROS", rot=-4)]},
    {"fondo": rayos("rojo"), "lines": L("Y mostraba peligro de flujos de lodo justo en el valle donde estaba Armero."),
     "items": [it("libro", 540, 1250, 1.2, anim="pop", abierto=True, color="#166534", texto="MAPA"),
               it("pin", 640, 1180, 0.45, delay=1.4, anim="drop", color="#ef4444", texto="ARMERO")],
     "cam": {"z": [1.0, 1.12], "f": [600, 1200]}},
    {"sigue": True, "lines": L("Pero el mapa casi no circuló, y muchos lo ignoraron o lo entendieron mal."),
     "items": [it("etiqueta", 540, 780, 1.0, delay=0.6, texto="IGNORADO", fondo="#ffffff", rot=6)]},

    # ------------------------------------------------------------ la noche
    {"fondo": {"tipo": "noche"}, "lines": L("Miércoles 13 de noviembre. Pasadas las tres de la tarde, el volcán lanzó columnas de ceniza."),
     "items": volcan(540, 1560, 0.9) + [it("reloj", 860, 780, 0.6, delay=0.8, anim="pop", hora=3),
                                         it("etiqueta", 540, 1000, 0.9, delay=2.2, texto="CENIZA", fondo="#94a3b8", rot=-3)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1350]}},
    {"fondo": rayos("gris"), "lines": L("Cayó ceniza sobre Armero, pero a la gente le pidieron calma y quedarse en casa."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="preocupado", brazos="cabeza", **VECINA),
               it("telefono", 800, 1200, 0.65, delay=1.4, anim="pop", texto="RADIO", color="#64748b"),
               it("etiqueta", 800, 820, 0.9, delay=2.6, texto="CALMA", fondo="#ffffff", rot=5)]},
    {"sigue": True, "lines": L("El alcalde y el párroco aseguraron que no había peligro esa noche."),
     "items": [it("icono", 300, 760, 0.8, delay=1.2, anim="pop", tipo="exclamacion")]},
    {"fondo": {"tipo": "oficina"}, "lines": L("Esa tarde se reunió un comité de emergencia. No ordenó evacuar esa noche."),
     "items": [it("persona", 300, 1640, 0.85, anim="left", cara="serio", brazos="cruzados", **FUNC),
               it("persona", 780, 1640, 0.85, delay=0.4, anim="right", cara="preocupado", flip=True, **CIENT),
               it("icono", 540, 800, 0.9, delay=2.4, anim="pop", tipo="x")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Por la noche llovía, y una tormenta tapaba la cima del volcán."),
     "items": volcan(540, 1560, 0.9) + [it("etiqueta", 540, 900, 1.0, delay=1.4, texto="TORMENTA", fondo="#64748b", tinta="#ffffff", rot=0)]},
    {"sigue": True, "lines": L("A las nueve y ocho minutos de la noche, el Ruiz entró en erupción.", pausa=0.3),
     "items": [it("chapa", 540, 1100, 1.5, delay=0.4, texto="21:08", sub="13 de noviembre")],
     "cam": {"z": [1.0, 1.12], "f": [540, 1150]}},
    {"fondo": rayos("rojo"), "lines": L("El calor derritió parte del hielo, y el agua se mezcló con ceniza, rocas y tierra."),
     "items": volcan(540, 1560, 0.9) + [it("olas", 540, 1420, 1.0, delay=2.2, anim="up", color=LODO)]},
    {"sigue": True, "lines": L("Así nacieron los lahares: ríos de lodo que crecían al arrastrar todo a su paso."),
     "items": [it("etiqueta", 540, 860, 1.1, delay=0.4, texto="LAHAR", fondo="#f0c448", rot=-5)]},
    {"fondo": rayos("durazno"), "lines": L("Bajaron por los cañones a hasta unos cincuenta kilómetros por hora."),
     "items": [it("olas", 540, 1350, 1.0, anim="left", color=LODO),
               it("flecha", 540, 1100, 0.9, delay=0.8, anim="left", rot=0)],
     "dato": dato(50, "VELOCIDAD ESTIMADA", suf=" KM/H", y=680, delay=1.6)},
    {"fondo": {"tipo": "liso", "c": "#e4e4ea"}, "lines": L("En los cañones más estrechos, el lodo superó los cuarenta metros de alto."),
     "items": [it("edificio", 540, 1560, 0.9, anim="crece", texto="", pisos=12, ancho=260),
               it("chapa", 540, 760, 1.4, delay=1.4, texto="+40 M", sub="altura del lodo")]},
    {"fondo": {"tipo": "noche"}, "lines": L("En Armero se fue la luz, y las alertas no llegaron."),
     "items": pueblo(delay=0.0) + [it("telefono", 540, 900, 0.5, delay=1.6, anim="pop", texto="SIN SEÑAL", color="#475569"),
                                    it("icono", 780, 760, 0.6, delay=2.4, anim="pop", tipo="x")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Hacia las once y media, dos horas y media después de la erupción, llegó el lodo."),
     "items": [it("reloj", 540, 1100, 1.1, anim="pop", hora=11.5),
               it("chapa", 540, 1460, 1.3, delay=1.6, texto="23:30", sub="llega el lodo")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1150]}},
    {"fondo": {"tipo": "noche"}, "lines": L("Primero entró agua fría. Unos diez minutos después llegó la oleada más grande."),
     "items": pueblo(delay=0.0) + [it("olas", 540, 1500, 1.0, delay=0.6, anim="left", color="#475569", id="agua1")]},
    {"sigue": True, "quita": ["agua1"], "lines": L("En diez a veinte minutos destruyó la mayoría de los edificios.", pausa=0.3),
     "items": [it("olas", 540, 1250, 1.0, anim="left", color=LODO)],
     "cam": {"z": [1.0, 1.08], "f": [540, 1350]}},
    {"fondo": rayos("gris"), "lines": L("Siguieron más oleadas hasta pasada la una de la madrugada."),
     "items": [it("reloj", 540, 1150, 1.0, anim="pop", hora=1),
               it("olas", 540, 1480, 1.0, delay=1.0, anim="left", color=LODO)]},
    {"fondo": {"tipo": "noche"}, "lines": L("Murieron cerca de tres de cada cuatro habitantes de Armero."),
     "items": [it("lapida", 540, 1560, 1.15, anim="crece", texto="ARMERO", sub="1985")],
     "dato": dato(75, "DE LOS HABITANTES", suf=" %", y=680, delay=1.2)},
    {"sigue": True, "lines": L("En total, más de veintitrés mil muertos; se estima que cerca de veinticinco mil."),
     "dato": dato(25000, "VÍCTIMAS ESTIMADAS", pre="~", y=680, delay=1.0),
     "cam": {"z": [1.0, 1.06], "f": [540, 1300]}},
    {"fondo": rayos("gris"), "lines": L("Hubo unos cinco mil heridos y más de cinco mil viviendas destruidas."),
     "items": [it("chapa", 290, 900, 1.3, texto="5.000", sub="heridos"),
               it("chapa", 800, 900, 1.3, delay=1.4, texto="+5.000", sub="viviendas"),
               it("edificio", 540, 1560, 0.6, delay=0.6, anim="crece", texto="", pisos=3, ancho=320, color="#94a3b8")]},

    # ------------------------------------------------------------ Omayra (sin mostrarla)
    {"fondo": rayos("cielo"), "lines": L("Entre los sobrevivientes atrapados estaba Omayra Sánchez, una niña de trece años."),
     "items": [it("nombre", 540, 760, 1.05, delay=0.8, id="nomy", texto="Omayra Sánchez", sub="13 años"),
               it("olas", 540, 1420, 1.0, delay=0.4, anim="up", color=AGUA)],
     "cam": {"z": [1.0, 1.05], "f": [540, 1100]}},
    {"sigue": True, "quita": ["nomy"], "lines": L("Quedó atrapada entre escombros y agua durante unas sesenta horas."),
     "items": [it("reloj", 540, 1180, 0.85, anim="pop", hora=6)],
     "dato": dato(60, "HORAS", suf=" H", y=680, delay=1.2)},
    {"fondo": rayos("lila"), "lines": L("Rescatistas y vecinos la acompañaron, y la televisión lo transmitió todo."),
     "items": [it("camara", 300, 1150, 0.75, anim="left", tipo="digital"),
               it("tv", 780, 1180, 0.75, delay=1.4, anim="right", play=False, texto="EN VIVO")]},
    {"sigue": True, "lines": L("Murió tres días después de la avalancha. Su historia dio la vuelta al mundo.", pausa=0.4),
     "items": [it("globo", 540, 1450, 0.45, delay=1.4, anim="pop")]},

    # ------------------------------------------------------------ cosas que casi nadie sabe
    {"fondo": rayos("durazno"), "lines": L("Y ahora, cosas que casi nadie sabe."),
     "items": [it("etiqueta", 540, 1150, 1.2, anim="pop", texto="¿SABÍAS?", rot=-5)]},
    {"fondo": rayos("cielo"), "lines": L("Uno. La erupción derritió apenas cerca del diez por ciento del hielo del volcán. Eso bastó."),
     "items": volcan(540, 1560, 0.9) + [it("chapa", 540, 780, 1.5, delay=1.6, texto="~10 %", sub="del hielo")]},
    {"fondo": rayos("lila"), "lines": L("Dos. La foto de Omayra, del francés Frank Fournier, ganó el World Press Photo de 1986.",
                                        say={0: "Dos. La foto de Omayra, del francés Frank Furnié, ganó el World Press Photo de 1986."}),
     "items": [it("camara", 540, 1250, 1.0, anim="pop", tipo="antigua"),
               it("nombre", 540, 760, 0.95, delay=1.6, texto="Frank Fournier", sub="fotografo"),
               it("chapa", 540, 1560, 1.2, delay=3.0, texto="1986", sub="World Press Photo")]},
    {"fondo": rayos("menta"), "lines": L("Tres. Según el Servicio Geológico Colombiano, con una alerta a tiempo habrían tenido al menos dos horas para salir."),
     "items": [it("reloj", 540, 1150, 1.0, anim="pop", hora=2),
               it("chapa", 540, 1500, 1.3, delay=1.8, texto="2 HORAS", sub="para salir")]},
    {"fondo": rayos("oro"), "lines": L("Cuatro. El 6 de julio de 1986, el papa Juan Pablo II rezó en Armero, frente a una cruz donde estaba la iglesia."),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="triste", brazos="objeto", ropa="bata", camisa="#f8fafc", pelo="#c9c9c9", peinado="canoso"),
               it("nombre", 540, 720, 0.95, delay=1.4, texto="Juan Pablo II", sub="papa"),
               it("calendario", 870, 1050, 0.5, delay=2.4, anim="pop", texto="1986")]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("gris"), "lines": L("¿Y qué pasó después?"),
     "items": [it("icono", 540, 1150, 1.1, anim="pop", tipo="pregunta")]},
    {"sigue": True, "lines": L("Armero nunca se reconstruyó. Hoy es un camposanto de ruinas, tumbas y maleza."),
     "items": [it("lapida", 300, 1560, 0.8, anim="crece", texto="ARMERO"),
               it("lapida", 780, 1560, 0.8, delay=0.5, anim="crece", texto="1985")]},
    {"fondo": rayos("lila"), "lines": L("Según la BBC, su tumba es el lugar más visitado: la rodean flores y tarjetas de agradecimiento."),
     "items": [it("sobre", 300, 1250, 0.9, anim="drop", color="#ec4899", texto="GRACIAS", disco=False),
               it("sobre", 780, 1250, 0.9, delay=0.5, anim="drop", color="#f59e0b", texto="GRACIAS", disco=False),
               it("etiqueta", 540, 820, 0.9, delay=1.8, texto="FLORES Y MENSAJES", fondo="#fbcfe8", rot=-3)]},
    {"fondo": rayos("azul"), "lines": L("En 1988, Colombia creó un sistema nacional para prevenir y atender desastres."),
     "items": [it("edificio", 540, 1560, 0.8, anim="crece", texto="PREVENCIÓN", pisos=6, ancho=480),
               it("calendario", 860, 760, 0.5, delay=1.2, anim="pop", id="cal88", texto="1988")]},
    {"sigue": True, "quita": ["cal88"], "lines": L("Y hoy el Servicio Geológico vigila en tiempo real veinticinco volcanes."),
     "items": [],
     "dato": dato(25, "VOLCANES VIGILADOS", y=680, delay=1.0)},
    {"fondo": {"tipo": "noche"}, "lines": L("Y hay una herida abierta: una fundación ha documentado unos quinientos ochenta niños desaparecidos."),
     "items": [it("nino", 300, 1560, 1.4, anim="left", cara="triste", camisa="#22c55e"),
               it("nino", 780, 1560, 1.4, delay=0.5, anim="right", cara="triste", camisa="#f59e0b", flip=True)],
     "dato": dato(580, "NIÑOS DESAPARECIDOS", y=680, delay=1.8)},
    {"fondo": rayos("menta"), "lines": L("Algunos fueron dados en adopción. Gracias a pruebas de ADN, han encontrado a cuatro con vida."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="feliz", brazos="saluda", **VECINA),
               it("persona", 780, 1560, 0.9, delay=0.5, anim="right", cara="feliz", brazos="saluda", flip=True, **VECINO),
               it("chapa", 540, 760, 1.4, delay=1.8, texto="4", sub="reencuentros")]},

    # ------------------------------------------------------------ cierre
    {"fondo": {"tipo": "noche"}, "lines": L("Había un mapa. Había científicos. Había dos horas."),
     "items": [it("libro", 230, 1150, 0.45, anim="pop", abierto=True, color="#166534", texto="MAPA"),
               it("persona", 540, 1560, 0.8, delay=0.9, anim="up", cara="preocupado", **CIENT),
               it("reloj", 850, 1150, 0.5, delay=1.8, anim="pop", hora=2)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1250]}},
    {"sigue": True, "lines": L("Lo que faltó fue que el aviso llegara a tiempo.", pausa=0.4),
     "items": [it("etiqueta", 540, 760, 1.0, delay=0.4, texto="EL AVISO NO LLEGÓ", fondo="#ef4444", rot=-4)]},
    {"fondo": rayos("oro"), "lines": L("¿Tú sabrías qué hacer si en tu ciudad sonara una alerta así? Te leo en los comentarios."),
     "items": [it("telefono", 540, 1200, 0.9, anim="pop", texto="ALERTA", color="#ef4444"),
               it("etiqueta", 540, 760, 1.0, delay=1.6, texto="¿Y TÚ?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "El volcán avisó, los científicos avisaron... y Armero desapareció igual",
    "description": ("13 de noviembre de 1985: la erupción del Nevado del Ruiz derritió parte de sus glaciares y los lahares "
                    "borraron Armero, en Colombia. Un mes antes ya existía un mapa de amenaza que marcaba el peligro. "
                    "En memoria de las victimas y de Omayra Sanchez.\n"
                    "Fuentes: Servicio Geologico Colombiano (GeoFlash 2015 y 'Cinco lecciones que la tragedia de Armero nos dejo'); "
                    "USGS (Volcano Watch y ficha de lahares del Ruiz); NOAA NGDC; EARTH Magazine; Scientific American; "
                    "BBC News Mundo (2025); AP (2025); El Heraldo; Vaticano (oracion en Armero, 6/7/1986); World Press Photo."),
    "hashtags": ["#DatoBomba", "#Armero", "#NevadodelRuiz", "#Colombia", "#historiasreales"],
    "source_url": "https://www2.sgc.gov.co/Noticias/Paginas/Cinco-lecciones-que-la-tragedia-de-Armero-nos-dejo.aspx",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_armero.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55),
      "titulo:", len(guion["title"]))
