from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import StreamingResponse
import asyncio
import json
import random

app = FastAPI()

# Store active WebSocket connections
active_connections = []

def generate_simulation_data(simulation_type: str):
    """
    Simulates real-time data streaming for different simulation types (FEA, CFD, Thermal).
    Used for HTTP-based streaming with Server-Sent Events (SSE).
    """
    for step in range(1, 11):  # Simulating 10 steps
        data = {
            "step": step,
            "simulation_type": simulation_type,
            "progress": step * 10,
            "result": f"Simulated data for {simulation_type} at step {step}"
        }
        yield f"data: {json.dumps(data)}\n\n"
        asyncio.sleep(1)  # Simulate computation delay

@app.get("/api/simulations")
async def run_simulation(simulation_type: str = Query("fea", enum=["fea", "cfd", "thermal"])):
    """
    API endpoint for real-time simulation updates.
    Supports: FEA, CFD, Thermal Analysis.
    HTTP streaming using Server-Sent Events (SSE).
    """
    return StreamingResponse(generate_simulation_data(simulation_type), media_type="text/event-stream")

@app.websocket("/api/simulations")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket API for real-time simulation updates.
    Simulates live sensor data: temperature, pressure, velocity.
    """
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
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
    """
    Returns the number of active WebSocket connections.
    """
    return {"active_connections": len(active_connections)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
