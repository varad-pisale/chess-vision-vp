# ♟️ Chess Vision

An AI-powered physical chess assistant that watches a real chessboard through a camera, understands the board state, and suggests the best move using the Stockfish engine — all in real time.

---

## 🧠 Concept

Chess Vision bridges the physical and digital world. Place your camera above a chessboard, and the system will:
- Detect the board and correct its perspective
- Identify all pieces and their positions
- Generate a FEN string representing the current game state
- Feed it to Stockfish and return the best move

No e-board. No sensors. Just a camera and computer vision.

---

## 🏗️ System Architecture

```
IP Webcam / Local Camera
        │
        ▼
┌──────────────────┐
│  Board Detector  │  ← OpenCV: edge detection, contour finding, homography
│  (BoardDetector) │
└────────┬─────────┘
         │ 480×480 warped board frame
         ▼
┌──────────────────┐
│ Piece Detector   │  ← YOLOv8n: detects pieces, maps to 8×8 grid
│ (PieceDetector)  │
└────────┬─────────┘
         │ list of (piece, grid_position)
         ▼
┌──────────────────┐
│  FEN Generator   │  ← Converts grid detections → FEN string
└────────┬─────────┘
         │ FEN string
         ▼
┌──────────────────┐
│ Stockfish Engine │  ← Returns best move in UCI notation
└────────┬─────────┘
         │ best move
         ▼
  Web / Mobile Interface
```

---

## 📁 Project Structure

```
Chess_vision/
│
├── config.py               # All constants: paths, thresholds, class names
├── main.py                 # Entry point — orchestrates the full pipeline
│
├── core/
│   ├── board_detector.py   # Board detection and perspective warp
│   └── piece_detector.py   # YOLOv8 inference + grid mapping
│
├── engine/
│   └── stockfish_engine.py # Stockfish integration via FEN input
│
├── interface/
│   └── display.py          # Move display (web/mobile interface)
│
├── utils/
│   └── camera.py           # Camera abstraction with source fallback
│
└── runs/                   # YOLO training output (weights stored here)
    └── detect/chess_v1/weights/best.pt
```

---

## ⚙️ Modules

### `config.py`
Central configuration file. All paths, thresholds, and class names are defined here — no magic numbers scattered across the codebase.

### `utils/camera.py` — `Camera`
- Priority-based camera source fallback (IP webcam → local webcam)
- Retry logic with configurable attempts
- Context manager support (`with Camera() as cam`)
- Graceful release on exit

### `core/board_detector.py` — `BoardDetector`
- Converts frame to grayscale → Gaussian blur → Canny edge detection
- Finds contours, selects the largest quadrilateral
- Uses `getPerspectiveTransform` (homography) to warp the board to a clean **480×480** top-down view
- `is_detected()` health check for pipeline gating

### `core/piece_detector.py` — `PieceDetector`
- Loads YOLOv8n model once at init (`self.model = YOLO(MODEL_PATH)`)
- Runs inference on the warped board frame
- Maps bounding box centers to an 8×8 grid coordinate system
- Returns per-frame detections (stateless by design)

### FEN Generator
- Takes the 8×8 grid of piece detections
- Encodes it into a valid FEN string for engine consumption

### `engine/stockfish_engine.py`
- Accepts FEN string
- Returns best move in UCI notation via Stockfish

### `interface/display.py`
- Displays the suggested move to the user via a web or mobile-friendly interface

---

## 🤖 ML Model

| Property | Value |
|---|---|
| Architecture | YOLOv8n |
| Classes | 12 (black/white × bishop, king, knight, pawn, queen, rook) |
| mAP@50 | **0.992** |
| Weights | `runs/detect/chess_v1/weights/best.pt` |

---
<!-- 
## 🖼️ Detection Samples

| Board Warped (480×480) | Piece Detections | Move Suggestion |
|---|---|---|
| ![board](assets/board_warp.png) | ![pieces](assets/piece_detections.png) | ![move](assets/move_display.png) | -->

<!-- --- -->

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Conda (recommended)
- Stockfish installed and path set in `config.py`
- A camera or IP webcam app (e.g., DroidCam)

### Installation

```bash
git clone https://github.com/yourusername/Chess_vision.git
cd Chess_vision

conda create --prefix ./env python=3.10
conda activate ./env

pip install ultralytics opencv-python python-chess
```

### Run

```bash
python main.py
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Computer Vision | OpenCV |
| Object Detection | YOLOv8n (Ultralytics) |
| Chess Engine | Stockfish |
| Camera Input | IP Webcam / OpenCV VideoCapture |

---

## 📌 Design Decisions

- **Per-frame statelessness** — `PieceDetector` returns detections rather than storing them, keeping modules decoupled
- **FEN generation is a separate module** — not bundled into `PieceDetector`, following single-responsibility principle
- **Model loaded once at init** — avoids reloading weights on every frame, critical for real-time performance
- **Config-first** — all tuneable values live in `config.py` for easy updates without touching core logic

---

## 📋 TODO

- Improve piece recognition accuracy in varied lighting conditions

---
