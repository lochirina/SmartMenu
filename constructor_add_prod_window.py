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
                self.parent.refresh_storage_table()
                self.win.close()
            else:
                QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                              "Не удалось добавить продукт!")

        except ValueError:
            QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                          "Пожалуйста, проверьте правильность введенных данных!")


class EditProductWindow:
    def __init__(self, product_id):


        self.win = uic.loadUi("static/ui/add_prod.ui")
        self.db_controller = DatabaseController()
        self.product_id = product_id

        #Настройка интерфейса
        self.load_measurement_units()
        self.load_product_data(product_id)
        print(f"Открываем окно для продукта с ID: {product_id}")
        self.win.addProdPushButton.clicked.connect(self.save_product)

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

    def load_product_data(self, product_id):
        # Загрузка данных продукта из базы
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT name, measurement_unit_id, carbohydrates, fats, calories, proteins, shelf_life_days 
                FROM products WHERE id = ?
            ''', (product_id,))
            product_data = cursor.fetchone()
            print(product_data)
            conn.close()

            if product_data:
                self.win.nameOProdLineEdit.setText(str(product_data[0]))
                self.win.unitComboBox.setCurrentText(str(product_data[1]))
                self.win.carbohLineEdit.setText(str(product_data[2]))
                self.win.fatsLineEdit.setText(str(product_data[3]))
                self.win.kaloriesLineEdit.setText(str(product_data[4]))
                self.win.proteinsLineEdit.setText(str(product_data[5]))
                self.win.shelfLifeLineEdit.setText(str(product_data[6]))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при загрузке данных: {str(e)}")
            conn.close()


    def save_product(self):
        try:
            # Получаем данные из полей ввода
            name = self.win.nameOProdLineEdit.text()
            unit = self.win.unitComboBox.currentText()
            carbohydrates = int(self.win.carbohLineEdit.text())
            fats = int(self.win.fatsLineEdit.text())
            calories = int(self.win.kaloriesLineEdit.text())
            proteins = int(self.win.proteinsLineEdit.text())
            shelf_life = int(self.win.shelfLifeLineEdit.text())

            if self.product_id:
                # Обновление существующего продукта
                success = self.db_controller.update_product(self.product_id, name, unit, carbohydrates,
                                                            fats, calories, proteins, shelf_life)
            else:
                # Добавление нового продукта
                success = self.db_controller.add_product(name, unit, carbohydrates, fats,
                                                         calories, proteins, shelf_life)

            if success:
                QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Продукт успешно сохранен!")
                # Обновляем таблицу в главном окне
                self.parent.refresh_products_table()
                self.parent.refresh_storage_table()
                self.win.close()
            else:
                QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                              "Не удалось сохранить продукт!")

        except ValueError:
            QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                          "Пожалуйста, проверьте правильность введенных данных!")