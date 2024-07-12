from fastapi import APIRouter, UploadFile, File, Form, WebSocket, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from cloud_providers.openai.openai_api_stt import OpenAISTT
from cloud_providers.openai.openai_api_tts import OpenAITTS
from server.utils.logger import speech_to_speech_logger
import os
import asyncio

router = APIRouter()

# Initialize OpenAI clients
stt_client = OpenAISTT(api_key=os.getenv("OPENAI_API_KEY"))
tts_client = OpenAITTS(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/speech-to-speech")
async def speech_to_speech(
    file: UploadFile = File(...),
    stt_model: str = Form("whisper-1"),
    tts_model: str = Form("tts-1"),
    voice: str = Form("alloy"),
    language: Optional[str] = Form(None),
):
    try:
        speech_to_speech_logger.info(f"Processing speech-to-speech for file: {file.filename}")
        contents = await file.read()
        
        # Step 1: Speech-to-Text
        transcription_result = await stt_client.transcribe(contents, {
            "model": stt_model,
            "language": language,
        })
        transcription = transcription_result["text"]
        speech_to_speech_logger.info("Transcription completed")
        
        # Step 2: Text-to-Speech
        audio_content = await tts_client.text_to_speech(transcription, {
            "model": tts_model,
            "voice": voice,
        })
        speech_to_speech_logger.info("Text-to-speech conversion completed")
        
        # Prepare the response
        def iterfile():
            yield audio_content
        
        headers = {
            'Content-Disposition': f'attachment; filename="speech_output.mp3"'
        }
        
        return StreamingResponse(
            iterfile(),
            media_type="audio/mpeg",
            headers=headers,
            background=JSONResponse(content={"transcription": transcription})
        )
    except Exception as e:
        error_message = f"Speech-to-speech processing failed: {str(e)}"
        speech_to_speech_logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.websocket("/stream-speech-to-speech")
async def stream_speech_to_speech(websocket: WebSocket):
    await websocket.accept()
    try:
        speech_to_speech_logger.info("Started streaming speech-to-speech")
        
        # Receive configuration
        config = await websocket.receive_json()
        stt_model = config.get("stt_model", "whisper-1")
        tts_model = config.get("tts_model", "tts-1")
        voice = config.get("voice", "alloy")
        language = config.get("language")
        duration = config.get("duration", 10)  # Duration in seconds
        
        # Streaming audio input
        async def audio_stream():
            start_time = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_time < duration:
                yield await websocket.receive_bytes()
        
        # Speech-to-Text
        full_transcription = ""
        async for result in stt_client.stream_transcribe(audio_stream(), {"model": stt_model, "language": language}):
            if "error" in result:
                await websocket.send_json({"error": result["error"]})
            else:
                full_transcription += result["text"] + " "
                await websocket.send_json({"transcription": result["text"]})
        
        # Text-to-Speech
        audio_content = await tts_client.text_to_speech(full_transcription, {"model": tts_model, "voice": voice})
        
        # Send the final audio
        await websocket.send_bytes(audio_content)
        
    except Exception as e:
        error_message = f"Streaming speech-to-speech error: {str(e)}"
        speech_to_speech_logger.error(error_message)
        await websocket.send_json({"error": error_message})
    finally:
        speech_to_speech_logger.info("Ended streaming speech-to-speech")
        await websocket.close()