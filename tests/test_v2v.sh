curl -X POST "http://localhost:8000/api/v1/speech-to-speech" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./audio.wav" \
     -F "stt_model=whisper-1" \
     -F "tts_model=tts-1" \
     -F "voice=alloy" \
     -F "language=en" \
     --output response.mp3