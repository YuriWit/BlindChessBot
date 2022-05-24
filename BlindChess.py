import chess

class BlindChessGame:
    def __init__(self):
        self.player_err = [0,0]
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = chess.Board()
        self.turn = 0

        self.err_tol = [5,5]
    
    def isGameOver(self):
        if (self.player_err[0] > self.err_tol[0]):
            return True
        elif (self.player_err[1] > self.err_tol[1]):
            return True
        elif (self.board.is_game_over()):
            return True
        else:
            return False

    def setLevel(self, level):
        self.level = level
    
    def sanMove(self, san):
        try:
            self.board.push_san(san)
            self.trun = 1 if self.turn == 0 else 0
            return True
        except ValueError as e:
            print(e)
            if "illegal san" in str(e):
                self.player_err[self.turn] += 1
            return False
    
    def getTurn(self):
        return "Black to play" if self.turn == 1 else "White to play"
    

