# How do I test the APIs ?
To use these test scripts:


1. Install the required testing libraries if you haven't already:
   ```
   pip install pytest pytest-asyncio
   ```
2. Run the tests using pytest:
   ```
   pytest test_api.py
   ```

Here's a breakdown of the test cases:

1. `test_transcribe`: Tests the file transcription endpoint.
2. `test_text_to_speech`: Tests the text-to-speech conversion endpoint.
3. `test_speech_to_speech`: Tests the speech-to-speech conversion endpoint.
4. `test_stream_transcribe`: Tests the WebSocket endpoint for live transcription.
5. `test_root`: Tests the root endpoint of the API.

These tests cover the basic functionality of each endpoint. They use mock data and don't make actual calls to external APIs, which is suitable for unit testing. For integration testing, you'd need to set up test API keys and potentially use real audio files.

- Testing with invalid API keys
- Testing with unsupported file formats
- Testing with very large files
- Testing rate limiting if implemented
- Testing various error conditions for each endpoint

## TODO
consider setting up a CI/CD pipeline that runs these tests automatically whenever changes are pushed to your repository.