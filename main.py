from PyQt5 import QtWidgets, uic, QtCore
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

from constructor_add_dish_window import *
from constructor_add_menu import *
from constructor_add_store_item_window import *
from constructor_add_prod_window import *
from constructor_inspect_dish_window import *
# from constructor_edit_store_item import StorageEditDialog
from db_controller import *

class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = uic.loadUi("static/ui/main.ui")
        self.db_controller = DatabaseController()
        self.setup_products_table()
        self.setup_dishes_table()
        self.setup_storage_table()

        # Настройка кнопки удаления и изменения из запасов
        self.win.deliteStorageItemPushButton.clicked.connect(self.delete_storage_item)
        self.win.editStoraItemPushButton.clicked.connect(self.edit_storage_item)

        # Настройка кнопки удаления и изменения из блюд
        self.win.deliteDishPushButton.clicked.connect(self.delete_dish)
        self.win.inspectDishPushButton.clicked.connect(self.open_inspect_dish)

        # Настройка кнопки удаления и изменения из продуктов
        self.win.deliteProdPushButton.clicked.connect(self.delete_product)
        self.win.editProdPushButton.clicked.connect(self.open_edit_product_window)

        # Подключаем обработчики нажатий кнопок
        self.win.addProdPushButton.clicked.connect(self.open_add_prod)
        self.win.addMenuPushButton.clicked.connect(self.open_add_menu)
        self.win.addDishPushButton.clicked.connect(self.open_add_dish)
        self.win.addStorageItemPushButton.clicked.connect(self.open_add_storage)

        self.win.show()
        sys.exit(self.app.exec())

    def open_add_prod(self):
        self.add_prod_window = AddProductWindow()
        self.add_prod_window.parent = self  # Передаем ссылку на главное окно

    def open_add_menu(self):
        self.add_menu_window = AddMenuWindow()
        self.add_menu_window.parent = self
        # self.add_menu_window = uic.loadUi("res/ui/add_menu.ui")
        # self.add_menu_window.show()

    def open_add_dish(self):
        self.add_dish_window = AddDishWindow()
        self.add_dish_window.parent = self

    def delete_dish(self):
        # Получаем выбранную строку
        selected_indexes = self.win.dishListTableView.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите блюдо для удаления")
            return

        # Получаем название блюда из выбранной строки
        selected_row = selected_indexes[0].row()
        dish_name = self.win.dishListTableView.model().data(
            self.win.dishListTableView.model().index(selected_row, 1)  # Название блюда в столбце 1
        )

        # Получаем ID блюда из базы данных
        try:
            dish_id = self.db_controller.get_dish_id_by_name(dish_name)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Не удалось найти ID блюда: {str(e)}")
            return

        # Удаляем блюдо и связанные записи
        try:
            success = self.db_controller.delete_dish(dish_id)
            if success:
                # Обновляем таблицу
                self.refresh_dishes_table()
                QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Блюдо успешно удалено")
            else:
                raise Exception("Удаление завершилось с ошибкой.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении блюда: {str(e)}")

    def open_inspect_dish(self):
        self.inspect_dish_window = InspectDishWindow()
        self.inspect_dish_window.parent = self

    def open_add_storage(self):
        self.add_storage_window = AddStorageWindow()
        self.add_storage_window.parent = self

    def open_edit_product_window(self):
        selected = self.win.prodListTableView.currentIndex().row()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self.win, "Внимание", "Пожалуйста, выберите продукт для редактирования.")
            return
        # product_id = int(selected[0].data())  # Получение ID выбранного продукта
        # Получаем данные о продукте из модели
        product_id = self.prod_model.index(selected, 0).data()  # ID продукта
        # product_name = self.prod_model.index(selected, 1).data()  # Имя продукта

        self.edit_prod_window = EditProductWindow(product_id)
        self.edit_prod_window.parent = self

    def edit_storage_item(self):
        # Получаем выбранную строку
        selected_row = self.win.storageListTableView.currentIndex().row()

        if selected_row < 0: # != 1
            QtWidgets.QMessageBox.warning(self.win, "Внимание", "Пожалуйста, выберите продукт для редактирования.")
            return

        # Получаем данные о продукте из модели
        product_id = self.storage_model.index(selected_row, 0).data()  # ID продукта
        product_name = self.storage_model.index(selected_row, 1).data()  # Имя продукта

        # Получаем дату покупки из базы данных
        try:
            conn = sqlite3.connect("db/smart_menu.db")
            cursor = conn.cursor()
            cursor.execute("SELECT purchase_date FROM products WHERE id = ?", (product_id,))
            purchase_date = cursor.fetchone()
            if purchase_date:
                purchase_date = QtCore.QDate.fromString(purchase_date[0], "yyyy-MM-dd")
            else:
                raise ValueError("Дата покупки не найдена.")
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Не удалось загрузить данные о продукте: {e}")
            return

        # Открываем диалог редактирования
        print("Окно вызывается")
        self.edit_store_window = EditStorageWindow(product_id, product_name)
        self.edit_store_window.parent = self


    def delete_storage_item(self):
        # Полученик индекса выбранной строки
        index = self.win.storageListTableView.currentIndex()
        if not index.isValid():
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите продукт для удаления")
            return

        # Получаение id продукта из модели
        product_id = self.storage_model.data(self.storage_model.index(index.row(), 0))

        try:

            # Обновление отображения таблицы
            self.refresh_storage_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              "Продукт успешно удален из хранилища")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении продукта: {str(e)}")

    def delete_product(self):
        # Получаем выбранную строку
        selected_indexes = self.win.prodListTableView.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите продукт для удаления")
            return

        # Получаем имя продукта из выбранной строки
        selected_row = selected_indexes[0].row()
        product_name = self.win.prodListTableView.model().data(
            self.win.prodListTableView.model().index(selected_row, 1)  # Предполагаем, что название продукта в столбце 1
        )

        # Подтверждение удаления
        reply = QtWidgets.QMessageBox.question(
            self.win,
            "Подтверждение",
            f"Вы уверены, что хотите удалить продукт \"{product_name}\"?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.No:
            return

        # Удаление продукта из базы данных
        try:
            self.db_controller.delete_product_by_name(product_name)

            # Обновление таблицы
            self.refresh_products_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              f"Продукт \"{product_name}\" успешно удален")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении продукта: {str(e)}")

    def setup_products_table(self):
        # Создаем подключение к базе данных через QtSql
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('db/smart_menu.db')
        db.open()

        # Создаем модель для таблицы
        self.prod_model = QSqlTableModel()
        self.prod_model.setTable('products')

        # Устанавливаем заголовки столбцов
        # self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Название продукта")

        # Выбираем только столбец с названием
        self.prod_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.prod_model.select()

        # Устанавливаем модель для таблицы
        self.win.prodListTableView.setModel(self.prod_model)

        # Скрываем все столбцы кроме названия продукта
        for column in range(self.prod_model.columnCount()):
            if column != 1:  # 1 - индекс столбца name в таблице products
                self.win.prodListTableView.hideColumn(column)

        # Растягиваем столбец на всю ширину таблицы
        self.win.prodListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def setup_dishes_table(self):
        # Настройка таблицы блюд
        self.dishes_model = QSqlTableModel()
        self.dishes_model.setTable("dishes")
        self.dishes_model.setFilter("")  # Показываем все блюда
        self.dishes_model.select()
        self.dishes_model.setHeaderData(1, Qt.Horizontal, "Название блюда")

        self.win.dishListTableView.setModel(self.dishes_model)
        self.win.dishListTableView.setColumnHidden(0, True)  # Скрываем id
        # Оставляем видимым только столбец с названием
        for i in range(2, self.dishes_model.columnCount()):
            self.win.dishListTableView.setColumnHidden(i, True)

        # Растягиваем столбец на всю ширину таблицы
        self.win.dishListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def setup_storage_table(self):
        # Настройка таблицы запасов
        self.storage_model = QSqlTableModel()
        self.storage_model.setTable("products")
        self.storage_model.setFilter("quantity > 0")  # Показываем только продукты с ненулевым количеством
        self.storage_model.select()
        self.storage_model.setHeaderData(1, Qt.Horizontal, "Название продукта")
        self.storage_model.setHeaderData(8, Qt.Horizontal, "Кол-во")

        self.win.storageListTableView.setModel(self.storage_model)
        self.win.storageListTableView.setColumnHidden(0, True)  # Скрываем id
        # Оставляем видимыми только столбцы с названием и количеством
        for i in range(2, self.storage_model.columnCount()):
            if i != 8:  # 8 - это индекс столбца quantity
                self.win.storageListTableView.setColumnHidden(i, True)

        # Обновляем таблицы при изменении данных
        self.storage_model.dataChanged.connect(self.refresh_storage_table)

        # Растягиваем столбец на всю ширину таблицы
        self.win.storageListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def refresh_products_table(self):
        self.prod_model.select()

    def refresh_dishes_table(self):
        self.dishes_model.select()

    def refresh_storage_table(self):
        self.storage_model.select()


if __name__ == '__main__':
    MainWindow()

