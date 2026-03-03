import re
from io import BytesIO
from docx import Document


# ─── PDF Text Extraction ──────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_bytes):
    """
    Primary extractor: pdfplumber (handles complex layouts + fonts well).
    Fallback:          pdfminer  (if pdfplumber not installed or fails).
    After extraction, runs deep_clean_pdf_text() to remove artifacts.
    """
    text = ""

    # 1. Try pdfplumber first — much cleaner output for structured resumes
    try:
        import pdfplumber
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            pages = []
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if page_text:
                    pages.append(page_text)
            text = "\n".join(pages)
        print(f"DEBUG: pdfplumber extracted {len(text)} chars")
    except Exception as e:
        print(f"DEBUG: pdfplumber failed ({e}), falling back to pdfminer")
        text = ""

    # 2. Fallback to pdfminer if pdfplumber gave empty result or failed
    if not text.strip():
        try:
            from pdfminer.high_level import extract_text as pdfminer_extract
            text = pdfminer_extract(BytesIO(pdf_bytes))
            print(f"DEBUG: pdfminer extracted {len(text)} chars")
        except Exception as e:
            print(f"DEBUG: pdfminer also failed: {e}")
            text = ""

    return deep_clean_pdf_text(text)


def deep_clean_pdf_text(text):
    """
    Aggressively cleans raw PDF-extracted text:
    - Removes (cid:N) artifacts from unembedded fonts
    - Fixes common ligature replacements (fi, fl, ff)
    - Collapses excessive whitespace
    - Deduplicates repeated content blocks
    """
    if not text:
        return ""

    # Remove CID artifacts e.g. (cid:9), (cid:32), (cid:131)
    text = re.sub(r'\(cid:\d+\)', '', text)

    # Fix ligature artifacts
    ligature_map = {
        'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi',
        'ﬄ': 'ffl', 'ﬅ': 'st', 'ﬆ': 'st',
    }
    for bad, good in ligature_map.items():
        text = text.replace(bad, good)

    # Remove null bytes and other control chars except newlines/tabs
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Collapse more than 2 consecutive blank lines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove lines that are only dots, dashes, underscores (decorative lines)
    text = re.sub(r'(?m)^[\.\-_=\s]{5,}$', '', text)

    # Strip trailing spaces from each line
    text = '\n'.join(line.rstrip() for line in text.splitlines())

    # Deduplicate repeated content blocks
    text = deduplicate_text(text)

    return text.strip()


def deduplicate_text(text):
    """
    Removes duplicate paragraph blocks that sometimes appear in PDFs
    when footers/headers are repeated or when the document has two columns
    that get merged in a garbled way.

    Strategy: split into paragraphs, keep only first occurrence of each paragraph
    that appears more than once (if paragraph > 40 chars).
    """
    paragraphs = re.split(r'\n{2,}', text)
    seen = set()
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if not stripped:
            continue
        # Only deduplicate longer blocks (short lines like "Education" are OK to repeat)
        key = re.sub(r'\s+', ' ', stripped).lower()
        if len(key) > 40:
            if key in seen:
                continue
            seen.add(key)
        result.append(stripped)
    return '\n\n'.join(result)


# ─── DOCX Text Extraction ─────────────────────────────────────────────────────

def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    lines = []
    for para in doc.paragraphs:
        if para.text.strip():
            lines.append(para.text)
    # Also extract from tables
    for table in doc.tables:
        for row in table.rows:
            row_text = ' | '.join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                lines.append(row_text)
    return '\n'.join(lines)


# ─── XML Safety Cleanup ───────────────────────────────────────────────────────

def clean_xml_compatible(text):
    """
    Removes characters not allowed in XML 1.0 (used before writing to DOCX).
    Valid: #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    """
    if not text:
        return ""
    return "".join(ch for ch in text if (
        0x20 <= ord(ch) <= 0xD7FF or
        ord(ch) in (0x9, 0xA, 0xD) or
        0xE000 <= ord(ch) <= 0xFFFD or
        0x10000 <= ord(ch) <= 0x10FFFF
    ))


