from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

def generate_simulation_data(simulation_type: str):
    """
    Simulates real-time data streaming for different simulation types.
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
    """
    return StreamingResponse(generate_simulation_data(simulation_type), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
