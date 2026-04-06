from config import MODEL_PATH, NAMES, CONF,IOU
from ultralytics import YOLO
import cv2

class PieceDetect:
    def __init__(self) -> None:
        # load YOLO model once at startup
        self.model = YOLO(MODEL_PATH)

    def detect_pieces(self, frame):
        # Pass imgsz=480 to ensure YOLO doesn't downscale your crop
        results = self.model(frame, verbose=False, imgsz=480, iou=IOU,conf=CONF)
        pos = []
        
        for res in results:
            for box in res.boxes:
                # 1. Visualization (Draw on the frame directly)
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                label = f"{NAMES[cls_id]} {conf:.2f}"
                
                # Draw bounding box and label
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1)-5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

                # 2. Refined Grid Mapping (Use Bottom-Center)
                # Square size is 60 (480 / 8)
                cx = ((x1 + x2) / 2) / 60
                cy = ((y1 + y2) / 2) / 60  # Using y2 (the base) is critical for perspective
                
                row = int(cy)
                col = int(cx)

                # 3. Validation Gate: Clamp to 0-7
                row = max(0, min(7, row))
                col = max(0, min(7, col))

                pos.append({
                    "class_name": NAMES[cls_id],
                    "row": row,
                    "col": col
                })
        return pos