import asyncio
import websockets
import time
from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import json

# Initialize Whisper model with 'small' size for balance between performance and accuracy
model = WhisperModel("small", compute_type="int8")

async def transcribe_audio():
    # Record and transcribe audio in real-time
    audio = record_chunk(duration=3, fs=16000)
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        wav.write(f.name, 16000, audio)
        segments, _ = model.transcribe(f.name)
        for seg in segments:
            return seg.text
    return ""

def record_chunk(duration, fs):
    # Record audio chunk with specified duration and sample rate
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio

async def caption_stream(websocket):
    try:
        # Send connection confirmation message
        await websocket.send(json.dumps({
            "type": "connection",
            "status": "connected"
        }))
        
        # Main caption loop
        while True:
            caption_text = await transcribe_audio()
            if caption_text:
                # Send caption data to client
                await websocket.send(json.dumps({
                    "type": "caption",
                    "text": caption_text,
                    "timestamp": time.time()
                }))
    except websockets.exceptions.ConnectionClosed:
        # Handle client disconnection gracefully
        pass

async def main():
    # Start WebSocket server with specific configurations
    async with websockets.serve(
        caption_stream,
        "0.0.0.0",  # Allow connections from any IP
        8765,       # Port number
        ping_interval=None,  # Disable automatic ping
        ping_timeout=None    # Disable ping timeout
    ) as server:
        print("🎙️ Caption server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # Keep server running indefinitely

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(main())
