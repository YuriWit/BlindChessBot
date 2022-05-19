import chess
import chess.engine
import random

# set engine
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

engine.configure({"Skill Level":1})


board.is_game_over()

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
        except ValueError as e:
                

    

