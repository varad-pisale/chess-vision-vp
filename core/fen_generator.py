name_map= {'black-bishop':'b', 'black-king':'k', 'black-knight':'n', 'black-pawn':'p', 'black-queen':'q', 'black-rook':'r', 'white-bishop':'B', 'white-king':'K', 'white-knight':'N', 'white-pawn':'P', 'white-queen':'Q', 'white-rook':'R'}

class FenGenerator:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_Fen(pos):
        fen=""
        # empty 8X8 matrix
        board_grid=[[None for _ in range(8)] for _ in range(8)]
        for p in pos:
            board_grid[p["row"]][p["col"]]=name_map[p["class_name"]]
        
        for r in range(8):
            nones=0
            for c in range(8):
                if board_grid[r][c] is not None:
                    if nones !=0:
                        fen=fen+str(nones)+board_grid[r][c]
                    else:
                        fen=fen+board_grid[r][c]
                    nones=0
                else:
                    nones+=1
            if nones !=0:
                fen=fen+str(nones)
            if r==7 :
                break
            fen=fen+'/'
        
        fen=fen+" w KQkq - 0 1"
        return fen