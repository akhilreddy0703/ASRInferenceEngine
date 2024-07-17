from typing import Union, Dict, Any, AsyncGenerator
from .base import CloudProviderBase
from openai import OpenAI
import io
import tempfile
from pydub import AudioSegment
import numpy as np

class OpenAIAPI(CloudProviderBase):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def transcribe(self, audio_file: Union[str, bytes], options: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if isinstance(audio_file, bytes):
                file = io.BytesIO(audio_file)
                file.name = "audio.wav"
            else:
                file = open(audio_file, 'rb')

            response = self.client.audio.transcriptions.create(
                model=options.get("model", "whisper-1"),
                file=file,
                response_format=options.get("response_format", "json"),
                language=options.get("language"),
                prompt=options.get("prompt"),
                temperature=options.get("temperature", 0)
            )
            return {"text": response.text}
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
        finally:
            if isinstance(file, io.IOBase) and not isinstance(file, io.BytesIO):
                file.close()

    async def stream_transcribe(self, audio_stream: AsyncGenerator[bytes, None], options: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        buffer = b""
        window_size = options.get("window_size", 10)  # 10 seconds of audio
        sample_rate = options.get("sample_rate", 16000)
        window_bytes = window_size * sample_rate * 2  # 16-bit audio
        
        async for chunk in audio_stream:
            buffer += chunk
            if len(buffer) >= window_bytes:
                try:
                    audio_array = np.frombuffer(buffer, dtype=np.int16)
                    audio_segment = AudioSegment(
                        audio_array.tobytes(),
                        frame_rate=sample_rate,
                        sample_width=2,
                        channels=1
                    )
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        audio_segment.export(temp_file.name, format="wav")
                        temp_file_path = temp_file.name

                    result = await self.transcribe(temp_file_path, options)
                    yield result

                    buffer = buffer[window_bytes//2:]
                except Exception as e:
                    yield {"error": str(e)}
        
        if buffer:
            try:
                audio_array = np.frombuffer(buffer, dtype=np.int16)
                audio_segment = AudioSegment(
                    audio_array.tobytes(),
                    frame_rate=sample_rate,
                    sample_width=2,
                    channels=1
                )
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    audio_segment.export(temp_file.name, format="wav")
                    temp_file_path = temp_file.name
                result = await self.transcribe(temp_file_path, options)
                yield result
            except Exception as e:
                yield {"error": str(e)}

    async def text_to_speech(self, text: str, options: Dict[str, Any]) -> bytes:
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