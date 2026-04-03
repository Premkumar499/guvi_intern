#!/usr/bin/env python3
"""
encode_file.py
──────────────
Quick helper: converts any file to a base64 string and prints a
ready-to-use JSON request body for Postman or cURL.

Usage:
    python encode_file.py path/to/document.pdf
    python encode_file.py path/to/report.docx
    python encode_file.py path/to/scan.png
"""

import sys
import base64
import json
import os

SUPPORTED = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".tiff": "image",
    ".bmp": "image",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python encode_file.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    ext = os.path.splitext(file_path)[1].lower()
    file_type = SUPPORTED.get(ext)

    if not file_type:
        print(f"Unsupported extension '{ext}'. Supported: {list(SUPPORTED.keys())}")
        sys.exit(1)

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    body = {
        "fileName": os.path.basename(file_path),
        "fileType": file_type,
        "fileBase64": encoded,
    }

    output_path = "request_body.json"
    with open(output_path, "w") as out:
        json.dump(body, out, indent=2)

    print(f"✅ Encoded '{file_path}' ({file_type})")
    print(f"📄 Request body saved to: {output_path}")
    print()
    print("── cURL Command ──────────────────────────────────────")
    print(f'curl -X POST http://localhost:8000/api/document-analyze \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -H "x-api-key: sk_track2_987654321" \\')
    print(f'  -d @request_body.json')


if __name__ == "__main__":
    main()
