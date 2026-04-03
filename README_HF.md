---
title: AI Document Analysis API
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# AI Document Analysis API

An intelligent document processing REST API that extracts, analyzes, and summarizes content from PDF, DOCX, and image files using Google Gemini AI.

## Features

- Multi-format support: PDF, DOCX, and images (JPG, PNG, TIFF, BMP)
- Automatic text extraction with OCR support
- AI-powered summarization
- Named entity extraction (names, dates, organizations, amounts)
- Sentiment analysis
- API key authentication

## Usage

The API is available at the Space URL. Use the interactive documentation at `/docs` to test the endpoints.

### Authentication

All requests require an API key header:
```
x-api-key: sk_track2_987654321
```

### Endpoints

- `GET /health` - Health check
- `POST /api/document-analyze` - Analyze a document

### Example Request

```bash
curl -X POST https://your-space-url/api/document-analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track2_987654321" \
  -d '{
    "fileName": "document.pdf",
    "fileType": "pdf",
    "fileBase64": "base64_encoded_content"
  }'
```

## Tech Stack

- Python 3.11 + FastAPI
- Google Gemini 2.5 Flash
- Tesseract OCR
- pdfplumber, python-docx, pytesseract

## Environment Variables

Set these in your Space settings:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `API_SECRET_KEY` - API authentication key (default: sk_track2_987654321)
