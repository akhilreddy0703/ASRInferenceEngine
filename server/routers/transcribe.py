from fastapi import APIRouter, UploadFile, File, Form, WebSocket, HTTPException, WebSocketDisconnect
from typing import Optional
from cloud_providers.openai.openai_api_stt import OpenAISTT
from server.utils.logger import transcribe_logger
import os
import io

router = APIRouter()

# Initialize OpenAI client
openai_client = OpenAISTT(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form("whisper-1"),
    language: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
):
    try:
        transcribe_logger.info(f"Transcribing file: {file.filename}")
        transcribe_logger.info(f"File content type: {file.content_type}")
        contents = await file.read()
        transcribe_logger.info(f"File size: {len(contents)} bytes")
        
        result = await openai_client.transcribe(contents, {
            "model": model,
            "language": language,
            "prompt": prompt,
        })
        transcribe_logger.info("Transcription completed successfully")
        return result
    except Exception as e:
        error_message = f"Transcription failed: {str(e)}"
        transcribe_logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.websocket("/stream-transcribe")
async def stream_transcribe(websocket: WebSocket):
    await websocket.accept()
    try:
        transcribe_logger.info("Started streaming transcription")
        
        async def audio_stream():
            while True:
                try:
                    chunk = await websocket.receive_bytes()
                    yield chunk
                except WebSocketDisconnect:
                    transcribe_logger.info("WebSocket disconnected")
                    break

        async for result in openai_client.stream_transcribe(audio_stream(), {
            "model": "whisper-1",
            "window_size": 30,  # 30 seconds window
            "sample_rate": 16000,
            "language": "en",
        }):
            if "error" in result:
                transcribe_logger.error(f"Transcription error: {result['error']}")
                await websocket.send_json({"error": result['error']})
            else:
                await websocket.send_json(result)
    except WebSocketDisconnect:
        transcribe_logger.info("WebSocket disconnected")
    except Exception as e:
        error_message = f"Streaming transcription error: {str(e)}"
        transcribe_logger.error(error_message)
        await websocket.send_json({"error": error_message})
    finally:
        transcribe_logger.info("Ended streaming transcription")
        await websocket.close()