from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, WebSocket
from typing import Optional
from server.utils.logger import transcribe_logger
from server.utils.auth import get_api_key
from cloud_providers.openai_api_handler import OpenAIAPI
import json

router = APIRouter()

@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form("whisper-1"),
    language: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    response_format: str = Form("json"),
    api_key: str = Depends(get_api_key)
):
    try:
        transcribe_logger.info(f"Transcribing file: {file.filename}")
        transcribe_logger.info(f"File content type: {file.content_type}")
        contents = await file.read()
        transcribe_logger.info(f"File size: {len(contents)} bytes")
        
        openai_client = OpenAIAPI(api_key=api_key)
        result = await openai_client.transcribe(contents, {
            "model": model,
            "language": language,
            "prompt": prompt,
            "response_format": response_format,
        })
        
        transcribe_logger.info("Transcription completed successfully")
        return {"text": result if isinstance(result, str) else result.get("text", "")}
    except Exception as e:
        error_message = f"Transcription failed: {str(e)}"
        transcribe_logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)



@router.websocket("/stream-transcribe")
async def stream_transcribe(websocket: WebSocket):
    await websocket.accept()
    try:
        transcribe_logger.info("Started streaming transcription")
        
        # Receive configuration
        config = await websocket.receive_json()
        api_key = config.get("api_key")
        model = config.get("sttModel", "whisper-1")
        language = config.get("language")
        response_format = "verbose_json"
        word_timestamps = config.get("wordTimestamps", False)
        
        openai_client = OpenAIAPI(api_key=api_key)
        
        buffer = b""
        async for data in websocket.iter_bytes():
            buffer += data
            if len(buffer) >= 4000:  # Process in ~4KB chunks
                try:
                    result = await openai_client.transcribe(buffer, {
                        "model": model,
                        "language": language,
                        "response_format": response_format,
                        "timestamp_granularities": ["word"] if word_timestamps else None,
                    })
                    
                    if isinstance(result, str):
                        result = json.loads(result)
                    
                    response = {
                        "text": result.get("text", ""),
                        "words": result.get("words", []) if word_timestamps else None
                    }
                    
                    await websocket.send_json(response)
                    buffer = b""
                except Exception as e:
                    error_message = f"Streaming transcription error: {str(e)}"
                    transcribe_logger.error(error_message)
                    await websocket.send_json({"error": error_message})
    
    except Exception as e:
        error_message = f"Websocket error: {str(e)}"
        transcribe_logger.error(error_message)
    finally:
        transcribe_logger.info("Ended streaming transcription")
        await websocket.close()