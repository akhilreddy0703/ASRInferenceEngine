import asyncio
import websockets
import json
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

async def send_audio(websocket):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording")

    try:
        while True:
            data = stream.read(CHUNK)
            await websocket.send(data)
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("* Stopped recording")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def receive_transcriptions(websocket):
    current_line = ""
    try:
        while True:
            result = await websocket.recv()
            word_data = json.loads(result)
            if "word" in word_data:
                current_line += word_data["word"] + " "
                print(f"\rCurrent transcription: {current_line}", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection closed")

async def main():
    uri = "ws://localhost:8000/api/v1/stream-transcribe"
    async with websockets.connect(uri) as websocket:
        send_task = asyncio.create_task(send_audio(websocket))
        receive_task = asyncio.create_task(receive_transcriptions(websocket))
        
        await asyncio.gather(send_task, receive_task)

if __name__ == "__main__":
    asyncio.run(main())