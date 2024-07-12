# Inference Server for ASR models

## Overview

This is a FastAPI-based server that acts as a interface between your application and cloud-based AI services. It focuses on three main tasks:

1. Converting speech to text (transcription)
2. Converting text to speech
3. Converting speech to speech (a combination of the above two)

Currently, it uses OpenAI's API for these services, but it's designed so we can add other providers in the future.

## Features

1. **Transcription (Speech-to-Text)**
   - Asynchronous file upload and transcription
   - Streaming transcription via WebSocket

2. **Text-to-Speech**
   - Convert text to speech with various voice options

3. **Speech-to-Speech**
   - Convert speech input to text and then back to speech
   - Support for both file upload and streaming via WebSocket

## Project Structure

```
.
├── cloud_providers/
│   ├── base.py
│   └── openai_api_handler.py
├── server/
│   ├── main.py
│   ├── routers/
│   │   ├── transcribe.py
│   │   ├── tts.py
│   │   └── speech_to_speech.py
│   └── utils/
│       └── logger.py
|
└── requirements.txt
└── README.md
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
    
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
   ```
   pip install -r requirements
   ```
4. Set up environment variables:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   ```


## Starting the Server

To start the server, navigate to the project directory and run:

```
python server/main.py
```

This will start the FastAPI server, typically on `http://localhost:8000`.

- For more details about API check [`API docs`](./docs/api.md)

## Logging

The application uses rotating file handlers for logging, with separate log files for different components:

- `logs/main.log`: Main application logs
- `logs/transcription.log`: Transcription-specific logs
- `logs/tts.log`: Text-to-speech logs
- `logs/speech_to_speech.log`: Speech-to-speech logs

## Error Handling

The application includes error handling for various scenarios, including API errors and WebSocket disconnections. Errors are logged and appropriate HTTP exceptions are raised.

## Extensibility

The project is designed with extensibility in mind. The `CloudProviderBase` abstract base class in `base.py` allows for easy integration of additional cloud providers beyond OpenAI.

## Security Considerations

- Ensure that your OpenAI API key is kept secure and not exposed in the code or version control.
- The server currently allows all origins in CORS settings. In a production environment, you should restrict this to specific allowed origins.

## Future Improvements

1. Add support for additional cloud providers (e.g., Google Cloud, Azure)
2. Add more configuration options for the AI models
3. Improve error handling and provide more detailed error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]
