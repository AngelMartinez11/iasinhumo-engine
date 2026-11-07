"""Genera ejemplos/hsf_louvre.json: el robo de las joyas de la corona en el Louvre, 2025 (Dato Bomba, canal historias, motor v4, formato largo).

Estructura: gancho -> pregunta -> historia en orden (el camion, el golpe, el botin, las fallas, la caza)
-> cosas que casi nadie sabe -> que paso despues -> cierre con pregunta.
Nota para la biblioteca: no hay piezas de joya, corona, camion elevador ni moto; las gemas se hacen con
etiquetas giradas 45 grados y el elevador con una flecha vertical.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

LADRON = {"camisa": "#facc15", "pelo": "#1f1f1f", "peinado": "gorra", "pantalon": "#1f2937"}
LADRON2 = {"camisa": "#facc15", "pelo": "#3a2a1e", "peinado": "gorra", "pantalon": "#1f2937", "piel": "#c68a5c"}
POLI = {"camisa": "#1e3a8a", "pelo": "#1f1f1f", "peinado": "gorra", "pantalon": "#1e293b"}
FISCAL = {"ropa": "traje", "corbata": "#1d1d2b", "pelo": "#a16207", "peinado": "largo", "piel": "#f5d0b0"}
DIRECTORA = {"ropa": "traje", "corbata": "#7c3aed", "pelo": "#6b4423", "peinado": "largo", "lentes": True}
NUEVO = {"ropa": "traje", "corbata": "#f0c448", "pelo": "#c9c9c9", "peinado": "calvo", "lentes": True}
PIEDRA = "#e7dcc4"
ESMERALDA, ZAFIRO, DIAMANTE, PERLA = "#22c55e", "#3b82f6", "#f8fafc", "#fde7c7"


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


def gema(x, y, color, s=1.0, delay=0.0, id=None):
    """Gema hecha con una etiqueta vacia girada 45 grados."""
    return it("etiqueta", x, y, s, delay=delay, anim="pop", id=id, texto=" ", fondo=color, rot=45, size=64)


def gemas(colores, y=1250, s=1.0, delay=0.0, sep=230, prefijo="g"):
    n = len(colores)
    x0 = 540 - sep * (n - 1) / 2
    return [gema(x0 + i * sep, y, c, s, delay + i * 0.35, id=f"{prefijo}{i}") for i, c in enumerate(colores)]


def museo(x=540, s=1.0, delay=0.0, id="museo"):
    return it("edificio", x, 1560, s, delay=delay, anim="crece", id=id, texto="LOUVRE", pisos=5, ancho=620,
              color=PIEDRA, ventana="#bfdbfe", letrero="#1d1d2b")


def elevador(x=820, delay=0.0, id="elev"):
    return [it("flecha", x, 1180, 1.0, delay=delay, anim="crece", id=id, rot=-90, largo=640, color="#f59e0b"),
            it("etiqueta", x, 1480, 0.6, delay=delay + 0.6, id=id + "t", texto="ELEVADOR", fondo="#ffffff", rot=0)]


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": rayos("cielo"), "lines": L("Domingo 19 de octubre de 2025. El Louvre, en París, acababa de abrir."),
     "items": [museo(), it("calendario", 870, 760, 0.55, delay=1.4, anim="pop", texto="19 OCT"),
               it("multitud", 540, 1700, 1.0, delay=2.2, anim="up", n=14, filas=1, ancho=900, escala=0.3)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1300]}},
    {"fondo": {"tipo": "noche"}, "lines": L("En unos siete minutos, ocho joyas de la corona de Francia desaparecieron."),
     "items": gemas([ESMERALDA, DIAMANTE, ZAFIRO, PERLA], y=1250, s=1.2, sep=220) + [it("chapa", 540, 800, 1.4, delay=1.8, texto="~7 MIN")],
     "cam": {"z": [1.1, 1.0], "f": [540, 1250]}},
    {"sigue": True, "quita": ["g0", "g1", "g2", "g3"], "lines": L("Valían, según la fiscalía, unos ochenta y ocho millones de euros."),
     "items": [it("bolsa_dinero", 540, 1560, 1.1, anim="drop", texto="€")],
     "dato": dato(88, "MILLONES DE EUROS", suf=" M€", y=680, delay=1.2)},
    {"sigue": True, "lines": L("Y más de un año después, siguen sin aparecer.", pausa=0.3),
     "items": [it("icono", 830, 1250, 0.8, delay=0.6, anim="pop", tipo="pregunta")]},
    {"fondo": rayos("oro"), "lines": L("¿Cómo se roba el Louvre a plena luz del día, en menos de diez minutos?"),
     "items": [museo(s=0.8), it("reloj", 540, 780, 0.6, delay=1.4, anim="pop", hora=9.5)]},

    # ------------------------------------------------------------ el camion
    {"fondo": rayos("azul"), "lines": L("Todo empezó nueve días antes, el 10 de octubre."),
     "items": [it("calendario", 540, 1150, 1.0, anim="drop", texto="10 OCT")]},
    {"sigue": True, "lines": L("Según la fiscalía, dos hombres reservaron un camión con elevador de muebles, fingiendo una mudanza."),
     "items": [it("persona", 230, 1560, 0.75, delay=0.3, anim="left", id="l1", brazos="telefono", **LADRON),
               it("persona", 850, 1560, 0.75, delay=0.7, anim="right", id="l2", flip=True, **LADRON2),
               it("etiqueta", 540, 760, 0.9, delay=2.4, texto="MUDANZA", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("rojo"), "lines": L("Cuando llegó el dueño, lo amenazaron y se llevaron el camión."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="sorpresa", brazos="arriba", camisa="#64748b"),
               it("flecha", 760, 1000, 0.6, delay=1.4, anim="right", largo=300, color="#ef4444"),
               it("icono", 760, 760, 0.6, delay=1.8, anim="pop", tipo="exclamacion")]},
    {"fondo": rayos("menta"), "lines": L("Una canasta que sube por una escalera extensible, para meter muebles por las ventanas."),
     "items": [it("edificio", 380, 1560, 0.9, anim="crece", texto="", pisos=5, ancho=420, color=PIEDRA)] + elevador(800, 0.8),
     "cam": {"z": [1.0, 1.08], "f": [700, 1200]}},

    # ------------------------------------------------------------ el golpe
    {"fondo": rayos("cielo"), "lines": L("El 19 de octubre, a las nueve y media, lo estacionaron junto al Sena, al pie del museo."),
     "items": [museo(380, 0.95)] + elevador(860, 0.8) + [it("reloj", 860, 700, 0.5, delay=2.4, anim="pop", hora=9.5)],
     "cam": {"z": [1.0, 1.05], "f": [540, 1250]}},
    {"sigue": True, "lines": L("Pusieron conos de tráfico para que pareciera una obra."),
     "items": [it("etiqueta", 380, 900, 0.9, delay=0.4, texto="OBRA", fondo="#f97316", rot=-4)]},
    {"fondo": rayos("durazno"), "lines": L("Iban disfrazados de trabajadores, con chalecos amarillos."),
     "items": [it("persona", 320, 1560, 0.95, anim="left", id="l1", **LADRON),
               it("persona", 760, 1560, 0.95, delay=0.5, anim="right", id="l2", flip=True, **LADRON2),
               it("etiqueta", 540, 760, 0.85, delay=1.8, texto="CHALECOS AMARILLOS", rot=-3)]},
    {"fondo": rayos("cielo"), "lines": L("Dos de ellos subieron en la canasta hasta un balcón del primer piso."),
     "items": [museo(380, 0.95)] + elevador(860, 0.0) + [it("persona", 860, 1000, 0.45, delay=0.8, anim="up", **LADRON)],
     "cam": {"z": [1.0, 1.12], "f": [800, 1000]}},
    {"fondo": rayos("oro"), "lines": L("Detrás estaba la Galería de Apolo, donde se exhiben las joyas de la corona francesa."),
     "items": [it("etiqueta", 540, 760, 0.9, anim="pop", texto="GALERÍA DE APOLO", fondo="#ffffff", rot=-3)] + gemas([ESMERALDA, ZAFIRO, DIAMANTE], y=1250, s=1.0, delay=1.2)},
    {"fondo": {"tipo": "noche"}, "lines": L("A las nueve y treinta y cuatro rompieron la ventana con cortadoras de disco."),
     "items": [it("chapa", 540, 1100, 1.5, anim="pop", texto="9:34", sub="entran"),
               it("icono", 540, 1450, 0.8, delay=1.6, anim="pop", tipo="exclamacion")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1150]}},
    {"sigue": True, "lines": L("La alarma sonó de inmediato."),
     "items": [it("etiqueta", 540, 780, 1.0, delay=0.2, texto="ALARMA", fondo="#ef4444", tinta="#1d1d2b", rot=5)]},
    {"fondo": rayos("rojo"), "lines": L("Amenazaron a los vigilantes, y el personal evacuó la sala."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", cara="sorpresa", brazos="arriba", **POLI),
               it("multitud", 760, 1600, 0.9, delay=1.4, anim="right", n=8, filas=2, ancho=420, escala=0.3, cara="sorpresa")]},
    {"fondo": {"tipo": "noche"}, "lines": L("Cortaron dos vitrinas y sacaron las joyas."),
     "items": [it("celda", 540, 1500, 0.8, anim="fade", barrotes=1, ancho=600, alto=420)] + gemas([ESMERALDA, ZAFIRO, PERLA], y=1300, s=1.1, delay=0.6)},
    {"sigue": True, "lines": L("Adentro estuvieron menos de cuatro minutos."),
     "items": [it("chapa", 540, 780, 1.45, delay=0.3, texto="< 4 MIN", sub="dentro de la sala")]},
    {"fondo": rayos("cielo"), "lines": L("A las nueve y treinta y ocho salieron por la misma ventana."),
     "items": [museo(380, 0.95)] + elevador(860, 0.0) + [it("chapa", 860, 700, 1.2, delay=0.8, texto="9:38", sub="salen")]},
    {"fondo": rayos("durazno"), "lines": L("Abajo los esperaban dos cómplices en motos scooter de alta potencia."),
     "items": [it("persona", 300, 1560, 0.9, anim="left", brazos="senala", camisa="#1f2937", peinado="gorra"),
               it("persona", 780, 1560, 0.9, delay=0.5, anim="right", flip=True, camisa="#334155", peinado="gorra"),
               it("etiqueta", 540, 780, 0.9, delay=1.6, texto="2 MOTOS", rot=-4)]},
    {"fondo": rayos("rojo"), "lines": L("Intentaron quemar el camión para borrar pruebas, pero no lo lograron."),
     "items": elevador(540, 0.0) + [it("icono", 540, 760, 0.8, delay=1.6, anim="pop", tipo="x")]},
    {"fondo": {"tipo": "noche"}, "lines": L("En la huida se les cayó una pieza: la corona de la emperatriz Eugenia."),
     "items": [it("nombre", 540, 760, 1.0, delay=0.8, texto="Corona de Eugenia", sub="hecha para la Exposicion de 1855"),
               gema(350, 1150, ESMERALDA, 1.0, 1.6), gema(540, 1060, DIAMANTE, 1.3, 1.8), gema(730, 1150, ESMERALDA, 1.0, 2.0)],
     "cam": {"z": [1.0, 1.1], "f": [540, 1200]}},
    {"sigue": True, "lines": L("Tiene mil trescientos cincuenta y cuatro diamantes, cincuenta y seis esmeraldas y ocho águilas de oro."),
     "items": [it("chapa", 260, 1420, 1.05, texto="1.354", sub="diamantes"),
               it("chapa", 540, 1420, 1.05, delay=1.4, texto="56", sub="esmeraldas"),
               it("chapa", 820, 1420, 1.05, delay=2.6, texto="8", sub="aguilas")]},
    {"fondo": rayos("gris"), "lines": L("Quedó aplastada, pero se puede restaurar."),
     "items": [gema(540, 1200, DIAMANTE, 1.2), it("etiqueta", 540, 1500, 0.85, delay=1.0, texto="SE PUEDE RESTAURAR", fondo="#ffffff", rot=-3)]},

    # ------------------------------------------------------------ el botin
    {"fondo": rayos("oro"), "lines": L("Las otras ocho piezas sí se fueron."),
     "items": [it("chapa", 540, 1150, 1.6, anim="pop", texto="8", sub="piezas robadas")]},
    {"fondo": rayos("menta"), "lines": L("Entre ellas, el collar que Napoleón le regaló a María Luisa por su boda en 1810: treinta y dos esmeraldas y más de mil cien diamantes."),
     "items": gemas([ESMERALDA, DIAMANTE, ESMERALDA, DIAMANTE, ESMERALDA], y=1130, s=0.85, sep=185) +
              [it("chapa", 300, 1430, 1.15, delay=2.0, texto="32", sub="esmeraldas"),
               it("chapa", 780, 1430, 1.15, delay=3.0, texto="1.138", sub="diamantes"),
               it("calendario", 540, 780, 0.5, delay=1.2, anim="pop", texto="1810", color="#22c55e")]},
    {"fondo": rayos("lila"), "lines": L("La diadema de perlas de Eugenia, con doscientas doce perlas y casi dos mil diamantes."),
     "items": gemas([PERLA, DIAMANTE, PERLA, DIAMANTE, PERLA], y=1130, s=0.85, sep=185) +
              [it("chapa", 300, 1430, 1.15, delay=1.6, texto="212", sub="perlas"),
               it("chapa", 780, 1430, 1.15, delay=2.6, texto="~2.000", sub="diamantes")]},
    {"fondo": rayos("azul"), "lines": L("Joyas de zafiros que usaron las reinas María Amelia y Hortensia, y un broche y un gran moño de diamantes."),
     "items": gemas([ZAFIRO, ZAFIRO, DIAMANTE], y=1200, s=1.15) + [it("etiqueta", 540, 1500, 0.8, delay=2.4, texto="ZAFIROS + BROCHE + MOÑO", rot=-3)]},
    {"fondo": rayos("durazno"), "lines": L("La fiscal de París, Laure Beccuau, citó el cálculo del museo: ochenta y ocho millones de euros.", say={0: "La fiscal de París, Lor Bekó, citó el cálculo del museo: ochenta y ocho millones de euros."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="fiscal", cara="serio", brazos="cruzados", **FISCAL),
               it("nombre", 540, 720, 1.0, delay=1.6, texto="Laure Beccuau", sub="fiscal de Paris")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"sigue": True, "lines": L("Y según el gobierno, ninguna tenía seguro privado."),
     "items": [it("etiqueta", 780, 1150, 0.7, delay=0.6, texto="SIN SEGURO", fondo="#ef4444", rot=6)]},

    # ------------------------------------------------------------ las fallas
    {"fondo": {"tipo": "oficina"}, "lines": L("Días después, la presidenta del museo, Laurence des Cars, declaró ante el Senado francés.", say={0: "Días después, la presidenta del museo, Lorans de Car, declaró ante el Senado francés."}),
     "items": [it("persona", 540, 1640, 0.95, anim="up", id="dir", cara="preocupado", **DIRECTORA),
               it("nombre", 540, 720, 1.0, delay=1.6, texto="Laurence des Cars", sub="presidenta del Louvre")]},
    {"sigue": True, "lines": L("Admitió que la cámara más cercana apuntaba hacia el oeste y no cubría el balcón por donde entraron."),
     "items": [it("camara", 860, 1150, 0.5, delay=0.6, anim="pop", tipo="digital"),
               it("icono", 860, 900, 0.5, delay=1.8, anim="pop", tipo="x")],
     "cam": {"z": [1.0, 1.08], "f": [700, 1200]}},
    {"sigue": True, "lines": L("Ofreció su renuncia. Se la rechazaron.", pausa=0.2),
     "items": [it("sobre", 230, 1150, 0.5, delay=0.3, anim="drop", color="#f8fafc", texto="RENUNCIA", disco=False)]},

    # ------------------------------------------------------------ la caza
    {"fondo": rayos("azul"), "lines": L("Mientras tanto, unos cien investigadores trabajaban en el caso."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", brazos="telefono", **POLI),
               it("persona", 780, 1560, 0.85, delay=0.4, anim="right", flip=True, brazos="senala", **POLI)],
     "dato": dato(100, "INVESTIGADORES", pre="~", y=680, delay=1.2)},
    {"sigue": True, "lines": L("Revisaron cámaras y unas ciento cincuenta muestras del camión y del museo."),
     "items": [it("tv", 540, 1250, 0.6, delay=0.4, anim="pop", play=False, texto="CCTV"),
               it("chapa", 540, 1520, 1.1, delay=1.8, texto="150", sub="muestras")]},
    {"fondo": rayos("cielo"), "lines": L("Seis días después del robo detuvieron a un sospechoso en el aeropuerto Charles de Gaulle.", say={0: "Seis días después del robo detuvieron a un sospechoso en el aeropuerto Charl de Gol."}),
     "items": [it("avion", 540, 900, 0.9, anim="left"),
               it("persona", 300, 1560, 0.85, delay=1.0, anim="left", cara="preocupado", **LADRON2),
               it("persona", 780, 1560, 0.85, delay=1.4, anim="right", flip=True, brazos="senala", **POLI)]},
    {"sigue": True, "lines": L("Tenía un boleto solo de ida a Argelia."),
     "items": [it("etiqueta", 540, 1150, 0.9, delay=0.2, texto="SOLO IDA", fondo="#ffffff", rot=-5)]},
    {"fondo": {"tipo": "noche"}, "lines": L("El ADN llevó a otros. En pocas semanas cayeron los cuatro hombres que, según la policía, formaban el comando."),
     "items": [it("celda", 540, 1560, 1.1, anim="fade", barrotes=7, ancho=760, alto=620),
               it("persona", 400, 1560, 0.7, delay=1.6, anim="up", cara="serio", **LADRON),
               it("persona", 680, 1560, 0.7, delay=2.0, anim="up", cara="serio", flip=True, **LADRON2),
               it("chapa", 540, 760, 1.3, delay=2.8, texto="4", sub="detenidos del comando")]},
    {"fondo": rayos("gris"), "lines": L("La fiscal los describió como delincuentes locales, no como una red de crimen organizado."),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="serio", brazos="senala", **FISCAL),
               it("etiqueta", 540, 760, 0.85, delay=1.8, texto="DELINCUENTES LOCALES", fondo="#ffffff", rot=-3)]},
    {"sigue": True, "lines": L("Algunos admitieron en parte su participación. Pero ninguno dijo dónde están las joyas.", pausa=0.3),
     "items": [it("icono", 850, 1100, 0.8, delay=1.6, anim="pop", tipo="pregunta")]},

    # ------------------------------------------------------------ cosas que casi nadie sabe
    {"fondo": rayos("durazno"), "lines": L("Y ahora, cosas que casi nadie sabe."),
     "items": [it("etiqueta", 540, 1150, 1.2, anim="pop", texto="¿SABÍAS?", rot=-5)]},
    {"fondo": rayos("menta"), "lines": L("Uno. Según la fiscalía, el camión lo robaron en un pueblo al norte de París que se llama Louvres."),
     "items": [it("pin", 540, 1450, 0.9, anim="drop", color="#ef4444", texto="LOUVRES"),
               it("chapa", 540, 780, 1.3, delay=2.2, texto="LOUVRES", sub="con S al final")]},
    {"fondo": rayos("cielo"), "lines": L("Dos. Según el diario francés Libération, en una auditoría de 2014 la contraseña del servidor de videovigilancia era LOUVRE.",
                                         say={0: "Dos. Según el diario francés Liberasión, en una auditoría de 2014 la contraseña del servidor de videovigilancia era Louvre."}),
     "items": [it("laptop", 540, 1450, 1.0, anim="pop", texto="LOUVRE", color="#4ade80"),
               it("chapa", 540, 780, 1.3, delay=2.0, texto="2014", sub="auditoria")]},
    {"fondo": rayos("oro"), "lines": L("Tres. Los ladrones dejaron en su lugar el Regente, un diamante de ciento cuarenta quilates de la misma galería."),
     "items": [gema(540, 1200, DIAMANTE, 1.5),
               it("chapa", 540, 780, 1.3, delay=1.6, texto="140 QUILATES", sub="el Regente")]},
    {"fondo": rayos("lila"), "lines": L("Cuatro. En 1887, Francia vendió casi todas sus joyas de la corona. El collar de María Luisa recién volvió al Louvre en 2004."),
     "items": [it("calendario", 300, 1150, 0.7, anim="pop", texto="1887"),
               it("flecha", 540, 1150, 0.4, delay=1.6, anim="fade"),
               it("calendario", 780, 1150, 0.7, delay=2.6, anim="pop", texto="2004", color="#22c55e")]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("gris"), "lines": L("¿Y qué pasó después?"),
     "items": [it("icono", 540, 1150, 1.1, anim="pop", tipo="pregunta")]},
    {"fondo": rayos("azul"), "lines": L("En febrero de 2026, Laurence des Cars renunció. La reemplazó Christophe Leribault, que dirigía el Palacio de Versalles.",
                                        say={0: "En febrero de 2026, Lorans de Car renunció. La reemplazó Cristóf Leribó, que dirigía el Palacio de Versalles."}),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="triste", **DIRECTORA),
               it("persona", 780, 1560, 0.85, delay=1.8, anim="right", flip=True, cara="serio", **NUEVO),
               it("nombre", 700, 720, 0.85, delay=2.6, texto="Christophe Leribault", sub="nuevo presidente")]},
    {"fondo": rayos("oro"), "lines": L("El 22 de julio de 2026, la Galería de Apolo volvió a abrir. Pero sin vitrinas y sin joyas."),
     "items": [it("calendario", 540, 1150, 0.9, anim="pop", texto="22 JUL"),
               it("etiqueta", 540, 1450, 0.85, delay=2.4, texto="SIN JOYAS", fondo="#ffffff", rot=-4)]},
    {"sigue": True, "lines": L("Las piezas que no se robaron se llevaron a un lugar más seguro."),
     "items": [it("celda", 790, 1560, 0.6, delay=0.4, anim="fade", barrotes=4, ancho=360, alto=420)]},
    {"fondo": {"tipo": "noche"}, "lines": L("A un año del robo, las ocho piezas siguen en la base de datos de obras robadas de Interpol."),
     "items": [it("globo", 540, 1250, 0.8, anim="pop", id="globo"),
               it("etiqueta", 540, 760, 0.9, delay=1.8, texto="INTERPOL: ROBADAS", fondo="#ef4444", rot=-3)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1200]}},
    {"sigue": True, "quita": ["globo"], "lines": L("Lo último que se sabe: un video las muestra en una bodega subterránea de Aubervilliers, al norte de París.",
                               say={0: "Lo último que se sabe: un video las muestra en una bodega subterránea de Obervilié, al norte de París."}),
     "items": [it("tv", 540, 1250, 1.0, delay=0.4, anim="pop", play=False, texto="ÚLTIMO VIDEO")]},
    {"fondo": rayos("gris"), "lines": L("Los expertos temen que el oro se funda y las piedras se recorten para venderlas."),
     "items": gemas([ESMERALDA, ZAFIRO, DIAMANTE], y=1250, s=1.2) + [it("icono", 540, 780, 0.8, delay=1.8, anim="pop", tipo="exclamacion")]},

    # ------------------------------------------------------------ cierre
    {"fondo": {"tipo": "noche"}, "lines": L("Siete minutos para llevárselas. Más de un año buscándolas."),
     "items": [it("chapa", 290, 1150, 1.4, texto="7 MIN", sub="el robo"),
               it("flecha", 540, 1150, 0.35, delay=1.0, anim="fade"),
               it("chapa", 790, 1150, 1.4, delay=1.6, texto="+1 AÑO", sub="buscandolas")],
     "cam": {"z": [1.0, 1.06], "f": [540, 1150]}},
    {"fondo": rayos("oro"), "lines": L("¿Tú crees que algún día van a aparecer, o ya no existen como joyas? Te leo en los comentarios."),
     "items": gemas([ESMERALDA, ZAFIRO, PERLA], y=1300, s=1.2) + [it("etiqueta", 540, 780, 1.0, delay=1.6, texto="¿Y TÚ?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "Robaron 8 joyas de la corona del Louvre en 7 minutos... y siguen sin aparecer",
    "description": ("19 de octubre de 2025: cuatro hombres con un camion elevador entraron a la Galeria de Apolo del Louvre "
                    "y se llevaron ocho joyas de la corona francesa valuadas en unos 88 millones de euros. "
                    "Se les cayo la corona de Eugenia, detuvieron a los sospechosos... y a un ano del robo las joyas siguen sin aparecer.\n"
                    "Fuentes: AP (cronologia del robo y detenciones); Reuters; AFP (via Express Tribune y Daily Sabah, octubre de 2026); "
                    "Al Jazeera; NBC News; CBS News; Smithsonian Magazine; The Irish Times; The Local; Euronews (22/07/2026); "
                    "Sortiraparis; Cyprus Mail (25/02/2026); Washington Times y Tom's Hardware (sobre Liberation); Insurance Journal; louvre.fr."),
    "hashtags": ["#DatoBomba", "#Louvre", "#robo", "#Paris", "#joyas"],
    "source_url": "https://wtop.com/world/2025/10/a-timeline-of-the-jewel-heist-at-the-louvre-in-paris-2",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_louvre.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55),
      "titulo:", len(guion["title"]))
