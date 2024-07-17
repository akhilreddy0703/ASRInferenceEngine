# Speech Processing API Backend

This FastAPI-based backend provides endpoints for speech-to-text, text-to-speech, and speech-to-speech conversions using various cloud provider APIs.

## Table of Contents

1. [Usage](#usage)
2. [Configuration](#configuration)
3. [Cloud Provider Integration](#cloud-provider-integration)
4. [Testing](#testing)

## Usage

The API provides several endpoints for speech processing tasks. All endpoints require an API key for authentication, which should be passed in the `Authorization` header as a Bearer token.

### 1. File Transcription

**Endpoint**: `POST /api/v1/transcribe`

**Description**: Transcribe an uploaded audio file to text.

**curl Example**:
```bash
curl -X POST "${BASE_URL}/api/v1/transcribe" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio/file.wav" \
     -F "model=whisper-1" \
     -F "language=en" \
     -F "response_format=json"
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
wscat -H "Authorization: Bearer ${API_KEY}" -c "${BASE_URL}/api/v1/stream-transcribe"
> {"sttModel": "whisper-1", "language": "en", "response_format": "json"}
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
curl -X POST "${BASE_URL}/api/v1/text-to-speech" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, this is a test." \
     -d "voice=alloy" \
     -d "model=tts-1" \
     -d "response_format=mp3" \
     -d "speed=1.0" \
     --output speech.mp3
```

**Response**: Audio file (speech.mp3)

### 4. Speech-to-Speech

**Endpoint**: `POST /api/v1/speech-to-speech`

**Description**: Convert speech to text and then back to speech, optionally with a different voice.

**curl Example**:
```bash
curl -X POST "${BASE_URL}/api/v1/speech-to-speech" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio/file.wav" \
     -F "stt_model=whisper-1" \
     -F "tts_model=tts-1" \
     -F "voice=alloy" \
     -F "language=en" \
     -F "stt_response_format=json" \
     -F "tts_response_format=mp3" \
     --output output_speech.mp3
```

**Response**: 
- Audio file (output_speech.mp3)
- JSON response containing the transcription and audio data:
```json
{
  "transcription": "This is the transcribed text.",
  "audio": "base64_encoded_audio_data"
}
```

### 5. LLM (Language Model) Call

**Endpoint**: `POST /api/v1/llm`

**Description**: Generate text using a language model.

**curl Example**:
```bash
curl -X POST "${BASE_URL}/api/v1/llm" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Complete this sentence: The quick brown fox" \
     -d "model=gpt-3.5-turbo"
```

**Response**:
```json
{
  "text": "The quick brown fox jumps over the lazy dog."
}
```

## Configuration

The API can be configured using environment variables or a configuration file. Key configuration options include:

- `OPENAI_API_KEY`: Your OpenAI API key
- `STT_MODEL`: Default speech-to-text model (e.g., "whisper-1")
- `TTS_MODEL`: Default text-to-speech model (e.g., "tts-1")
- `DEFAULT_VOICE`: Default voice for text-to-speech (e.g., "alloy")
- `DEFAULT_LANGUAGE`: Default language for speech recognition (e.g., "en")
- `STT_RESPONSE_FORMAT`: Default response format for speech-to-text (e.g., "json")
- `TTS_RESPONSE_FORMAT`: Default response format for text-to-speech (e.g., "mp3")

## Cloud Provider Integration

Currently, the API supports OpenAI's speech processing services. Integration with other cloud providers (AWS, Azure, GCP) is planned for future releases.

For more detailed information on the API implementation, refer to the source code and inline documentation.

## Testing

### Setup

Before running the test scripts, set up your environment variables:

```bash
export BASE_URL="http://localhost:8000"  # Replace with your actual API base URL
export API_KEY="your_api_key_here"       # Replace with your actual API key
```

### Running Tests

Each API endpoint has a corresponding test script in the `testing/` directory. To run a test, navigate to the `testing/` directory and execute the desired script. For example:

```bash
cd testing
./test_transcribe.sh
```

### Test Scripts

1. **File Transcription**: [`test_transcribe.sh`](../testing/test_transcribe.sh)
2. **Live Transcription**: [`test_live_transcription.sh`](../testing/test_live_transcription.sh)
(**Note** : This requires a WebSocket client)
3. **Text-to-Speech**: [`test_tts.sh`](../testing/test_tts.sh)
4. **Speech-to-Speech**: [`test_v2v.sh`](../testing/test_v2v.sh)
5. **LLM Call**: [`test_llm.sh`](../testing/test_llm.sh)

Each test script sends requests to the corresponding API endpoint and checks for expected responses. Make sure to review and modify the scripts as needed, especially for file paths and specific test cases.

### Troubleshooting

- Ensure the API server is running before executing tests.
- Check that `BASE_URL` and `API_KEY` environment variables are set correctly.
- Verify file paths for any audio files used in tests.
- For WebSocket tests, ensure you have the necessary WebSocket client installed.

### Security Note

While using environment variables is more secure than hardcoding API keys, still be cautious when working with sensitive information. Ensure you're working in a secure environment and avoid sharing your terminal history or environment variables with others.

For more detailed information on the API implementation, refer to the source code and inline documentation.