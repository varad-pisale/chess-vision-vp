from utils.camera import Camera
from core.board_detector import BoardDetect
from core.fen_generator import FenGenerator
from core.piece_detector import PieceDetect
from engine.stockfish_engine import Engine
import config
import cv2
import time

if __name__ == "__main__":

    cam = Camera(sources=config.SOURCES)
    board = BoardDetect()
    pieces = PieceDetect()
    fen = FenGenerator()
    chess_engine = Engine()
    last_fen = ""

    with cam as c:
        while c.active_source:
            # get frame from camera
            ret, frame = c.read()
            if not ret:
                print("getting camera frame")
                continue
            # cv2.imwrite("raw_frame.png", frame)
            # detect board corners via ArUco markers
            board.detect(frame=frame)
            # print("detected:", board.is_detected())
            # if not board.is_detected():
                # continue

            chess_board = board.warp(frame=frame)
            if chess_board is None:
                continue

            # 2. Run YOLO (Now draws boxes on chess_board internally)
            positions = pieces.detect_pieces(frame=chess_board)

            # 3. SHOW THE DETECTIONS WINDOW
            # This is your debugging gold mine.
            cv2.imshow("Live Detections", chess_board)
            cv2.waitKey(1)

            # 4. Generate FEN
            fen_str = fen.create_Fen(positions)
            # only call Stockfish if board state changed
            if fen_str == last_fen:
                continue
            last_fen = fen_str
            print("FEN:", fen_str)

            # get best move from Stockfish
            output = chess_engine.next_move(fen_str)
            print(output)
            
            time.sleep(1)