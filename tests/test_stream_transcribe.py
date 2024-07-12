import asyncio
import websockets
import json
from pydub import AudioSegment

async def send_audio(websocket, audio_data):
    chunk_size = 3200  # 0.1 seconds of 16-bit audio at 16kHz
    for i in range(0, len(audio_data), chunk_size):
        chunk = audio_data[i:i+chunk_size]
        await websocket.send(chunk)
        await asyncio.sleep(0.1)  # Simulate real-time streaming

async def receive_transcriptions(websocket):
    while True:
        try:
            result = await websocket.recv()
            print(json.loads(result))
        except websockets.exceptions.ConnectionClosed:
            break

async def test_stream_transcribe():
    uri = "ws://localhost:8000/api/v1/stream-transcribe"
    async with websockets.connect(uri) as websocket:
        # Load and prepare audio file
        audio = AudioSegment.from_wav("./data/harvard.wav")
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Get raw audio data
        audio_data = audio.raw_data

        # Create tasks for sending audio and receiving transcriptions
        send_task = asyncio.create_task(send_audio(websocket, audio_data))
        receive_task = asyncio.create_task(receive_transcriptions(websocket))

        # Wait for both tasks to complete
        await asyncio.gather(send_task, receive_task)

asyncio.get_event_loop().run_until_complete(test_stream_transcribe())