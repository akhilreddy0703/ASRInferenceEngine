import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers import transcribe, tts, speech_to_speech
from server.utils.logger import main_logger

app = FastAPI(title="Inference Server for Cloud Providers")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe.router, prefix="/api/v1", tags=["transcribe"])
app.include_router(tts.router, prefix="/api/v1", tags=["tts"])
app.include_router(speech_to_speech.router, prefix="/api/v1", tags=["speech-to-speech"])

@app.get("/")
async def root():
    main_logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Inference Server for Cloud Providers"}

if __name__ == "__main__":
    import uvicorn
    main_logger.info("Starting server")
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)