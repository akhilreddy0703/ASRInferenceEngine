curl -X POST "http://localhost:8000/api/v1/text-to-speech" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, this is a test of the text to speech functionality." \
     -d "voice=alloy" \
     -d "model=tts-1" \
     -d "response_format=mp3" \
     -d "speed=1.0" \
     --output outputs/tts_output.mp3
