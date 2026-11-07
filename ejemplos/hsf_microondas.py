"""Genera ejemplos/hsf_microondas.json: el microondas nacio por un chocolate derretido.

Canal Dato Bomba (canal "historias", motor v4, formato largo, sin tarjetas de capitulo).
Estructura: gancho -> pregunta -> la historia en orden -> como funciona -> curiosidades -> que paso despues -> cierre.

Notas para la biblioteca de piezas: no existe pieza "microondas" (se usa maletin_pc cerrado en blanco, que tiene
ventana y panel), ni "magnetron" (se usa disco), ni "radarange" de gabinete (se usa edificio sin ventanas),
ni "chocolate" o "palomitas" (se usan etiquetas).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

SPENCER = {"ropa": "traje", "corbata": "#b45309", "pelo": "#c9c9c9", "peinado": "canoso", "lentes": True}
COLEGA = {"ropa": "bata", "pelo": "#3a2a1e", "peinado": "corto"}
CHOCO = "#7c4a2d"
MICRO = {"abierto": False, "color": "#f1f5f9", "pantalla": "#334155"}
RADAR = {"texto": "RADARANGE", "pisos": 4, "ancho": 340, "color": "#cbd5e1", "ventana": "#cbd5e1", "letrero": "#334155"}


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


def micro(x=540, y=1500, s=0.9, **kw):
    return it("maletin_pc", x, y, s, **kw, **MICRO)


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": rayos("azul"), "lines": L("Hoy calientas tu café en un minuto, con un aparato que cabe en cualquier cocina."),
     "items": [micro(540, 1520, 0.95, anim="pop"),
               it("chapa", 540, 760, 1.4, delay=1.6, texto="1 MIN", sub="un cafe")],
     "cam": {"z": [1.0, 1.05], "f": [540, 1250]}},
    {"fondo": NOCHE, "lines": L("Pero el primer horno de microondas pesaba unos 340 kilos.", say={0: "Pero el primer horno de microondas pesaba unos trescientos cuarenta kilos."}),
     "items": [it("bascula", 540, 1560, 1.25, anim="up", texto="340 KG"),
               it("edificio", 540, 1470, 0.75, delay=0.8, anim="drop", **RADAR)],
     "dato": dato(340, "KILOS", suf=" KG", y=640, delay=2.0),
     "cam": {"z": [1.1, 1.0], "f": [540, 1250]}},
    {"fondo": rayos("durazno"), "lines": L("Y todo empezó con una barra de chocolate derretida en un bolsillo."),
     "items": [it("etiqueta", 540, 1150, 1.4, anim="pop", texto="CHOCOLATE", fondo=CHOCO, tinta="#1d1d2b", rot=-5),
               it("etiqueta", 540, 1400, 0.9, delay=1.8, texto="DERRETIDO", fondo="#ffffff", rot=4)]},
    {"fondo": rayos("oro"), "lines": L("¿Cómo una pieza del radar de guerra terminó calentando tus sobras?"),
     "items": [it("avion", 300, 1000, 0.6, anim="left"),
               it("flecha", 540, 1250, 0.6, delay=0.8, anim="fade"),
               micro(790, 1520, 0.55, delay=1.4, anim="right"),
               it("icono", 540, 760, 1.0, delay=2.4, anim="pop", tipo="pregunta")]},

    # ------------------------------------------------------------ 1. un hombre sin escuela
    {"fondo": rayos("lila"), "lines": L("Esta historia empieza con un hombre que nunca terminó la escuela: Percy Spencer.",
                                        say={0: "Esta historia empieza con un hombre que nunca terminó la escuela: Pérsi Spénser."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="spencer", cara="serio", brazos="cruzados", **SPENCER),
               it("nombre", 540, 700, 0.95, delay=2.0, texto="Percy Spencer", sub="ingeniero de Raytheon")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1100]}},
    {"fondo": rayos("cielo"), "lines": L("Nació en 1894 en Howland, un pueblo de Maine, en Estados Unidos.",
                                         say={0: "Nació en 1894 en Jáuland, un pueblo de Méin, en Estados Unidos."}),
     "items": [it("pin", 540, 1400, 1.1, anim="drop", texto="MAINE, EE. UU."),
               it("chapa", 540, 760, 1.35, delay=1.2, texto="1894", sub="nace Spencer")]},
    {"fondo": rayos("gris"), "lines": L("Su padre murió cuando él tenía año y medio, y lo criaron sus tíos."),
     "items": [it("nino", 540, 1560, 1.3, anim="up", cara="triste", camisa="#94a3b8")]},
    {"sigue": True, "lines": L("Dejó la escuela en quinto grado para trabajar."),
     "items": [it("chapa", 540, 760, 1.4, texto="5º GRADO", sub="dejo la escuela"),
               it("icono", 840, 1150, 0.7, delay=0.8, anim="pop", tipo="x")]},
    {"fondo": rayos("durazno"), "lines": L("A los 16 años ayudó a electrificar una fábrica de papel, y aprendió leyendo libros de noche.",
                                           say={0: "A los dieciséis años ayudó a electrificar una fábrica de papel, y aprendió leyendo libros de noche."}),
     "items": [it("libro", 300, 1200, 0.8, anim="left", abierto=True, texto="VOLTS"),
               it("reloj", 800, 1150, 0.8, delay=1.0, anim="pop", hora=11),
               it("chapa", 540, 760, 1.3, delay=0.4, texto="16 AÑOS")]},
    {"fondo": rayos("azul"), "lines": L("Luego fue operador de radio en la Marina, y estudió solo cálculo, física y química."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="feliz", brazos="objeto", camisa="#f8fafc", peinado="corto", pelo="#6b4423"),
               it("etiqueta", 780, 900, 0.75, delay=1.6, texto="CÁLCULO", fondo="#ffffff", rot=-5),
               it("etiqueta", 780, 1100, 0.75, delay=2.2, texto="FÍSICA", fondo="#ffffff", rot=4),
               it("etiqueta", 780, 1300, 0.75, delay=2.8, texto="QUÍMICA", fondo="#ffffff", rot=-3)]},
    {"fondo": {"tipo": "oficina"}, "lines": L("En 1925 entró a una pequeña empresa de Massachusetts: Raytheon.",
                                              say={0: "En 1925 entró a una pequeña empresa de Masachúsets: Réizion."}),
     "items": [it("edificio", 540, 1560, 0.8, anim="crece", texto="RAYTHEON", pisos=5, ancho=480),
               it("calendario", 860, 720, 0.55, delay=1.4, anim="pop", texto="1925")]},

    # ------------------------------------------------------------ 2. el radar
    {"fondo": NOCHE, "lines": L("Llegó la Segunda Guerra Mundial, y con ella, el radar."),
     "items": [it("avion", 540, 1000, 0.9, anim="left", color="#94a3b8")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1000]}},
    {"fondo": rayos("rojo"), "lines": L("El corazón del radar era el magnetrón: un tubo que produce microondas, ondas de radio muy cortas."),
     "items": [it("disco", 540, 1200, 1.3, anim="pop", id="mag"),
               it("etiqueta", 540, 760, 1.0, delay=1.0, texto="MAGNETRÓN", rot=-4)],
     "cam": {"z": [1.0, 1.1], "f": [540, 1200]}},
    {"sigue": True, "lines": L("En 1941 se hacían unos 17 al día, según el Salón de la Fama de los Inventores."),
     "items": [it("chapa", 540, 1600, 1.35, delay=1.8, texto="17", sub="por dia, 1941")]},
    {"fondo": rayos("cielo"), "lines": L("Spencer cambió el método: en vez de tallar cobre sólido, apiló láminas delgadas de metal."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="feliz", brazos="senala", **SPENCER),
               it("disco", 800, 1000, 0.5, delay=1.4, anim="drop"),
               it("disco", 800, 1150, 0.5, delay=1.8, anim="drop"),
               it("disco", 800, 1300, 0.5, delay=2.2, anim="drop")]},
    {"fondo": rayos("menta"), "lines": L("La producción subió a 2.600 por día.", say={0: "La producción subió a dos mil seiscientos por día."}),
     "items": [it("grafica", 540, 1540, 1.15, anim="crece", tipo="sube", color="#22c55e")],
     "dato": dato(2600, "MAGNETRONES AL DÍA", y=640, delay=1.0)},
    {"sigue": True, "lines": L("Y la Marina le dio su máximo premio para un civil.", pausa=0.2),
     "items": [it("chapa", 540, 780, 1.3, texto="PREMIO", sub="Marina de EE. UU.")]},

    # ------------------------------------------------------------ 3. el chocolate
    {"fondo": rayos("durazno"), "lines": L("Cerca de 1945, Spencer estaba junto a un magnetrón encendido."),
     "items": [it("persona", 330, 1560, 0.9, anim="left", id="sp", cara="serio", **SPENCER),
               it("disco", 800, 1150, 0.8, delay=0.8, anim="pop", id="mag2"),
               it("calendario", 800, 760, 0.5, delay=1.6, anim="pop", texto="1945")]},
    {"sigue": True, "quita": ["sp"], "lines": L("Y notó que la barra de chocolate que llevaba en el bolsillo se había derretido."),
     "items": [it("persona", 330, 1560, 0.9, anim="fade", cara="sorpresa", **SPENCER),
               it("etiqueta", 330, 1250, 0.7, delay=1.6, texto="¡CHOCOLATE!", fondo=CHOCO, rot=6)],
     "cam": {"z": [1.0, 1.12], "f": [330, 1000]}},
    {"fondo": rayos("oro"), "lines": L("En vez de ignorarlo, hizo una prueba: puso granos de maíz frente al magnetrón."),
     "items": [it("disco", 300, 1150, 0.8, anim="pop"),
               it("etiqueta", 790, 1150, 0.8, delay=1.6, texto="MAÍZ", fondo="#fde68a", rot=-4)]},
    {"sigue": True, "lines": L("Y se convirtieron en palomitas."),
     "items": [it("etiqueta", 700, 850, 0.7, texto="POP", fondo="#ffffff", rot=8),
               it("etiqueta", 900, 1000, 0.7, delay=0.3, texto="POP", fondo="#ffffff", rot=-8),
               it("etiqueta", 760, 1400, 0.7, delay=0.6, texto="POP", fondo="#ffffff", rot=5)]},
    {"fondo": rayos("rojo"), "lines": L("Después probó con un huevo.", "Según la Sociedad Americana de Física, el huevo explotó y salpicó a un colega que miraba de cerca."),
     "items": [it("disco", 300, 1150, 0.7, anim="pop"),
               it("etiqueta", 300, 820, 0.8, texto="HUEVO", fondo="#ffffff", rot=-4),
               it("persona", 780, 1560, 0.85, at=1, anim="right", cara="sorpresa", brazos="cabeza", **COLEGA),
               it("etiqueta", 780, 1000, 1.0, at=1, delay=1.6, texto="¡PLAF!", fondo="#fde047", rot=7)]},
    {"fondo": rayos("gris"), "lines": L("Ojo: algunos historiadores dicen que fueron varias observaciones, no un solo momento."),
     "items": [it("icono", 540, 1150, 1.2, anim="pop", tipo="exclamacion", color="#f0c448"),
               it("etiqueta", 540, 1450, 0.9, delay=1.6, texto="SE DISCUTE", fondo="#ffffff", rot=4)]},
    {"fondo": rayos("lila"), "lines": L("Lo seguro: el 8 de octubre de 1945, Raytheon pidió la patente."),
     "items": [it("libro", 540, 1250, 1.0, anim="pop", texto="PATENTE", color="#1e3a8a"),
               it("calendario", 540, 760, 0.6, delay=1.6, anim="pop", texto="1945")]},

    # ------------------------------------------------------------ 4. como funciona
    {"fondo": rayos("cielo"), "lines": L("Pero, ¿cómo calienta la comida?"),
     "items": [micro(540, 1520, 1.0, anim="pop", id="mic"),
               it("icono", 540, 760, 1.0, delay=0.6, anim="pop", tipo="pregunta", id="preg")]},
    {"sigue": True, "quita": ["preg"], "lines": L("Adentro hay un magnetrón que produce ondas de unos 2.450 megahercios.", say={0: "Adentro hay un magnetrón que produce ondas de unos dos mil cuatrocientos cincuenta megahercios."}),
     "items": [it("chapa", 540, 760, 1.3, delay=1.0, texto="2.450 MHz")]},
    {"fondo": rayos("azul"), "lines": L("Las paredes de metal hacen rebotar las ondas, y la comida las absorbe."),
     "items": [micro(540, 1520, 1.0, anim="fade"),
               it("flecha", 300, 900, 0.5, delay=0.6, anim="fade", rot=30),
               it("flecha", 780, 900, 0.5, delay=1.2, anim="fade", rot=150)]},
    {"fondo": rayos("menta"), "lines": L("Las moléculas de agua tienen un lado positivo y otro negativo. Las ondas las hacen vibrar sin parar."),
     "items": [it("etiqueta", 330, 1000, 1.0, texto="+", fondo="#ef4444", rot=0),
               it("etiqueta", 750, 1000, 1.0, delay=0.6, texto="−", fondo="#3b82f6", rot=0),
               it("etiqueta", 540, 1350, 1.0, delay=2.0, texto="H₂O", fondo="#bfdbfe", rot=-4)]},
    {"sigue": True, "lines": L("Ese movimiento produce fricción, y la fricción produce calor."),
     "items": [it("etiqueta", 540, 760, 1.0, delay=0.4, texto="CALOR", fondo="#fb923c", rot=5)]},
    {"fondo": rayos("durazno"), "lines": L("Por eso lo que tiene más agua, como las verduras, se calienta antes."),
     "items": [it("etiqueta", 540, 1150, 1.2, anim="pop", texto="VERDURAS", fondo="#86efac", rot=-4),
               it("chapa", 540, 760, 1.3, delay=1.6, texto="+ AGUA", sub="mas rapido")]},
    {"fondo": rayos("gris"), "lines": L("La rejilla de metal de la puerta tiene agujeros mucho más chicos que las ondas, que miden unos doce centímetros."),
     "items": [micro(540, 1520, 1.0, anim="fade"),
               it("chapa", 540, 760, 1.35, delay=2.4, texto="12 CM", sub="cada onda")],
     "cam": {"z": [1.0, 1.12], "f": [400, 1250]}},
    {"sigue": True, "lines": L("La luz sale y puedes ver tu comida. Las microondas, no.", pausa=0.2),
     "items": [it("icono", 850, 1000, 0.8, delay=1.6, anim="pop", tipo="check")]},

    # ------------------------------------------------------------ 5. el Radarange
    {"fondo": rayos("lila"), "lines": L("En 1947 salió a la venta el primer horno de microondas: el Radarange.", say={0: "En 1947 salió a la venta el primer horno de microondas: el Rádar Reinch."}),
     "items": [it("edificio", 540, 1560, 1.0, anim="crece", **RADAR),
               it("calendario", 860, 720, 0.55, delay=1.4, anim="pop", texto="1947")]},
    {"sigue": True, "lines": L("Era del tamaño de un refrigerador: de un metro setenta a un metro ochenta, según la fuente."),
     "items": [it("persona", 830, 1560, 0.85, anim="right", cara="sorpresa", **COLEGA),
               it("chapa", 330, 760, 1.1, delay=1.6, texto="1,7-1,8 M", sub="de alto")]},
    {"fondo": {"tipo": "liso", "c": "#e4e4ea"}, "lines": L("Pesaba unos 340 kilos. Y se enfriaba con agua, por tuberías.", say={0: "Pesaba unos trescientos cuarenta kilos. Y se enfriaba con agua, por tuberías."}),
     "items": [it("bascula", 540, 1560, 1.25, anim="up", texto="340 KG"),
               it("edificio", 540, 1470, 0.7, delay=0.5, anim="drop", **RADAR)],
     "dato": dato(340, "EL RADARANGE, 1947", suf=" KG", y=640, delay=1.0)},
    {"fondo": rayos("menta"), "lines": L("Y costaba entre dos mil y cinco mil dólares, según la fuente."),
     "items": [it("billetes", 540, 1400, 1.0, anim="drop", n=4),
               it("chapa", 540, 760, 1.35, delay=1.6, texto="$2.000-5.000", sub="segun la fuente")]},
    {"fondo": rayos("cielo"), "lines": L("Lo compraban restaurantes, barcos, trenes y hospitales."),
     "items": [it("tienda", 540, 1560, 0.7, anim="crece", texto="RESTAURANTE", letrero="#b91c1c", letra="#ffffff"),
               it("etiqueta", 250, 760, 0.7, delay=0.8, texto="BARCOS", fondo="#ffffff", rot=-5),
               it("etiqueta", 540, 900, 0.7, delay=1.4, texto="TRENES", fondo="#ffffff", rot=4),
               it("etiqueta", 830, 760, 0.7, delay=2.0, texto="HOSPITALES", fondo="#ffffff", rot=-3)]},
    {"fondo": rayos("oro"), "lines": L("Hasta hubo una máquina de hot dogs calentados con microondas: la Speedy Weeny.",
                                       say={0: "Hasta hubo una máquina de jot dogs calentados con microondas: la Spídi Uíni."}),
     "items": [it("tienda", 540, 1560, 0.6, anim="crece", texto="HOT DOGS", letrero="#facc15", letra="#1d1d2b", ancho=480),
               it("etiqueta", 540, 760, 0.9, delay=2.6, texto="SPEEDY WEENY", fondo="#ffffff", rot=-4)]},

    # ------------------------------------------------------------ 6. llega a la casa
    {"fondo": rayos("azul"), "lines": L("En 1955, la empresa Tappan sacó el primero para la casa. Costaba 1.295 dólares.",
                                        say={0: "En 1955, la empresa Tápan sacó el primero para la casa. Costaba mil doscientos noventa y cinco dólares."}),
     "items": [micro(540, 1520, 0.9, anim="pop"),
               it("chapa", 540, 760, 1.4, delay=2.0, texto="$1.295", sub="Tappan, 1955")]},
    {"sigue": True, "lines": L("El primer año fabricaron solo 34.", say={0: "El primer año fabricaron solo treinta y cuatro."}),
     "items": [it("etiqueta", 540, 960, 0.9, delay=0.6, texto="SOLO 34", fondo="#ef4444", rot=-4)]},
    {"fondo": {"tipo": "oficina"}, "lines": L("A mediados de los sesenta, Raytheon compró Amana, que hacía refrigeradores.",
                                              say={0: "A mediados de los sesenta, Réizion compró Amána, que hacía refrigeradores."}),
     "items": [it("edificio", 300, 1560, 0.7, anim="crece", texto="RAYTHEON", pisos=5, ancho=380),
               it("flecha", 540, 1250, 0.35, delay=1.0, anim="fade"),
               it("tienda", 790, 1560, 0.5, delay=1.6, anim="crece", texto="AMANA", ancho=480)]},
    {"fondo": rayos("oro"), "lines": L("Y en 1967 llegó el que lo cambió todo: el Radarange de mesa de Amana.", say={0: "Y en 1967 llegó el que lo cambió todo: el Rádar Reinch de mesa de Amána."}),
     "items": [it("mesa", 540, 1560, 1.0, anim="up"),
               micro(540, 1330, 0.7, delay=0.6, anim="drop"),
               it("calendario", 860, 720, 0.55, delay=1.6, anim="pop", texto="1967")]},
    {"sigue": True, "lines": L("Cabía sobre la mesa de la cocina y costaba 495 dólares.", say={0: "Cabía sobre la mesa de la cocina y costaba cuatrocientos noventa y cinco dólares."}),
     "dato": dato(495, "AMANA, 1967", pre="$", y=640, delay=1.4)},
    {"sigue": True, "lines": L("Con la inflación, hoy serían unos cuatro mil dólares."),
     "items": [it("etiqueta", 480, 900, 0.85, delay=0.6, texto="HOY: ~$4.000", fondo="#ffffff", rot=4)]},
    {"fondo": rayos("menta"), "lines": L("En 1975, en Estados Unidos ya se vendían más microondas que estufas de gas."),
     "items": [micro(300, 1520, 0.55, anim="left"),
               it("icono", 300, 900, 0.7, delay=1.4, anim="pop", tipo="check"),
               it("chapa", 790, 1100, 1.35, delay=0.8, texto="1975", sub="supera al gas")]},

    # ------------------------------------------------------------ curiosidades
    {"fondo": rayos("durazno"), "lines": L("Y ahora, cosas que casi nadie sabe.", pausa=0.2),
     "items": [it("icono", 540, 1150, 1.4, anim="pop", tipo="exclamacion", color="#f0c448")]},
    {"fondo": rayos("oro"), "lines": L("Uno. Spencer tuvo más de cien patentes, pero Raytheon solo le pagaba el bono normal: dos dólares por cada una."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="preocupado", **SPENCER),
               it("libro", 790, 1200, 0.6, delay=0.8, anim="pop", texto="100+", color="#1e3a8a")],
     "dato": dato(2, "POR PATENTE", pre="$", y=640, delay=3.0, cuenta=False)},
    {"fondo": rayos("cielo"), "lines": L("Dos. Las microondas no cocinan de adentro hacia afuera.", "Entran apenas uno o dos centímetros; el centro se calienta porque el calor se va pasando."),
     "items": [it("icono", 540, 1150, 1.1, anim="pop", tipo="x"),
               it("chapa", 540, 760, 1.35, at=1, delay=0.8, texto="1-2 CM", sub="lo que entran")]},
    {"sigue": True, "lines": L("Por eso conviene dejarla reposar un poco."),
     "items": [it("reloj", 850, 1450, 0.6, delay=0.4, anim="pop", hora=1)]},
    {"fondo": rayos("menta"), "lines": L("Tres. La comida no se vuelve radiactiva. Las microondas no son como los rayos X: solo producen calor."),
     "items": [micro(540, 1520, 0.85, anim="pop"),
               it("etiqueta", 540, 760, 1.0, delay=1.0, texto="NO RADIACTIVA", fondo="#86efac", rot=-4)]},
    {"fondo": rayos("lila"), "lines": L("Y cuatro. No destruye más nutrientes que otros métodos. Como es rápido y usa poca agua, puede conservar más vitamina C."),
     "items": [it("etiqueta", 540, 1150, 1.2, anim="pop", texto="VITAMINA C", fondo="#fdba74", rot=4),
               it("icono", 840, 820, 0.8, delay=2.0, anim="pop", tipo="check")]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("azul"), "lines": L("¿Y qué pasó después? Entre 1986 y 2001, los hogares de Estados Unidos con microondas pasaron del 25 por ciento a más del 90."),
     "items": [it("grafica", 540, 1540, 1.15, anim="crece", tipo="sube", color="#3b82f6"),
               it("chapa", 300, 760, 1.3, delay=1.8, texto="25%", sub="1986"),
               it("chapa", 790, 760, 1.3, delay=3.0, texto="+90%", sub="2001")]},
    {"fondo": rayos("gris"), "lines": L("Spencer llegó a vicepresidente de Raytheon. Murió en 1970, a los 76 años.", say={0: "Spénser llegó a vicepresidente de Réizion. Murió en 1970, a los setenta y seis años."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="feliz", **SPENCER),
               it("chapa", 540, 700, 1.3, delay=1.8, texto="1894-1970", id="anios")]},
    {"sigue": True, "quita": ["anios"], "lines": L("Y en 1999 entró al Salón Nacional de la Fama de los Inventores.", pausa=0.2),
     "items": [it("etiqueta", 540, 740, 0.85, delay=0.6, texto="SALÓN DE LA FAMA", fondo="#f0c448", rot=5)]},

    # ------------------------------------------------------------ cierre
    {"fondo": NOCHE, "lines": L("De 340 kilos y enfriada con agua, a una caja que cabe en cualquier cocina.",
                                say={0: "De trescientos cuarenta kilos y enfriada con agua, a una caja que cabe en cualquier cocina."}),
     "items": [it("edificio", 270, 1560, 0.6, anim="left", **RADAR),
               it("flecha", 540, 1300, 0.4, delay=1.0, anim="fade"),
               micro(810, 1520, 0.45, delay=1.6, anim="right")],
     "cam": {"z": [1.0, 1.06], "f": [540, 1300]}},
    {"fondo": rayos("durazno"), "lines": L("Todo por un chocolate que se derritió en el bolsillo de un hombre curioso.", pausa=0.2),
     "items": [it("persona", 540, 1560, 1.0, anim="up", cara="risa", **SPENCER),
               it("etiqueta", 780, 1100, 0.85, delay=1.4, texto="CHOCOLATE", fondo=CHOCO, rot=6)]},
    {"fondo": rayos("oro"), "lines": L("¿Y tú? ¿Qué es lo más raro que has calentado en el microondas? Te leo en los comentarios."),
     "items": [micro(540, 1520, 0.9, anim="pop"),
               it("etiqueta", 540, 760, 1.1, delay=1.4, texto="¿QUÉ CALENTASTE?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "El microondas nació por un chocolate derretido: la historia de Percy Spencer",
    "description": ("En 1945, el ingeniero Percy Spencer notó que un chocolate se derritió en su bolsillo junto a un magnetrón de radar. "
                    "De ahí salió el Radarange de 1947 (unos 340 kilos, enfriado con agua) y, en 1967, el microondas de mesa de Amana por 495 dólares. "
                    "Además: cómo funciona y tres mitos desmentidos.\n"
                    "Fuentes: National Inventors Hall of Fame; American Physical Society (APS News); IEEE Spectrum; NPR; History.com; "
                    "Lemelson-MIT; Mass Moments (Mass Humanities); MIT Technology Review; FDA y EPA (seguridad del microondas); "
                    "Harvard Health (nutrientes); Encyclopaedia Britannica; The Saturday Evening Post; Ingenium (museo de Canadá); The Henry Ford."),
    "hashtags": ["#DatoBomba", "#microondas", "#inventos", "#ciencia", "#historia"],
    "source_url": "https://www.invent.org/inductees/percy-l-spencer",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_microondas.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55))
