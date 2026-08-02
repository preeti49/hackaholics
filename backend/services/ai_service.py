import os
import google.generativeai as genai
from utils.llm_utils import generate_ai_summary as base_summary

TRANSLATION_PROMPTS = {
    "English": "Provide summary in clear English.",
    "Hindi": "सारांश शुद्ध और सरल हिंदी भाषा में प्रदान करें।",
    "Bengali": "সংক্ষিপ্তসারটি পরিষ্কার এবং সহজ বাংলা ভাষায় প্রদান করুন।",
    "Tamil": "சுருக்கத்தை தெளிவான மற்றும் எளிய தமிழில் வழங்கவும்.",
    "Marathi": "सारांश स्पष्ट आणि सोप्या मराठी भाषेत द्या.",
    "Gujarati": "સારાંશ સ્પષ્ટ અને સરળ ગુજરાતી ભાષામાં આપો."
}

def generate_medical_ai_summary(raw_text: str, language: str = "English") -> dict:
    """
    Generates health summary + Doctor Recommendations in target language:
    Supported Languages: English, Hindi, Bengali, Tamil, Marathi, Gujarati
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
            except Exception:
                model = genai.GenerativeModel("gemini-pro")
            
            lang_instruction = TRANSLATION_PROMPTS.get(language, TRANSLATION_PROMPTS["English"])
            
            prompt = f"""
            Analyze the following medical report text and provide:
            1. Key Health Findings (e.g. Blood Sugar, Vitamin D, Hemoglobin, Liver function status).
            2. Clear Doctor Recommendation.

            Language Instruction: {lang_instruction}

            Medical Report Text:
            {raw_text[:2000]}
            """
            
            response = model.generate_content(prompt)
            if response and response.text:
                return {
                    "summary": response.text.strip(),
                    "language": language
                }
        except Exception as e:
            print("Gemini AI Service fallback:", e)

    # Base rule-based fallback summary with multi-language recommendations
    base_text = base_summary(raw_text, language)
    
    recommendations = {
        "English": "\nRecommendation: Take Vitamin D supplements (60k IU weekly) and consult your doctor for a routine follow-up.",
        "Hindi": "\nसुझाव: विटामिन डी सप्लीमेंट (60k IU साप्ताहिक) लें और अपने डॉक्टर से परामर्श करें।",
        "Bengali": "\nসুপারিশ: ভিটামিন ডি সাপ্লিমেন্ট (সাপ্তাহিক 60k IU) গ্রহণ করুন এবং ডাক্তারের সাথে পরামর্শ করুন।",
        "Tamil": "\nபரிந்துரை: வைட்டமின் டி கூடுதல் உணவுகளை எடுத்துக் கொள்ளுங்கள் மற்றும் உங்கள் மருத்துவரை அணுகவும்.",
        "Marathi": "\nशिफारस: व्हिटॅमिन डी सप्लीमेंट्स (साप्ताहिक 60k IU) घ्या आणि तुमच्या डॉक्टरांचा सल्ला घ्या.",
        "Gujarati": "\nભલામણ: વિટામિન ડી સપ્લીમેન્ટ્સ લો અને તમારા ડૉક્ટરની સલાહ લો."
    }

    rec = recommendations.get(language, recommendations["English"])

    return {
        "summary": base_text + rec,
        "language": language
    }
