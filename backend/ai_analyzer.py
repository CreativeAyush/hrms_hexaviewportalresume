import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume_with_ai(resume_text):
    """
    Uses OpenAI to extract structured data for the hiring recommendation page.
    """
    if not os.getenv("OPENAI_API_KEY") or "your_actual_key" in os.getenv("OPENAI_API_KEY"):
        return None

    prompt = f"""
    You are an expert executive recruiter and hiring manager with 6+ years of experience at Hexaview Technologies. 
    Analyze the following resume text and provide a highly professional, structured summary for a "Hiring Recommendation" page.
    
    Structure your output as a JSON object with EXACTLY these keys:
    - NAME: The candidate's full name.
    - REC_SUMMARY: A professional summary. Use 2-3 bullet points (starting with -) to highlight the core value proposition. 
    - REC_EDUCATION: A concise list of degrees and certifications. Use | to separate items on the same line.
    - REC_WORK: A brief summary of work history. Use bullet points (starting with -) to describe key roles and achievements.
    - REC_STRENGTHS: A bulleted list (starting with -) of 5-6 top-tier technical or leadership strengths.
    - REC_RECOMMENDATION: A structured recommendation in 3 distinct bullet points (starting with -):
        1. "YES — Strong Fit for [Senior/Specific Role] Roles."
        2. A 2-3 sentence justification of their maturity and fit.
        3. "Don’t hesitate to call me if you have any doubts/concern"
    
    CRITICAL: 
    - The JSON object must be FLAT. Do NOT nest objects like {{"REC_SUMMARY": {{"value": "..."}}}}. 
    - Values must be either a STRING or a LIST OF STRINGS.

    - Use the character '-' for all bullet points.

    
    Style Guidelines:
    - Write as a seasoned HR professional.
    - Be concise but impactful.
    - Focus on executive-level delivery and enterprise governance.

    Resume Text:
    \"\"\"{resume_text}\"\"\"
    """



    try:
        print(f"DEBUG: Sending {len(resume_text)} chars to AI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured recruitment data."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        print(f"DEBUG: AI Response: {content[:200]}...") # Log first 200 chars
        return json.loads(content)
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return None

