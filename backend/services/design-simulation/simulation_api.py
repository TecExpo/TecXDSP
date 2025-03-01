from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
import asyncio
import json
import random

# Secret key for JWT signing
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

# OAuth2 scheme for handling token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database (hashed password for "password")
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode(),
        "role": "admin"
    }
}

# Store active WebSocket connections
active_connections = []

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    """
    Verifies if the plain password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def authenticate_user(username: str, password: str):
    """
    Authenticates a user by checking credentials.
    """
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validates JWT token and returns the user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = fake_users_db.get(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to generate JWT access tokens.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

def generate_simulation_data(simulation_type: str):
    """
    Simulates real-time data streaming for different simulation types (FEA, CFD, Thermal).
    Used for HTTP-based streaming with Server-Sent Events (SSE).
    """
    for step in range(1, 11):
        data = {
            "step": step,
            "simulation_type": simulation_type,
            "progress": step * 10,
            "result": f"Simulated data for {simulation_type} at step {step}"
        }
        yield f"data: {json.dumps(data)}\n\n"
        asyncio.sleep(1)

@app.get("/api/simulations")
async def run_simulation(simulation_type: str = Query("fea", enum=["fea", "cfd", "thermal"]), user: dict = Depends(get_current_user)):
    """
    API endpoint for real-time simulation updates.
    Supports: FEA, CFD, Thermal Analysis.
    HTTP streaming using Server-Sent Events (SSE).
    Requires JWT authentication.
    """
    return StreamingResponse(generate_simulation_data(simulation_type), media_type="text/event-stream")

@app.websocket("/api/simulations")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    """
    WebSocket API for real-time simulation updates.
    Requires a valid JWT token as a query parameter.
    """
    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            await websocket.close(code=1008)
            return
    except jwt.PyJWTError:
        await websocket.close(code=1008)
        return

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
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/api/simulations/clients")
async def get_active_clients(user: dict = Depends(get_current_user)):
    """
    Returns the number of active WebSocket connections.
    Requires JWT authentication.
    """
    return {"active_connections": len(active_connections)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
