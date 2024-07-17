curl -i -X POST "$BASE_URL/api/v1/speech-to-speech" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./data/DYSARTHRIA.wav" \
     -F "stt_model=whisper-1" \
     -F "tts_model=tts-1" \
     -F "voice=alloy" \
     -F "language=en" \
     --output v2v_response.mp3