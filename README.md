# iasinhumo-engine

Motor de render de Shorts verticales (1080x1920, 30 fps) del canal IA SinHumo.

- Voz offline con sherpa-onnx (voces Piper en español).
- Escenas animadas (hook, title, bullets, chat, versus, stat, cta), mascota Bit y subtítulos palabra por palabra.

## Uso

```bash
pip install "sherpa-onnx<1.13" soundfile numpy pillow
python3 engine.py ejemplos/p1_synthid.json salida.mp4 --voices /ruta/a/voces
```

Requiere ffmpeg con libass y la fuente Poppins.
