curl -i -X POST "http://localhost:8000/api/v1/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./data/audio.wav" \
     -F "model=whisper-1" \
     -F "language=en" | tee -a outputs/transcript.txt