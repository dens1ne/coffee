import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QSizePolicy, QComboBox
import sys

con = sqlite3.connect('coffee.sqlite')
cur = con.cursor()


class AddEditForm(QMainWindow):
    def __init__(self, operation, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.operation = operation

        self.variety.addItems(map(lambda x: x[0], cur.execute("""SELECT name FROM varietes""").fetchall()))
        self.roast_degree.addItems(map(lambda x: x[0], cur.execute("""SELECT name FROM roast_degree""").fetchall()))
        self.structure.addItems(map(lambda x: x[0], cur.execute("""SELECT name FROM structure""").fetchall()))

        if operation == 'UPDATE':
            result = cur.execute("""SELECT * FROM coffee WHERE id = ?""",
                                 (self.parent().coffee.currentRow() + 1,)).fetchone()
            print(result)
            self.variety.setCurrentIndex(result[1] - 1)
            self.roast_degree.setCurrentIndex(result[2] - 1)
            self.structure.setCurrentIndex(result[3] - 1)
            self.taste.setText(result[4])
            self.value.setText(str(result[5]))
            self.cost.setText(str(result[6]))

        self.cancel.clicked.connect(self.close)
        self.ok.clicked.connect(self.operate)

    def operate(self):
        try:
            value, cost = int(self.value.text()), int(self.cost.text())
            if value <= 0 or cost <= 0:
                raise ValueError

            if self.operation == 'INSERT':
                cur.execute("""INSERT INTO coffee(variety, roast_degree, structure, taste, value, cost) 
                            VALUES(?, ?, ?, ?, ?, ?)""",
                            (self.variety.currentIndex() + 1, self.roast_degree.currentIndex() + 1,
                             self.structure.currentIndex() + 1, self.taste.text(), value, cost))
            elif self.operation == 'UPDATE':
                cur.execute("""UPDATE coffee SET variety = ?, roast_degree = ?, structure = ?,
                            taste = ?, value = ?, cost = ? WHERE id = ?""",
                            (self.variety.currentIndex() + 1, self.roast_degree.currentIndex() + 1,
                             self.structure.currentIndex() + 1, self.taste.text(), value, cost,
                             self.parent().coffee.currentRow() + 1))
            con.commit()
            self.parent().update_result()
            self.close()
        except ValueError:
            self.statusBar().showMessage('Неверное заполнение полей')


class Capuccino(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.coffee: QTableWidget
        self.coffee.setColumnCount(6)
        self.coffee.setHorizontalHeaderLabels([
            'Вид', 'Степень прожарки', 'Структура', 'Описание вкуса', 'Объём', 'Цена'
        ])

        self.add.clicked.connect(self.add_db)
        self.edit.clicked.connect(self.edit_db)

        self.update_result()
        # Невообразимые цены на кофе!

    def update_result(self):
        # Be ready for goofy ah goofy code
        result = cur.execute(
            """SELECT varietes.name, roast_degree.name, structure.name, coffee.taste, coffee.value, coffee.cost
             FROM coffee INNER JOIN varietes ON coffee.variety = varietes.id
             INNER JOIN roast_degree ON coffee.roast_degree = roast_degree.id
             INNER JOIN structure ON coffee.structure = structure.id""").fetchall()

        self.coffee.setRowCount(len(result))
        for row, position in enumerate(result):
            for column, info in enumerate(position):
                self.coffee.setItem(row, column, QTableWidgetItem(str(info)))

            self.coffee.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.coffee.sizeHint()

    def edit_db(self):
        self.coffee: QTableWidget
        edit_form = AddEditForm('UPDATE', self)
        edit_form.show()

    def add_db(self):
        add_form = AddEditForm('INSERT', self)
        add_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Capuccino()
    ex.show()
    sys.exit(app.exec_())
