curl -i -X POST "$BASE_URL/api/v1/text-to-speech" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, this is a test." \
     -d "voice=alloy" \
     -d "model=tts-1" \
     -d "response_format=mp3" \
     -d "speed=1.0" \
     --output tts_output.mp3