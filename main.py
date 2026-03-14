from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

print("GROQ KEY LOADED:", os.getenv("GROQ_API_KEY")[:10] if os.getenv("GROQ_API_KEY") else "NOT FOUND")

from models.schemas import CodeReviewRequest, CodeReviewResponse
from agents.orchestrator import orchestrate

app = FastAPI(
    title="Multi-Agent Code Review System",
    description="3 AI agents collaborate to review, test, and improve your code",
    version="1.0.0"
)

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    try:
        result = await orchestrate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "running"}