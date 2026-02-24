from docx import Document
import re
import os

def templatize(input_path, output_path):
    doc = Document(input_path)
    
    # We'll look for common resume patterns and replace them with placeholders
    # Since we saw 'Sparsh Pant' in the first line, let's target that.
    # A more robust way is to just look for sections.
    
    # Let's try to identify the name/title section
    # Usually the first few paragraphs or a text at the top
    
    found_name = False
    
    for para in doc.paragraphs:
        # If it's the first non-empty paragraph, it's likely the name
        if not found_name and para.text.strip():
            # Replace the whole paragraph text with {{NAME}} and potentially title
            if "–" in para.text:
                para.text = "{{NAME}} – {{TITLE}}"
            else:
                para.text = "{{NAME}}"
            found_name = True
            continue

        # Look for Email
        if re.search(r'[\w\.-]+@[\w\.-]+', para.text):
            para.text = re.sub(r'[\w\.-]+@[\w\.-]+', '{{EMAIL}}', para.text)
            
        # Look for Phone (basic pattern)
        if re.search(r'(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', para.text):
            para.text = re.sub(r'(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', '{{PHONE}}', para.text)

    # Now for sections, we'll look for keywords and replace the *following* content
    # This is tricky in Word because content is in multiple paragraphs.
    # A simpler approach for this "basic application" is to replace the text in section placeholders.
    
    # Let's just add placeholders for the major sections we extracted earlier
    # We will search for 'Summary', 'Experience', 'Education', 'Skills' headers
    
    sections = {
        "SUMMARY": ["summary", "profile", "objective", "about me"],
        "EXPERIENCE": ["experience", "work history", "employment", "professional background"],
        "EDUCATION": ["education", "academic", "scholar", "studies"],
        "SKILLS": ["skills", "technical skills", "expertise", "competencies"]
    }
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.lower()
        for section, keywords in sections.items():
            if any(k in text and len(text) < 30 for k in keywords):
                # We found a section header. The next paragraph should probably be the placeholder.
                # However, to preserve the "look", we might want to just append {{SECTION}}
                # For now, let's keep it simple: the user will likely have a template with these placeholders.
                # But since the user wants ME to do it:
                pass

    # SAVE the result
    doc.save(output_path)
    print(f"Template saved to {output_path}")

if __name__ == "__main__":
    indir = "templates"
    infile = os.path.join(indir, "Resume - Piyush Nirwan.docx")
    outfile = os.path.join(indir, "hexaview_template.docx")
    if os.path.exists(infile):
        templatize(infile, outfile)
    else:
        print(f"File {infile} not found")
