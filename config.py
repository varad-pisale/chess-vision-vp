# anything you'd want to tweak without touching logic goes in config. 

# Paths (model weights, output dirs)
# Camera source URL/index
# Detection thresholds (confidence, IOU)
# Board detection tuning params (min contour area, etc.)
# Class names list
# Stockfish path + settings
from pathlib import Path

# MODEL_PATH=Path("secondary_models/chess-model-yolov8m.pt")
MODEL_PATH=Path("runs/detect/runs/chess_v1/weights/best.pt")
SOURCES=["IP_LINK",0]
CONF=0.4
IOU=0.45
NAMES= ['black-bishop', 'black-king', 'black-knight', 'black-pawn', 'black-queen', 'black-rook', 'white-bishop', 'white-king', 'white-knight', 'white-pawn', 'white-queen', 'white-rook']
STOCKFISH="/usr/games/stockfish"