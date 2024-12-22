import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox


class Game2048(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2048")
        self.setGeometry(100, 100, 400, 400)

        self.grid = [[0] * 4 for _ in range(4)]
        self.initUI()
        self.add_new_tile()
        self.add_new_tile()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.buttons = [[QPushButton() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.layout.addWidget(self.buttons[i][j], i, j)
                self.buttons[i][j].setFixedSize(80, 80)
                self.buttons[i][j].setStyleSheet("font-size: 24px;")

        self.up_button = QPushButton("Up")
        self.down_button = QPushButton("Down")
        self.left_button = QPushButton("Left")
        self.right_button = QPushButton("Right")

        self.layout.addWidget(self.up_button, 4, 0, 1, 4)
        self.layout.addWidget(self.down_button, 5, 0, 1, 4)
        self.layout.addWidget(self.left_button, 6, 0, 1, 2)
        self.layout.addWidget(self.right_button, 6, 2, 1, 2)

        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)

        self.update_ui()

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                self.buttons[i][j].setText(str(self.grid[i][j]) if self.grid[i][j] != 0 else "")
                self.buttons[i][j].setStyleSheet(
                    "font-size: 24px; background-color: {}".format(self.get_color(self.grid[i][j])))

    def get_color(self, value):
        colors = {
            0: "#ccc0b3",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f67c5f",
            128: "#f9f85d",
            256: "#f9f85d",
            512: "#f9f85d",
            1024: "#f9f85d",
            2048: "#f9f85d",
        }
        return colors.get(value, "#3c3a32")

    def move_up(self):
        self.move_tiles(-1, 0)

    def move_down(self):
        self.move_tiles(1, 0)

    def move_left(self):
        self.move_tiles(0, -1)

    def move_right(self):
        self.move_tiles(0, 1)

    def move_tiles(self, dx, dy):
        moved = False
        for _ in range(4):
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] != 0:
                        ni, nj = i + dx, j + dy
                        while 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] == 0:
                            self.grid[ni][nj] = self.grid[i][j]
                            self.grid[i][j] = 0
                            moved = True
                            i, j = ni, nj
                            ni, nj = i + dx, j + dy
                        if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] == self.grid[i][j]:
                            self.grid[ni][nj] *= 2
                            self.grid[i][j] = 0
                            moved = True
                            self.add_new_tile()

        if moved:
            self.add_new_tile()
            self.update_ui()
            if not self.can_move():
                self.show_game_over()

    def can_move(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def show_game_over(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("А всё, програл ты")
        msg.setWindowTitle("2048")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game2048()
    game.show()
    sys.exit(app.exec_())
