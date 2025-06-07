import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from playsound import playsound
import time

# Inisialisasi MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, model_complexity=1)

# Konfigurasi piano
tuts = {
    'C4': (100, 500, 150, 550),  # x1, y1, x2, y2
    'D4': (160, 500, 210, 550),
    'E4': (220, 500, 270, 550),
    'F4': (280, 500, 330, 550),
    'G4': (340, 500, 390, 550),
    'C#4': (130, 480, 138, 485),  # Tuts hitam
    'D#4': (190, 480, 198, 485),
    'C5': (400, 500, 450, 550),
    'D5': (460, 500, 510, 550),
    'E5': (520, 500, 570, 550),
    'F5': (580, 500, 630, 550),
    'G5': (640, 500, 690, 550),
    'C#5': (430, 480, 438, 485),
    'D#5': (490, 480, 498, 485)
}
tap_threshold = 20
last_played = {}

# Interface Streamlit
st.title("Piano Virtual dengan MediaPipe")
run = st.checkbox("Jalankan Kamera")
FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Webcam tidak terdeteksi. Coba ganti cv2.VideoCapture(1).")
        st.stop()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (800, 600))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                x = int(hand_landmarks.landmark[8].x * 800)  # Ujung telunjuk
                y = int(hand_landmarks.landmark[8].y * 600)
                z = hand_landmarks.landmark[8].z * 1000  # Kedalaman

                for note, (x1, y1, x2, y2) in tuts.items():
                    if x1 <= x <= x2 and y1 <= y <= y2 and abs(z) < tap_threshold:
                        if note not in last_played or time.time() - last_played[note] > 0.5:
                            playsound(f"sounds/{note}.wav")  # Mainkan suara
                            last_played[note] = time.time()
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)  # Tuts merah

        # Gambar tuts piano
        for note, (x1, y1, x2, y2) in tuts.items():
            color = (0, 0, 0) if '#' in note else (255, 255, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

        FRAME_WINDOW.image(frame_rgb)
    else:
        cap.release()

    if st.button("Stop"):
        cap.release()
        st.stop()