#!/usr/bin/env python3
"""
Genera o edita imagenes usando la API de imagenes de OpenAI (modelo gpt-image-1,
el mismo motor de imagenes que usa ChatGPT).

Uso:

  # Crear una imagen desde texto
  python openai_image.py generate \
      --prompt "un gato astronauta en acuarela" \
      --out salida.png \
      --size 1024x1024

  # Editar una o varias imagenes existentes segun una instruccion
  python openai_image.py edit \
      --prompt "ponle un sombrero rojo" \
      --image entrada.png \
      --out salida.png

La API key se lee de la variable de entorno OPENAI_API_KEY.
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
import uuid

API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")


def _ssl_context():
    """Contexto SSL que respeta un CA bundle propio si el entorno lo define
    (p. ej. cuando se corre detras de un proxy corporativo)."""
    ca = (
        os.environ.get("OPENAI_CA_BUNDLE")
        or os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
    )
    if ca and os.path.exists(ca):
        return ssl.create_default_context(cafile=ca)
    return ssl.create_default_context()


def _api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit(
            "ERROR: falta la variable de entorno OPENAI_API_KEY.\n"
            "Consiguela en https://platform.openai.com/api-keys y expórtala:\n"
            "  export OPENAI_API_KEY='sk-...'"
        )
    return key


def _save_result(payload, out_path):
    data = payload.get("data")
    if not data:
        sys.exit("ERROR: la API no devolvió ninguna imagen.\n" + json.dumps(payload)[:800])
    b64 = data[0].get("b64_json")
    if not b64:
        sys.exit("ERROR: la respuesta no trae imagen en base64.\n" + json.dumps(payload)[:800])
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"OK: imagen guardada en {out_path}")


def _handle_http_error(e):
    body = ""
    try:
        body = e.read().decode("utf-8", "replace")
    except Exception:
        pass
    sys.exit(f"ERROR HTTP {e.code} desde OpenAI:\n{body[:1000]}")


def generate(args):
    url = f"{API_BASE}/images/generations"
    body = {
        "model": MODEL,
        "prompt": args.prompt,
        "n": 1,
        "size": args.size,
    }
    if args.quality:
        body["quality"] = args.quality
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_ssl_context(), timeout=300) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        _handle_http_error(e)
    _save_result(payload, args.out)


def _multipart(fields, files):
    """Construye un cuerpo multipart/form-data. files = [(campo, ruta)]."""
    boundary = "----openaiimg" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields.items():
        out += f"--{boundary}\r\n".encode()
        out += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        out += f"{value}\r\n".encode()
    for name, path in files:
        fname = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            content = f.read()
        out += f"--{boundary}\r\n".encode()
        out += (
            f'Content-Disposition: form-data; name="{name}"; filename="{fname}"\r\n'
        ).encode()
        out += f"Content-Type: {ctype}\r\n\r\n".encode()
        out += content
        out += b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), boundary


def edit(args):
    url = f"{API_BASE}/images/edits"
    for p in args.image:
        if not os.path.exists(p):
            sys.exit(f"ERROR: no existe la imagen de entrada: {p}")
    fields = {"model": MODEL, "prompt": args.prompt, "size": args.size, "n": "1"}
    if args.quality:
        fields["quality"] = args.quality
    # El campo se llama "image[]" cuando se mandan varias imagenes.
    field = "image[]" if len(args.image) > 1 else "image"
    files = [(field, p) for p in args.image]
    if args.mask:
        files.append(("mask", args.mask))
    body, boundary = _multipart(fields, files)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_ssl_context(), timeout=300) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        _handle_http_error(e)
    _save_result(payload, args.out)


def main():
    parser = argparse.ArgumentParser(description="Generar/editar imagenes con OpenAI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Crear una imagen desde un texto")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", required=True, help="Ruta del archivo de salida (.png)")
    g.add_argument("--size", default="1024x1024",
                   help="1024x1024 | 1536x1024 | 1024x1536 | auto")
    g.add_argument("--quality", default=None, help="low | medium | high | auto")
    g.set_defaults(func=generate)

    e = sub.add_parser("edit", help="Editar una o varias imagenes existentes")
    e.add_argument("--prompt", required=True, help="Instruccion de edicion")
    e.add_argument("--image", required=True, action="append",
                   help="Imagen de entrada (repetible para varias)")
    e.add_argument("--mask", default=None,
                   help="Mascara PNG opcional: las zonas transparentes se editan")
    e.add_argument("--out", required=True, help="Ruta del archivo de salida (.png)")
    e.add_argument("--size", default="1024x1024")
    e.add_argument("--quality", default=None, help="low | medium | high | auto")
    e.set_defaults(func=edit)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
