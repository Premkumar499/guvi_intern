#  Setup & Usage Guide

Follow these simple steps to get the project up and running on your system.

---

##  Prerequisites

Before starting, make sure you have:

* Python 3.11 or higher installed
* Tesseract OCR installed on your system
* A free Gemini API key (from Google AI Studio)

---

##  Step-by-Step Setup

### 1. Install Tesseract OCR

This tool helps extract text from images.

**Ubuntu / Debian:**

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
```

**macOS (Homebrew):**

```bash
brew install tesseract
```

**Windows:**

* Download from: https://github.com/UB-Mannheim/tesseract/wiki
* Install and add it to your system PATH

---

### 2. Clone the Project

```bash
git clone https://github.com/your-username/doc-analysis-api.git
cd doc-analysis-api
```

---

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Linux / macOS:**

```bash
source venv/bin/activate
```

* **Windows:**

```bash
venv\Scripts\activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Now open `.env` and add your details:

```env
GEMINI_API_KEY=your_api_key_here
API_SECRET_KEY=your_secret_key_here
```

 You can get a free Gemini API key from:
https://aistudio.google.com/app/apikey

---

### 6. Run the Server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

##  Access the API

Once the server starts:

* API Base URL:
  http://localhost:8000

* Interactive API Docs (Swagger UI):
  http://localhost:8000/docs

---

##  How to Use the API

### Endpoint:

```
POST /api/document-analyze
```

### Required Headers:

```
Content-Type: application/json
x-api-key: your_secret_key
```

### Request Body Example:

```json
{
  "fileName": "sample.pdf",
  "fileType": "pdf",
  "fileBase64": "your_base64_encoded_file"
}
```

---

##  How to Convert File to Base64

Use the helper script:

```bash
python encode_file.py path/to/your/file.pdf
```

This will generate a `request_body.json` file.

---

##  Test Using cURL

```bash
curl -X POST http://localhost:8000/api/document-analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secret_key" \
  -d @request_body.json
```

---

##  Expected Result

You’ll get a JSON response containing:

* Summary of the document
* Extracted entities (names, dates, organizations, etc.)
* Sentiment (positive / negative / neutral)

---

##  Optional: Run with Docker

```bash
docker-compose up --build
```

Run in background:

```bash
docker-compose up -d
```

Stop:

```bash
docker-compose down
```

---

##  You're Ready!

Your document analysis API is now live and ready to use.
You can start sending files and getting structured insights instantly.
