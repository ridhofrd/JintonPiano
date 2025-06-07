from fastapi import FastAPI, UploadFile, File
import cv2
import mediapipe as mp
import numpy as np
import pygame
import time

app = FastAPI()
mp_hands = mp.solutions.hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
pygame.mixer.init()

# Konfigurasi piano (dari command line)
tuts = {
    "C4": (100, 500, 150, 550),
    "D4": (160, 500, 210, 550),
    "E4": (220, 500, 270, 550),
    "F4": (280, 500, 330, 550),
    "G4": (340, 500, 390, 550),
    "C#4": (130, 480, 138, 485),
    "D#4": (190, 480, 198, 485)
}
sounds = {note: pygame.mixer.Sound(f"sounds/{note}.wav") for note in tuts}
tap_threshold = 20
last_played = {}

@app.post("/play_piano")
async def play_piano(file: UploadFile = File(...)):
    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame, (800, 600))  # Sesuai --shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = mp_hands.process(frame_rgb)
    notes = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x = int(hand_landmarks.landmark[8].x * 800)  # Ujung telunjuk
            y = int(hand_landmarks.landmark[8].y * 600)
            z = hand_landmarks.landmark[8].z * 1000
            for note, (x1, y1, x2, y2) in tuts.items():
                if x1 <= x <= x2 and y1 <= y <= y2 and abs(z) < tap_threshold:
                    if note not in last_played or time.time() - last_played[note] > 0.5:
                        sounds[note].play()
                        last_played[note] = time.time()
                        notes.append(note)
    
    return {"notes_played": notes}