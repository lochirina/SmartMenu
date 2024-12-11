from PyQt5 import QtWidgets, uic, QtCore
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

from constructor_add_dish_window import *
from constructor_add_menu import *
from constructor_add_store_item_window import *
from constructor_add_prod_window import *
from db_controller import *

class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = uic.loadUi("static/ui/main.ui")
        self.db_controller = DatabaseController()
        self.setup_products_table()
        self.setup_dishes_table()
        self.setup_storade_table()

        # Настройка кнопки удаления и изменения из запасов
        self.win.deliteStorageItemPushButton.clicked.connect(self.delete_storage_item)
        self.win.editStoraItemPushButton.clicked.connect(self.open_edit_storage_item)

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
        # Полученик индекса выбранной строки
        index = self.win.dishListTableView.currentIndex()
        if not index.isValid():
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите продукт для удаления")
            return

        # Получаение id продукта из модели
        dish_id = self.storage_model.data(self.dishes_model.index(index.row(), 0))

        try:
            # Обновление количества через контроллер БД
            self.db_controller.update_product_quantity(dish_id, 0)

            # Обновление отображения таблицы
            self.refresh_storade_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              "Продукт успешно удален из хранилища")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении продукта: {str(e)}")


    def open_edit_storage_item(self):
        # Получаем индекс выбранной строки
        index = self.win.storageListTableView.currentIndex()

        # Получаем данные из модели таблицы
        product_id = self.storage_model.data(self.storage_model.index(index.row(), 0))  # ID в первой колонке
        product_name = self.storage_model.data(self.storage_model.index(index.row(), 1))  # Название во второй колонке

        self.edit_storage_window = EditStorageWindow(product_id, product_name)
        self.edit_storage_window.parent = self
    def open_add_storage(self):

        self.add_storage_window = AddStorageWindow()
        self.add_storage_window.parent = self

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
            self.refresh_dishes_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              "Продукт успешно удален из хранилища")

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

    def setup_storade_table(self):
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
        self.storage_model.dataChanged.connect(self.refresh_storade_table)

        # Растягиваем столбец на всю ширину таблицы
        self.win.storageListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)


    def refresh_products_table(self):
        self.prod_model.select()

    def refresh_dishes_table(self):
        self.dishes_model.select()

    def refresh_storade_table(self):
        self.storage_model.select()


if __name__ == '__main__':
    MainWindow()