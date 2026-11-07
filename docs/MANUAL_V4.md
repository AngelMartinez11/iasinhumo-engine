# Manual del motor v4 (guionistas del canal Dato Bomba)

Desde el 6 de noviembre de 2026 los dos formatos se publican en UN solo canal: **Dato Bomba** (YouTube y TikTok).
- `canal: "iasinhumo"` = videos de TECNOLOGIA (2 al dia, 07:30 y 17:30).
- `canal: "historias"` = videos GENERALES de formato largo (2 al dia, 12:30 y 20:30).
Los dos usan la marca DATO BOMBA, la voz `it-IT-GiuseppeMultilingualNeural` y no usan tarjetas de capitulo.

El motor v4 (`engine4.py`) arma cada escena con piezas reutilizables de `piezas.py`.
El guion NO dibuja SVG: solo nombra piezas, posiciones y tiempos. Eso ahorra tokens
y hace que todos los videos tengan el mismo estilo.

## 1. Estructura del guion

```json
{
  "motor": 4,
  "canal": "historias",            // o "iasinhumo" (lee canales/<canal>.json)
  "title": "...", "description": "...", "hashtags": ["#..."], "source_url": "https://...",
  "scenes": [ { ...escena... } ]
}
```

### Escena

| Campo | Que hace |
|---|---|
| `lines` | Lista de `{"text": "...", "say": "...", "pausa": 0.3}`. `text` es el subtitulo; `say` (opcional) es como debe pronunciarse; `pausa` agrega silencio despues. |
| `fondo` | `{"tipo":"rayos","paleta":"lila"}` (paletas: lila, durazno, azul, menta, rojo, oro, gris, cielo), `{"tipo":"split","c":["#cfe0ff","#ffd6d6"]}`, `{"tipo":"noche"}`, `{"tipo":"oficina"}`, `{"tipo":"liso","c":"#e4e4ea"}`. Opcional `"suelo":"no"` o un color. |
| `items` | Piezas que aparecen (ver seccion 3). |
| `sigue` | `true` = continua la escena anterior: mismo fondo, mismas piezas ya visibles y camara donde quedo. Asi la escena se va construyendo. |
| `quita` | Lista de `id` de piezas que se van (se desvanecen) al empezar esta escena. Solo con `sigue`. |
| `dato` | Tarjeta negra y dorada con numero que cuenta: `{"num": 9094, "pre": "$", "suf": " MILLONES", "texto": "TIENDAS EN 2004", "y": 590, "at": 0, "delay": 1.5, "cuenta": true}`. |
| `capitulo` | Tarjeta de capitulo a pantalla completa: `{"t": "LA REUNIÓN", "n": 2}` con `"min_dur": 1.7`. |
| `cam` | Camara: `{"z": [1.0, 1.12], "f": [540, 1100], "x": [0, 0], "y": [0, 0]}`. `z` es el zoom inicial y final (se multiplica por el zoom base del canal), `f` el punto que queda fijo en pantalla, `x`/`y` paneo en pixeles. |
| `min_dur` | Duracion minima de la escena en segundos. |

### Pieza (item)

```json
{"p": "persona", "x": 540, "y": 1560, "s": 0.85, "at": 0, "delay": 0.4, "anim": "right", "id": "ceo",
 "a": {"ropa": "traje", "cara": "risa", "brazos": "cruzados"}}
```

- La voz sale de `canales/<canal>.json` -> `tts` (Historias Sin Filtro: `it-IT-GiuseppeMultilingualNeural`; IA SinHumo: `es-ES-AlvaroNeural`). No pongas `tts` en el guion salvo que se pida otra voz.
- `x`, `y`: punto de anclaje en el lienzo de 1080 x 1920. Personas, tiendas, edificios, graficas,
  bolsas y lapidas se anclan en los PIES (abajo al centro); lo demas en su CENTRO.
