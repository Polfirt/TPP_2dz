import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox
from collections import deque

EMPTY = 0  # Пустая клетка
WALL = 1   # Стенка
START = 2  # Начальная точка
END = 3    # Конечная точка
PATH = 4   # Тип для отображения пути

class MazeGame(QMainWindow):
    def __init__(self, grid_size):
        super().__init__()
        self.setWindowTitle("Maze Game")
        self.setGeometry(100, 100, 800, 600)

        self.grid_size = grid_size  # Размеры лабиринта
        self.grid = [[EMPTY for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]  # Создаем сетку лабиринта
        self.start_pos = None  # Начальная позиция
        self.end_pos = None  # Конечная позиция

        self.central_widget = QWidget()  # Создаем центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.layout = QGridLayout(self.central_widget)  # Создаем сеточный макет для центрального виджета

        self.buttons = [[None for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]  # Создаем список кнопок
        for i in range(self.grid_size[0]):  # Проходим по строкам
            for j in range(self.grid_size[1]):  # Проходим по столбцам
                button = QPushButton()
                button.setFixedSize(40, 40)
                button.setStyleSheet("background-color: white;")
                button.clicked.connect(lambda checked, x=i, y=j: self.change_cell(x, y))  # Подключаем обработчик нажатия кнопки. Lambda — это инструмент в Python для вызова анонимных функций, анонимно означает, что вы используете ее, не объявляя ее нигде. В буквальном смысле, анонимная функция — это функция без имени.
                self.layout.addWidget(button, i, j)  # Добавляем кнопку в макет
                self.buttons[i][j] = button  # Сохраняем кнопку в списке

        # Кнопка для начала прохождения лабиринта
        self.start_button = QPushButton("Начать прохождение")
        self.start_button.clicked.connect(self.start_solving)
        self.layout.addWidget(self.start_button, self.grid_size[0], 0, 1, self.grid_size[1])  # Добавляем кнопку в макет

    def change_cell(self, x, y):  # Метод для изменения типа клетки при нажатии на кнопку
        if self.grid[x][y] == EMPTY:
            self.grid[x][y] = WALL
            self.buttons[x][y].setStyleSheet("background-color: gray;")
        elif self.grid[x][y] == WALL:
            self.grid[x][y] = START
            self.buttons[x][y].setStyleSheet("background-color: green;")
            if self.start_pos is None:  # Если стартовая позиция еще не установлена
                self.start_pos = (x, y)  # Устанавливаем стартовую позицию
        elif self.grid[x][y] == START:
            self.grid[x][y] = END
            self.buttons[x][y].setStyleSheet("background-color: red;")
            if self.end_pos is None:  # Если конечная позиция еще не установлена
                self.end_pos = (x, y)  # Устанавливаем конечную позицию
        elif self.grid[x][y] == END:
            self.grid[x][y] = EMPTY
            self.buttons[x][y].setStyleSheet("background-color: white;")
            self.end_pos = None  # Сбрасываем конечную позицию
        else:
            # Если нажали на стену или пустую клетку, ничего не делаем
            pass


    def start_solving(self):  # Метод для запуска поиска пути
        if self.start_pos and self.end_pos:
            path = self.bfs(self.start_pos, self.end_pos)  # Запускаем BFS для нахождения пути
            if path:  # Если путь найден
                self.visualize_path(path)  # Визуализируем путь
            else:
                QMessageBox.warning(self, "Ошибка", "Нет пути от начала до конца!")
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо установить начальную и конечную точки!")

    def bfs(self, start, end):  # Метод для поиска пути с помощью BFS
        queue = deque([start])  # Создаем очередь и добавляем начальную позицию
        visited = set()  # Создаем множество для отслеживания посещенных клеток
        visited.add(start)  # Добавляем начальную позицию в посещенные
        parent = {start: None}  # Словарь для хранения предшествующих клеток

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Направления: вниз, вверх, вправо, влево

        while queue:  # Пока очередь не пуста
            current = queue.popleft()  # Извлекаем текущую клетку из очереди

            if current == end:  # Если достигли конечной точки
                # Если достигли конца, восстанавливаем путь
                path = []  # Список для хранения пути
                while current is not None:  # Пока есть предшествующая клетка
                    path.append(current)  # Добавляем текущую клетку в путь
                    current = parent[current]  # Переходим к предшествующей клетке
                path.reverse()  # Обратим порядок, чтобы получить путь от начала до конца
                return path  # Возвращаем найденный путь

            for direction in directions:  # Проходим по всем направлениям
                neighbor = (current[0] + direction[0], current[1] + direction[1])  # Вычисляем соседнюю клетку
                # Проверяем, находится ли соседняя клетка в пределах границ и не является ли она стеной
                if (0 <= neighbor[0] < self.grid_size[0] and
                        0 <= neighbor[1] < self.grid_size[1] and
                        self.grid[neighbor[0]][neighbor[1]] != WALL and
                        neighbor not in visited):
                    visited.add(neighbor)  # Добавляем соседнюю клетку в посещенные
                    parent[neighbor] = current  # Устанавливаем текущую клетку как предшествующую
                    queue.append(neighbor)  # Добавляем соседнюю клетку в очередь

        return None  # Если путь не найден, возвращаем None

    def visualize_path(self, path):  # Метод для визуализации найденного пути
        for x, y in path:  # Проходим по всем клеткам в пути
            if self.grid[x][y] != START and self.grid[x][y] != END:
                self.grid[x][y] = PATH  # Устанавливаем тип клетки как PATH
                self.buttons[x][y].setStyleSheet("background-color: blue;")

if __name__ == "__main__":
    height = int(input("Введите высоту лабиринта: "))
    width = int(input("Введите ширину лабиринта: "))

    app = QApplication(sys.argv)
    game = MazeGame((height, width))
    game.show()
    sys.exit(app.exec_())
