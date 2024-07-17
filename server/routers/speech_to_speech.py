from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import base64
from typing import Optional
from server.utils.auth import get_api_key
from cloud_providers.openai_api_handler import OpenAIAPI
from server.utils.logger import speech_to_speech_logger as logger

router = APIRouter()

@router.post("/speech-to-speech")
async def speech_to_speech(
    file: UploadFile = File(...),
    stt_model: str = Form("whisper-1"),
    tts_model: str = Form("tts-1"),
    voice: str = Form("alloy"),
    language: Optional[str] = Form(None),
    api_key: str = Depends(get_api_key)
):
    try:
        logger.info(f"Processing speech-to-speech for file: {file.filename}")
        contents = await file.read()
        openai_client = OpenAIAPI(api_key=api_key)
        
        # Step 1: Speech-to-Text
        transcription_result = await openai_client.transcribe(contents, {
            "model": stt_model,
            "language": language,
        })
        transcription = transcription_result["text"]
        logger.info("Transcription completed")
        
        # Step 2: Text-to-Speech
        audio_content = await openai_client.text_to_speech(transcription, {
            "model": tts_model,
            "voice": voice,
        })
        logger.info("Text-to-speech conversion completed")
        
        # Encode audio content as base64
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')
        
        # Prepare the response
        return JSONResponse(content={
            "transcription": transcription,
            "audio": audio_base64
        })
    except Exception as e:
        error_message = f"Speech-to-speech processing failed: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)