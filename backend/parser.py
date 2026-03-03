import re
from io import BytesIO
from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_pdf(pdf_bytes):
    text = extract_text(BytesIO(pdf_bytes))
    # Fix common PDF extraction artifacts (ligatures)
    # ti often becomes $ or similar
    # fi often becomes F
    # ff often becomes f
    # fl often becomes fl
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬀ', 'ff')
    text = text.replace('ﬁ', 'fi')
    # Custom fixes for the user's specific case
    # In many PDF extractions, 'ti' is corrupted to 'F' or '$'
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬀ', 'ff')
    
    # Generic regex for the common '$' and 'F' issues in ligatures
    # Mapping both to 'ti' as seen in the user's examples
    text = re.sub(r'([a-zA-Z])\$([a-zA-Z])', r'\1ti\2', text)
    text = re.sub(r'([a-zA-Z])F([a-zA-Z])', r'\1ti\2', text)

    
    return text

def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def clean_xml_compatible(text):
    """
    Removes characters that are not allowed in XML 1.0.
    Valid characters: #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    """
    if not text:
        return ""
    return "".join(ch for ch in text if (
        0x20 <= ord(ch) <= 0xD7FF or
        ord(ch) in (0x9, 0xA, 0xD) or
        0xE000 <= ord(ch) <= 0xFFFD or
        0x10000 <= ord(ch) <= 0x10FFFF
    ))

def extract_candidate_name(all_lines):
    """
    Heuristically extract the candidate's name from the top lines of the resume.
    Looks for the first short line (< 60 chars) that is not an email/phone/URL
    and does not start with a common section keyword.
    """
    skip_keywords = [
        "summary", "profile", "objective", "experience", "education",
        "skills", "contact", "address", "curriculum vitae", "resume",
        "linkedin", "github", "portfolio"
    ]
    for line in all_lines[:15]:  # Only check top 15 lines
        stripped = line.strip()
        if not stripped:
            continue
        lower = stripped.lower()
        # Skip lines that look like contact info, URLs, or section headers
        if any(k in lower for k in skip_keywords):
            continue
        if re.search(r'[@+\d/\\|]', stripped):  # phone/email/separator
            continue
        if len(stripped) > 60:
            continue
        # Name usually has 2-4 words of reasonable length
        words = stripped.split()
        if 2 <= len(words) <= 5 and all(len(w) >= 2 for w in words):
            return stripped
    return "Candidate"


def parse_resume(text):
    # Clean text of control characters that break python-docx
    clean_text = clean_xml_compatible(text)
    
    # 1. Try AI Analysis first
    from ai_analyzer import analyze_resume_with_ai
    ai_data = analyze_resume_with_ai(clean_text)

    if ai_data:
        # Map AI labels to our template placeholders
        return {
            "EVALUATOR": ai_data.get("NAME", "Candidate"),
            "REC_SUMMARY": ai_data.get("REC_SUMMARY", ""),
            "REC_EDUCATION": ai_data.get("REC_EDUCATION", ""),
            "REC_WORK": ai_data.get("REC_WORK", ""),
            "REC_STRENGTHS": ai_data.get("REC_STRENGTHS", ""),
            "REC_RECOMMENDATION": ai_data.get("REC_RECOMMENDATION", ""),
            "FULL_CONTENT": clean_text
        }

    # 2. Fallback to Section Based Extraction if AI fails or no key
    all_lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    sections_map = {
        "REC_SUMMARY": ["summary", "profile", "objective", "career", "professional", "highlights"],
        "REC_EDUCATION": ["education", "academic", "studies", "qualification"],
        "REC_WORK": ["experience", "work history", "employment", "roles", "responsibilities", "projects"],
        "REC_STRENGTHS": ["skills", "technical skills", "strengths", "highlights", "competencies", "expertise"]
    }

    # Extract candidate name from top of resume (no longer hardcoded)
    candidate_name = extract_candidate_name(all_lines)

    extracted_data = {
        "EVALUATOR": candidate_name,
        "REC_SUMMARY": "",
        "REC_EDUCATION": "",
        "REC_WORK": "",
        "REC_STRENGTHS": "",
        "REC_RECOMMENDATION": (
            f"- YES — Strong Fit for this Role.\n"
            f"- {candidate_name} demonstrates a solid background and relevant expertise "
            f"for the position applied. Based on the resume, the candidate shows strong "
            f"alignment with the required qualifications.\n"
            f"- Don't hesitate to call me if you have any doubts/concerns."
        ),
        "FULL_CONTENT": clean_text
    }

    current_section = None
    for line in all_lines:
        lower_line = line.lower()
        found_header = False
        for section_key, keywords in sections_map.items():
            if any(keyword in lower_line and len(lower_line) < 40 for keyword in keywords):
                current_section = section_key
                found_header = True
                break
        
        if found_header:
            continue
            
        if current_section:
            extracted_data[current_section] += line + "\n"

    # Cleanup granular sections
    for key in sections_map.keys():
        if not extracted_data[key].strip():
            extracted_data[key] = "Details not specifically found in original resume."
        else:
            extracted_data[key] = extracted_data[key].strip()

    return extracted_data

def get_resume_data(file_bytes, filename):
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_bytes)
    else:
        text = ""
        
    return parse_resume(text)

