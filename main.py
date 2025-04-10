from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import shutil
import os

def analyze_image(file_path):
    return {
        "nodule_detected": True,
        "size_mm": 9,
        "location": "Right Upper Lobe",
        "malignancy_risk": "Low to Moderate",
        "recommendation": "Follow-up CT in 6-12 months"
    }

class QuestionRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(file_location)
    return JSONResponse(content=result)

@app.post("/ask", response_model=ChatResponse)
def ask_question(request: QuestionRequest):
    if "biopsy" in request.question.lower():
        return ChatResponse(response="Typically, nodules under 10mm are monitored rather than biopsied unless other risk factors are present.")
    return ChatResponse(response="Please provide more context about your question or the nodule findings.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
