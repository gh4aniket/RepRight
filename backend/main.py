import cv2
import base64
import numpy as np
import mediapipe as mp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from lunges import lunges
from squats import squats
from pushup import pushups
# ---------------- FastAPI setup ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------- WebSocket endpoint ----------------
@app.websocket("/ws/lunges")
async def video_stream(websocket: WebSocket):
   await lunges(websocket)

@app.websocket("/ws/squats")
async def video_stream(websocket: WebSocket):
   await squats(websocket)   

@app.websocket("/ws/push")
async def video_stream(websocket: WebSocket):
   await pushups(websocket)    