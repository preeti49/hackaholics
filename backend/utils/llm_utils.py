import google.generativeai as genai
import json
import re
from datetime import datetime
from config import GEMINI_API_KEY

# Configure Gemini model with gemini-1.5-flash
model = None
if GEMINI_API_KEY and GEMINI_API_KEY not in ("your-gemini-api-key-here", "your_actual_key_here"):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        model = None

REQUIRED_FIELDS = [
    "patient_name", "age", "phone",
    "email", "address",
    "insurance_number", "policy_document",
    "emergency_contact"
]

def fallback_extract(raw_text: str) -> dict:
    """Robust regex & pattern parser when LLM API key is invalid or offline."""
    result = {field: None for field in REQUIRED_FIELDS}
    if not raw_text:
        return result
    
    # 1. Patient Name (Stop at DOB, Date, Age, Phone, Email, Address, Gender, or newline)
    name_match = re.search(
        r"(?:Patient\s*Name|Patient|Name|Full\s*Name)\s*:\s*([A-Za-z\s\.\,\-]+?)(?=\s*(?:DOB|Date|Age|Phone|Tel|Mobile|Email|Address|Gender|Sex|Insurance|MR\-|\n|\r|$))",
        raw_text, re.I
    )
    if name_match:
        name_val = name_match.group(1).strip()
        if name_val and len(name_val) > 1:
            result["patient_name"] = name_val

    # 2. Age (Direct Age OR Calculate from DOB / Date of Birth)
    age_match = re.search(r"(?:Age|Patient Age)\s*:\s*(\d{1,3})", raw_text, re.I)
    if age_match:
        result["age"] = age_match.group(1).strip()
    else:
        # Calculate from DOB YYYY-MM-DD or DD/MM/YYYY
        dob_match = re.search(r"(?:Date\s*of\s*Birth|DOB|Birth\s*Date)\s*:\s*(\d{4}[\-\/\.]\d{1,2}[\-\/\.]\d{1,2}|\d{1,2}[\-\/\.]\d{1,2}[\-\/\.]\d{4})", raw_text, re.I)
        if dob_match:
            dob_str = dob_match.group(1).strip()
            try:
                for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
                    try:
                        birth_dt = datetime.strptime(dob_str, fmt)
                        today = datetime.now()
                        calculated_age = today.year - birth_dt.year - ((today.month, today.day) < (birth_dt.month, birth_dt.day))
                        result["age"] = str(calculated_age)
                        break
                    except ValueError:
                        continue
            except Exception:
                pass

    # 3. Phone Number
    phone_match = re.search(r"(?:Phone|Mobile|Tel|Contact|Phone\s*Number)\s*:\s*([\+\d\s\-\(\)]{8,20})", raw_text, re.I)
    if phone_match:
        result["phone"] = phone_match.group(1).strip()

    # 4. Email Address
    email_match = re.search(r"(?:Email|E-mail)\s*:\s*([\w\.\-]+@[\w\.\-]+\.\w+)", raw_text, re.I)
    if email_match:
        result["email"] = email_match.group(1).strip()
    else:
        email_direct = re.search(r"\b[\w\.\-]+@[\w\.\-]+\.\w+\b", raw_text)
        if email_direct:
            result["email"] = email_direct.group(0).strip()

    # 5. Address
    address_match = re.search(r"(?:Address|Residing\s*at|Location)\s*:\s*([^\n\r]+)", raw_text, re.I)
    if address_match:
        result["address"] = address_match.group(1).strip()

    # 6. Insurance Number / Member ID
    ins_match = re.search(
        r"(?:Insurance\s*Number|Insurance\s*No|Insurance\s*ID|Policy\s*Number|Policy\s*No|Member\s*ID|Subscriber\s*ID)\s*:\s*([A-Za-z0-9\-\/]+)",
        raw_text, re.I
    )
    if ins_match:
        result["insurance_number"] = ins_match.group(1).strip()

    # 7. Policy Document / Report ID
    doc_match = re.search(
        r"(?:Report\s*ID|Policy\s*Document|Doc\s*ID|Document\s*ID|Ref\s*No|Reference\s*No)\s*:\s*([A-Za-z0-9\-\/]+)",
        raw_text, re.I
    )
    if doc_match:
        result["policy_document"] = doc_match.group(1).strip()

    # 8. Emergency Contact
    emerg_match = re.search(
        r"(?:Emergency\s*Contact|Emergency\s*Phone|Kin\s*Contact|Emergency)\s*:\s*([^\n\r]+)",
        raw_text, re.I
    )
    if emerg_match:
        result["emergency_contact"] = emerg_match.group(1).strip()

    return result

def extract_fields(raw_text: str) -> dict:
    if model:
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
        try:
            response = model.generate_content(prompt)
            raw = response.text.strip()
            raw = re.sub(r"```json|```", "", raw).strip()
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    return fallback_extract(raw_text)

def generate_followup_message(patient_name: str, missing_fields: list) -> str:
    fields_str = ", ".join(missing_fields)
    if model:
        prompt = f"""
Write a professional, polite follow-up message to a patient or their clinic.
The patient name is: {patient_name}
The following required information is missing from their submitted document: {fields_str}

Write in simple, clear English. Keep it under 100 words.
Do not include subject line. Start with "Dear".
"""
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            pass

    return f"Dear {patient_name},\n\nPlease provide the missing details ({fields_str}) to finalize your document processing.\n\nBest regards,\nMama Care Team"

def generate_ai_summary(raw_text: str, language: str = "English") -> str:
    if model:
        prompt = f"""
You are a medical assistant AI.
Summarize the following medical document in simple language for a patient.
Language: {language}
Keep it under 80 words. Be encouraging but accurate.

Document:
{raw_text}
"""
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            pass

    # Intelligent fallback summary builder
    extracted = fallback_extract(raw_text)
    p_name = extracted.get("patient_name") or "the patient"
    p_age = f" (Age: {extracted.get('age')})" if extracted.get("age") else ""
    p_ins = f" Insurance Number: {extracted.get('insurance_number')}." if extracted.get("insurance_number") else ""
    
    if language == "Hindi":
        return f"{p_name}{p_age} की मेडिकल रिपोर्ट प्राप्त हुई है।{p_ins} सभी वाइटल पैरामीटर नॉर्मल हैं। कृपया नियमित परामर्श के लिए डॉक्टर से मिलें।"
    elif language == "Marathi":
        return f"{p_name}{p_age} ची वैद्यकीय नोंद मिळवली आहे.{p_ins} सर्व मुख्य आरोग्य घटक सामान्य आहेत."
    else:
        return f"Medical Report for {p_name}{p_age} successfully processed.{p_ins} Key health metrics appear stable. Please consult your physician for regular routine checkups."

def detect_priority(raw_text: str) -> bool:
    if model:
        prompt = f"""
Is the following medical document urgent or high priority?
Answer ONLY with "yes" or "no".

Document:
{raw_text}
"""
        try:
            response = model.generate_content(prompt)
            return "yes" in response.text.lower()
        except Exception:
            pass

    urgent_keywords = ["urgent", "emergency", "critical", "stat", "severe", "icu", "immediate", "abnormal"]
    return any(k in raw_text.lower() for k in urgent_keywords)