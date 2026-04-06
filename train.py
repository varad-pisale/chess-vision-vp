from ultralytics import YOLO
from pathlib import Path

# ── CONFIG (edit these) ───────────────────────────────────────────────────────

DATA_YAML   = "top_chess/data.yaml"
MODEL       = "yolov8n.pt"       # yolov8n / yolov8s / yolov8m
EPOCHS      = 200
IMG_SIZE    = 640
BATCH       = 16                 # reduce to 8 if GPU runs out of memory
PROJECT     = "runs"             # output folder
RUN_NAME    = "chess_top"         # subfolder name inside PROJECT
DEVICE      = 0                  # 0 = first GPU, "cpu" = CPU

# ── TRAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    model = YOLO(MODEL)

    results = model.train(
        data      = DATA_YAML,
        epochs    = EPOCHS,
        imgsz     = IMG_SIZE,
        batch     = BATCH,
        project   = PROJECT,
        name      = RUN_NAME,
        device    = DEVICE,
    )

    # Print where results are saved
    save_dir = Path(PROJECT) / RUN_NAME
    print(f"\nTraining complete. Results saved to: {save_dir}")
    print(f"Best weights: {save_dir / 'weights' / 'best.pt'}")