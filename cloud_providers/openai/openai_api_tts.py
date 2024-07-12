import asyncio
from typing import Dict, Any
from ..base import CloudProviderBase
from openai import OpenAI
import io

class OpenAITTS(CloudProviderBase):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def text_to_speech(self, text: str, options: Dict[str, Any]) -> bytes:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_text_to_speech, text, options)

    def _sync_text_to_speech(self, text: str, options: Dict[str, Any]) -> bytes:
        response = self.client.audio.speech.create(
            model=options.get("model", "tts-1"),
            voice=options.get("voice", "alloy"),
            input=text,
            response_format=options.get("response_format", "mp3"),
            speed=options.get("speed", 1.0)
        )
        
        buffer = io.BytesIO()
        for chunk in response.iter_bytes():
            buffer.write(chunk)
        buffer.seek(0)
        return buffer.getvalue()

    async def transcribe(self, audio_file: bytes, options: Dict[str, Any]) -> Dict[str, Any]:
        # This method is implemented in openai_api_stt.py
        raise NotImplementedError("Transcription is not implemented in this class")

    async def stream_transcribe(self, audio_stream, options: Dict[str, Any]):
        # This method is implemented in openai_api_stt.py
        raise NotImplementedError("Stream transcription is not implemented in this class")