---
name: generar-imagen
description: >-
  Crea o edita imágenes usando la API de imágenes de OpenAI (modelo gpt-image-1,
  el mismo motor que usa ChatGPT para generar imágenes). Úsala siempre que el
  usuario pida crear, generar, dibujar, diseñar una imagen desde cero, o editar,
  modificar, retocar, cambiar o combinar una imagen existente. Palabras clave:
  "crea una imagen", "genera una imagen", "edita esta foto", "hazme un logo",
  "modifica la imagen", "quítale el fondo", "ponle...".
---

# Generar y editar imágenes con OpenAI (gpt-image-1)

Esta skill delega la creación y edición de imágenes a la API de imágenes de
OpenAI, que es el mismo modelo de imagen que usa ChatGPT. El resultado se guarda
en un archivo y se le entrega al usuario.

## Requisito previo

Debe existir la variable de entorno `OPENAI_API_KEY` con una clave válida de
OpenAI (con billing activo en https://platform.openai.com). Si no está definida,
el script lo avisa. Comprobar con:

```bash
test -n "$OPENAI_API_KEY" && echo "API key OK" || echo "Falta OPENAI_API_KEY"
```

Si falta, pídele al usuario que la configure (ver sección "Configurar la API key"
al final) y no intentes continuar sin ella.

## Cómo usarla

El script está en `scripts/openai_image.py` (ruta relativa a esta skill) y no
necesita instalar nada: usa solo la librería estándar de Python 3.

### Crear una imagen desde texto

```bash
python3 <ruta-skill>/scripts/openai_image.py generate \
    --prompt "DESCRIPCION DETALLADA DE LA IMAGEN" \
    --out /ruta/de/salida.png \
    --size 1024x1024
```

### Editar / modificar una imagen existente

```bash
python3 <ruta-skill>/scripts/openai_image.py edit \
    --prompt "QUE CAMBIO HACER" \
    --image /ruta/entrada.png \
    --out /ruta/salida.png
```

- Para combinar varias imágenes, repite `--image` por cada archivo.
- Para editar solo una zona, pasa una máscara PNG con `--mask` (las zonas
  **transparentes** de la máscara son las que se editan).

### Opciones

- `--size`: `1024x1024` (cuadrada), `1536x1024` (horizontal),
  `1024x1536` (vertical) o `auto`.
- `--quality`: `low`, `medium`, `high` o `auto` (más calidad = más costo/tiempo).

## Flujo recomendado al atender al usuario

1. Confirma que `OPENAI_API_KEY` está definida.
2. Convierte lo que pide el usuario en un `--prompt` claro y descriptivo (añade
   estilo, encuadre, colores, etc. si ayuda al resultado).
3. Guarda la salida en el directorio de trabajo o en el scratchpad con un nombre
   descriptivo (ej. `logo-cafeteria.png`).
4. Entrega el archivo al usuario con la herramienta de enviar archivos y escribe
   la ruta absoluta completa.
5. Si el usuario quiere ajustes, usa `edit` sobre la imagen ya generada.

## Notas

- `gpt-image-1` devuelve la imagen en base64; el script la decodifica y la
  guarda como PNG automáticamente.
- Errores comunes: HTTP 401 = API key inválida; HTTP 429 = sin saldo o límite de
  tasa; el script muestra el mensaje exacto de OpenAI para diagnosticar.

## Configurar la API key

En Linux/macOS, de forma persistente:

```bash
echo 'export OPENAI_API_KEY="sk-TU_CLAVE_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

O solo para la sesión actual:

```bash
export OPENAI_API_KEY="sk-TU_CLAVE_AQUI"
```
