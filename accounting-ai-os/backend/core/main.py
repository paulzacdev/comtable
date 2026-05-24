import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from agents.collector import collector
from agents.auditor import auditor
from agents.analyst import analyst

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTHORIZED_COMMANDS = {
    "open_calculator": "calc",
    "open_notepad": "notepad",
    "list_files": "dir",
    "open_explorer": "explorer .",
    "system_info": "systeminfo"
}

class CommandRequest(BaseModel):
    command_id: str
    action: str
    params: Dict = {}

class BridgeManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_command(self, command_id: str, action: str):
        payload = json.dumps({"command_id": command_id, "action": action})
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except:
                pass

bridge_manager = BridgeManager()

@app.websocket("/ws/bridge")
async def websocket_endpoint(websocket: WebSocket):
    await bridge_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        bridge_manager.disconnect(websocket)

@app.post("/api/execute")
async def execute_action(request: CommandRequest):
    if request.action in AUTHORIZED_COMMANDS:
        await bridge_manager.send_command(request.command_id, request.action)
        return {"status": "command_sent", "action": request.action}
    return {"status": "error", "message": "Action not authorized"}, 403

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # Simulate OCR reading the file content
    content = await file.read()
    simulated_text = f"Invoice for Client A. Amount: 500 USD. Tax: 50 USD. Date: 2026-05-14. Vendor: CloudServices Inc."

    # 1. Collection
    extracted = collector.process_document(simulated_text)

    # 2. Auditing
    audit = auditor.audit_transaction(extracted)

    # 3. Analysis
    insight = analyst.analyze_trend([extracted])

    return {
        "filename": file.filename,
        "extracted": extracted,
        "audit": audit,
        "insight": insight
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
