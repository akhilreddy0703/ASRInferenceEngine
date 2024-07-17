# Speech Processing API Backend

This FastAPI-based backend provides endpoints for speech-to-text, text-to-speech, and speech-to-speech conversions using various cloud provider APIs.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Documentation](#api-documentation)
4. [Configuration](#configuration)
5. [Cloud Provider Integration](#cloud-provider-integration)

## Installation

[Installation instructions remain unchanged]

## Usage

The API provides several endpoints for speech processing tasks. All endpoints require an API key for authentication, which should be passed in the `Authorization` header as a Bearer token.

## API Documentation

### 1. File Transcription

**Endpoint**: `POST /api/v1/transcribe`

**Description**: Transcribe an uploaded audio file to text.

**curl Example**:
```bash
curl -X POST http://localhost:8000/api/v1/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@/path/to/audio.mp3" \
  -F "model=whisper-1" \
  -F "language=en"
```

**Response**:
```json
{
  "text": "This is the transcribed text."
}
```

### 2. Live Transcription

**Endpoint**: `WebSocket /api/v1/stream-transcribe`

**Description**: Perform real-time transcription of streaming audio data.

**Example using wscat**:
```bash
wscat -c ws://localhost:8000/api/v1/stream-transcribe
> {"api_key": "YOUR_API_KEY", "model": "whisper-1", "language": "en"}
> [Binary audio data]
```

**Response**:
```json
{"text": "Partial transcription..."}
```

### 3. Text-to-Speech

**Endpoint**: `POST /api/v1/text-to-speech`

**Description**: Convert text to speech.

**curl Example**:
```bash
curl -X POST http://localhost:8000/api/v1/text-to-speech \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello, this is a test.&voice=alloy&model=tts-1" \
  --output speech.mp3
```

**Response**: Audio file (speech.mp3)

### 4. Speech-to-Speech

**Endpoint**: `POST /api/v1/speech-to-speech`

**Description**: Convert speech to text and then back to speech, optionally with a different voice.

**curl Example**:
```bash
curl -X POST http://localhost:8000/api/v1/speech-to-speech \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@/path/to/input_audio.mp3" \
  -F "stt_model=whisper-1" \
  -F "tts_model=tts-1" \
  -F "voice=alloy" \
  -F "show_intermediate=true" \
  --output output_speech.mp3
```

**Response**: 
- Audio file (output_speech.mp3)
- Header `X-Transcription` containing the intermediate transcription (if `show_intermediate=true`)

## Configuration

[Configuration instructions remain unchanged]

## Cloud Provider Integration

[Cloud Provider Integration instructions remain unchanged]

For more detailed information on the API implementation, refer to the source code and inline documentation.