# iasinhumo-engine

Motor de render v2 (revision 3) de Shorts verticales (1080x1920, 30 fps) del canal IA SinHumo.

- Estilo explainer ilustrado: cada escena trae capas SVG que aparecen animadas al ritmo de la voz.
- Voces: Edge (neuronales de Microsoft, por defecto), ElevenLabs (con API key) o Kokoro offline.
- Subtitulos palabra por palabra sincronizados con la voz.
- Render automatico en GitHub Actions (`.github/workflows/render.yml`), resultados en el release `cola`.

## Uso local

```bash
pip install edge-tts numpy pillow cairosvg
python3 engine.py ejemplos/v2_estafas.json salida.mp4
```

Requiere ffmpeg y la fuente Poppins en /usr/share/fonts/truetype/google-fonts.

## Variables del workflow (Settings > Secrets and variables > Actions)

- Variable `SHEET_CSV_URL`: URL CSV de la bitacora.
- Variable `ISH_VOICE` (opcional): voz de Edge, por ejemplo `es-MX-JorgeNeural`.
- Variable `ISH_TTS` (opcional): `edge` o `elevenlabs`.
- Secreto `ELEVENLABS_API_KEY` y variable `ELEVENLABS_VOICE_ID` (solo si se usa ElevenLabs).
