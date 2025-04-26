from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import tensorflow as tf
import cv2
import numpy as np

# Load the model
def load_detection_model(model_path):
    model = tf.saved_model.load(model_path).signatures['serving_default']
    return model

# FastAPI app
app = FastAPI()

model_path = "path_to_your_model"
detection_model = load_detection_model(model_path)

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Resize and process frame for detection
        frame_resized = cv2.resize(frame, (640, 640))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        input_tensor = tf.convert_to_tensor(frame_rgb)[tf.newaxis, ...]
        output_dict = detection_model(input_tensor)

        # Process detections (similar to your existing logic)
        detected_objects = []
        for i in range(int(output_dict['num_detections'][0])):
            score = output_dict['detection_scores'][0][i].numpy()
            if score > 0.5:
                box = output_dict['detection_boxes'][0][i].numpy()
                detected_objects.append(box)

        # Send detected objects to frontend
        await websocket.send_text(f"{len(detected_objects)} objects detected")

    cap.release()