- `s`: escala. `at`: indice de la linea con la que aparece. `delay`: segundos extra. `t`: segundo exacto dentro de la escena (en vez de `at`).
- `anim`: `up` (default), `pop` (default de etiquetas e iconos), `left`, `right`, `fade`, `drop` (cae rebotando), `crece` (sube desde el suelo: edificios, tiendas, graficas).
- `flip`: `true` voltea la pieza.

## 2. Zonas del lienzo (1080 x 1920)

- 0 - 240: marca del canal y barra de progreso. No poner nada.
- 250 - 510: banda del subtitulo. No poner nada importante.
- 560 - 900: zona alta: etiquetas, rotulos de nombre, tarjetas de dato, iconos.
- 900 - 1560: zona principal: personajes y objetos grandes.
- 1560: linea del suelo (los pies van aqui). Debajo solo multitudes de primer plano.
- El zoom base del canal (1.12) recorta un poco el suelo: usa piezas grandes (personas s 0.8 a 1.2).

## 3. Catalogo de piezas (`p` y sus argumentos `a`)

| Pieza | Argumentos |
|---|---|
| `persona` | `camisa`, `pelo`, `piel`, `pantalon`, `cara` (serio, feliz, sorpresa, triste, enojado, risa, preocupado), `brazos` (abajo, arriba, cabeza, senala, cruzados, telefono, saluda, objeto), `ropa` (camiseta, traje, bata), `corbata`, `peinado` (corto, largo, calvo, canoso, gorra), `lentes`, `sandalias` |
| `multitud` | `n`, `filas`, `semilla`, `ancho`, `escala`, `cara`, `camisa` |
| `tienda` | `texto`, `letrero`, `letra`, `pared`, `ancho` |
| `edificio` | `texto`, `pisos`, `color`, `ancho`, `ventana`, `letrero` |
| `mesa` | `ancho` |
| `sobre` | `color`, `texto` |
| `vhs` | `etiqueta`, `color` |
| `disco`, `globo`, `robot` | (sin argumentos; `robot` es la mascota de IA SinHumo) |
| `billetes` | `n` |
| `bolsa_dinero` | `texto` |
| `reloj` | `hora` |
| `calendario` | `texto`, `color` |
| `telefono` | `texto`, `color`, `play` |
| `tv` | `play`, `color`, `texto` |
| `laptop` | `texto`, `color` |
| `avion` | `color` |
| `grafica` | `tipo` (sube, baja), `color`, `barras` |
| `lapida` | `texto`, `sub` |
| `pin` | `texto`, `color` |
| `icono` | `tipo` (x, check, pregunta, exclamacion), `color` |
| `flecha` | `color`, `largo`, `rot` |
| `linea_tiempo` | `pasos` (lista), `activo` (indice) |
| `etiqueta` | `texto`, `fondo`, `tinta`, `size`, `rot` (etiqueta amarilla inclinada) |
| `nombre` | `texto`, `sub` (rotulo de persona: "John Antioco / director de Blockbuster") |
| `chapa` | `texto`, `sub` (placa negra y dorada para datos cortos: "11 KG", "1981"; usa `s` 1.2 a 1.5) |
| `pc_escritorio` | `texto`, `pantalla`, `tinta`, `torre` (computadora de escritorio de los 80) |
| `maletin_pc` | `texto`, `color`, `abierto` (computadora "portatil" de maletin: Osborne, IBM 5100) |
| `clamshell` | `abierto`, `color`, `tinta`, `texto` (laptop de bisagra de los 80) |
| `laptop_moderna` | `color`, `pantalla`, `texto` |
| `transbordador` | `color` (nave espacial de lado) |
| `bateria` | `nivel` (0 a 1), `color` |
| `bascula` | `texto` (bascula con pantalla; pon el objeto pesado encima, unos 90 px mas arriba) |
| `libro` | `texto`, `color`, `abierto` (libro, cuaderno, revista abierta) |
| `nino` | igual que `persona` pero pequeno |
| `camara`, `rollo`, `celda`, `cama`, `isla`, `balsa`, `cuchara`, `olas` | ver `piezas.py` |
| `texto` | `texto`, `size`, `color`, `contorno` |

