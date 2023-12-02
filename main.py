import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QSizePolicy
import sys

con = sqlite3.connect('coffee.sqlite')
cur = con.cursor()


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.coffee: QTableWidget

        self.coffee.setColumnCount(6)
        self.coffee.setHorizontalHeaderLabels([
            'Вид', 'Степень прожарки', 'Структура', 'Описание вкуса', 'Объём', 'Цена'
        ])

        # Be ready for goofy ah goofy code
        for row, position in enumerate(cur.execute('SELECT * FROM coffee').fetchall()):
            self.coffee.setRowCount(self.coffee.rowCount() + 1)
            self.coffee.setItem(row, 0, QTableWidgetItem(cur.execute(
                f'SELECT name FROM varietes WHERE id = {position[1]}').fetchone()[0]
            ))
            self.coffee.setItem(row, 1, QTableWidgetItem(cur.execute(
                f'SELECT name FROM "roast degree" WHERE id = {position[2]}').fetchone()[0]
            ))
            self.coffee.setItem(row, 2, QTableWidgetItem(cur.execute(
                f'SELECT name FROM structure WHERE id = {position[3]}').fetchone()[0]
            ))

            print(cur.execute(
                f'SELECT name FROM structure WHERE id = {position[3]}').fetchone()[0]
            )

            for column, info in enumerate(position[4:]):
                self.coffee.setItem(row, column + 3, QTableWidgetItem(str(info)))

            self.coffee.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.coffee.sizeHint()

        # Невообразимые цены на кофе!


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())
