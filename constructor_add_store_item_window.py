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

        # Подключение обработчиков кнопок
        self.win.addStoragePushButton.clicked.connect(self.add_storage_item)
        self.win.cancelStorageItemPushButton.clicked.connect(self.win.close)

        self.win.show()

    def load_products_to_combobox(self):
        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        # Получение только продуктов с quantity = 0
        cursor.execute('SELECT name FROM products WHERE quantity = 0 ORDER BY name')
        products = cursor.fetchall()

        # Очистка comboBox
        self.win.storeComboBox.clear()

        # Добавление продуктов в comboBox
        for product in products:
            self.win.storeComboBox.addItem(product[0])

        conn.close()

    def add_storage_item(self):
        try:
            # Получение данных из формы
            product_name = self.win.storeComboBox.currentText()
            quantity = self.win.storeSpinBox.value()
            purchase_date = self.win.purchaseDateDateEdit.date().toString("yyyy-MM-dd")

            # Подключение к базе данных
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()

            # Обновление данных продукта
            cursor.execute('''
                UPDATE products
                SET quantity = ?, purchase_date = ?
                WHERE name = ?
            ''', (quantity, purchase_date, product_name))

            conn.commit()
            conn.close()

            self.parent.refresh_storade_table()
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
        self.win = uic.loadUi("static/ui/add_storage_item.ui")
        # self.db = DatabaseController()
        # self.product_id = product_id

        # Установка имени продукта
        self.win.storeComboBox.addItem(product_name)
        self.win.storeComboBox.setEnabled(False)  # Делаем comboBox неактивным

        # Загрузка текущих данных продукта
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()
        cursor.execute('SELECT quantity, purchase_date FROM products WHERE id = ?', (product_id,))
        product_data = cursor.fetchone()
        conn.close()

        if product_data:
            self.win.storeSpinBox.setValue(product_data[0])
            if product_data[1]:
                date = QtWidgets.QDateEdit.fromString(product_data[1], "yyyy-MM-dd")
                self.win.purchaseDateDateEdit.setDate(date)
            else:
                self.win.purchaseDateDateEdit.setDate(QtWidgets.QDateEdit.currentDate())

        # Подключение обработчиков кнопок
        self.win.addStoragePushButton.clicked.connect(self.update_storage_item)
        self.win.cancelStorageItemPushButton.clicked.connect(self.win.close)

        self.win.show()

    def update_storage_item(self):
        try:
            quantity = self.win.storeSpinBox.value()
            purchase_date = self.win.purchaseDateDateEdit.date().toString("yyyy-MM-dd")

            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE products
                SET quantity = ?, purchase_date = ?
                WHERE id = ?
            ''', (quantity, purchase_date, self.product_id))

            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Данные продукта успешно обновлены")
            self.win.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при обновлении данных продукта: {str(e)}")
            if 'conn' in locals():
                conn.close()