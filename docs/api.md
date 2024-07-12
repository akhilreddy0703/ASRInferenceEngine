# API Documentation

This document provides detailed information about the endpoints available in the Cloud Provider Inference Server, including their parameters and example usage.

## Table of Contents

1. [Transcription](#transcription)
   - [File Upload](#file-upload-transcription)
   - [Streaming](#streaming-transcription)
2. [Text-to-Speech](#text-to-speech)
3. [Speech-to-Speech](#speech-to-speech)
   - [File Upload](#file-upload-speech-to-speech)
   - [Streaming](#streaming-speech-to-speech)

## Transcription

### File Upload Transcription

Endpoint: `POST /api/v1/transcribe`

This endpoint allows you to upload an audio file for transcription.

Parameters:
- `file`: The audio file to transcribe (required)
- `model`: The transcription model to use (optional, default: "whisper-1")
- `language`: The language of the audio (optional)
- `prompt`: An optional prompt to guide the transcription (optional)

Example usage with curl:

```bash
curl -X POST "http://localhost:8000/api/v1/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audiofile.mp3" \
     -F "model=whisper-1" \
     -F "language=en" \
     -F "prompt=This is a conversation about AI"
```

Example response:

```json
{
  "text": "This is the transcribed text from your audio file."
}
```

### Streaming Transcription

Endpoint: `WebSocket /api/v1/stream-transcribe`

This endpoint allows you to stream audio for real-time transcription.

To use this endpoint, you need to establish a WebSocket connection and send audio data in chunks. The server will respond with transcription results as they become available.

Example usage with JavaScript:

```javascript
const socket = new WebSocket('ws://localhost:8000/api/v1/stream-transcribe');

socket.onopen = function(e) {
  console.log("Connection established");
  // Start sending audio data
};

socket.onmessage = function(event) {
  console.log(`Transcription: ${event.data}`);
};

// Send audio data
socket.send(audioChunk);
```

## Text-to-Speech

Endpoint: `POST /api/v1/text-to-speech`

This endpoint converts text to speech.

Parameters:
- `text`: The text to convert to speech (required)
- `voice`: The voice to use (optional, default: "alloy")
- `model`: The TTS model to use (optional, default: "tts-1")
- `response_format`: The audio format of the response (optional, default: "mp3")
- `speed`: The speed of the speech (optional, default: 1.0)

Example usage with curl:

```bash
curl -X POST "http://localhost:8000/api/v1/text-to-speech" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, world!&voice=alloy&model=tts-1&response_format=mp3&speed=1.0" \
     --output speech.mp3
```

The response will be the audio file in the specified format.

## Speech-to-Speech

### File Upload Speech-to-Speech

Endpoint: `POST /api/v1/speech-to-speech`

This endpoint converts speech from an uploaded file to text and then back to speech.

Parameters:
- `file`: The audio file to convert (required)
- `stt_model`: The speech-to-text model to use (optional, default: "whisper-1")
- `tts_model`: The text-to-speech model to use (optional, default: "tts-1")
- `voice`: The voice to use for text-to-speech (optional, default: "alloy")
- `language`: The language of the input audio (optional)

Example usage with curl:

```bash
curl -X POST "http://localhost:8000/api/v1/speech-to-speech" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audiofile.mp3" \
     -F "stt_model=whisper-1" \
     -F "tts_model=tts-1" \
     -F "voice=alloy" \
     -F "language=en" \
     --output converted_speech.mp3
```

The response will be the converted audio file.

### Streaming Speech-to-Speech

Endpoint: `WebSocket /api/v1/stream-speech-to-speech`

This endpoint allows you to stream audio for real-time speech-to-speech conversion.

To use this endpoint, you need to establish a WebSocket connection, send configuration parameters as a JSON object, and then send audio data in chunks. The server will respond with the converted speech audio.

Example usage with JavaScript:

```javascript
const socket = new WebSocket('ws://localhost:8000/api/v1/stream-speech-to-speech');

socket.onopen = function(e) {
  console.log("Connection established");
  
  // Send configuration
  socket.send(JSON.stringify({
    stt_model: "whisper-1",
    tts_model: "tts-1",
    voice: "alloy",
    language: "en",
    duration: 10 // Duration in seconds
  }));

  // Start sending audio data
};

socket.onmessage = function(event) {
  if (typeof event.data === 'string') {
    // Handle JSON messages (e.g., transcription updates)
    console.log(`Message: ${event.data}`);
  } else {
    // Handle binary data (converted audio)
    console.log("Received converted audio");
    // Process the audio data
  }
};

// Send audio data
socket.send(audioChunk);
```

The response will include both transcription updates (as JSON) and the final converted audio (as binary data).

Note: For all endpoints, ensure you handle errors appropriately. The server will return appropriate HTTP status codes and error messages in case of any issues.