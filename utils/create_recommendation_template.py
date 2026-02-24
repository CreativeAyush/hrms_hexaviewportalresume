from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def create_recommendation_template(branding_template_path, output_path):
    # 1. Start with the branding template (logo already isolated)
    doc = Document(branding_template_path)
    
    # 2. Clear paragraphs after the logo if any (Should only have {{CONTENT}} now)
    for p in doc.paragraphs:
        if "{{CONTENT}}" in p.text:
            p.text = ""
            # Add content below the logo
            
    # 3. Add "Comments from Hexaview (Evaluator Name)"
    eval_p = doc.add_paragraph()
    run = eval_p.add_run("Comments from Hexaview ({{EVALUATOR}})")
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.underline = True
    run.font.color.rgb = RGBColor(0, 112, 192) # Hexaview Blue
    
    doc.add_paragraph() # Spacer
    
    # 4. Helper to add sections
    def add_section(header_text, placeholder_key, with_line=False):
        h = doc.add_paragraph()
        run = h.add_run(header_text)
        run.bold = True
        run.font.size = Pt(12)
        
        doc.add_paragraph("{{" + placeholder_key + "}}")
        doc.add_paragraph() # Spacer
        
        if with_line:
            # Add a horizontal line
            line_p = doc.add_paragraph()
            line_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = line_p.add_run("________________________________________________________________________________")
            run.font.color.rgb = RGBColor(180, 180, 180)
            doc.add_paragraph() # Spacer

    add_section("Summary", "REC_SUMMARY", with_line=True)
    add_section("Education", "REC_EDUCATION")
    add_section("Employer and Work", "REC_WORK")
    add_section("Candidate Strengths", "REC_STRENGTHS")
    add_section("Hexaview Hiring Recommendation", "REC_RECOMMENDATION")


    doc.save(output_path)
    print(f"Hiring Recommendation Template saved to {output_path}")

if __name__ == "__main__":
    branding_path = "templates/branded_template_final.docx"
    output_path = "templates/recommendation_template.docx"
    if os.path.exists(branding_path):
        create_recommendation_template(branding_path, output_path)
    else:
        print(f"Error: {branding_path} not found. Run branding script first.")
