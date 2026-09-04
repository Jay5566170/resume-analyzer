import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # ✅ CORRECT MODEL NAME
    model = genai.GenerativeModel('models/gemini-3.6-flash')
    print("✅ Gemini configured successfully!")
else:
    print("❌ GEMINI_API_KEY not found in .env")
    model = None

def analyze_resume_with_ai(text_content):
    """Send resume text to Gemini and extract structured data."""
    
    print(f"📝 Text length: {len(text_content)} characters")
    
    if not text_content or len(text_content.strip()) < 50:
        print("❌ Text too short or empty")
        return {
            "error": "Resume text is too short",
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "experience": [],
            "education": [],
            "summary": None
        }
    
    if model is None:
        print("❌ Gemini model not initialized. Check your API key.")
        return {
            "error": "Gemini not configured",
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "experience": [],
            "education": [],
            "summary": None
        }
    
    try:
        prompt = f"""
        Analyze the following resume text and extract key information.
        Return ONLY a valid JSON response with this EXACT structure:
        {{
            "name": "Full name of the candidate",
            "email": "Email address found",
            "phone": "Phone number found",
            "skills": ["skill1", "skill2", "skill3"],
            "experience": ["Job title - Company (Years)", ...],
            "education": ["Degree - University (Year)", ...],
            "summary": "A brief 2-3 sentence professional summary"
        }}
        
        Resume Text:
        {text_content[:3000]}
        """
        
        print("📤 Sending to Gemini API...")
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        print(f"📥 Received response from Gemini")
        
        # Try to extract JSON from the response
        try:
            # Remove markdown code blocks if present
            if "```json" in result_text:
                start = result_text.find("```json") + 7
                end = result_text.rfind("```")
                result_text = result_text[start:end].strip()
            elif "```" in result_text:
                start = result_text.find("```") + 3
                end = result_text.rfind("```")
                result_text = result_text[start:end].strip()
            
            data = json.loads(result_text)
            print("✅ Successfully parsed JSON response")
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            return {
                "name": None,
                "email": None,
                "phone": None,
                "skills": [],
                "experience": [],
                "education": [],
                "summary": result_text[:200],
                "error": "Failed to parse structured data"
            }
            
    except Exception as e:
        print(f"❌ Gemini analysis error: {e}")
        return {
            "error": str(e),
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "experience": [],
            "education": [],
            "summary": None
        }