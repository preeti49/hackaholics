import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

REQUIRED_FIELDS = [
    "patient_name", "age", "phone",
    "email", "address",
    "insurance_number", "policy_document",
    "emergency_contact"
]

def extract_fields(raw_text: str) -> dict:
    prompt = f"""
You are a medical document parser.
Extract the following fields from the text below.
Return ONLY a valid JSON object. If a field is not found, return null for that field.
Do NOT guess or invent values.

Fields to extract:
- patient_name
- age
- phone
- email
- address
- insurance_number
- policy_document
- emergency_contact
- diagnosis (if present)
- doctor_name (if present)
- visit_date (if present)

Text:
{raw_text}

Return JSON only. No explanation.
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {field: None for field in REQUIRED_FIELDS}

def generate_followup_message(patient_name: str, missing_fields: list) -> str:
    fields_str = ", ".join(missing_fields)
    prompt = f"""
Write a professional, polite follow-up message to a patient or their clinic.
The patient name is: {patient_name}
The following required information is missing from their submitted document: {fields_str}

Write in simple, clear English. Keep it under 100 words.
Do not include subject line. Start with "Dear".
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_ai_summary(raw_text: str, language: str = "English") -> str:
    prompt = f"""
You are a medical assistant AI.
Summarize the following medical document in simple language for a patient.
Language: {language}
Keep it under 80 words. Be encouraging but accurate.

Document:
{raw_text}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def detect_priority(raw_text: str) -> bool:
    prompt = f"""
Is the following medical document urgent or high priority?
Answer ONLY with "yes" or "no".

Document:
{raw_text}
"""
    response = model.generate_content(prompt)
    return "yes" in response.text.lower()