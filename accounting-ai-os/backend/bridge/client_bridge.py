import asyncio
import json
import subprocess
import websockets
from typing import Dict

COMMAND_MAP = {
    "open_calculator": "calc",
    "open_notepad": "notepad",
    "list_files": "dir",
    "open_explorer": "explorer .",
    "system_info": "systeminfo"
}

async def local_bridge_client():
    uri = "ws://localhost:8080/ws/bridge"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to AI Accounting OS Server...")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    action = data.get("action")
                    if action in COMMAND_MAP:
                        cmd = COMMAND_MAP[action]
                        subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(local_bridge_client())