Si una historia necesita un objeto que no existe, usa el mas parecido o una `etiqueta`, y anotalo en
la columna notas para que se agregue a la biblioteca.

## 4. Reglas de estilo (lo que hace que atrape)

1. Algo nuevo en pantalla cada 2 a 3 segundos (una pieza, un dato o un cambio de escena).
2. Escenas que se construyen: usa `sigue` + `quita` en vez de cortar a cada frase.
3. Personajes con emocion en casi todas las escenas; protagonista reconocible por ropa y color durante todo el video.
4. Un dato fuerte por bloque en tarjeta `dato` (numeros verificados).
5. Cambia la paleta del fondo cuando cambia el tono; `noche` para momentos dramaticos.
6. Camara: zoom lento hacia la cara en momentos clave; alejarse para revelar.
7. Personas reales: personajes genericos con su `nombre` en rotulo. Nunca intentar parecido fisico ni poner frases que no dijeron.

## 5. Estructura por canal

**Historias Sin Filtro** (1 video al dia, FORMATO LARGO de 3 a 5 minutos, 600 a 760 palabras, 50 a 70 escenas, musica de intriga).
Referencia: el video de D. B. Cooper de Empty (@emptymind63). No basta con contar la historia: hay que INFORMAR.
1. Gancho (2 a 4 escenas): el contraste o dato mas fuerte ("hoy pesa un kilo; la primera pesaba 25") y una pregunta.
2. La historia en 3 a 5 bloques, en orden (SIN tarjetas de capitulo: el canal tiene `"capitulos": false` y el motor las quita; los bloques se marcan con cambio de fondo), con fechas, lugares, cifras y nombres concretos en casi cada escena.
   Explica COMO funcionaba la cosa (la estructura del avion, por que la pantalla era chica, que tenia adentro).
3. Un bloque de datos curiosos (se abre con una frase como "Y ahora, cosas que casi nadie sabe") con 3 o 4 curiosidades verificadas y numeradas ("Uno...", "Dos...").
4. "Que paso despues": consecuencias, lo que se descubrio anos despues, el estado actual.
5. Cierre: vuelve al contraste del gancho y termina con una pregunta personal para comentarios.
Reglas de informacion: cada cifra con fuente seria (minimo dos para datos clave); si algo se discute, dilo ("segun X", "se discute").
Datos cortos en `chapa`, datos grandes en `dato`. Usa `say` para nombres en ingles (Osborne -> "Osborn").
Temas: caidas y errores de empresas, inventos y su historia, desastres reales, rescates, misterios con fuentes, robos,
megaproyectos, politica actual explicada de forma neutral. Ejemplos de referencia: `ejemplos/hsf_laptop.py` (formato largo) y `ejemplos/hsf_blockbuster.py`.

**IA SinHumo** (2 al dia, 40 a 75 s, musica alegre): mismo motor y estilo; mascota `robot` como guia;
un solo tema de IA por video con dato verificado.

## 6. Version Short para YouTube (generales)

YouTube solo toma como Short un video vertical de 3 minutos o menos. Un general largo (3.5-5 min)
sube como video normal, asi que cada general genera tambien una version corta automatica:

- En las escenas que sobran para el Short se agrega `"corto": false` (se omiten en la version corta).
- Una escena puede traer `"lines_corto": [...]` para decir lo mismo en menos lineas dentro del Short.
- Opcional: `"title_corto"` con un titulo distinto para el Short.
- Meta: la version corta debe durar entre 120 y 170 s (nunca mas de 178 s). Debe conservar el gancho,
  el giro principal y el cierre; se recortan los bloques de contexto y curiosidades.
- El render produce `<id>.mp4` (largo) y `<id>_short.mp4` (Short) con su `_publicacion.txt`.
  Si el Short pasa de 178 s, el archivo de publicacion trae un AVISO.
