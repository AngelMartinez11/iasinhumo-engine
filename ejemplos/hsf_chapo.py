"""Genera ejemplos/hsf_chapo.json: la fuga de Joaquin Guzman del penal del Altiplano (Dato Bomba, canal historias, motor v4, formato largo).

Enfoque: ingenieria del tunel y fallas de seguridad. Tono neutral e informativo, sin glorificar.
Estructura: gancho -> pregunta -> historia en orden -> datos curiosos -> que paso despues -> cierre con pregunta.
Los bloques se marcan con la narracion y con cambio de fondo (el canal no usa tarjetas de capitulo).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

# protagonista: uniforme beige de reo, siempre igual
REO = {"camisa": "#c8b48a", "pantalon": "#a8956b", "pelo": "#1f1f1f", "peinado": "corto"}
GUARDIA = {"camisa": "#334155", "pantalon": "#1f2937", "pelo": "#3a2a1e", "peinado": "gorra"}
MARINO = {"camisa": "#4b5d3a", "pantalon": "#3f4d31", "pelo": "#1f1f1f", "peinado": "gorra"}
FISCAL = {"ropa": "traje", "corbata": "#1e3a8a", "pelo": "#3a2a1e"}
TIERRA = {"tipo": "liso", "c": "#6b4f3a", "suelo": "no"}


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


escenas = [
    # ------------------------------------------------------------ gancho
    {"fondo": {"tipo": "noche"}, "lines": L("Una cárcel federal de máxima seguridad, vigilada con cámaras día y noche."),
     "items": [it("edificio", 540, 1560, 0.95, anim="crece", id="penal", texto="ALTIPLANO", pisos=5, ancho=760, color="#94a3b8"),
               it("etiqueta", 540, 760, 0.85, delay=1.6, texto="MÁXIMA SEGURIDAD", fondo="#ef4444", rot=-4)],
     "cam": {"z": [1.0, 1.06], "f": [540, 1200]}},
    {"fondo": rayos("gris"), "lines": L("Y un hueco de cincuenta por cincuenta centímetros, escondido en la regadera de una celda."),
     "items": [it("celda", 540, 1560, 1.15, anim="up"),
               it("chapa", 540, 1420, 1.45, delay=1.8, anim="pop", texto="50 x 50 CM", sub="el hueco")],
     "cam": {"z": [1.0, 1.12], "f": [540, 1400]}},
    {"fondo": {"tipo": "noche"}, "lines": L("Por ahí escapó el narcotraficante más buscado de México."),
     "items": [it("persona", 540, 1560, 1.0, anim="up", id="reo", cara="serio", **REO),
               it("nombre", 540, 700, 1.0, delay=1.4, texto="Joaquín Guzmán Loera", sub="alias El Chapo")],
     "cam": {"z": [1.0, 1.1], "f": [540, 1050]}},
    {"fondo": rayos("oro"), "lines": L("¿Cómo se cava un túnel de un kilómetro y medio hasta una celda vigilada, sin que nadie lo note?"),
     "items": [it("chapa", 540, 1250, 1.5, anim="pop", texto="1.5 KM", sub="de túnel"),
               it("icono", 540, 760, 1.1, delay=2.4, anim="pop", tipo="pregunta")]},

    # ------------------------------------------------------------ antes de la fuga
    {"fondo": rayos("gris"), "lines": L("Antes, algo claro: esta no es una historia de héroes."),
     "items": [it("persona", 540, 1560, 0.95, anim="fade", cara="serio", **REO)]},
    {"sigue": True, "lines": L("Guzmán dirigía el cártel de Sinaloa y hoy cumple cadena perpetua."),
     "items": [it("etiqueta", 540, 780, 0.9, delay=1.4, texto="CADENA PERPETUA", fondo="#ef4444", rot=-4)]},
    {"fondo": rayos("azul"), "lines": L("Y no era su primera fuga. El 19 de enero de 2001 escapó del penal de Puente Grande, en Jalisco."),
     "items": [it("calendario", 300, 1250, 0.9, anim="pop", texto="2001"),
               it("pin", 790, 1300, 0.9, delay=2.2, anim="drop", texto="JALISCO")]},
    {"sigue": True, "lines": L("Según la versión oficial, salió escondido en un carrito de lavandería."),
     "items": [it("etiqueta", 540, 760, 0.95, delay=0.8, texto="LAVANDERÍA", rot=5)]},
    {"fondo": rayos("lila"), "lines": L("Pasó trece años prófugo, hasta que lo detuvieron en Mazatlán, en febrero de 2014."),
     "items": [it("chapa", 540, 760, 1.4, texto="13 AÑOS", sub="prófugo"),
               it("pin", 540, 1450, 1.0, delay=1.8, anim="drop", texto="MAZATLÁN", color="#3b82f6")]},
    {"fondo": rayos("durazno"), "lines": L("Lo encerraron en el Altiplano, en Almoloya de Juárez, Estado de México."),
     "items": [it("edificio", 540, 1560, 0.9, anim="crece", texto="ALTIPLANO", pisos=5, ancho=760, color="#94a3b8"),
               it("pin", 870, 800, 0.6, delay=1.6, anim="drop", texto="EDOMEX")]},
    {"sigue": True, "lines": L("Ocupaba la celda veinte del pasillo dos, en la zona de tratamientos especiales."),
     "items": [it("chapa", 380, 700, 1.2, texto="CELDA 20"),
               it("chapa", 380, 860, 0.95, delay=1.0, texto="PASILLO 2")]},

    # ------------------------------------------------------------ la noche
    {"fondo": {"tipo": "noche"}, "lines": L("Casi año y medio después, el sábado 11 de julio de 2015, el día parecía normal."),
     "items": [it("calendario", 540, 1150, 1.0, anim="pop", texto="11 JUL"),
               it("chapa", 540, 1480, 1.3, delay=1.8, texto="2015")]},
    {"fondo": rayos("gris"), "lines": L("A las ocho y cincuenta y dos de la noche, una cámara lo grabó entrando al área de la regadera."),
     "items": [it("celda", 540, 1560, 1.15, anim="fade", id="celda"),
               it("persona", 540, 1540, 0.85, delay=0.4, anim="right", id="reo2", cara="serio", **REO),
               it("chapa", 540, 720, 1.4, delay=1.4, texto="20:52", sub="última imagen")]},
    {"sigue": True, "lines": L("Era el único rincón de la celda que las cámaras no alcanzaban a ver."),
     "items": [it("etiqueta", 680, 960, 0.8, delay=0.8, texto="PUNTO CIEGO", fondo="#ef4444", rot=6)]},
    {"sigue": True, "quita": ["reo2"], "lines": L("Y ya no volvió a salir.", pausa=0.4),
     "cam": {"z": [1.0, 1.15], "f": [540, 1250]}},
    {"fondo": rayos("rojo"), "lines": L("Cuando los guardias entraron, encontraron el hueco."),
     "items": [it("persona", 230, 1560, 0.85, anim="left", cara="sorpresa", brazos="cabeza", **GUARDIA),
               it("icono", 700, 1100, 0.9, delay=1.2, anim="pop", tipo="exclamacion")]},
    {"sigue": True, "lines": L("Y debajo, un pozo de unos diez metros con escalera."),
     "items": [it("flecha", 700, 1350, 0.9, delay=0.4, anim="drop", rot=90, color="#ffd23f"),
               it("chapa", 700, 760, 1.4, delay=1.2, texto="10 M", sub="de profundidad")]},

    # ------------------------------------------------------------ la ingenieria del tunel
    {"fondo": TIERRA, "lines": L("Abajo empezaba un túnel de alrededor de un kilómetro y medio."),
     "items": [it("linea_tiempo", 540, 1250, 0.85, anim="fade", pasos=["CELDA", "TÚNEL", "CASA"], activo=0, ancho=620)],
     "dato": dato(1500, "METROS DE TÚNEL", suf=" M", delay=1.0)},
    {"sigue": True, "lines": L("Medía entre un metro y medio y un metro setenta de alto, y unos ochenta centímetros de ancho."),
     "items": [it("chapa", 290, 1500, 1.25, texto="1.7 M", sub="de alto"),
               it("chapa", 790, 1500, 1.25, delay=1.6, texto="80 CM", sub="de ancho")]},
    {"fondo": TIERRA, "lines": L("Tenía luz eléctrica a lo largo del recorrido y una tubería de PVC para ventilar.",
                                say={0: "Tenía luz eléctrica a lo largo del recorrido y una tubería de pe ve ce para ventilar."}),
     "items": [it("etiqueta", 300, 1000, 0.95, anim="pop", texto="LUZ", rot=-6),
               it("etiqueta", 760, 1250, 0.95, delay=1.8, texto="AIRE", fondo="#7dd3fc", rot=5),
               it("persona", 540, 1600, 0.75, delay=0.6, anim="up", cara="serio", **REO)]},
    {"fondo": rayos("menta"), "lines": L("Y lo más llamativo: una motocicleta adaptada para correr sobre rieles."),
     "items": [it("etiqueta", 540, 1150, 0.95, anim="pop", texto="MOTO SOBRE RIELES", rot=-4),
               it("flecha", 540, 1400, 1.2, delay=1.4, anim="left", largo=420)]},
    {"sigue": True, "lines": L("Según las autoridades, servía para sacar tierra y meter herramientas. Esa noche también sirvió para huir."),
     "items": [it("chapa", 540, 760, 1.3, delay=0.4, texto="TIERRA", sub="y herramientas")]},
    {"fondo": rayos("cielo"), "lines": L("El túnel terminaba en una casa en obra negra, al suroeste del penal, en la colonia Santa Juanita."),
     "items": [it("edificio", 540, 1560, 0.9, anim="crece", texto="OBRA NEGRA", pisos=2, ancho=560, color="#a8a29e", ventana="#57534e"),
               it("pin", 840, 1230, 0.6, delay=2.4, anim="drop", texto="STA. JUANITA")]},
    {"sigue": True, "lines": L("Ahí había tanques de oxígeno, combustible y un generador eléctrico."),
     "items": [it("chapa", 540, 700, 1.1, texto="OXÍGENO"),
               it("chapa", 540, 860, 1.1, delay=1.2, texto="GENERADOR")]},
    {"fondo": rayos("oro"), "lines": L("Expertos calculan que una obra así toma entre dieciocho meses y dos años."),
     "items": [it("reloj", 540, 1250, 1.2, anim="pop", hora=10)],
     "dato": dato(18, "MESES O MÁS", suf=" MESES", delay=1.2)},
    {"sigue": True, "lines": L("Él llevaba unos dieciséis meses preso, así que algunos creen que empezaron a cavar antes de que llegara."),
     "items": [it("etiqueta", 540, 1560, 0.85, delay=2.0, texto="SE DISCUTE", fondo="#ffffff", rot=5)]},
    {"fondo": rayos("gris"), "lines": L("¿Y cómo atinaron justo a la regadera? Según especialistas, tuvieron que conocer los planos del penal."),
     "items": [it("libro", 540, 1200, 1.1, anim="pop", abierto=True, texto="PLANOS"),
               it("icono", 860, 800, 0.8, delay=2.6, anim="pop", tipo="exclamacion")]},

    # ------------------------------------------------------------ las fallas
    {"fondo": {"tipo": "noche"}, "lines": L("Las fallas quedaron a la vista. Dieciocho empleados del penal fueron llevados a declarar."),
     "items": [it("multitud", 540, 1600, 1.0, anim="up", n=12, filas=2, escala=0.6, cara="preocupado", camisa="#334155"),
               it("chapa", 540, 760, 1.4, delay=2.2, texto="18", sub="empleados a declarar")]},
    {"sigue": True, "lines": L("Y el gobierno destituyó a tres altos funcionarios de prisiones, entre ellos el director del penal."),
     "items": [it("icono", 860, 1000, 0.85, delay=1.6, anim="pop", tipo="x")]},
    {"fondo": rayos("rojo"), "lines": L("Se instalaron retenes en las carreteras y se suspendieron los vuelos en el aeropuerto de Toluca."),
     "items": [it("avion", 540, 1150, 1.0, anim="left"),
               it("icono", 540, 1150, 0.9, delay=2.6, anim="pop", tipo="x")]},
    {"fondo": rayos("menta"), "lines": L("La Procuraduría ofreció sesenta millones de pesos de recompensa."),
     "items": [it("bolsa_dinero", 540, 1560, 1.1, anim="drop", texto="$")],
     "dato": dato(60, "PESOS DE RECOMPENSA", suf=" MILLONES", delay=1.2)},
    {"sigue": True, "lines": L("Unos tres millones ochocientos mil dólares."),
     "items": [it("chapa", 540, 1050, 1.3, texto="~3.8 MDD", sub="en dólares")]},

    # ------------------------------------------------------------ la recaptura
    {"fondo": rayos("azul"), "lines": L("La búsqueda duró ciento ochenta y dos días."),
     "items": [it("calendario", 540, 1250, 1.1, anim="pop", texto="182")],
     "dato": dato(182, "DÍAS PRÓFUGO", delay=0.8)},
    {"fondo": {"tipo": "noche"}, "lines": L("El 8 de enero de 2016, marinos entraron a una casa en Los Mochis, Sinaloa."),
     "items": [it("persona", 300, 1560, 0.85, anim="left", cara="serio", brazos="senala", **MARINO),
               it("persona", 520, 1560, 0.8, delay=0.3, anim="left", cara="serio", **MARINO),
               it("pin", 840, 1150, 0.8, delay=1.6, anim="drop", texto="LOS MOCHIS")]},
    {"sigue": True, "lines": L("Hubo un enfrentamiento: murieron cinco personas y un marino resultó herido."),
     "items": [it("chapa", 540, 760, 1.4, texto="5 MUERTOS")]},
    {"fondo": rayos("gris"), "lines": L("Y otra vez, un túnel: escondido detrás de un espejo en un clóset, conectaba con el drenaje."),
     "items": [it("flecha", 540, 1150, 1.1, anim="drop", rot=90),
               it("etiqueta", 540, 1450, 0.9, delay=1.8, texto="DRENAJE", fondo="#94a3b8", rot=-4)]},
    {"sigue": True, "lines": L("Salió por una alcantarilla, robó un auto y la Policía Federal lo detuvo en una carretera."),
     "items": [it("persona", 830, 1560, 0.8, delay=1.6, anim="right", flip=True, cara="triste", brazos="arriba", **REO)]},

    # ------------------------------------------------------------ datos curiosos
    {"fondo": rayos("oro"), "lines": L("Y ahora, cosas que casi nadie sabe."),
     "items": [it("etiqueta", 540, 1150, 1.3, anim="pop", texto="¿SABÍAS?", fondo="#f0c448", rot=-4)],
     "min_dur": 2.0},
    {"fondo": rayos("durazno"), "lines": L("Uno. En el penal llevaba un brazalete electrónico."),
     "items": [it("persona", 540, 1560, 0.95, anim="up", cara="serio", **REO),
               it("chapa", 540, 760, 1.3, delay=1.4, id="braz", texto="BRAZALETE")]},
    {"sigue": True, "quita": ["braz"], "lines": L("Pero según el gobierno no tenía GPS: fuera de la cárcel no se le podía rastrear.",
                               say={0: "Pero según el gobierno no tenía ge pe ese: fuera de la cárcel no se le podía rastrear."}),
     "items": [it("etiqueta", 540, 760, 1.0, delay=1.2, texto="SIN GPS", fondo="#ef4444", rot=-5)]},
    {"fondo": rayos("cielo"), "lines": L("Dos. La luz y el aire del túnel dependían de un generador que, según el Christian Science Monitor, era del tamaño de un auto pequeño."),
     "items": [it("bateria", 540, 1200, 1.1, anim="pop", nivel=0.9, color="#facc15"),
               it("etiqueta", 540, 760, 0.9, delay=3.0, texto="GENERADOR", rot=4)]},
    {"fondo": rayos("menta"), "lines": L("Tres. Nadie cobró los sesenta millones."),
     "items": [it("bolsa_dinero", 540, 1560, 1.0, anim="drop", texto="$"),
               it("icono", 800, 1050, 0.85, delay=1.2, anim="pop", tipo="x")]},
    {"sigue": True, "lines": L("Según la Procuraduría, la llamada que lo ubicó era para reportar el robo de un auto, no para denunciarlo."),
     "items": [it("chapa", 540, 760, 1.25, delay=1.6, texto="AUTO ROBADO")]},
    {"fondo": rayos("lila"), "lines": L("Y cuatro. Fue extraditado a Estados Unidos el 19 de enero de 2017."),
     "items": [it("avion", 540, 1100, 0.9, anim="left"),
               it("calendario", 540, 760, 0.6, delay=1.6, anim="pop", texto="2017")]},
    {"sigue": True, "lines": L("Dieciséis años exactos después de su fuga de Puente Grande."),
     "items": [it("linea_tiempo", 540, 1400, 1.0, anim="fade", pasos=["2001", "2017"], activo=1, ancho=460)]},

    # ------------------------------------------------------------ que paso despues
    {"fondo": rayos("azul"), "lines": L("Lo juzgaron en Nueva York."),
     "items": [it("pin", 540, 1150, 0.9, anim="drop", texto="NUEVA YORK")]},
    {"fondo": {"tipo": "oficina"}, "lines": L("El 12 de febrero de 2019, un jurado lo declaró culpable de diez cargos."),
     "items": [it("persona", 300, 1640, 0.9, anim="left", cara="serio", brazos="senala", **FISCAL),
               it("persona", 780, 1640, 0.9, delay=0.6, anim="right", flip=True, cara="triste", **REO),
               it("chapa", 540, 760, 1.4, delay=2.6, texto="10 CARGOS")]},
    {"sigue": True, "lines": L("Entre ellos, narcotráfico, uso de armas y lavado de dinero.")},
    {"fondo": {"tipo": "noche"}, "lines": L("El 17 de julio de 2019 recibió cadena perpetua más treinta años."),
     "items": [it("celda", 540, 1560, 1.15, anim="drop"),
               it("chapa", 540, 760, 1.35, delay=1.6, texto="PERPETUA + 30", sub="17 de julio de 2019")],
     "cam": {"z": [1.0, 1.08], "f": [540, 1200]}},
    {"fondo": rayos("rojo"), "lines": L("Y el juez ordenó decomisarle doce mil seiscientos millones de dólares."),
     "items": [it("billetes", 540, 1300, 1.1, anim="drop", n=4)],
     "dato": dato(12600, "DÓLARES A DECOMISAR", pre="$", suf=" MILLONES", delay=1.0)},
    {"fondo": rayos("gris"), "lines": L("Hoy está en la prisión ADX Florence, en Colorado, donde los reos pasan unas veintidós horas al día en su celda.",
                                       say={0: "Hoy está en la prisión A D X Flórens, en Colorado, donde los reos pasan unas veintidós horas al día en su celda."}),
     "items": [it("edificio", 540, 1560, 1.05, anim="crece", texto="ADX FLORENCE", pisos=3, ancho=720, color="#cbd5e1", ventana="#334155"),
               it("chapa", 540, 760, 1.35, delay=2.6, texto="22 H", sub="al día en la celda")]},
    {"fondo": rayos("gris"), "lines": L("La violencia de su organización dejó miles de muertos en México."),
     "items": [it("multitud", 540, 1600, 1.0, anim="up", n=12, filas=2, escala=0.6, cara="triste"),
               it("etiqueta", 540, 780, 0.85, delay=2.0, texto="MILES DE MUERTOS", fondo="#ffffff", rot=-3)]},
    {"sigue": True, "lines": L("Y la fuga expuso las fallas del sistema penitenciario."),
     "items": [it("icono", 860, 1000, 0.8, delay=1.0, anim="pop", tipo="exclamacion")]},

    # ------------------------------------------------------------ cierre
    {"fondo": {"tipo": "noche"}, "lines": L("Cámaras, guardias, un brazalete y muros de concreto. Y bastó un punto ciego de cincuenta centímetros."),
     "items": [it("celda", 540, 1560, 1.15, anim="fade"),
               it("chapa", 540, 1400, 1.45, delay=3.0, texto="50 CM")],
     "cam": {"z": [1.0, 1.12], "f": [540, 1350]}},
    {"fondo": rayos("oro"), "lines": L("¿Qué falla te parece más grave: el punto ciego, el brazalete sin GPS o que alguien conociera los planos? Te leo en los comentarios.",
                                      say={0: "¿Qué falla te parece más grave: el punto ciego, el brazalete sin ge pe ese o que alguien conociera los planos? Te leo en los comentarios."}),
     "items": [it("chapa", 540, 1100, 1.2, delay=0.8, texto="PUNTO CIEGO"),
               it("chapa", 540, 1270, 1.2, delay=2.6, texto="SIN GPS"),
               it("chapa", 540, 1440, 1.2, delay=3.8, texto="PLANOS"),
               it("etiqueta", 540, 760, 1.0, delay=5.0, texto="¿TÚ QUÉ OPINAS?", rot=-5)]},
]

guion = {
    "motor": 4,
    "canal": "historias",
    "title": "Un túnel de 1.5 km hasta una regadera: así fue la fuga de El Chapo del Altiplano",
    "description": ("El 11 de julio de 2015, Joaquín Guzmán escapó del penal del Altiplano por un hueco de 50 x 50 cm en la regadera "
                    "conectado a un túnel de unos 1.5 km con luz, ventilación y una moto sobre rieles. Cómo se construyó, qué fallas "
                    "de seguridad lo permitieron, su recaptura en Los Mochis y su condena a cadena perpetua en Estados Unidos.\n"
                    "Fuentes: Departamento de Justicia de EE.UU. (sentencia, 17/07/2019); PBS Frontline; CBS News / AP; NPR; Al Jazeera; "
                    "El Financiero; Excélsior; Zeta Tijuana; Expansión; Christian Science Monitor; Xataka; The Mob Museum."),
    "hashtags": ["#DatoBomba", "#ElChapo", "#Altiplano", "#Mexico", "#historiasreales"],
    "source_url": "https://www.justice.gov/opa/pr/joaquin-el-chapo-guzman-sinaloa-cartel-leader-sentenced-life-prison-plus-30-years",
    "scenes": escenas,
}

with open(os.path.join(AQUI, "hsf_chapo.json"), "w", encoding="utf-8") as f:
    json.dump(guion, f, ensure_ascii=False, indent=1)
palabras = sum(len(ln["text"].split()) for sc in escenas for ln in sc.get("lines", []))
print("escenas:", len(escenas), "palabras:", palabras, "duracion estimada (s):", round(palabras / 2.55),
      "titulo:", len(guion["title"]))
