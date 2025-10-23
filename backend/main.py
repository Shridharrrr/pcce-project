from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes.team_routes import router as team_router
from app.routes.message_routes import router as message_router
from app.routes.user_routes import router as user_router
from app.services.websocket_service import websocket_endpoint

app = FastAPI(title="Planora API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(team_router)
app.include_router(message_router)
app.include_router(user_router)

# WebSocket endpoint
@app.websocket("/ws/{team_id}")
async def websocket_route(websocket: WebSocket, team_id: str, token: str):
    await websocket_endpoint(websocket, team_id, token)

@app.get("/")
async def root():
    return {"message": "Planora API is running..."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)