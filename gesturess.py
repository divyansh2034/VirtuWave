import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import time

# Init pygame sound
pygame.init()
pygame.mixer.init()

# Load sounds
piano_notes = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4']
piano_sounds = {note: pygame.mixer.Sound(f"assets/piano_sounds/{note}.wav") for note in piano_notes}

drum_sounds = {
    'kick': pygame.mixer.Sound("assets/drum_sounds/kick.wav"),
    'snare': pygame.mixer.Sound("assets/drum_sounds/snare.wav"),
    'hihat': pygame.mixer.Sound("assets/drum_sounds/hihat_closed.wav"),
    'clap': pygame.mixer.Sound("assets/drum_sounds/clap.wav"),
    'cymbal': pygame.mixer.Sound("assets/drum_sounds/crash.wav"),
    'tom': pygame.mixer.Sound("assets/drum_sounds/tom.wav"),
    'openhat': pygame.mixer.Sound("assets/drum_sounds/hihat_open.wav"),
    'chime': pygame.mixer.Sound("assets/drum_sounds/chime.wav")
}

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open camera.")
    exit()

mode = 'piano'
prev_zone = None
prev_drum = None
last_y = 0
last_trigger_time = time.time()

drum_keys = list(drum_sounds.keys())

print("Press 'p' for Piano Mode, 'd' for Drum Mode, and 'q' to quit")

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = img.shape
    cv2.putText(img, f"MODE: {mode.upper()}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark
        index_tip = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        ix, iy = int(index_tip.x * w), int(index_tip.y * h)

        # Piano Mode
        if mode == 'piano' and iy < h // 2:
            key_width = w // 12
            zone_index = ix // key_width
            zone_index = min(zone_index, 11)
            note = piano_notes[zone_index]
            cv2.rectangle(img, (zone_index * key_width, 0), ((zone_index + 1) * key_width, h // 2), (200, 200, 255), 2)
            cv2.putText(img, note, (zone_index * key_width + 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            if prev_zone != zone_index:
                piano_sounds[note].play()
                prev_zone = zone_index

        # Drum Mode (gesture-based hit)
        elif mode == 'drum':
            pad_width = w // 4
            pad_height = h // 2 // 2
            drum_hit = None

            for i, name in enumerate(drum_keys):
                col = i % 4
                row = i // 4
                x1 = col * pad_width
                y1 = row * pad_height
                x2 = x1 + pad_width
                y2 = y1 + pad_height

                cv2.rectangle(img, (x1, y1), (x2, y2), (100, 50, 255), 2)
                cv2.putText(img, name.upper(), (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                if x1 < ix < x2 and y1 < iy < y2:
                    # Check vertical speed
                    speed = iy - last_y
                    if speed > 20 and (time.time() - last_trigger_time) > 0.25:
                        drum_sounds[name].play()
                        prev_drum = name
                        last_trigger_time = time.time()
                        break

        last_y = iy
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        prev_zone = None
        prev_drum = None

    cv2.imshow("VirtuWave – Air Piano & Drum Kit", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('d'):
        mode = 'drum'
        print("Switched to DRUM mode")
    elif key == ord('p'):
        mode = 'piano'
        print("Switched to PIANO mode")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()