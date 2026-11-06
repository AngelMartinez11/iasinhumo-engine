"""Genera ejemplos/hsf_laptop.json: la historia de la primera laptop (Historias Sin Filtro, motor v4, formato largo).

Estructura de formato largo (estilo Empty, video de referencia: D. B. Cooper):
gancho -> pregunta -> capitulos de la historia -> capitulo de datos curiosos -> que paso despues -> cierre con pregunta.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

KAY = {"camisa": "#7c3aed", "pelo": "#6b4423", "peinado": "corto", "lentes": True}
ADAM = {"ropa": "traje", "corbata": "#f0c448", "pelo": "#c9c9c9", "peinado": "canoso"}
BILL = {"camisa": "#0ea5e9", "pelo": "#a16207", "peinado": "calvo", "lentes": True}
EJEC = {"ropa": "traje", "corbata": "#ef4444", "pelo": "#1f1f1f"}
NOTE = "#ef4444"


def L(*txts, pausa=0, say=None):
    out = [{"text": t} for t in txts]
    if say:
        for i, s in say.items():
            out[i]["say"] = s
    if pausa:
        out[-1]["pausa"] = pausa
    return out


def S(text, say):
    return {"text": text, "say": say}


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


def dato(num, texto, pre="", suf="", y=600, delay=1.0, cuenta=True):
    return {"num": num, "pre": pre, "suf": suf, "texto": texto, "y": y, "delay": delay, "cuenta": cuenta}


def cap(t, n):
    return {"capitulo": {"t": t, "n": n}, "min_dur": 1.8}


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": rayos("azul"), "lines": L("Hoy una laptop cabe en tu mochila y pesa poco más de un kilo."),
     "items": [it("laptop_moderna", 540, 1500, 1.0, anim="pop", id="lap", texto="HOY"),
               it("chapa", 540, 760, 1.4, delay=1.6, texto="~1 KG", sub="laptop actual")],
     "cam": {"z": [1.0, 1.05], "f": [540, 1200]}},
    {"fondo": {"tipo": "noche"}, "lines": L("Pero la primera computadora que se vendió como portátil pesaba veinticinco kilos."),
     "items": [it("bascula", 540, 1560, 1.25, anim="up", texto="25 KG"),
               it("maletin_pc", 540, 1450, 0.95, delay=0.9, anim="drop", texto="5100")],
     "dato": dato(25, "KILOS", suf=" KG", y=640, delay=2.2),
     "cam": {"z": [1.12, 1.0], "f": [540, 1250]}},
    {"sigue": True, "lines": L("Y costaba lo mismo que un carro."),
     "items": [it("etiqueta", 540, 900, 1.0, texto="HASTA $19.975", fondo="#ef4444", rot=-5)]},
    {"fondo": rayos("oro"), "lines": L("¿Cómo pasamos de máquinas que se cargaban como maletas a algo que se abre como un libro?"),
     "items": [it("maletin_pc", 290, 1500, 0.55, anim="left"),
               it("flecha", 540, 1240, 0.8, delay=1.0, anim="fade"),
               it("laptop_moderna", 800, 1500, 0.55, delay=1.6, anim="right"),
               it("icono", 540, 820, 1.1, delay=2.6, anim="pop", tipo="pregunta")]},
    # ------------------------------------------------------------ 1. el sueno
    cap("EL SUEÑO", 1),
    {"fondo": rayos("lila"), "lines": [S("A finales de los sesenta, un investigador llamado Alan Kay tuvo una idea rara para su época.", "A finales de los sesenta, un investigador llamado Álan Kéi tuvo una idea rara para su época.")],
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="kay", cara="feliz", brazos="cabeza", **KAY),
               it("nombre", 540, 700, 1.0, delay=1.8, texto="Alan Kay", sub="cientifico de la computacion")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"sigue": True, "lines": L("Una computadora del tamaño de un cuaderno."),
     "items": [it("libro", 830, 1150, 0.55, delay=1.6, anim="pop", id="libro", texto="DYNA")]},
    {"sigue": True, "lines": [S("La llamó Dynabook, y la pensó para niños.", "La llamó Dáinabuk, y la pensó para niños.")],
     "items": [it("nino", 230, 1560, 1.0, anim="left", cara="feliz", camisa="#22c55e"),
               it("etiqueta", 830, 860, 0.85, delay=0.6, texto="DYNABOOK", rot=6)]},
    {"fondo": rayos("durazno"), "lines": L("En 1972 la describió en un artículo: una computadora personal para niños de todas las edades."),
     "items": [it("libro", 540, 1150, 1.0, anim="pop", abierto=True, texto="1972"),
               it("chapa", 540, 720, 1.35, delay=2.0, texto="1972", sub="el articulo de Kay")]},
    {"fondo": rayos("cielo"), "lines": [S("Su equipo en Xerox intentó construirla. El prototipo se llamó NoteTaker.", "Su equipo en Sérox intentó construirla. El prototipo se llamó Nout téiker.")],
     "items": [it("edificio", 540, 1560, 0.8, anim="crece", texto="XEROX PARC", pisos=6, ancho=520)],
     "cam": {"z": [1.0, 1.1], "f": [540, 1200]}},
    {"fondo": {"tipo": "liso", "c": "#e4e4ea"}, "lines": L("¿El problema? Pesaba unos veintidós kilos."),
     "items": [it("bascula", 540, 1560, 1.25, anim="up"),
               it("maletin_pc", 540, 1450, 0.9, delay=0.5, anim="drop", color="#cbd5e1", texto="ST-78")],
     "dato": dato(22, "EL NOTETAKER, 1976", suf=" KG", y=640, delay=1.2)},
    {"sigue": True, "lines": L("Nunca salió a la venta. Pero la semilla ya estaba plantada.", pausa=0.3),
     "items": [it("etiqueta", 760, 900, 0.9, texto="NO SE VENDIÓ", fondo="#ef4444", rot=7)]},

    # ------------------------------------------------------------ 2. las computadoras maleta
    cap("COMPUTADORAS MALETA", 2),
    {"fondo": rayos("azul"), "lines": L("En 1975, IBM sacó su modelo 5100 y lo llamó computadora portátil."),
     "items": [it("maletin_pc", 540, 1520, 1.0, anim="crece", texto="IBM"),
               it("calendario", 860, 760, 0.55, delay=0.8, anim="pop", texto="1975")]},
    {"sigue": True, "lines": L("Pesaba veinticinco kilos y había que enchufarla. Portátil, con mucha fe."),
     "items": [it("chapa", 540, 760, 1.4, texto="25 KG"),
               it("etiqueta", 540, 1640, 0.85, delay=1.6, texto="SIN BATERÍA", fondo="#ffffff", rot=-4)]},
    {"fondo": rayos("durazno"), "lines": [S("Seis años después llegó un hombre que cambió el juego: Adam Osborne.", "Seis años después llegó un hombre que cambió el juego: Ádam Ósborn.")],
     "items": [it("persona", 540, 1560, 0.95, anim="up", id="adam", cara="risa", brazos="cruzados", **ADAM),
               it("nombre", 540, 700, 1.0, delay=1.6, texto="Adam Osborne", sub="escritor de libros de computacion")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1150]}},
    {"fondo": rayos("oro"), "lines": [S("El 3 de abril de 1981 presentó la Osborne 1.", "El 3 de abril de 1981 presentó la Ósborn uan.")],
     "items": [it("maletin_pc", 540, 1520, 1.05, anim="drop", id="osb", texto="CP/M"),
               it("calendario", 860, 720, 0.55, delay=1.0, anim="pop", texto="1981")],
     "cam": {"z": [1.0, 1.06], "f": [540, 1250]}},
    {"sigue": True, "lines": L("Tenía una pantalla de apenas cinco pulgadas, dos disqueteras y un asa para cargarla."),
     "items": [it("chapa", 290, 760, 1.25, delay=0.3, texto="5\"", sub="pantalla"),
               it("chapa", 800, 760, 1.25, delay=1.4, texto="2", sub="disqueteras")]},
    {"fondo": rayos("menta"), "lines": L("Pero lo que hizo ruido fue el precio: mil setecientos noventa y cinco dólares."),
     "items": [it("bolsa_dinero", 540, 1560, 1.1, anim="drop", texto="$")],
     "dato": dato(1795, "LA OSBORNE 1", pre="$", y=640, delay=1.6)},
    {"sigue": True, "lines": L("Y traía programas que, por separado, costaban unos mil quinientos dólares."),
     "items": [it("sobre", 250, 1150, 0.6, anim="drop", color="#3b82f6", texto="SOFT"),
               it("sobre", 830, 1150, 0.6, delay=0.4, anim="drop", color="#22c55e", texto="SOFT")]},
    {"fondo": rayos("cielo"), "lines": [S("La revista InfoWorld repitió el precio en su portada, por si los lectores pensaban que era un error.", "La revista Info uórld repitió el precio en su portada, por si los lectores pensaban que era un error.")],
     "items": [it("libro", 540, 1250, 1.15, anim="pop", abierto=True, texto="1981"),
               it("etiqueta", 540, 760, 1.1, delay=0.6, texto="$1795", rot=-4),
               it("etiqueta", 540, 960, 1.1, delay=2.4, texto="SÍ, $1795", fondo="#ef4444", rot=4)]},
    {"fondo": rayos("cielo"), "lines": L("La publicidad decía que cabía debajo del asiento de un avión."),
     "items": [it("avion", 540, 820, 0.9, anim="left"),
               it("maletin_pc", 540, 1520, 0.7, delay=1.2, anim="up")]},
    {"fondo": {"tipo": "liso", "c": "#e4e4ea"}, "lines": L("Pesaba once kilos, como una máquina de coser. Y no tenía batería."),
     "items": [it("bascula", 540, 1560, 1.25, anim="up", texto="11 KG"),
               it("maletin_pc", 540, 1450, 0.9, delay=0.5, anim="drop", texto="CP/M")],
     "dato": dato(11, "KILOS", suf=" KG", y=640, delay=1.0)},
    {"fondo": rayos("menta"), "lines": L("Aun así, fue un éxito. En su mejor momento vendía unas diez mil al mes."),
     "items": [it("grafica", 540, 1520, 1.15, anim="crece", tipo="sube", color="#22c55e")],
     "dato": dato(10000, "UNIDADES AL MES", y=640, delay=1.4)},

    # ------------------------------------------------------------ 3. el error
    cap("EL ERROR QUE TIENE NOMBRE", 3),
    {"fondo": {"tipo": "oficina"}, "lines": L("A principios de 1983, Osborne empezó a mostrarle a la prensa su siguiente modelo, más potente.", say=None),
     "items": [it("persona", 300, 1640, 0.85, anim="left", cara="feliz", brazos="senala", **ADAM),
               it("maletin_pc", 760, 1560, 0.6, delay=1.4, anim="pop", color="#94a3b8", texto="EXEC")]},
    {"sigue": True, "lines": L("Y pasó algo que no esperaba.")},
    {"fondo": rayos("rojo"), "lines": L("Las tiendas cancelaron sus pedidos de la Osborne 1. ¿Para qué comprar la vieja, si venía una mejor?"),
     "items": [it("tienda", 540, 1560, 0.75, anim="crece", texto="COMPUTADORAS", letrero="#1e3a8a", letra="#ffffff"),
               it("icono", 820, 820, 0.9, delay=1.4, anim="pop", tipo="x")]},
    {"sigue": True, "lines": L("Las máquinas se acumularon. Bajaron el precio, y aun así no se vendían."),
     "items": [it("maletin_pc", 230, 1560, 0.42, anim="drop", abierto=False),
               it("maletin_pc", 540, 1560, 0.42, delay=0.3, anim="drop", abierto=False),
               it("maletin_pc", 850, 1560, 0.42, delay=0.6, anim="drop", abierto=False)]},
    {"fondo": {"tipo": "noche"}, "lines": L("El 13 de septiembre de 1983, la empresa se declaró en quiebra.", pausa=0.3),
     "items": [it("lapida", 540, 1560, 1.25, anim="crece", texto="OSBORNE", sub="1983")],
     "cam": {"z": [1.12, 1.0], "f": [540, 1250]}},
    {"fondo": rayos("gris"), "lines": L("Hoy, en el mundo de los negocios, anunciar un producto antes de tiempo y matar las ventas del actual se llama el efecto Osborne.",
                                        say={0: "Hoy, en el mundo de los negocios, anunciar un producto antes de tiempo y matar las ventas del actual se llama el efecto Ósborn."}),
     "items": [it("etiqueta", 540, 1100, 1.1, texto="EFECTO OSBORNE", fondo="#f0c448", rot=-4)]},
    {"sigue": True, "lines": L("Aunque ex empleados dicen que la empresa ya venía con problemas de dinero."),
     "items": [it("etiqueta", 540, 1400, 0.8, delay=0.5, texto="SE DISCUTE", fondo="#ffffff", rot=5)]},

    # ------------------------------------------------------------ 4. el clon
    # ------------------------------------------------------------ 5. nace la laptop
    cap("NACE LA LAPTOP", 4),
    {"fondo": rayos("durazno"), "lines": [S("Pero la verdadera revolución venía de Japón. Epson presentó la HX-20.", "Pero la verdadera revolución venía de Japón. Épson presentó la hache equis veinte.")],
     "items": [it("laptop", 540, 1350, 1.2, anim="pop", texto="HX-20", color="#facc15")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1150]}},
    {"sigue": True, "lines": L("Del tamaño de una hoja de papel, con su propia impresora integrada."),
     "items": [it("etiqueta", 540, 760, 1.0, delay=0.6, texto="IMPRESORA INCLUIDA", rot=-4)]},
    {"fondo": rayos("menta"), "lines": L("Y lo más loco: con una carga, la batería duraba unas cincuenta horas."),
     "items": [it("bateria", 540, 1250, 1.2, anim="pop", nivel=1.0)],
     "dato": dato(50, "HORAS DE BATERÍA", suf=" H", y=640, delay=1.4)},
    {"fondo": {"tipo": "liso", "c": "#e4e4ea"}, "lines": L("Pesaba un kilo y seiscientos gramos, cuando la Osborne pesaba once."),
     "items": [it("bascula", 290, 1560, 1.0, anim="up", texto="1.6 KG"),
               it("laptop", 290, 1300, 0.62, delay=0.4, anim="drop", texto="HX-20", color="#facc15"),
               it("bascula", 800, 1560, 1.0, delay=0.9, anim="up", texto="11 KG"),
               it("maletin_pc", 800, 1470, 0.62, delay=1.3, anim="drop")]},
    {"fondo": rayos("cielo"), "lines": [S("Y en 1982 apareció otra máquina, diseñada por el británico Bill Moggridge: la GRiD Compass.", "Y en 1982 apareció otra máquina, diseñada por el británico Bil Móguerich: la Grid Cómpas.")],
     "items": [it("persona", 260, 1560, 0.8, anim="left", cara="serio", brazos="senala", **BILL),
               it("nombre", 360, 720, 0.85, delay=1.4, texto="Bill Moggridge", sub="disenador industrial"),
               it("clamshell", 760, 1500, 0.6, delay=2.4, anim="pop", abierto=False, id="grid")]},
    {"sigue": True, "quita": ["grid"], "lines": L("Su gran idea fue la bisagra: una pantalla que se cierra sobre el teclado como una concha."),
     "items": [it("clamshell", 760, 1500, 0.6, anim="fade", abierto=True)],
     "cam": {"z": [1.0, 1.12], "f": [760, 1300]}},
    {"fondo": rayos("gris"), "lines": L("Casi todas las laptops de hoy usan esa forma."),
     "items": [it("clamshell", 290, 1560, 0.62, anim="left"), it("laptop_moderna", 800, 1560, 0.6, delay=0.8, anim="right")]},
    {"fondo": rayos("rojo"), "lines": L("Costaba ocho mil ciento cincuenta dólares. Era tan cara que su gran cliente fue el gobierno de Estados Unidos."),
     "items": [it("clamshell", 540, 1500, 0.8, anim="pop")],
     "dato": dato(8150, "LA GRID COMPASS, 1982", pre="$", y=640, delay=1.2)},
    {"fondo": {"tipo": "noche"}, "lines": L("Y en noviembre de 1983 voló al espacio en el transbordador Columbia."),
     "items": [it("transbordador", 540, 1100, 1.1, anim="left"),
               it("chapa", 540, 1480, 1.3, delay=1.8, texto="1983", sub="transbordador Columbia")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1100]}},
    {"sigue": True, "lines": L("Fue la primera laptop usada en una misión espacial.", pausa=0.3)},

    {"fondo": rayos("azul"), "lines": L("Faltaba una cosa: que fuera para todos. En 1985, Toshiba lanzó la T1100."),
     "items": [it("clamshell", 540, 1500, 0.85, anim="pop", color="#475569", tinta="#cbd5e1", texto="T1100"),
               it("calendario", 860, 720, 0.55, delay=1.6, anim="pop", texto="1985")]},
    {"sigue": True, "lines": L("Batería recargable, pantalla plana, disquete pequeño, y compatible con los programas de la IBM PC.", say={0: "Batería recargable, pantalla plana, disquete pequeño, y compatible con los programas de la I B M P C."}),
     "items": [it("chapa", 290, 760, 1.25, texto="4.1 KG"), it("chapa", 800, 760, 1.25, delay=1.2, texto="$1899")]},
    {"sigue": True, "lines": L("Toshiba la llama la primera laptop para el mercado masivo.", pausa=0.2)},
    # ------------------------------------------------------------ 6. el diseno que copiamos todos
    cap("EL DISEÑO QUE COPIAMOS TODOS", 5),
    {"fondo": rayos("lila"), "lines": [S("En octubre de 1991, Apple presentó sus primeras PowerBook.", "En octubre de 1991, Ápol presentó sus primeras Páuer buk.")],
     "items": [it("laptop_moderna", 540, 1500, 0.9, anim="pop", color="#64748b", pantalla="#0f172a")]},
    {"sigue": True, "lines": L("Su truco fue mover el teclado hacia atrás y dejar espacio para apoyar las manos, con el control del cursor en el centro."),
     "items": [it("etiqueta", 540, 1640, 0.85, delay=1.4, texto="REPOSAMANOS", rot=-3)],
     "cam": {"z": [1.0, 1.12], "f": [540, 1450]}},
    {"sigue": True, "lines": L("Mira tu laptop: todavía es así."),
     "items": [it("icono", 850, 820, 0.8, anim="pop", tipo="check")]},
    {"fondo": rayos("oro"), "lines": L("En su primer año, esas computadoras le dejaron a Apple más de mil millones de dólares."),
     "items": [it("billetes", 300, 1450, 0.9, anim="drop", n=4), it("bolsa_dinero", 780, 1560, 1.0, delay=0.4, anim="drop")],
     "dato": dato(1000, "MILLONES EL PRIMER AÑO", pre="$", y=640, delay=1.4)},

    # ------------------------------------------------------------ 7. el adelantamiento
    cap("EL DÍA QUE GANARON", 6),
    {"fondo": rayos("azul"), "lines": L("Durante décadas, la computadora de verdad era la de escritorio. La portátil era un lujo."),
     "items": [it("pc_escritorio", 540, 1560, 0.95, anim="crece")]},
    {"fondo": rayos("menta"), "lines": L("Hasta 2008. Ese año, por primera vez, en el mundo se enviaron más laptops que computadoras de escritorio en un trimestre."),
     "items": [it("pc_escritorio", 280, 1560, 0.5, anim="left"),
               it("laptop_moderna", 800, 1560, 0.6, delay=1.0, anim="right"),
               it("calendario", 540, 760, 0.6, delay=2.0, anim="pop", texto="2008")]},
    # ------------------------------------------------------------ 8. datos curiosos
    cap("DATOS QUE NO SABÍAS", 7),
    {"fondo": rayos("durazno"), "lines": L("Uno. Epson anunciaba la HX-20 con una foto en dos páginas de revista y un título: tamaño real.", say={0: "Uno. Épson anunciaba la hache equis veinte con una foto en dos páginas de revista y un título: tamaño real."}),
     "items": [it("libro", 540, 1200, 1.1, anim="pop", abierto=True, texto="1:1")]},
    {"fondo": rayos("cielo"), "lines": L("Dos. En la T1100, la pantalla funcionaba con solo cinco chips. En la IBM PC de escritorio hacían falta casi cien.", say={0: "Dos. En la te mil cien, la pantalla funcionaba con solo cinco chips. En la I B M P C de escritorio hacían falta casi cien."}),
     "items": [it("clamshell", 290, 1560, 0.55, anim="left", color="#475569", tinta="#cbd5e1", texto="T1100"), it("chapa", 290, 820, 1.5, delay=0.6, texto="5", sub="chips"),
               it("pc_escritorio", 800, 1560, 0.55, delay=2.0, anim="right"), it("chapa", 800, 820, 1.5, delay=2.6, texto="~100", sub="chips")]},
    {"fondo": rayos("menta"), "lines": L("Y tres. Alan Kay dice que su Dynabook todavía no se ha inventado, porque lo importante no era la máquina, sino aprender con ella.", say={0: "Y tres. Álan Kéi dice que su Dáinabuk todavía no se ha inventado, porque lo importante no era la máquina, sino aprender con ella."}),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="serio", **KAY),
               it("libro", 830, 1150, 0.5, delay=1.4, anim="pop", texto="DYNA")]},

    # ------------------------------------------------------------ cierre
    {"fondo": {"tipo": "noche"}, "lines": L("De veinticinco kilos y enchufada a la pared, a poco más de un kilo y horas de batería."),
     "items": [it("maletin_pc", 270, 1560, 0.45, anim="left"),
               it("flecha", 540, 1300, 0.4, delay=1.0, anim="fade"),
               it("laptop_moderna", 810, 1560, 0.45, delay=1.6, anim="right")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1350]}},
    {"fondo": rayos("lila"), "lines": L("Todo empezó con un dibujo de un niño con una computadora en las manos.", pausa=0.3),
     "items": [it("nino", 540, 1560, 1.5, anim="up", cara="feliz", camisa="#22c55e"), it("libro", 700, 1060, 0.32, delay=0.6, anim="pop", texto="")]},
    {"fondo": rayos("oro"), "lines": L("¿Y tú? ¿Cuál fue tu primera computadora? Te leo en los comentarios."),
     "items": [it("etiqueta", 540, 1200, 1.1, texto="¿LA TUYA?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "La primera laptop pesaba 25 kilos: así nació la computadora portátil",
    "description": ("De la idea de Alan Kay en 1972 a la Osborne 1 de 11 kilos, la GRiD Compass que voló al espacio, "
                    "la Epson HX-20 con 50 horas de batería y el día de 2008 en que las laptops superaron a las de escritorio.\n"
                    "Fuentes: Computer History Museum; IEEE (hito Toshiba T1100); Epson (historia corporativa HX-20); "
                    "IEEE Spectrum (GRiD Compass en el transbordador); InfoWorld 1981; iSuppli (envios Q3 2008)."),
    "hashtags": ["#HistoriasSinFiltro", "#laptop", "#tecnologia", "#historia", "#computadoras"],
    "source_url": "https://www.computerhistory.org/revolution/mobile-computing/18/316",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_laptop.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55))
