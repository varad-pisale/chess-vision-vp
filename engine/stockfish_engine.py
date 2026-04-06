from stockfish import Stockfish
from config import STOCKFISH

class Engine:
    def __init__(self) -> None:
        try:
            self.engine=Stockfish(path=STOCKFISH)
        except:
            print("Stockfish engine not found ")
            raise
        
        
    def next_move(self,fen):
        
        if self.engine.is_fen_valid(fen):
            self.engine.set_fen_position(fen)
            return self.engine.get_best_move()
        
        return None