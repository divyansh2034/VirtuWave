import cv2
import mediapipe as mp
import math
import pygame

# Initialize Pygame mixer
pygame.mixer.init()
sounds = {
    "pinch": pygame.mixer.Sound("assets/sound/pinch.wav"),
    "open_palm": pygame.mixer.Sound("assets/sound/open_palm.wav"),
    "thumbs_up": pygame.mixer.Sound("assets/sound/fist.wav")
}

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Distance helper
def get_distance(point1, point2):
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

# Play sound once per trigger
last_played = None

# Webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            lm = hand_landmarks.landmark
            landmarks = [(int(p.x * w), int(p.y * h)) for p in lm]

            # Landmark indices
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]

            index_pip = landmarks[6]
            middle_pip = landmarks[10]
            ring_pip = landmarks[14]
            pinky_pip = landmarks[18]
            thumb_ip = landmarks[3]

            # Gesture 1: Pinch
            if get_distance(thumb_tip, index_tip) < 40:
                if last_played != "pinch":
                    print("Gesture: Pinch")
                    sounds["pinch"].play()
                    last_played = "pinch"

            # Gesture 2: Open Palm
            elif (index_tip[1] < index_pip[1] and
                  middle_tip[1] < middle_pip[1] and
                  ring_tip[1] < ring_pip[1] and
                  pinky_tip[1] < pinky_pip[1] and
                  thumb_tip[0] < thumb_ip[0]):
                if last_played != "open_palm":
                    print("Gesture: Open Palm")
                    sounds["open_palm"].play()
                    last_played = "open_palm"

            # Gesture 3: Thumbs Up
            elif (thumb_tip[1] < thumb_ip[1] and
                  index_tip[1] > index_pip[1] and
                  middle_tip[1] > middle_pip[1] and
                  ring_tip[1] > ring_pip[1] and
                  pinky_tip[1] > pinky_pip[1]):
                if last_played != "thumbs_up":
                    print("Gesture: Thumbs Up")
                    sounds["thumbs_up"].play()
                    last_played = "thumbs_up"

            else:
                last_played = None

    cv2.imshow("VirtuWave - Gesture Music Composer", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
