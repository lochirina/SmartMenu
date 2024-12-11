from PyQt5 import QtWidgets, uic
import sqlite3
from db_controller import DatabaseController


class AddProductWindow:
    def __init__(self):

        self.win = uic.loadUi("static/ui/add_prod.ui")
        self.db_controller = DatabaseController()
        self.load_measurement_units()
        self.win.addProdPushButton.clicked.connect(self.add_product)
        self.win.show()

    def load_measurement_units(self):
        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        # Получение всех единиц измерения
        cursor.execute('SELECT name FROM measurement_units')
        units = cursor.fetchall()

        # Очистка comboBox и добавление единиц измерения
        self.win.unitComboBox.clear()
        for unit in units:
            self.win.unitComboBox.addItem(unit[0])

        conn.close()

    def add_product(self):
        try:
            # Получаем данные из полей ввода
            name = self.win.nameOProdLineEdit.text()
            unit = self.win.unitComboBox.currentText()
            carbohydrates = int(self.win.carbohLineEdit.text())
            fats = int(self.win.fatsLineEdit.text())
            calories = int(self.win.kaloriesLineEdit.text())
            proteins = int(self.win.proteinsLineEdit.text())
            shelf_life = int(self.win.shelfLifeLineEdit.text())

            if self.db_controller.add_product(name, unit, carbohydrates, fats,
                                              calories, proteins, shelf_life):
                QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Продукт успешно добавлен!")
                # Обновляем таблицу в главном окне
                self.parent.refresh_products_table()
                self.win.close()
            else:
                QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                              "Не удалось добавить продукт!")

        except ValueError:
            QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                          "Пожалуйста, проверьте правильность введенных данных!")