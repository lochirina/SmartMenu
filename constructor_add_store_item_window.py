from PyQt5 import QtWidgets, uic
from datetime import datetime
import sqlite3

from db_controller import DatabaseController

class AddStorageWindow:
    def __init__(self):

        self.win = uic.loadUi("static/ui/add_storage_item.ui")
        self.db = DatabaseController()
        self.load_products_to_combobox()

        # Установка текущей даты
        current_date = datetime.now()
        self.win.purchaseDateDateEdit.setDate(current_date)
        print("Дата")

        # Подключение обработчиков кнопок
        self.win.addStoragePushButton.clicked.connect(self.add_storage_item)

        self.win.show()

    def load_products_to_combobox(self):
        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        # Получение только продуктов с quantity = 0
        cursor.execute('SELECT name FROM products WHERE quantity = 0 ORDER BY name')
        products = cursor.fetchall()

        # Очистка и добавление в comboBox
        self.win.storeComboBox.clear()
        for product in products:
            self.win.storeComboBox.addItem(product[0])

        conn.close()

    def add_storage_item(self):

        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        try:
            # Получение данных из формы
            product_name = self.win.storeComboBox.currentText()
            quantity = self.win.storeSpinBox.value()
            purchase_date = self.win.purchaseDateDateEdit.date().toString("yyyy-MM-dd")

            # Обновление данных продукта
            cursor.execute('''
                UPDATE products
                SET quantity = ?, purchase_date = ?
                WHERE name = ?
            ''', (quantity, purchase_date, product_name))

            conn.commit()
            conn.close()

            self.parent.refresh_storage_table()
            self.win.close()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              "Продукт успешно добавлен в запасы")
            self.win.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при добавлении продукта: {str(e)}")
            conn.close()


class EditStorageWindow:
    def __init__(self, product_id, product_name):

        print(f"Открываем окно для продукта: {product_name} с ID: {product_id}")
        self.win = uic.loadUi("static/ui/add_storage_item.ui")
        self.db = DatabaseController()
        self.product_id = product_id

        # Настройка интерфейса для редактирования
        self.win.storeComboBox.clear()
        self.win.storeComboBox.addItem(product_name)
        self.win.storeComboBox.setEnabled(False)  # Делаем comboBox неактивным
        self.load_product_data(product_id)
        print("Интерфейс загружен")

        # Подключение обработчиков кнопок
        # self.win.addStoragePushButton.clicked.disconnect()
        self.win.addStoragePushButton.clicked.connect(self.update_storage_item)
        print("Кнопки инициированы")

        self.win.show()

    def load_product_data(self, product_id):
        try:
            # Подключение к базе данных
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()

            # Получение текущих данных продукта
            cursor.execute('SELECT quantity, purchase_date FROM products WHERE id = ?', (product_id,))
            product_data = cursor.fetchone()
            conn.close()

            if product_data:
                self.win.storeSpinBox.setValue(product_data[0])
                if product_data[1]:
                    date = datetime.strptime(product_data[1], "%Y-%m-%d").date()
                    self.win.purchaseDateDateEdit.setDate(date)
                else:
                    self.win.purchaseDateDateEdit.setDate(datetime.now())
            else:
                QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                               "Не удалось загрузить данные продукта.")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при загрузке данных: {str(e)}")

    def update_storage_item(self):

        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        try:
            # Получение данных из формы
            quantity = self.win.storeSpinBox.value()
            purchase_date = self.win.purchaseDateDateEdit.date().toString("yyyy-MM-dd")

            # Обновление данных продукта
            cursor.execute('''
                UPDATE products
                SET quantity = ?, purchase_date = ?
                WHERE id = ?
            ''', (quantity, purchase_date, self.product_id))

            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self.win, "Успех", "Данные продукта успешно обновлены")

            # Обновляем таблицу в главном окне
            self.parent.refresh_storage_table()
            self.win.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при обновлении данных продукта: {str(e)}")
            if 'conn' in locals():
                conn.close()
