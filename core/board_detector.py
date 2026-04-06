import cv2 as cv
import numpy as np

class BoardDetect:
    def __init__(self, board_size=480):
        self.detected = False
        self.M = None  # Homography matrix
        self.board_size = board_size
        self.dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
        self.parameters = cv.aruco.DetectorParameters()
        self.detector = cv.aruco.ArucoDetector(self.dictionary, self.parameters)

        # Mapping: ID -> (Target Destination Index, Marker's Inner Corner Index)
        # Standard: 0:TL, 1:TR, 2:BR, 3:BL (Clockwise)
        self.marker_map = {
            1: (0, 2),  # TL marker -> use BR inner corner -> dst TL
            3: (1, 3),  # TR marker -> use BL inner corner -> dst TR
            0: (2, 1),  # BL marker -> use TR inner corner -> dst BL
            2: (3, 0),  # BR marker -> use TL inner corner -> dst BR
        }

    def detect(self, frame):
        corners, ids, _ = self.detector.detectMarkers(frame)
        
        if ids is None or len(ids) < 4:
            self.detected = False
            return

        ids_flat = ids.flatten()
        for i, mid in enumerate(ids_flat):
            print(f"ID {mid} center:", corners[i][0].mean(axis=0))
        
        # Validation Gate: Ensure all required IDs (0, 1, 2, 3) are present
        if not all(m_id in ids_flat for m_id in self.marker_map):
            self.detected = False
            return

        src_pts = np.zeros((4, 2), dtype=np.float32)
        found_count = 0

        for i, marker_id in enumerate(ids_flat):
            if marker_id in self.marker_map:
                target_idx, corner_idx = self.marker_map[marker_id]
                src_pts[target_idx] = corners[i][0][corner_idx]
                found_count += 1

        if found_count == 4:
            # Destination points ordered: TL, TR, BR, BL
            s = self.board_size - 1
            dst_pts = np.array([
                [0, 0],    # TL
                [s, 0],    # TR
                [0, s],    # BL
                [s, s],    # BR
            ], dtype=np.float32)

            self.M = cv.getPerspectiveTransform(src_pts, dst_pts)
            self.detected = True
        else:
            self.detected = False

    def warp(self, frame):
        if not self.detected or self.M is None:
            return None
        return cv.warpPerspective(frame, self.M, (self.board_size, self.board_size))
    
    def is_detected(self):
        return self.detected