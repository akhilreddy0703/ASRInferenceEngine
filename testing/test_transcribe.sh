curl -i -X POST "$BASE_URL/api/v1/transcribe" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./data/audio.wav" \
     -F "model=whisper-1" \
     -F "language=en" | tee -a transcript.txt