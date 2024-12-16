import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Установка размера окна
        self.setGeometry(100, 100, 500, 600)
        self.setWindowTitle('Калькулятор')

        # Создание основного вертикального макета (посидел на документациях)
        layout = QVBoxLayout()

        # Создание текстового поля для ввода
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # Создание сеточного макета для кнопок
        grid_layout = QGridLayout()

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('C', 3, 1), ('=', 3, 2), ('+', 3, 3)
        ]

        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.setFixedSize(150, 150)
            button.setFont(QFont('Arial', 16))  # Шрифт
            button.clicked.connect(self.on_button_click)
            grid_layout.addWidget(button, row, col)

        # Добавление сеточного макета в основной макет
        layout.addLayout(grid_layout)

        self.setLayout(layout)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.input_field.clear()
        elif text == '=':
            try:
                result = eval(self.input_field.text())
                self.input_field.setText(str(result))
                if result == 8769079:
                    self.input_field.setText('Кое кто пасхалочку нашёл. Недурно...')
                if result == 4567234:
                    self.input_field.setText('Если интересно, почему здесь пасхалки, то могу сказать, что мне нечем было заняться вечером.')
            except Exception as e:
                self.input_field.setText('Ошибка')
        else:
            current_text = self.input_field.text()
            new_text = current_text + text
            self.input_field.setText(new_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
