# 🏋️‍♂️ REPRIGHT — AI-Powered Exercise Posture Tracking Web App

REPRIGHT is a **computer vision and AI/ML based web application** that acts as a virtual gym trainer. Using just a webcam, it continuously monitors a user’s exercise posture, provides real-time corrective feedback, visualizes body landmarks and joint angles, and automatically counts repetitions — helping users train **safely and correctly without a personal trainer**.

---

## 🔥 Inspiration

One day, while scrolling through social media reels, I came across a video of a person performing a leg press where his **knee joints suddenly broke** due to incorrect posture. It was extremely traumatizing to watch. What stayed with me was the thought that this injury could have been avoided if someone had told him that his posture was wrong — that he shouldn’t completely lock his legs or extend them close to **180 degrees**.

That moment made me realize how many people work out alone without guidance. Not everyone can afford a premium gym with a personal trainer assigned at all times. This led to the idea of **REPRIGHT** — an AI-powered virtual trainer that watches every rep, detects unsafe posture in real time, and gives instant corrective feedback.

---

## 🚀 What REPRIGHT Does

REPRIGHT continuously analyzes exercise posture in real time using the camera and provides actionable feedback:

- Captures live camera feed from the browser  
- Streams frames to the backend using **WebSockets**  
- Detects body landmarks using **MediaPipe**  
- Calculates critical joint angles for each exercise  
- Evaluates posture as good or bad in real time  
- Displays corrective feedback like  
  *“bend your knees more”*, *“keep your back straight”*  
- Tracks movement phases (up/down) to automatically count reps  
- Visualizes landmarks and joint angles for better understanding  

Supported exercises:
- Squats  
- Lunges  
- Push-ups  

---

## 🛠️ How We Built It

- **Frontend** captures camera feed and sends frames to the backend using WebSockets  
- **Backend** processes each frame in real time using:
  - MediaPipe for pose detection  
  - OpenCV for frame processing and visualization  
  - NumPy for angle calculations  
- Exercise-specific posture rules generate meaningful feedback  
- Movement tracking logic detects upward and downward motion to count reps  
- Processed frames and feedback are streamed back to the frontend instantly  

This continuous WebSocket loop ensures **low latency and real-time responsiveness**.

---

## 🧰 Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- WebSocket client
- Browser camera APIs

### Backend
- Python
- FastAPI
- WebSockets
- OpenCV
- MediaPipe
- NumPy

---


## ⚙️ Installation & Running the Project

### ✅ Prerequisites
- Python 3.9 or higher
- A device with a working webcam
- A modern web browser (Google Chrome recommended)

---

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/repright.git
cd repright
```

###2️⃣ Create and Activate a Virtual Environment
``` 
python -m venv venv
venv\Scripts\activate
```
###3️⃣ Install Backend Dependencies
```
cd backend
pip install -r requirements.txt
```
###4️⃣ Run the Backend Server
```
uvicorn main:app --reload

```
Once started, the backend will be available at:

```
http://127.0.0.1:8000
```
5️⃣ Run the Frontend

Navigate to the frontend folder

Open index.html in a web browser

Allow camera access when prompted

Select an exercise and start performing reps
