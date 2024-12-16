import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QLineEdit, QMessageBox


class TableApp(QWidget):
    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Табличка приятная')
        self.setGeometry(100, 100, width, height)

        self.layout = QVBoxLayout()

        self.table = QTableWidget(self.rows, self.columns)
        self.layout.addWidget(self.table)

        # Кнопки
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton('Добавить строку')
        self.add_button.clicked.connect(self.add_row)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Удалить строку')
        self.delete_button.clicked.connect(self.delete_row)
        self.button_layout.addWidget(self.delete_button)

        self.save_button = QPushButton('Сохранить в файл')
        self.save_button.clicked.connect(self.save_to_file)
        self.button_layout.addWidget(self.save_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления.')

    def save_to_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                for row in range(self.table.rowCount()):
                    row_data = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        row_data.append(item.text() if item else '')
                    f.write(','.join(row_data) + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    width = int(input("Вводите ширину таблицы Вашей. "))
    if width == 8642:
        width = int(input("Пасхалко. Ладно, шутка. Еще раз вводи) "))
    height = int(input("А теперь высоту. "))
    rows = int(input("Скок строк надо? "))
    columns = int(input("А столбцов? "))

    table_app = TableApp(rows, columns)
    table_app.show()

    sys.exit(app.exec_())
