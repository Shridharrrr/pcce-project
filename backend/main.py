from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes.team_routes import router as team_router
from app.routes.message_routes import router as message_router
from app.routes.user_routes import router as user_router
from app.routes.todo_routes import router as todo_router
from app.routes.summary_routes import router as summary_router
from app.services.websocket_service import websocket_endpoint
from app.dependencies.auth import get_current_user
from app.services.firestore_service import get_user_teams

app = FastAPI(title="Workspace Management API", version="1.0.0")

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
app.include_router(user_router)
app.include_router(team_router)
app.include_router(message_router)
app.include_router(todo_router)
app.include_router(summary_router)

# WebSocket endpoint
@app.websocket("/ws/{team_id}")
async def websocket_route(websocket: WebSocket, team_id: str, token: str):
    await websocket_endpoint(websocket, team_id, token)

@app.get("/")
async def root():
    return {"message": "Workspace Management API is running..."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.get("/me/teams")
async def get_my_teams(current_user: dict = Depends(get_current_user)):
    """Get all teams for the current user"""
    user_id = current_user.get("uid")
    teams = get_user_teams(user_id)
    return teams

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)