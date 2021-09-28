import chess
import chess.svg
import chess.engine
import random
import os

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
engine.configure({"Skill Level":1})
engine.configure({"Skill Level":3})

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(0, 0, 800, 800)

        self.chessboard = chess.Board()
        self.turn = 0 #random.randint(0,1) == 1

    def loop(self):
        strike = 0
        a = os.system('clear')
        while not self.chessboard.is_game_over() and strike < 5:
            if self.chessboard.turn == self.turn:
                result = engine.play(self.chessboard, chess.engine.Limit(time=0.1))
                print(self.chessboard.san(result.move))
                self.chessboard.push(result.move)
            else:
                move = ''
                while move == '' and strike < 5:
                    try:
                        move = input("Your move: ")
                        self.chessboard.push_san(move)
                    except:
                        if move == "show":
                            self.see()
                            self.show()
                        elif move == "cls":
                            a = os.system('clear')
                        else:
                            strike += 1
                            print("non valid move")
                        move = ''
                a = os.system('clear')
        print("game over")
        print(str(self.chessboard.halfmove_clock)+" moves")
        self.see()
        self.show()

    def see(self):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.loop()
    input("close")
    window.close()
    #app.exec()