import os
import base64
import io
import json
import re
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

from extractor import extract_text_from_document

load_dotenv()

app = FastAPI(
    title="AI Document Analysis API",
    description="Extracts summary, entities, and sentiment from PDF, DOCX, and image files using Gemini AI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "sk_track2_987654321")

client = genai.Client(api_key=GEMINI_API_KEY)


class DocumentRequest(BaseModel):
    fileName: str
    fileType: str          
    fileBase64: str


class EntitiesResponse(BaseModel):
    names: list[str]
    dates: list[str]
    organizations: list[str]
    amounts: list[str]


class DocumentResponse(BaseModel):
    status: str
    fileName: str
    summary: str
    entities: EntitiesResponse
    sentiment: str

def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API key.")
    return x_api_key

def analyze_with_gemini(text: str) -> dict:
    """Send extracted text to Gemini and get structured JSON analysis."""

    prompt = f"""
You are an expert document analyst. Analyze the following document text and return ONLY a valid JSON object with NO markdown formatting, NO code blocks, NO extra text.

Document Text:
\"\"\"
{text[:8000]}
\"\"\"

Return exactly this JSON structure:
{{
  "summary": "A concise 2-3 sentence summary of the document.",
  "entities": {{
    "names": ["Person names, roles, or job titles mentioned (e.g. 'Security Researcher', 'Cybersecurity Analyst'). Use empty list [] only if absolutely none found."],
    "dates": ["Any dates, time periods, or timeframes mentioned (e.g. 'recently', '2024', 'Q3'). Use empty list [] only if absolutely none found."],
    "organizations": ["Any organizations, companies, institutions, agencies, or groups mentioned (e.g. 'Regional Banks', 'Government Agencies'). Use empty list [] only if absolutely none found."],
    "amounts": ["Any numbers, quantities, monetary values, percentages, or statistics mentioned. Use empty list [] only if absolutely none found."]
  }},
  "sentiment": "Positive or Negative or Neutral"
}}

Rules:
- summary: 2-3 sentences max, capturing the core purpose and key facts.
- entities: Be thorough — extract every possible entity even if generic. Only use empty list [] if truly nothing exists for that category.
- sentiment: Must be exactly one of: Positive, Negative, Neutral.
- Return ONLY the JSON. No explanation. No markdown. No code fences.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    raw = response.text.strip()

    # Strip markdown fences if Gemini adds them
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()

    return json.loads(raw)

@app.get("/")
def root():
    return {"message": "AI Document Analysis API is running.", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/document-analyze", response_model=DocumentResponse)
def analyze_document(
    payload: DocumentRequest,
    api_key: str = Depends(verify_api_key),
):
    file_type = payload.fileType.lower().strip()
    if file_type not in ("pdf", "docx", "image"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported fileType '{payload.fileType}'. Accepted: pdf, docx, image."
        )

    try:
        file_bytes = base64.b64decode(payload.fileBase64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 encoding.")

    try:
        extracted_text = extract_text_from_document(file_bytes, file_type, payload.fileName)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Text extraction failed: {str(e)}")

    if not extracted_text or len(extracted_text.strip()) < 10:
        raise HTTPException(status_code=422, detail="Could not extract meaningful text from the document.")

    try:
        analysis = analyze_with_gemini(extracted_text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    return DocumentResponse(
        status="success",
        fileName=payload.fileName,
        summary=analysis.get("summary", ""),
        entities=EntitiesResponse(
            names=analysis.get("entities", {}).get("names", []),
            dates=analysis.get("entities", {}).get("dates", []),
            organizations=analysis.get("entities", {}).get("organizations", []),
            amounts=analysis.get("entities", {}).get("amounts", []),
        ),
        sentiment=analysis.get("sentiment", "Neutral"),
    )
