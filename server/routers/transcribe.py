from fastapi import APIRouter, UploadFile, File, Form, WebSocket, HTTPException, WebSocketDisconnect
from typing import Optional
from cloud_providers.openai_api_handler import OpenAIAPI
from server.utils.logger import transcribe_logger
import os
import io
import tempfile
from pydub import AudioSegment

router = APIRouter()

# Initialize OpenAI client
openai_client = OpenAIAPI(api_key=os.getenv("OPENAI_API_KEY"))

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
    buffer = io.BytesIO()
    try:
        transcribe_logger.info("Started streaming transcription")
        
        while True:
            try:
                data = await websocket.receive_bytes()
                buffer.write(data)
                
                # Process audio in 5-second chunks
                if buffer.tell() >= 160000:  # 5 seconds of 16-bit audio at 16kHz
                    buffer.seek(0)
                    audio = AudioSegment.from_raw(buffer, sample_width=2, frame_rate=16000, channels=1)
                    
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        audio.export(temp_file.name, format="wav")
                        temp_file_path = temp_file.name
                    
                    try:
                        result = await openai_client.transcribe(temp_file_path, {
                            "model": "whisper-1",
                            "language": "en",
                        })
                        await websocket.send_json(result)
                    except Exception as e:
                        transcribe_logger.error(f"Transcription error: {str(e)}")
                        await websocket.send_json({"error": str(e)})
                    
                    # Reset buffer, keeping any excess data
                    excess = buffer.read()
                    buffer = io.BytesIO()
                    buffer.write(excess)
            
            except WebSocketDisconnect:
                transcribe_logger.info("WebSocket disconnected")
                break
    
    except Exception as e:
        error_message = f"Streaming transcription error: {str(e)}"
        transcribe_logger.error(error_message)
        await websocket.send_json({"error": error_message})
    finally:
        transcribe_logger.info("Ended streaming transcription")
        await websocket.close()