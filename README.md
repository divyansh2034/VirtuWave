
# 🎵 VirtuWave – Air Piano & Drum Kit

VirtuWave is a gesture-based virtual instrument that turns your webcam into a **touchless musical instrument**! Play a full **piano** or a **drum kit** using only your hand movements via your webcam. Built with OpenCV, MediaPipe, and PyGame, VirtuWave offers a fun, interactive way to compose music in real time — no MIDI keyboard needed!

---

## 🧠 Features

- 🎹 **Air Piano**: 12 notes (C4 to B4) mapped to screen zones.
- 🥁 **Gesture-Triggered Drum Kit**: 8 drum sounds triggered by fast downward hand motion.
- 👋 **Real-Time Hand Tracking**: Using Google's MediaPipe Hands.
- 🔁 **Mode Switching**: Easily switch between Piano and Drum modes with keyboard keys.
- 🖥️ **Optimized for Low-End Devices**: Runs smoothly even on budget laptops.

---

## 📁 Folder Structure

```
VirtuWave/
│
├── virtu_wave.py             # Main Python script
├── README.md                 # Project README
└── assets/
    ├── piano_sounds/         # Contains C4.wav to B4.wav
    │   ├── C4.wav
    │   ├── C#4.wav
    │   └── ... B4.wav
    └── drum_sounds/          # Contains 8 unique drum sounds
        ├── kick.wav
        ├── snare.wav
        ├── hihat_closed.wav
        ├── hihat_open.wav
        ├── clap.wav
        ├── crash.wav
        ├── tom.wav
        └── chime.wav
```

---

## ⚙️ Installation

1. Clone the repo or download the source code:

```bash
git clone https://github.com/yourusername/VirtuWave.git
cd VirtuWave
```

2. Install the required dependencies:

```bash
pip install opencv-python mediapipe pygame numpy
```

3. Place your `.wav` sound files inside the respective folders under `assets/`.

---

## ▶️ Running the App

```bash
python virtu_wave.py
```

- Press **`p`** to switch to **Piano Mode**
- Press **`d`** to switch to **Drum Mode**
- Press **`q`** to quit the app

---

## 🖐 Gesture Control

### Piano Mode:
- Your screen is divided into 12 vertical zones (notes).
- Move your **index finger** over a zone (top half of screen) to play the note.

### Drum Mode:
- 8 rectangular zones appear on screen.
- **Swipe your hand downward** over a drum pad to trigger the sound.

---

## 📦 Sound Samples

You can collect sound samples from:
- [SampleSwap](https://sampleswap.org/)
- [SampleFocus](https://samplefocus.com/)
- [Freesound](https://freesound.org/)

Ensure all sound files are in `.wav` format and named as per the folders.

---

## 📸 Webcam Notes

If the webcam doesn't start:
- Check if it works in your Camera app.
- Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in the code.
- Ensure privacy settings allow Python/OpenCV to access the camera.

---

## 🤖 Tech Stack

- **Python 3.x**
- [OpenCV](https://opencv.org/) – for video processing
- [MediaPipe](https://mediapipe.dev/) – for hand tracking
- [PyGame](https://www.pygame.org/) – for sound playback
