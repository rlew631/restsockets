import asyncio
import logging
import websockets
from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()
connected_clients = {}

@app.get('/api')
async def get_status(request: Request):
    """
    rest server logic
    """
    client_id = request.query_params.get('client_id')
    client = connected_clients[client_id]
    if client:
        print(client)
        # do something real here
    else:
        res = f'client "{client_id}" not found. Available clients: {connected_clients.keys()}'
        logging.warning(
            "recieved bad REST GET request from client"
        )
        raise HTTPException(status_code=500, detail = res)

async def handle_client(websocket, path):
    """
    websocket server logic
    """
    client_name = path.split("/")[1]
    connected_clients[client_name] = websocket
    try:
        async for message in websocket:
            print(f"Received message from {client_name}: {message}")
    finally:
        del connected_clients[client_name]

async def ws_server(port: int):
    """
    start websocket server
    """
    wss = await websockets.serve(handle_client, "0.0.0.0", port)
    await wss.wait_closed()

async def rest_server(port: int):
    """
    start rest server
    """
    uvicorn_config = uvicorn.Config(app, host='0.0.0.0', port=port)
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()

async def main():
    """
    starts rest and websocket servers
    """
    await asyncio.gather(ws_server(port=8765), rest_server(port=6000))

if __name__ == "__main__":
    asyncio.run(main())
