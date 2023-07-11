import asyncio
import websockets

async def send_messages():
    uri = "ws://localhost:8765/client1"
    
    async with websockets.connect(uri) as websocket:
        for i in range(1, 6):
            message = f"message {i}"
            await websocket.send(message)
            print(f"Sent message: {message}")
            await asyncio.sleep(1)
        await websocket.close()

# Run the client
asyncio.run(send_messages())
