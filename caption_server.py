import asyncio
import websockets
import json
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import time
from faster_whisper import WhisperModel

# Load the whisper model (adjust size based on speed/accuracy needs)
model = WhisperModel("small", compute_type="int8")  # or "tiny", "small"

# Record audio from mic
def record_audio_chunk(duration, fs):
    print(f"🎤 Recording {duration} seconds of audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    #print("Audio dtype:", audio.dtype, "Shape:", audio.shape, "Sample:", audio[0:10])
    sd.wait()
    return audio, fs

# Transcribe the recorded audio using faster-whisper
def transcribe_audio(audio, fs):
    text_segments = []
    #print(f"📥 Raw audio shape: {audio.shape}, dtype: {audio.dtype}")

    # ✅ Force to mono 1D shape
    audio = np.squeeze(audio)
    #print(f"✅ Squeezed audio shape: {audio.shape}, dtype after squeeze: {audio.dtype}")

    # ✅ Ensure correct dtype
    if audio.dtype != np.int16:
        audio = (audio * 32767).astype(np.int16)
        #print("✅ Converted audio to int16")

    #print("🎧 First 10 samples:", audio[:10])

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmpfile:
        wav.write(tmpfile.name, fs, audio)

        segments, _ = model.transcribe(tmpfile.name)

        for seg in segments:
            print(f"📃 [{seg.start:.2f}s – {seg.end:.2f}s]: {seg.text}")
            text_segments.append(seg.text)
        #text = {seg.start:.2f}s – {seg.end:.2f}s]: {seg.text}
        # if text:
        #     print(f"📜 Final transcription: {text}")
        # else:
        #     print(f"⚠️ Low-confidence or short speech: '{text}'")
        text = ''.join(text_segments).strip()
        print(f"🧩 Combined text: {text}")
        return text



# Store all connected WebSocket clients
connected_clients = set()

# Handle individual WebSocket connection
async def handle_client(websocket):
    connected_clients.add(websocket)
    print("✅ Client connected")

    await websocket.send(json.dumps({
        "type": "connection",
        "status": "connected"
    }))

    try:
        async for _ in websocket:
            pass  # Clients are passive listeners
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print("❌ Client disconnected")

# Transcribe and broadcast in loop
async def broadcaster():
    while True:
        audio, fs = record_audio_chunk(duration=4, fs=16000)
        text = transcribe_audio(audio, fs)

        if text:
            message = json.dumps({
                "type": "caption",
                "text": text,
                "timestamp": time.time()
            })
            print(f"📢 Broadcasting: {text}")
            if connected_clients:
                await asyncio.gather(*[client.send(message) for client in connected_clients])
        else:
            print("⚠️ No meaningful speech detected.")

        await asyncio.sleep(0.1)

# Start the WebSocket server and broadcaster
async def main():
    print("🎙️ Caption server running on ws://0.0.0.0:8765")
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await broadcaster()

if __name__ == "__main__":
    asyncio.run(main())