# ─── Name Extraction (Fallback) ───────────────────────────────────────────────

def extract_candidate_name(all_lines):
    """
    Heuristically extract the candidate's name from the top lines of the resume.
    Names are almost always the very first non-empty line.
    Skips lines that match common section headers, field labels, contact info, URLs.
    """
    skip_keywords = [
        "summary", "profile", "objective", "experience", "education",
        "skill", "contact", "address", "curriculum vitae", "resume",
        "linkedin", "github", "portfolio", "company", "role", "duration",
        "brief", "project", "tool", "technology", "stack", "certif",
        "qualification", "highlight", "strength", "achievement",
        "responsibility", "responsibilities", "background", "language",
        "framework", "platform", "database", "cloud", "devops",
        "biggest", "current", "organization", "automation", "engineer",
        "developer", "designer", "manager", "analyst", "architect",
        "consultant", "specialist", "lead", "senior", "junior", "intern",
        "expertise", "hexaview",
    ]

    for line in all_lines[:10]:
        stripped = line.strip()
        if not stripped:
            continue
        lower = stripped.lower()

        if stripped.endswith(":"):
            continue
        if any(k in lower for k in skip_keywords):
            continue
        if re.search(r'[@+\d/\\|,]', stripped):
            continue
        if len(stripped) > 50:
            continue

        words = stripped.split()
        if 2 <= len(words) <= 4 and all(len(w) >= 2 and w[0].isupper() for w in words):
            return stripped

    return "Candidate"


# ─── Main Parse Entry Point ───────────────────────────────────────────────────

def parse_resume(text):
    # Step 1: XML-safe cleanup
    clean_text = clean_xml_compatible(text)

    # Log what we're sending to AI (first 500 chars for debugging)
    print(f"DEBUG: Cleaned text preview:\n{clean_text[:500]}\n---")

    # Step 2: Try AI analysis
    try:
        from ai_analyzer import analyze_resume_with_ai
        ai_data = analyze_resume_with_ai(clean_text)
    except Exception as e:
        print(f"DEBUG: AI import/call failed: {e}")
        ai_data = None

    if ai_data:
        return {
            "EVALUATOR": ai_data.get("NAME", "Candidate"),
            "REC_SUMMARY": ai_data.get("REC_SUMMARY", ""),
            "REC_EDUCATION": ai_data.get("REC_EDUCATION", ""),
            "REC_WORK": ai_data.get("REC_WORK", ""),
            "REC_STRENGTHS": ai_data.get("REC_STRENGTHS", ""),
            "REC_RECOMMENDATION": ai_data.get("REC_RECOMMENDATION", ""),
            "FULL_CONTENT": clean_text
        }

    # Step 3: Fallback — section-based extraction
    all_lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    sections_map = {
        "REC_SUMMARY": ["summary", "profile", "objective", "career", "professional", "highlights"],
        "REC_EDUCATION": ["education", "academic", "studies", "qualification"],
        "REC_WORK": ["experience", "work history", "employment", "roles", "responsibilities", "projects"],
        "REC_STRENGTHS": ["skills", "technical skills", "strengths", "highlights", "competencies", "expertise"]
    }

    candidate_name = extract_candidate_name(all_lines)

    extracted_data = {
        "EVALUATOR": candidate_name,
        "REC_SUMMARY": "",
        "REC_EDUCATION": "",
        "REC_WORK": "",
        "REC_STRENGTHS": "",
        "REC_RECOMMENDATION": (
            f"* YES — Strong Fit for this Role.\n"
            f"* {candidate_name} demonstrates a solid background and relevant expertise "
            f"for the position applied. Based on the resume, the candidate shows strong "
            f"alignment with the required qualifications.\n"
            f"* Don't hesitate to call me if you have any doubts/concerns."
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
