from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from server.utils.auth import get_api_key
from cloud_providers.openai_api_handler import OpenAIAPI
from server.utils.logger import tts_logger
import io

router = APIRouter()

@router.post("/text-to-speech")
async def text_to_speech(
    text: str = Form(...),
    voice: str = Form("alloy"),
    model: str = Form("tts-1"),
    response_format: str = Form("mp3"),
    speed: float = Form(1.0),
    api_key: str = Depends(get_api_key)
):
    try:
        tts_logger.info(f"Converting text to speech. Voice: {voice}, Model: {model}")
        openai_client = OpenAIAPI(api_key=api_key)
        audio_content = await openai_client.text_to_speech(text, {
            "voice": voice,
            "model": model,
            "response_format": response_format,
            "speed": speed,
        })
        tts_logger.info("Text-to-speech conversion completed successfully")
        return StreamingResponse(io.BytesIO(audio_content), media_type=f"audio/{response_format}")
    except Exception as e:
        error_message = f"Text-to-speech conversion failed: {str(e)}"
        tts_logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)