from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List
import random
import asyncio

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

app = FastAPI()
active_connections = []
users_db = {
    "user@example.com": {"username": "user", "password": "hashedpassword", "role": "user"},
    "admin@example.com": {"username": "admin", "password": "hashedpassword", "role": "admin"},
}

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return users_db.get(username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != "password":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

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
            simulation_data = {"timestamp": asyncio.get_event_loop().time(), "temperature": round(random.uniform(20, 100), 2)}
            await websocket.send_json(simulation_data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/api/simulations/clients")
async def get_active_clients():
    return {"active_connections": len(active_connections)}
