# Hexaview Resume Converter

A professional enterprise-grade tool that processes candidate resumes (PDF or DOCX) by prepending an AI-powered **Hiring Recommendation** page, branded with Hexaview's identity, while preserving the original resume content with full fidelity.

---

## ✨ Features

- **AI-Powered Analysis** — Uses OpenAI (GPT-4o-mini) to generate structured, professional hiring recommendation content including:
  - Executive summary
  - Education & certifications overview
  - Work history highlights
  - Technical/leadership strengths
  - Final hiring recommendation
- **Smart Format Preservation**
  - **PDF input** → Recommendation page is rendered as PDF and merged directly — original pages untouched
  - **DOCX input** → Content is copied element-by-element (tables, styles, formatting) then converted to PDF via Microsoft Word
- **HR Override** — Recruiters can supply a custom recommendation text that replaces AI-generated content
- **De-duplication** — Auto-detects and skips existing recommendation pages on re-processed documents
- **Output filename** — Downloaded file keeps the original filename (just converted to `.pdf`)
- **Clean Professional UI** — React-based single-page app with a Branding Station and full-screen Document Preview

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python 3.9+) |
| AI Analysis | OpenAI API (`gpt-4o-mini`) |
| Document Parsing | `pdfminer.six`, `python-docx` |
| PDF Generation | `fpdf2`, `pypdf`, `docx2pdf` |
| Frontend | React 18 + Vite |
| HTTP Client | Axios |
| Environment | `python-dotenv` |

---

## 📦 Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Microsoft Word (required for DOCX → PDF conversion on Windows)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
```

Configure your OpenAI key:
```bash
# Edit .env
OPENAI_API_KEY=your_openai_key_here
```

Start the API server:
```bash
python main.py
# Server runs on http://localhost:8000
```

> **Note:** If you don't have an OpenAI key, the system will fall back to a rule-based resume parser automatically.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

---

## 🚀 Usage

1. Open **http://localhost:5173** in your browser
2. On the **Branding Station**, upload a `.pdf` or `.docx` resume
3. *(Optional)* Enter a custom HR recommendation in the text area to override the AI-generated content
4. Click **Run Branding Intelligence**
5. The processed document opens directly in the **Document Preview** tab
6. Click **Download PDF** to save the branded resume — filename matches the original

---

## 📂 Project Structure

```
Resume Convertor/
├── backend/
│   ├── main.py               # FastAPI app & /upload endpoint
│   ├── parser.py             # PDF/DOCX text extraction
│   ├── ai_analyzer.py        # OpenAI integration
│   ├── filler.py             # Template filling, PDF generation & merging
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # API keys (not committed)
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # All UI styles
│   │   └── main.jsx          # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── templates/
│   ├── branded_template_final.docx     # Hexaview-branded resume page template
│   └── recommendation_template.docx   # Hiring recommendation page template
└── utils/
    ├── create_brand_template.py        # Utility to regenerate brand template
    ├── create_recommendation_template.py
    └── templatize_docx.py              # Template placeholder tooling
```

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key for AI-powered resume analysis |

---

## 📝 Notes

- The `.env` file is not committed to version control — set your key before running
- `docx2pdf` requires **Microsoft Word** to be installed on Windows. On Linux/Mac, LibreOffice can be used as an alternative
- The `utils/` scripts are developer tools for maintaining and regenerating document templates — they are not part of the runtime flow
