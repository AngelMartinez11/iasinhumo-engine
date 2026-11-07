"""Genera ejemplos/hsf_yahoo.json: Yahoo pudo comprar Google y Facebook y termino vendida por una fraccion.

Canal Dato Bomba (canal "historias", motor v4, formato largo, sin tarjetas de capitulo).
Estructura: gancho -> pregunta -> la historia en orden -> curiosidades -> que paso despues -> cierre con pregunta.
Los bloques se marcan con la narracion y con cambio de fondo.

Notas para la biblioteca de piezas: no hay pieza de "trailer" (se usa edificio bajo con letrero).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

MORADO = "#7c3aed"
JERRY = {"camisa": MORADO, "pelo": "#1f1f1f", "peinado": "corto", "lentes": True}
DAVID = {"camisa": "#f0c448", "pelo": "#3a2a1e", "peinado": "largo"}
LARRY = {"camisa": "#3b82f6", "pelo": "#3a2a1e", "peinado": "corto"}
SERGEY = {"camisa": "#22c55e", "pelo": "#1f1f1f", "peinado": "corto"}
SEMEL = {"ropa": "traje", "corbata": MORADO, "pelo": "#c9c9c9", "peinado": "canoso"}
MARK = {"camisa": "#9ca3af", "pelo": "#6b4423", "peinado": "corto"}
BALLMER = {"ropa": "traje", "corbata": "#0ea5e9", "pelo": "#c9c9c9", "peinado": "calvo"}
EDIF_YAHOO = {"texto": "YAHOO!", "pisos": 7, "color": "#ddd6fe", "letrero": MORADO, "ancho": 420}


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


NOCHE = {"tipo": "noche"}


def dato(num, texto, pre="", suf="", y=640, delay=1.0, cuenta=True):
    return {"num": num, "pre": pre, "suf": suf, "texto": texto, "y": y, "delay": delay, "cuenta": cuenta}


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": rayos("lila"), "lines": L("En el año 2000, Yahoo llegó a valer unos 125 mil millones de dólares.",
                                        say={0: "En el año 2000, Yahoo llegó a valer unos ciento veinticinco mil millones de dólares."}),
     "items": [it("edificio", 540, 1560, 1.05, anim="crece", id="ed", **EDIF_YAHOO)],
     "dato": dato(125000, "MILLONES DE DÓLARES (2000)", pre="$", y=640, delay=1.4),
     "cam": {"z": [1.0, 1.06], "f": [540, 1200]}},
    {"fondo": NOCHE, "lines": L("Diecisiete años después, su negocio principal se vendió por menos de cinco mil millones."),
     "items": [it("edificio", 540, 1560, 0.8, anim="fade", **dict(EDIF_YAHOO, color="#a1a1aa")),
               it("etiqueta", 540, 1640, 0.9, delay=1.8, texto="VENDIDA EN 2017", fondo="#ef4444", rot=-4)],
     "dato": dato(4480, "MILLONES DE DÓLARES (2017)", pre="$", y=640, delay=2.2),
     "cam": {"z": [1.1, 1.0], "f": [540, 1250]}},
    {"fondo": rayos("rojo"), "lines": L("Y en el camino tuvo la oportunidad de comprar Google.", "Y también Facebook."),
     "items": [it("etiqueta", 540, 900, 1.15, texto="GOOGLE", fondo="#ffffff", rot=-5),
               it("icono", 850, 820, 0.7, delay=1.2, anim="pop", tipo="x"),
               it("etiqueta", 540, 1250, 1.15, at=1, texto="FACEBOOK", fondo="#ffffff", rot=4),
               it("icono", 850, 1180, 0.7, at=1, delay=0.8, anim="pop", tipo="x")]},
    {"fondo": rayos("oro"), "lines": L("¿Cómo deja pasar una empresa los dos mejores negocios de internet?"),
     "items": [it("persona", 540, 1560, 1.0, anim="up", cara="preocupado", brazos="cabeza", **SEMEL),
               it("icono", 540, 700, 1.0, delay=1.8, anim="pop", tipo="pregunta")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1000]}},

    # ------------------------------------------------------------ 1. dos estudiantes y una lista
    {"fondo": rayos("cielo"), "lines": L("Enero de 1994. Universidad de Stanford, en California."),
     "items": [it("pin", 540, 1400, 1.1, anim="drop", texto="STANFORD", color=MORADO),
               it("calendario", 860, 720, 0.55, delay=1.2, anim="pop", texto="1994")]},
    {"fondo": rayos("lila"), "lines": L("Dos estudiantes de doctorado, Jerry Yang y David Filo, tenían que escribir su tesis.",
                                        say={0: "Dos estudiantes de doctorado, Yérri Yang y Déivid Fáilo, tenían que escribir su tesis."}),
     "items": [it("persona", 300, 1560, 0.9, anim="left", id="jerry", cara="feliz", **JERRY),
               it("nombre", 300, 690, 0.8, delay=1.6, texto="Jerry Yang", sub="estudiante de Stanford"),
               it("persona", 780, 1560, 0.9, delay=0.6, anim="right", id="david", cara="serio", **DAVID),
               it("nombre", 780, 860, 0.8, delay=2.6, texto="David Filo", sub="estudiante de Stanford")],
     "cam": {"z": [1.0, 1.05], "f": [540, 1150]}},
    {"fondo": rayos("durazno"), "lines": L("Pero en vez de eso, armaban una lista con sus páginas web favoritas."),
     "items": [it("pc_escritorio", 540, 1560, 1.0, anim="crece", texto="LISTA"),
               it("etiqueta", 540, 760, 0.9, delay=1.6, texto="SUS WEBS FAVORITAS", rot=-4)]},
    {"fondo": rayos("menta"), "lines": L("Trabajaban en un tráiler dentro del campus."),
     "items": [it("edificio", 540, 1560, 1.0, anim="crece", texto="TRÁILER", pisos=2, ancho=640, color="#f1f5f9", letrero="#475569"),
               it("persona", 860, 1640, 0.55, delay=0.8, anim="right", cara="feliz", **JERRY)]},
    {"fondo": rayos("cielo"), "lines": L("La lista se llamaba la Guía de Jerry y David para la World Wide Web.",
                                         say={0: "La lista se llamaba la Guía de Yérri y Déivid para la Uórld Uáid Ueb."}),
     "items": [it("libro", 540, 1200, 1.2, anim="pop", abierto=True, texto="GUÍA"),
               it("chapa", 540, 760, 1.3, delay=1.4, texto="1994", sub="Jerry and David's Guide")]},
    {"fondo": rayos("lila"), "lines": L("No había buscadores como los de hoy: ellos ordenaban cada página a mano, por categorías."),
     "items": [it("etiqueta", 300, 760, 0.8, texto="DEPORTES", fondo="#ffffff", rot=-5),
               it("etiqueta", 780, 900, 0.8, delay=0.7, texto="CIENCIA", fondo="#ffffff", rot=4),
               it("etiqueta", 330, 1150, 0.8, delay=1.4, texto="MÚSICA", fondo="#ffffff", rot=3),
               it("etiqueta", 770, 1330, 0.8, delay=2.1, texto="NOTICIAS", fondo="#ffffff", rot=-3)]},
    {"fondo": rayos("oro"), "lines": L("Ese mismo año le pusieron un nombre más corto: Yahoo."),
     "items": [it("etiqueta", 540, 1150, 1.6, anim="pop", texto="YAHOO!", fondo="#ddd6fe", rot=-6)],
     "cam": {"z": [1.0, 1.1], "f": [540, 1150]}},
    {"sigue": True, "lines": L("Dicen que son unas siglas en inglés."),
     "items": [it("chapa", 540, 1450, 1.2, delay=0.8, texto="Y.A.H.O.O.", sub="siglas en ingles")]},
    {"fondo": rayos("durazno"), "lines": L("Pero lo eligieron por otra razón: en Los viajes de Gulliver, un yahoo es alguien rudo y sin modales.",
                                           say={0: "Pero lo eligieron por otra razón: en Los viajes de Gúliver, un yajú es alguien rudo y sin modales."}),
     "items": [it("libro", 540, 1250, 1.0, anim="pop", texto="GULLIVER", color="#b45309"),
               it("etiqueta", 540, 760, 0.9, delay=2.0, texto="RUDO Y SIN MODALES", fondo="#ffffff", rot=4)]},

    # ------------------------------------------------------------ 2. el portal
    {"fondo": rayos("azul"), "lines": L("En marzo de 1995 se convirtieron en empresa."),
     "items": [it("edificio", 540, 1560, 0.95, anim="crece", **EDIF_YAHOO),
               it("calendario", 860, 720, 0.55, delay=1.0, anim="pop", texto="1995")]},
    {"fondo": rayos("menta"), "lines": L("Y en abril de 1996 salieron a la bolsa, a trece dólares por acción."),
     "items": [it("grafica", 540, 1540, 1.1, anim="crece", tipo="sube", color=MORADO),
               it("chapa", 300, 760, 1.35, delay=1.6, texto="$13", sub="precio de salida")]},
    {"sigue": True, "lines": L("El primer día la acción llegó a cuarenta y tres."),
     "items": [it("chapa", 790, 760, 1.35, delay=0.4, texto="$43", sub="el mismo dia")]},
    {"fondo": rayos("lila"), "lines": L("A finales de los noventa, Yahoo era la puerta de entrada a internet: correo, noticias, chat, juegos."),
     "items": [it("laptop", 540, 1450, 1.1, anim="pop", texto="YAHOO!", color="#c4b5fd"),
               it("etiqueta", 250, 760, 0.7, delay=1.6, texto="CORREO", fondo="#ffffff", rot=-5),
               it("etiqueta", 540, 900, 0.7, delay=2.2, texto="NOTICIAS", fondo="#ffffff", rot=4),
               it("etiqueta", 830, 760, 0.7, delay=2.8, texto="CHAT", fondo="#ffffff", rot=-3)]},
    {"fondo": rayos("oro"), "lines": L("Hacia el año 2000, era el sitio más visitado de internet."),
     "items": [it("multitud", 540, 1560, 1.0, anim="up", n=24, filas=3, semilla=4, cara="feliz"),
               it("etiqueta", 540, 760, 1.0, delay=1.2, texto="Nº 1 EN VISITAS", rot=-4)]},

    # ------------------------------------------------------------ 3. Google
    {"fondo": rayos("cielo"), "lines": L("Mientras tanto, en Stanford, otros dos estudiantes tenían otra idea."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="feliz", **LARRY),
               it("nombre", 300, 700, 0.8, delay=1.8, texto="Larry Page", sub="fundador de Google"),
               it("persona", 780, 1560, 0.9, delay=0.5, anim="right", cara="serio", brazos="cruzados", **SERGEY),
               it("nombre", 780, 860, 0.8, delay=2.6, texto="Sergey Brin", sub="fundador de Google")]},
    {"fondo": rayos("menta"), "lines": L("Su buscador no ordenaba las páginas a mano.", "Las ordenaba según cuántas otras páginas las enlazaban. Lo llamaron PageRank.",
                                         say={1: "Las ordenaba según cuántas otras páginas las enlazaban. Lo llamaron Péich Rank."}),
     "items": [it("pc_escritorio", 540, 1560, 0.85, anim="crece", torre=False, texto="WEB"),
               it("flecha", 230, 900, 0.6, at=1, anim="fade", rot=30),
               it("flecha", 850, 900, 0.6, at=1, delay=0.4, anim="fade", rot=150),
               it("etiqueta", 540, 760, 0.9, at=1, delay=1.6, texto="PAGERANK", rot=-4)]},
    {"fondo": rayos("durazno"), "lines": L("Según varios relatos, en 1998 ofrecieron esa tecnología por alrededor de un millón de dólares."),
     "items": [it("bolsa_dinero", 540, 1560, 1.1, anim="drop", texto="$")],
     "dato": dato(1, "MILLÓN DE DÓLARES (1998)", pre="~$", y=640, delay=1.6, cuenta=False)},
    {"sigue": True, "lines": L("Y Yahoo dijo que no, aunque los detalles de esa oferta se discuten.", pausa=0.2),
     "items": [it("icono", 850, 1150, 0.9, anim="pop", tipo="x"),
               it("etiqueta", 540, 1000, 0.8, delay=1.6, texto="SE DISCUTE", fondo="#ffffff", rot=5)]},
    {"fondo": rayos("gris"), "lines": L("Yahoo confiaba en su directorio, que ya funcionaba. Lo de Google era una apuesta."),
     "items": [it("libro", 300, 1250, 0.8, anim="left", abierto=True, texto="YAHOO"),
               it("icono", 300, 820, 0.7, delay=0.8, anim="pop", tipo="check"),
               it("pc_escritorio", 800, 1560, 0.55, delay=1.6, anim="right", torre=False, texto="?")]},
    {"fondo": rayos("cielo"), "lines": L("Y en el 2000, lo irónico: Yahoo eligió a Google como buscador de su portal."),
     "items": [it("laptop", 540, 1450, 1.1, anim="pop", texto="YAHOO!", color="#c4b5fd"),
               it("etiqueta", 540, 800, 0.9, delay=2.0, texto="BUSCA CON GOOGLE", fondo="#ffffff", rot=-4)]},

    # ------------------------------------------------------------ 4. el regateo de 2002
    {"fondo": {"tipo": "oficina"}, "lines": L("En 2001 llegó un nuevo director a Yahoo: Terry Semel.", say={0: "En 2001 llegó un nuevo director a Yahoo: Térri Semél."}),
     "items": [it("persona", 540, 1640, 0.95, anim="up", id="semel", cara="serio", brazos="cruzados", **SEMEL),
               it("nombre", 540, 700, 0.9, delay=1.4, texto="Terry Semel", sub="director de Yahoo desde 2001")]},
    {"sigue": True, "lines": L("Y en el verano de 2002 intentó comprar Google."),
     "items": [it("etiqueta", 830, 1000, 0.8, delay=0.6, texto="GOOGLE", fondo="#ffffff", rot=5)]},
    {"fondo": rayos("menta"), "lines": L("Según la revista Wired, ofreció unos tres mil millones de dólares.", say={0: "Según la revista Uáired, ofreció unos tres mil millones de dólares."}),
     "items": [it("billetes", 540, 1400, 1.0, anim="drop", n=4)],
     "dato": dato(3000, "MILLONES: LA OFERTA (2002)", pre="$", y=640, delay=1.4)},
    {"sigue": True, "lines": L("Pero le dijeron que Google valía por lo menos cinco mil millones."),
     "items": [it("chapa", 540, 1680, 1.3, delay=0.6, texto="$5.000 M", sub="lo que valia, segun Wired")]},
    {"fondo": rayos("rojo"), "lines": L("Otras fuentes dan cifras distintas. Pero no hubo trato."),
     "items": [it("mesa", 540, 1560, 1.0, anim="up"),
               it("sobre", 540, 1270, 0.6, delay=0.6, anim="drop", color="#64748b", texto="OFERTA", disco=False),
               it("icono", 540, 760, 1.0, delay=2.0, anim="pop", tipo="x")]},
    {"fondo": NOCHE, "lines": L("Dos años después, en 2004, Google salió a la bolsa."),
     "items": [it("grafica", 540, 1540, 1.15, anim="crece", tipo="sube", color="#22c55e"),
               it("calendario", 860, 720, 0.55, delay=1.0, anim="pop", texto="2004")]},
    {"sigue": True, "lines": L("En 2025, la dueña de Google superó los tres billones de dólares: tres millones de millones."),
     "dato": dato(3, "BILLONES DE DÓLARES (2025)", pre="$", y=640, delay=1.4, cuenta=False)},

    # ------------------------------------------------------------ 5. Facebook
    {"fondo": rayos("azul"), "lines": L("En 2006 apareció otra oportunidad: una red social universitaria llamada Facebook."),
     "items": [it("laptop_moderna", 540, 1500, 1.0, anim="pop", texto="FACEBOOK", pantalla="#1e40af")]},
    {"fondo": rayos("cielo"), "lines": L("Su creador, Mark Zuckerberg, tenía apenas 22 años.", say={0: "Su creador, Mark Súkerberg, tenía apenas veintidós años."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="mark", cara="serio", brazos="cruzados", **MARK),
               it("nombre", 540, 700, 0.9, delay=1.4, texto="Mark Zuckerberg", sub="creador de Facebook")]},
    {"fondo": rayos("oro"), "lines": L("En junio de 2006, Yahoo ofreció unos mil millones de dólares."),
     "items": [it("bolsa_dinero", 300, 1560, 1.0, anim="drop"),
               it("bolsa_dinero", 780, 1560, 1.0, delay=0.4, anim="drop")],
     "dato": dato(1000, "MILLONES POR FACEBOOK", pre="$", y=640, delay=1.4)},
    {"fondo": rayos("rojo"), "lines": L("Zuckerberg no quiso vender.", say={0: "Súkerberg no quiso vender."}),
     "items": [it("persona", 540, 1560, 0.95, anim="fade", cara="serio", brazos="cruzados", **MARK),
               it("icono", 830, 820, 0.9, delay=0.6, anim="pop", tipo="x")]},
    {"sigue": True, "lines": L("Según el Wall Street Journal y el New York Times, después la oferta bajó a unos 900 millones.",
                               say={0: "Según el Uól Strit Yúrnal y el Niu Iork Táims, después la oferta bajó a unos novecientos millones."}),
     "items": [it("chapa", 830, 1300, 1.1, delay=1.8, texto="$900 M", sub="nueva oferta")]},
    {"sigue": True, "lines": L("Tampoco funcionó. Facebook nunca se vendió.", pausa=0.2),
     "items": [it("etiqueta", 540, 760, 1.0, texto="NO SE VENDIÓ", fondo="#ef4444", rot=-5)]},

    # ------------------------------------------------------------ 6. Microsoft
    {"fondo": NOCHE, "lines": L("Y luego llegó la oferta más grande. Esta vez, para comprar a Yahoo."),
     "items": [it("edificio", 540, 1560, 1.0, anim="crece", **EDIF_YAHOO)],
     "cam": {"z": [1.0, 1.1], "f": [540, 1200]}},
    {"fondo": {"tipo": "oficina"}, "lines": L("El 1 de febrero de 2008, Microsoft ofreció 44.600 millones de dólares.",
                                              say={0: "El primero de febrero de 2008, Máicrosoft ofreció cuarenta y cuatro mil seiscientos millones de dólares."}),
     "items": [it("persona", 540, 1640, 0.95, anim="up", cara="risa", brazos="senala", **BALLMER),
               it("nombre", 800, 1040, 0.8, delay=1.0, texto="Steve Ballmer", sub="director de Microsoft")],
     "dato": dato(44600, "MILLONES DE DÓLARES", pre="$", y=640, delay=1.8)},
    {"fondo": rayos("menta"), "lines": L("Eran 31 dólares por acción: un 62 por ciento más que en la bolsa."),
     "items": [it("chapa", 300, 760, 1.4, texto="$31", sub="por accion"),
               it("chapa", 790, 760, 1.4, delay=1.6, texto="+62%", sub="sobre la bolsa"),
               it("grafica", 540, 1540, 1.0, delay=0.6, anim="crece", tipo="sube", color="#22c55e")]},
    {"fondo": rayos("rojo"), "lines": L("El 11 de febrero, la junta de Yahoo la rechazó por unanimidad: dijo que era muy poco."),
     "items": [it("mesa", 540, 1560, 1.0, anim="up"),
               it("persona", 300, 1560, 0.75, delay=0.4, anim="left", cara="enojado", brazos="cruzados", **SEMEL),
               it("persona", 780, 1560, 0.75, delay=0.7, anim="right", cara="serio", brazos="cruzados", ropa="traje", corbata="#64748b"),
               it("icono", 540, 780, 1.0, delay=1.6, anim="pop", tipo="x")]},
    {"fondo": rayos("durazno"), "lines": L("Microsoft subió a 33 dólares por acción. Yahoo pedía 37."),
     "items": [it("chapa", 300, 900, 1.45, texto="$33", sub="Microsoft"),
               it("chapa", 790, 900, 1.45, delay=1.8, texto="$37", sub="lo que pedia Yahoo"),
               it("flecha", 540, 1300, 0.8, delay=1.0, anim="fade")]},
    {"fondo": NOCHE, "lines": L("En mayo de 2008, Microsoft retiró la oferta.", pausa=0.3),
     "items": [it("sobre", 540, 1250, 1.0, anim="drop", color="#64748b", texto="OFERTA", disco=False),
               it("etiqueta", 540, 760, 1.0, delay=1.2, texto="RETIRADA", fondo="#ef4444", rot=-5)],
     "cam": {"z": [1.1, 1.0], "f": [540, 1200]}},

    # ------------------------------------------------------------ 7. la caida
    {"fondo": rayos("gris"), "lines": L("Después vinieron los hackeos. En 2016, Yahoo reveló dos robos de datos enormes."),
     "items": [it("laptop", 540, 1450, 1.1, anim="pop", texto="HACKEO", color="#ef4444"),
               it("icono", 850, 800, 0.8, delay=1.4, anim="pop", tipo="exclamacion")]},
    {"sigue": True, "lines": L("En 2017 confirmó que uno había afectado a todas sus cuentas: tres mil millones."),
     "dato": dato(3000, "MILLONES DE CUENTAS", y=640, delay=2.2)},
    {"fondo": rayos("azul"), "lines": L("En julio de 2016, la telefónica Verizon había acordado comprarle su negocio principal por 4.830 millones.",
                                        say={0: "En julio de 2016, la telefónica Verizon había acordado comprarle su negocio principal por cuatro mil ochocientos treinta millones."}),
     "items": [it("edificio", 300, 1560, 0.75, anim="crece", texto="VERIZON", pisos=6, color="#fecaca", letrero="#b91c1c", ancho=380),
               it("flecha", 540, 1250, 0.4, delay=1.4, anim="fade"),
               it("edificio", 790, 1560, 0.75, delay=0.8, anim="crece", **EDIF_YAHOO),
               it("chapa", 540, 760, 1.3, delay=2.4, texto="$4.830 M", sub="precio acordado")]},
    {"sigue": True, "lines": L("Por los hackeos, en febrero de 2017 le bajaron el precio en 350 millones."),
     "items": [it("etiqueta", 540, 960, 1.0, delay=0.8, texto="-$350 M", fondo="#ef4444", rot=4)]},
    {"fondo": NOCHE, "lines": L("En junio de 2017 se cerró la venta: unos 4.480 millones de dólares.",
                                say={0: "En junio de 2017 se cerró la venta: unos cuatro mil cuatrocientos ochenta millones de dólares."}),
     "items": [it("lapida", 540, 1560, 1.2, anim="crece", texto="YAHOO", sub="1994-2017")],
     "dato": dato(4480, "MILLONES: LA VENTA", pre="$", y=640, delay=1.6),
     "cam": {"z": [1.1, 1.0], "f": [540, 1250]}},
    {"sigue": True, "lines": L("Lo que quedó de la vieja empresa pasó a llamarse Altaba."),
     "items": [it("etiqueta", 540, 1680, 0.85, delay=0.6, texto="ALTABA", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("rojo"), "lines": L("Era menos del cuatro por ciento de lo que valía en el 2000."),
     "items": [it("grafica", 540, 1540, 1.15, anim="crece", tipo="baja", color="#ef4444"),
               it("chapa", 540, 760, 1.45, delay=1.6, texto="< 4%", sub="del valor del 2000")]},

    # ------------------------------------------------------------ curiosidades
    {"fondo": rayos("durazno"), "lines": L("Y ahora, cosas que casi nadie sabe.", pausa=0.2),
     "items": [it("icono", 540, 1150, 1.4, anim="pop", tipo="exclamacion", color="#f0c448")]},
    {"fondo": rayos("cielo"), "lines": L("Uno. Yahoo creció tan rápido que saturó la red de Stanford, y tuvo que irse del campus."),
     "items": [it("pc_escritorio", 540, 1560, 0.9, anim="crece", texto="ERROR", tinta="#ef4444"),
               it("etiqueta", 540, 760, 0.9, delay=1.8, texto="RED SATURADA", fondo="#ef4444", rot=-4)]},
    {"sigue": True, "lines": L("Netscape, la empresa del navegador, les prestó sus computadoras.", say={0: "Nétscape, la empresa del navegador, les prestó sus computadoras."}),
     "items": [it("etiqueta", 540, 960, 0.85, delay=0.4, texto="NETSCAPE", fondo="#ffffff", rot=5)]},
    {"fondo": rayos("menta"), "lines": L("Dos. Su mejor apuesta fue en China: en 2005 pagó mil millones de dólares por el 40 por ciento de Alibaba."),
     "items": [it("globo", 540, 1250, 0.9, anim="pop"),
               it("chapa", 300, 760, 1.1, delay=1.4, texto="$1.000 M", sub="2005"),
               it("chapa", 790, 760, 1.1, delay=2.4, texto="40%", sub="de Alibaba")]},
    {"fondo": rayos("gris"), "lines": L("Tres. En 1999 compró GeoCities, un sitio de páginas personales, por unos 3.600 millones. Años después lo cerró.",
                                        say={0: "Tres. En 1999 compró Yío Cítis, un sitio de páginas personales, por unos tres mil seiscientos millones. Años después lo cerró."}),
     "items": [it("pc_escritorio", 540, 1560, 0.85, anim="crece", texto="GEO", tinta="#facc15"),
               it("chapa", 540, 760, 1.3, delay=1.8, texto="$3.600 M", sub="GeoCities, 1999"),
               it("etiqueta", 830, 1000, 0.8, delay=3.4, texto="CERRADO", fondo="#ef4444", rot=6)]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("azul"), "lines": L("¿Y qué pasó después? Verizon juntó Yahoo con AOL en una empresa llamada Oath.",
                                        say={0: "¿Y qué pasó después? Verizon juntó Yahoo con A O L en una empresa llamada Ouz."}),
     "items": [it("edificio", 300, 1560, 0.7, anim="crece", **EDIF_YAHOO),
               it("edificio", 790, 1560, 0.7, delay=0.6, anim="crece", texto="AOL", pisos=6, color="#bfdbfe", letrero="#1e3a8a", ancho=380),
               it("etiqueta", 540, 760, 1.0, delay=2.0, texto="OATH", rot=-4)]},
    {"fondo": rayos("lila"), "lines": L("En 2021 vendió el 90 por ciento al fondo Apollo, por unos cinco mil millones. Y la empresa volvió a llamarse Yahoo."),
     "items": [it("bolsa_dinero", 300, 1560, 0.9, anim="drop", texto="$"),
               it("chapa", 320, 760, 1.1, delay=1.0, texto="$5.000 M", sub="Apollo, 2021"),
               it("edificio", 790, 1560, 0.75, delay=2.6, anim="crece", **EDIF_YAHOO)]},

    # ------------------------------------------------------------ cierre
    {"fondo": NOCHE, "lines": L("Pudo comprar Google por un millón y Facebook por mil millones.", "Rechazó 44.600 millones.", "Y terminó vendida por menos de cinco mil.",
                                say={1: "Rechazó cuarenta y cuatro mil seiscientos millones."}),
     "items": [it("chapa", 290, 760, 0.9, texto="GOOGLE", sub="~$1 M"),
               it("chapa", 790, 760, 0.9, delay=1.4, texto="FACEBOOK", sub="~$1.000 M"),
               it("chapa", 540, 1050, 1.3, at=1, texto="$44.600 M", sub="rechazados"),
               it("chapa", 540, 1350, 1.3, at=2, texto="$4.480 M", sub="venta final")],
     "cam": {"z": [1.0, 1.05], "f": [540, 1000]}},
    {"fondo": rayos("oro"), "lines": L("¿Tú habrías aceptado la oferta de Microsoft? Te leo en los comentarios.", say={0: "¿Tú habrías aceptado la oferta de Máicrosoft? Te leo en los comentarios."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="preocupado", brazos="cabeza", **JERRY),
               it("etiqueta", 540, 760, 1.1, delay=1.4, texto="¿SÍ O NO?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "Yahoo pudo comprar Google y Facebook… y terminó vendida por una fracción",
    "description": ("Yahoo nació en 1994 como una lista de webs de dos estudiantes de Stanford y en el año 2000 llegó a valer unos "
                    "125.000 millones de dólares. Dejó pasar a Google (1998 y 2002) y a Facebook (2006), rechazó 44.600 millones "
                    "de Microsoft en 2008 y en 2017 vendió su negocio principal a Verizon por unos 4.480 millones.\n"
                    "Fuentes: NPR y Al Jazeera (oferta de Microsoft, 2008); CNN Money y MediaPost (venta a Verizon, 2017); "
                    "Wired, citado por John Naughton (oferta por Google, 2002); TechSpot; The Week; Business Insider y Betanews "
                    "(oferta por Facebook, 2006); Encyclopedia.com y Reference for Business (origen en Stanford); "
                    "Euronews (Alphabet, 2025); Wikipedia como apoyo."),
    "hashtags": ["#DatoBomba", "#Yahoo", "#Google", "#negocios", "#historiadeinternet"],
    "source_url": "https://www.techspot.com/article/2744-yahoo-what-went-wrong",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_yahoo.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55))
