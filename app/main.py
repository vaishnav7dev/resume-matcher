from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from app.matcher import analyze, get_model
from app.parser import extract_text_from_pdf

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_model()  # load the embedding model once, before the first request
    yield


app = FastAPI(title="Resume-JD Matcher", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_route(
    jd_text: str = Form(...),
    resume_text: str = Form(""),
    resume: UploadFile | None = File(None),
):
    if resume is not None and resume.filename:
        try:
            resume_text = extract_text_from_pdf(resume.file)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Could not read the PDF. Upload a text-based PDF or paste the text instead.",
            ) from None
    try:
        return analyze(resume_text, jd_text)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from None


# Must come last: it matches every path, so routes declared after it would never be reached.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")