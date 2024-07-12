from abc import ABC, abstractmethod
from typing import Union, Dict, Any

class CloudProviderBase(ABC):
    @abstractmethod
    async def transcribe(self, audio_file: Union[str, bytes], options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transcribe audio to text.
        :param audio_file: Path to audio file or bytes of audio data
        :param options: Dictionary of options for transcription
        :return: Dictionary containing transcription result
        """
        pass

    @abstractmethod
    async def text_to_speech(self, text: str, options: Dict[str, Any]) -> bytes:
        """
        Convert text to speech.
        :param text: Text to convert to speech
        :param options: Dictionary of options for text-to-speech
        :return: Bytes of audio data
        """
        pass

    @abstractmethod
    async def stream_transcribe(self, audio_stream, options: Dict[str, Any]):
        """
        Transcribe streaming audio to text.
        :param audio_stream: AsyncGenerator yielding chunks of audio data
        :param options: Dictionary of options for transcription
        :return: AsyncGenerator yielding transcription results
        """
        pass