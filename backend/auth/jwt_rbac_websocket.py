from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import random

# Secret key and algorithm for JWT authentication
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# Simulated user database
fake_users_db = {
    "admin": {"username": "admin", "password": "adminpass", "role": "admin"},
    "user": {"username": "user", "password": "userpass", "role": "user"}
}

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Function to authenticate users
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

# Function to create JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the current user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Role-Based Access Control (RBAC)
def require_role(required_role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user
    return role_dependency

app = FastAPI()

# Authentication Endpoint (OAuth2)
@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

# Protected Route
@app.get("/api/auth/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "Welcome!", "user": user}

# Admin-Only Route
@app.get("/api/auth/admin")
async def admin_route(user: dict = Depends(require_role("admin"))):
    return {"message": "Welcome, Admin!"}

# WebSocket API for Real-Time Simulations
@app.websocket("/api/simulations")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await get_current_user(token)
    if not user:
        await websocket.close()
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
            await asyncio.sleep(1)  # Send data every second
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Get Active WebSocket Clients
@app.get("/api/simulations/clients")
async def get_active_clients():
    return {"active_connections": len(active_connections)}

