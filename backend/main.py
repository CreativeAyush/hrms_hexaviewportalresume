from fastapi import FastAPI, UploadFile, File, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Optional
import os
from dotenv import load_dotenv

try:
    from .parser import get_resume_data
    from .filler import generate_multi_page_resume
except ImportError:
    from parser import get_resume_data
    from filler import generate_multi_page_resume

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"), override=False)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "templates", "branded_template_final.docx"
)
REC_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "templates", "recommendation_template.docx"
)

@app.get("/")
async def root():
    return {"message": "Resume Converter API is running"}

@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    candidate_name: Optional[str] = Form(None),
    custom_recommendation: Optional[str] = Form(None),
):
    file_bytes = await file.read()

    # 1. Extract data from uploaded resume
    data = get_resume_data(file_bytes, file.filename)

    # Override name if HR provided it manually (takes priority over AI/fallback)
    if candidate_name and candidate_name.strip():
        data["EVALUATOR"] = candidate_name.strip()

    # Optional custom recommendation override
    if custom_recommendation and custom_recommendation.strip():
        data["REC_RECOMMENDATION"] = custom_recommendation.strip()

    print(
        f"DEBUG: Extracted Data: {data.get('EVALUATOR')} - "
        f"Custom Rec: {'Yes' if custom_recommendation else 'No'} - "
        f"Manual Name: {'Yes' if candidate_name else 'No'}"
    )

    # 2. Verify templates exist
    if not os.path.exists(TEMPLATE_PATH) or not os.path.exists(REC_TEMPLATE_PATH):
        return {"error": "One or more templates are missing."}

    # 3. Generate multi-page PDF (or merged PDF)
    try:
        output_io = generate_multi_page_resume(
            REC_TEMPLATE_PATH,
            TEMPLATE_PATH,
            data,
            file_bytes,
            file.filename,
        )
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

    # 4. Stream the PDF back
    output_io.seek(0)
    filename_no_ext = file.filename.rsplit(".", 1)[0]

    return StreamingResponse(
        output_io,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename_no_ext}.pdf"'
        },
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
