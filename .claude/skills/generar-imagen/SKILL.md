---
name: generar-imagen
description: >-
  Crea o edita imágenes con IA usando Google Gemini "Nano Banana" (Gemini Flash
  Image), de forma gratuita. Úsala siempre que el usuario pida crear, generar,
  dibujar, diseñar una imagen desde cero, o editar, modificar, retocar, cambiar,
  combinar o quitar el fondo de una imagen existente. Palabras clave:
  "crea una imagen", "genera una imagen", "edita esta foto", "hazme un logo",
  "modifica la imagen", "quítale el fondo", "ponle...".
---

# Generar y editar imágenes con IA (Gemini "Nano Banana") — GRATIS

Esta skill crea y edita imágenes usando **Google Gemini Flash Image**
(apodado "Nano Banana"), a través de la API gratuita de Google AI Studio. Es una
alternativa sin coste a OpenAI/ChatGPT, con calidad comparable y especialmente
buena **editando** imágenes. El resultado se guarda en un archivo y se le entrega
al usuario.

## Requisito previo (gratis, sin tarjeta)

Debe existir la variable de entorno `GEMINI_API_KEY` con una clave de Google AI
Studio. Es **gratuita y no pide tarjeta**, solo una cuenta de Google. Se saca en
https://aistudio.google.com/apikey

Comprobar:

```bash
test -n "$GEMINI_API_KEY" && echo "API key OK" || echo "Falta GEMINI_API_KEY"
```

Si falta, pídele al usuario que la configure (ver "Configurar la API key" al
final) y no continúes sin ella.

> Nota: el nivel gratuito tiene un límite diario de imágenes (varía con el
> tiempo). Si aparece un error HTTP 429, es que se agotó la cuota del día.

## Cómo usarla

El script está en `scripts/gemini_image.py` (ruta relativa a esta skill) y no
necesita instalar nada: solo la librería estándar de Python 3.

### Crear una imagen desde texto

```bash
python3 <ruta-skill>/scripts/gemini_image.py generate \
    --prompt "DESCRIPCION DETALLADA DE LA IMAGEN" \
    --out /ruta/de/salida.png
```

### Editar / modificar una imagen existente

```bash
python3 <ruta-skill>/scripts/gemini_image.py edit \
    --prompt "QUE CAMBIO HACER (en lenguaje natural)" \
    --image /ruta/entrada.png \
    --out /ruta/salida.png
```

- Para **combinar varias imágenes** (p. ej. "pon este logo en esta foto"),
  repite `--image` por cada archivo.
- La edición entiende instrucciones en lenguaje natural: "quítale el fondo",
  "cámbialo a estilo cómic", "ponle un sombrero", "haz que sea de noche", etc.

## Flujo recomendado al atender al usuario

1. Confirma que `GEMINI_API_KEY` está definida.
2. Convierte lo que pide el usuario en un `--prompt` claro y descriptivo (añade
   estilo, encuadre, colores, iluminación… si ayuda al resultado).
3. Guarda la salida en el directorio de trabajo o en el scratchpad con un nombre
   descriptivo (ej. `logo-cafeteria.png`).
4. Entrega el archivo al usuario con la herramienta de enviar archivos y escribe
   la ruta absoluta completa.
5. Si el usuario quiere ajustes, usa `edit` sobre la imagen ya generada para
   iterar.

## Modelo

Por defecto usa `gemini-2.5-flash-image` (Nano Banana, con cuota gratuita). Se
puede cambiar a otro modelo de imagen con la variable `GEMINI_IMAGE_MODEL`
(p. ej. una versión Pro más nueva, si tu cuenta tiene acceso gratuito a ella).

## Notas y errores comunes

- HTTP 400 = petición mal formada o modelo sin acceso; HTTP 403 = clave sin
  permiso para ese modelo; HTTP 429 = se agotó la cuota diaria gratuita. El
  script muestra el mensaje exacto de Google para diagnosticar.
- Si el modelo responde solo con texto en vez de imagen (p. ej. rechaza el
  contenido por seguridad), el script lo informa en lugar de guardar un archivo.

## Configurar la API key

En Linux/macOS, de forma persistente:

```bash
echo 'export GEMINI_API_KEY="AIza_TU_CLAVE_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

O solo para la sesión actual:

```bash
export GEMINI_API_KEY="AIza_TU_CLAVE_AQUI"
```
