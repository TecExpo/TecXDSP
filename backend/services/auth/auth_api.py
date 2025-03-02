from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import asyncio
import random

# JWT Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

app = FastAPI()

# Simulated user database
users_db: Dict[str, Dict] = {
    "admin@example.com": {"username": "admin", "password": "adminpass", "role": "admin"},
    "user@example.com": {"username": "user", "password": "userpass", "role": "user"},
}

# Active WebSocket Connections
active_connections: List[WebSocket] = []

# Function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to verify JWT token
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
def require_role(role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user
    return role_dependency

# Authentication Route
@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route for Authenticated Users
@app.get("/api/auth/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "Welcome!", "user": user}

# Admin Only Route
@app.get("/api/auth/admin")
async def admin_route(user: dict = Depends(require_role("admin"))):
    return {"message": "Welcome, Admin!"}

# WebSocket for Real-Time Simulation
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
                "timestamp": datetime.utcnow().isoformat(),
                "temperature": round(random.uniform(20, 100), 2),
                "pressure": round(random.uniform(1, 10), 2),
                "velocity": round(random.uniform(0, 200), 2),
            }
            await websocket.send_json(simulation_data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# API to Check Active WebSocket Clients
@app.get("/api/simulations/clients")
async def get_active_clients():
    return {"active_connections": len(active_connections)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
