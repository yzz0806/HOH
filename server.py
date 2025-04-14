# server.py
import asyncio
import websockets

async def handler(websocket, path):
    print("✅ Client connected")
    try:
        async for message in websocket:
            print(f"📥 Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed:
        print("🔌 Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
