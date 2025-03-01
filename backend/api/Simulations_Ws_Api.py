from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import random

app = FastAPI()

# Store active WebSocket connections
active_connections = []

@app.websocket("/api/simulations")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Simulate real-time simulation data
            simulation_data = {
                "timestamp": asyncio.get_event_loop().time(),
                "temperature": round(random.uniform(20, 100), 2),
                "pressure": round(random.uniform(1, 10), 2),
                "velocity": round(random.uniform(0, 200), 2)
            }
            await websocket.send_json(simulation_data)
            await asyncio.sleep(1)  # Send data every second
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/api/simulations/clients")
async def get_active_clients():
    return {"active_connections": len(active_connections)}
