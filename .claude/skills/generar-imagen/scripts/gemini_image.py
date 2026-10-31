#!/usr/bin/env python3
"""
Genera o edita imagenes con Google Gemini "Nano Banana" (Gemini Flash Image),
usando la API gratuita de Google AI Studio.

Uso:

  # Crear una imagen desde texto
  python3 gemini_image.py generate \
      --prompt "un gato astronauta en acuarela" \
      --out salida.png

  # Editar / modificar una o varias imagenes existentes
  python3 gemini_image.py edit \
      --prompt "ponle un sombrero rojo y fondo de atardecer" \
      --image entrada.png \
      --out salida.png

La clave se lee de la variable de entorno GEMINI_API_KEY (o GOOGLE_API_KEY).
Consiguela GRATIS (sin tarjeta) en https://aistudio.google.com/apikey
No requiere paquetes externos: solo la libreria estandar de Python 3.
"""

import argparse
import base64
import json
import mimetypes
import os
import ssl
import sys
import urllib.request

API_BASE = os.environ.get(
    "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
).rstrip("/")
# gemini-2.5-flash-image = "Nano Banana" (GA, con cuota gratuita).
# Se puede cambiar con GEMINI_IMAGE_MODEL (p. ej. un modelo Pro mas nuevo).
MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")


def _ssl_context():
    ca = (
        os.environ.get("GEMINI_CA_BUNDLE")
        or os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
    )
    if ca and os.path.exists(ca):
        return ssl.create_default_context(cafile=ca)
    return ssl.create_default_context()


def _api_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit(
            "ERROR: falta la variable de entorno GEMINI_API_KEY.\n"
            "Consiguela GRATIS (sin tarjeta) en https://aistudio.google.com/apikey\n"
            "y expórtala:\n"
            "  export GEMINI_API_KEY='AIza...'"
        )
    return key


def _post(parts):
    url = f"{API_BASE}/models/{MODEL}:generateContent"
    body = json.dumps({"contents": [{"parts": parts}]}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": _api_key(),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_ssl_context(), timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        sys.exit(f"ERROR HTTP {e.code} desde Gemini:\n{body[:1200]}")


def _save_image(payload, out_path):
    candidates = payload.get("candidates") or []
    if not candidates:
        sys.exit("ERROR: la API no devolvió candidatos.\n" + json.dumps(payload)[:1000])
    parts = (candidates[0].get("content") or {}).get("parts") or []
    text_notes = []
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
            ext = mimetypes.guess_extension(mime) or ".png"
            root, cur = os.path.splitext(out_path)
            if not cur:
                out_path = root + ext
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(inline["data"]))
            print(f"OK: imagen guardada en {out_path}")
            return
        if part.get("text"):
            text_notes.append(part["text"])
    # No vino imagen: el modelo respondio solo texto (p. ej. rechazo de seguridad).
    msg = " ".join(text_notes).strip() or json.dumps(payload)[:1000]
    sys.exit("ERROR: el modelo no devolvió una imagen. Respondió:\n" + msg)


def generate(args):
    _save_image(_post([{"text": args.prompt}]), args.out)


def edit(args):
    parts = [{"text": args.prompt}]
    for p in args.image:
        if not os.path.exists(p):
            sys.exit(f"ERROR: no existe la imagen de entrada: {p}")
        mime = mimetypes.guess_type(p)[0] or "image/png"
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        parts.append({"inline_data": {"mime_type": mime, "data": data}})
    _save_image(_post(parts), args.out)


def main():
    parser = argparse.ArgumentParser(
        description="Generar/editar imagenes con Gemini (Nano Banana)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Crear una imagen desde un texto")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", required=True, help="Ruta del archivo de salida (.png)")
    g.set_defaults(func=generate)

    e = sub.add_parser("edit", help="Editar una o varias imagenes existentes")
    e.add_argument("--prompt", required=True, help="Instruccion de edicion")
    e.add_argument("--image", required=True, action="append",
                   help="Imagen de entrada (repetible para combinar varias)")
    e.add_argument("--out", required=True, help="Ruta del archivo de salida (.png)")
    e.set_defaults(func=edit)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
