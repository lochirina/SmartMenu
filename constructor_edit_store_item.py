from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sqlite3

class StorageEditDialog(QtWidgets.QDialog):
    def __init__(self, parent, product_id, product_name, purchase_date, current_quantity):
        super().__init__(parent)
        # uic.loadUi("static/ui/add_storage_item.ui", self)  # Загружаем UI

        try:
            uic.loadUi("static/ui/add_storage_item.ui", self)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Не удалось загрузить окно редактирования: {e}")

        self.product_id = product_id

        # Инициализация виджетов
        self.storeComboBox.setEditable(False)
        self.storeComboBox.addItem(product_name)  # Отображаем имя продукта
        self.storeComboBox.setEnabled(False)  # Блокируем редактирование

        self.purchaseDateDateEdit.setDate(purchase_date)  # Устанавливаем дату покупки
        self.purchaseDateDateEdit.setEnabled(False)  # Блокируем редактирование

        self.storeSpinBox.setValue(current_quantity)  # Устанавливаем текущее количество

        # Привязываем кнопку сохранения
        self.addStoragePushButton.clicked.connect(self.save_changes)

    def save_changes(self):
        # Получение нового количества из SpinBox
        new_quantity = self.storeSpinBox.value()

        try:
            # Сохранение изменений в базе данных
            conn = sqlite3.connect("db/smart_menu.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET quantity = ? WHERE id = ?",
                (new_quantity, self.product_id)
            )
            conn.commit()
            conn.close()

            # Успешное сохранение
            QtWidgets.QMessageBox.information(self, "Успех", "Количество успешно обновлено!")
            self.accept()  # Закрываем окно
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении данных: {e}")