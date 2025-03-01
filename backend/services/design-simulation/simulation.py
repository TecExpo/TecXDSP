from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Define a model for simulation input
class SimulationRequest(BaseModel):
    simulation_type: str
    parameters: dict

# Sample simulation types and dummy responses
SIMULATION_RESULTS = {
    "FEA": {"stress": random.uniform(100, 500), "strain": random.uniform(0.1, 0.5)},
    "CFD": {"velocity": random.uniform(5, 50), "pressure": random.uniform(1, 10)},
    "Thermal": {"temperature": random.uniform(300, 800)}
}

@app.post("/api/simulations")
def run_simulation(request: SimulationRequest):
    sim_type = request.simulation_type
    
    if sim_type not in SIMULATION_RESULTS:
        raise HTTPException(status_code=400, detail="Unsupported simulation type")
    
    # Simulate results based on the input parameters
    result = SIMULATION_RESULTS[sim_type]
    return {"simulation_type": sim_type, "results": result}
