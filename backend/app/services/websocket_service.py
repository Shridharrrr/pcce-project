from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import List, Dict
import json
import asyncio
from app.dependencies.auth import get_current_user_websocket
from app.services.firestore_service import create_document, get_document, update_document, get_team_messages
from app.models.message import Message, MessageCreate, MessageStatus
from datetime import datetime
import uuid

class ConnectionManager:
    def __init__(self):
        # Dictionary to store active connections by team_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Dictionary to store user info for each connection
        self.user_connections: Dict[WebSocket, Dict] = {}

    async def connect(self, websocket: WebSocket, team_id: str, user_info: Dict):
        """Accept a WebSocket connection and add to team room"""
        await websocket.accept()
        
        if team_id not in self.active_connections:
            self.active_connections[team_id] = []
        
        self.active_connections[team_id].append(websocket)
        self.user_connections[websocket] = user_info
        
        # Send join notification to other team members
        await self.broadcast_to_team(team_id, {
            "type": "user_joined",
            "user": user_info,
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_websocket=websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        user_info = self.user_connections.get(websocket)
        if user_info:
            # Find which team this connection belongs to
            for team_id, connections in self.active_connections.items():
                if websocket in connections:
                    connections.remove(websocket)
                    
                    # Send leave notification to other team members
                    asyncio.create_task(self.broadcast_to_team(team_id, {
                        "type": "user_left",
                        "user": user_info,
                        "timestamp": datetime.utcnow().isoformat()
                    }))
                    break
            
            del self.user_connections[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        await websocket.send_text(message)

    async def broadcast_to_team(self, team_id: str, message: Dict, exclude_websocket: WebSocket = None):
        """Broadcast a message to all connections in a team"""
        if team_id in self.active_connections:
            for connection in self.active_connections[team_id]:
                if connection != exclude_websocket:
                    try:
                        await connection.send_text(json.dumps(message))
                    except:
                        # Connection is closed, remove it
                        self.disconnect(connection)

    async def broadcast_message_to_team(self, team_id: str, message_data: Dict):
        """Broadcast a chat message to all team members"""
        await self.broadcast_to_team(team_id, {
            "type": "new_message",
            "message": message_data,
            "timestamp": datetime.utcnow().isoformat()
        })

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, team_id: str, token: str):
    """WebSocket endpoint for real-time chat"""
    try:
        # Verify user authentication
        user_info = await get_current_user_websocket(token)
        if not user_info:
            await websocket.close(code=1008, reason="Authentication failed")
            return

        # Verify user is member of the team
        team = get_document("teams", team_id)
        if not team:
            await websocket.close(code=1008, reason="Team not found")
            return

        user_id = user_info.get("uid")
        is_member = (team.get("admin_id") == user_id or 
                    any(member.get("user_id") == user_id for member in team.get("members", [])))
        
        if not is_member:
            await websocket.close(code=1008, reason="Access denied")
            return

        # Connect to the team room
        await manager.connect(websocket, team_id, user_info)

        # Send recent messages to the newly connected user
        recent_messages = get_team_messages(team_id, 20)
        await manager.send_personal_message(json.dumps({
            "type": "recent_messages",
            "messages": recent_messages
        }), websocket)

        # Listen for messages
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                if message_data.get("type") == "chat_message":
                    # Create and save the message
                    message_id = str(uuid.uuid4())
                    message = Message(
                        messageId=message_id,
                        teamId=team_id,
                        senderId=user_id,
                        sender_email=user_info.get("email"),
                        sender_name=user_info.get("name", user_info.get("email", "").split("@")[0]),
                        content=message_data.get("content", ""),
                        message_type="text",
                        status=MessageStatus.SENT,
                        created_at=datetime.utcnow()
                    )
                    
                    # Save to database
                    create_document("messages", message_id, message.dict())
                    
                    # Update team's last message timestamp
                    update_document("teams", team_id, {"last_message_at": datetime.utcnow()})
                    
                    # Broadcast to all team members
                    await manager.broadcast_message_to_team(team_id, message.dict())
                
                elif message_data.get("type") == "typing":
                    # Broadcast typing indicator
                    await manager.broadcast_to_team(team_id, {
                        "type": "typing",
                        "user": user_info,
                        "is_typing": message_data.get("is_typing", False),
                        "timestamp": datetime.utcnow().isoformat()
                    }, exclude_websocket=websocket)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await manager.send_personal_message(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }), websocket)
            except Exception as e:
                await manager.send_personal_message(json.dumps({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                }), websocket)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)