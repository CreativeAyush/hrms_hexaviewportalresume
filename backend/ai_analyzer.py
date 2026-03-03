import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume_with_ai(resume_text):
    """
    Uses OpenAI to extract structured data for the hiring recommendation page.
    All content is dynamically generated from the uploaded resume text.
    """
    if not os.getenv("OPENAI_API_KEY") or "your_actual_key" in os.getenv("OPENAI_API_KEY", ""):
        return None

    prompt = f"""
You are a senior Technical Recruiter and Hiring Manager at Hexaview Technologies with 10+ years of experience.
Your task is to read the resume below and produce a detailed, professional "Hiring Recommendation" report for it.

ALL content you generate MUST be grounded in the actual resume text — never invent facts.

Produce a flat JSON object with EXACTLY these keys and formats:

- NAME: The candidate's full name as written in the resume.

- REC_SUMMARY: Write 2 to 3 rich, flowing prose paragraphs — ABSOLUTELY NO bullet points, NO dashes, NO lists of any kind.
  Write this as a senior Hiring Manager at Hexaview Technologies who has personally reviewed this resume and is confidently recommending the candidate.
  Use a warm, authoritative, professional tone — like a written endorsement you would send to a client or leadership team.
  MUST include: total years of experience, current or most recent company and role, key domains/industries, notable accomplishments with real metrics from the resume, and why this candidate stands out.
  Each paragraph must flow naturally into the next. Do NOT start with "The candidate" — use their actual name.
  Example tone (do NOT copy this, generate fresh content from the resume):
    "Shubham brings over six years of progressive UX leadership across enterprise SaaS and fintech environments..."
    "What sets Shubham apart is his ability to bridge design thinking with measurable business outcomes..."
    "In my assessment, he is exceptionally well-prepared for senior product design roles..."

- REC_EDUCATION: A multi-line string listing each qualification on its own line.
  Format each line as: "Degree/Certification | Institution | Year (if available)"
  Example:
    B.Tech (Computer Science) | IIT Delhi | 2015
    PMP | PMI | 2020

- REC_WORK: A multi-line narrative + bullet summary of work history. Start with 1-2 short narrative paragraphs about the candidate's career arc, then list 4-6 bullet points (starting with *) covering key responsibilities/achievements drawn directly from the resume.
  Example format:
    John has 10+ years across fintech and SaaS...
    He currently leads engineering at XYZ Corp...
    * Led migration of 50+ microservices to AWS, reducing infra cost by 30%
    * Managed cross-functional teams of 40+ engineers across 3 time zones
    * ...

- REC_STRENGTHS: 5-7 bullet points (starting with *) listing specific, concrete technical or leadership strengths extracted from the resume. Be precise — use actual technologies, methodologies, certifications, or metrics from the resume.
  Example:
    * DevOps Modernization — Jenkins, GitHub Actions, Kubernetes
    * Portfolio Management ($4M+ budgets, 60-120 FTEs)
    * FedRAMP & SOC2 Compliance Leadership

- REC_RECOMMENDATION: Exactly 3 bullet points (starting with *):
    1. First bullet: "YES — Strong Fit for [specific role type matching resume] Roles."
    2. Second bullet: 2-3 sentences explaining WHY using specific evidence from the resume (role, metrics, skills).
    3. Third bullet: "Don't hesitate to call me if you have any doubts/concerns."

CRITICAL RULES:
- The JSON must be FLAT. No nested objects.
- All values must be STRING (multi-line strings are fine, use actual newlines).
- Do NOT use markdown syntax (no **, no ##, no ```) inside values.
- Use * for bullet points (NOT - or •).
- Every single detail must come from the resume. Do not fabricate companies, dates, or numbers.

Resume Text:
\"\"\"{resume_text}\"\"\"
"""

    try:
        print(f"DEBUG: Sending {len(resume_text)} chars to AI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert recruitment analyst. Extract and summarize resume data into a structured JSON hiring recommendation. Always ground your output in facts from the resume."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        content = response.choices[0].message.content
        print(f"DEBUG: AI Response: {content[:300]}...")
        parsed = json.loads(content)

        # Ensure all values are strings (flatten lists if AI returns them)
        for key in parsed:
            if isinstance(parsed[key], list):
                parsed[key] = "\n".join([str(v) for v in parsed[key]])

        return parsed

    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return None
