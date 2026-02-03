import cv2
import base64
import numpy as np
import mediapipe as mp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


# ---------------- MediaPipe setup ----------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# ---------------- State variables ----------------
stage = None
counter = 0

# ---------------- Utility functions ----------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

def decode_base64_frame(data: str):
    """
    data: base64 JPEG string from frontend
    returns: OpenCV BGR frame
    """
    img_bytes = base64.b64decode(data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return frame    


def check_lunge(landmarks, counter, stage):
    feedback = []

    back_knee  = calculate_angle(
        [landmarks[23].x, landmarks[23].y],
        [landmarks[25].x, landmarks[25].y],
        [landmarks[27].x, landmarks[27].y]
    )
    front_knee = calculate_angle(
        [landmarks[24].x, landmarks[24].y],
        [landmarks[26].x, landmarks[26].y],
        [landmarks[28].x, landmarks[28].y]
    )

    good = True

    if front_knee > 110:
        feedback.append("Lower your front knee more")
        good = False

    if back_knee < 20:
        feedback.append("Keep your back leg straighter")
        good = False

    if abs(front_knee - back_knee) < 20:
        feedback.append("Shift more weight to the front leg")
        good = False

    if good:
        feedback.append("Good lunge posture")

    if front_knee > 160 and back_knee > 160:
        stage = "down"

    if front_knee < 95 and back_knee > 20 and stage == "down":
        stage = "up"
        counter += 1

    return good, feedback, counter, stage, front_knee, back_knee
async def lunges(websocket:WebSocket):
    global stage, counter,good,feedback,color,symbol
    await websocket.accept()
    stage="down"
    counter=0
    good = "NO POSE"
    feedback = ""
    symbol="down"
    color = (255, 255, 255)
    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        try:
             while True:
                data = await websocket.receive_text()
                frame = decode_base64_frame(data)
                if frame is None:
                    continue

                frame = cv2.resize(frame, (800, 480))
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False
                results = pose.process(image_rgb)

                image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)


                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    good_bool, feedback_list, counter, stage, fk, bk = check_lunge(
                        landmarks, counter, stage
                    )

                    good = "GOOD" if good_bool else "BAD"
                    feedback = " | ".join(feedback_list)
                    color = (0, 255, 0) if good_bool else (0, 0, 255)
                    mid1 = [landmarks[25].x,landmarks[25].y]
                    mid2 = [landmarks[26].x,landmarks[26].y]
                    symbol="up" if stage=="up" else "down"
                    # Calculate angle
                    left_knee = calculate_angle([landmarks[23].x, landmarks[23].y],[landmarks[25].x, landmarks[25].y],[landmarks[27].x, landmarks[27].y])

                    right_knee = calculate_angle( [landmarks[24].x, landmarks[24].y],[landmarks[26].x, landmarks[26].y],[landmarks[28].x, landmarks[28].y])

                    # Draw angles
                    cv2.putText(image, str(left_knee), 
                           tuple(np.multiply(mid1, [800, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA
                                )
                    cv2.putText(image, str(right_knee), 
                           tuple(np.multiply(mid2, [800, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA
                                )
                    # Curl counter logic
                    cv2.rectangle(image, (0,0), (100,73), color, -1)
                    cv2.rectangle(image, (340,0), (800,73), color, -1)            
                    cv2.rectangle(image, (610,480), (800,440), (245,117,16), -1)  

                    # Draw landmarks
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2),
                        mp_drawing.DrawingSpec(color=color, thickness=2)
                    )

                # UI overlays
                

                cv2.putText(image, good, 
                    (10,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
                cv2.putText(image, feedback, 
                    (360,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)

                cv2.putText(image, symbol, 
                    (620,470), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2, cv2.LINE_AA)            
        
                cv2.putText(image, str(counter), 
                    (750,470), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2, cv2.LINE_AA)
                # Encode frame
                _, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                frame_base64 = base64.b64encode(buffer).decode("utf-8")

                # 🔥 SEND FRAME + DATA TO FRONTEND
                await websocket.send_json({
                    "frame": frame_base64,
                    "good": good,
                    "feedback": feedback,
                    "counter": counter,
                    "stage": stage
                    })


        finally:
            cap.release()

