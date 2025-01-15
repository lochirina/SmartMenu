import csv
import pandas as pd

from PyQt5.QtSql import QSqlDatabase

from constructor_add_dish_window import *
from constructor_add_menu import *
from constructor_add_prod_window import *
from constructor_add_store_item_window import *
from constructor_inspect_dish_window import *
from db_controller import *
from menu_display_controller import *
from menu_history_controller import *


class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = uic.loadUi("static/ui/main.ui")
        self.db_controller = DatabaseController()
        self.menu_display_controller = MenuDisplayController(self.win, "db/smart_menu.db")
        self.menu_history = MenuHistory(self)

        self.setup_products_table()
        self.setup_dishes_table()
        self.setup_storage_table()

        # Настройка кнопки удаления и изменения из запасов
        self.win.deliteStorageItemPushButton.clicked.connect(self.delete_storage_item)
        self.win.editStoraItemPushButton.clicked.connect(self.edit_storage_item)
        self.win.sortStorePushButton_a_z.clicked.connect(self.sort_storage_a_z)
        self.win.sortStorePushButton_1_n.clicked.connect(self.sort_storage_1_n)

        # Настройка кнопки удаления изменения и сортирорвки блюд
        self.win.deliteDishPushButton.clicked.connect(self.delete_dish)
        self.win.inspectDishPushButton.clicked.connect(self.open_inspect_dish)
        self.win.sortDishesPushButton.clicked.connect(self.sort_dishes)

        # Настройка кнопки удаления, изменения и сортировки продуктов
        self.win.deliteProdPushButton.clicked.connect(self.delete_product)
        self.win.editProdPushButton.clicked.connect(self.open_edit_product_window)
        self.win.sortProdPushButton.clicked.connect(self.sort_products)

        # Настройка кнопки удаления и экспорта сегодняшнего меню
        self.win.deliteMenuTodayPushButton.clicked.connect(self.delete_menu_today)
        self.win.exportTxtMenuPushButton.clicked.connect(self.export_to_txt)

        # Настройка кнопок экспорта меню
        self.win.exportExeDishesPushButton.clicked.connect(self.export_to_excel)
        self.win.exportCsvDishesPushButton.clicked.connect(self.export_to_csv)

        # Подключение обработчиков нажатий кнопок
        self.win.addProdPushButton.clicked.connect(self.open_add_prod)
        self.win.addMenuPushButton.clicked.connect(self.open_add_menu)
        self.win.addDishPushButton.clicked.connect(self.open_add_dish)
        self.win.addStorageItemPushButton.clicked.connect(self.open_add_storage)

        self.win.show()

        # Обновление информации о меню и историю меню
        self.menu_display_controller.update_menu_display()
        self.menu_history.load_menu_history()
        sys.exit(self.app.exec())

    def open_add_prod(self):
        self.add_prod_window = AddProductWindow()
        self.add_prod_window.parent = self

    def open_add_menu(self):
        self.add_menu_window = AddMenuWindow()
        self.add_menu_window.parent = self

    def open_add_dish(self):
        self.add_dish_window = AddDishWindow()
        self.add_dish_window.parent = self

    def delete_dish(self):
        # Получение выбранную строку
        selected_indexes = self.win.dishListTableView.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите блюдо для удаления")
            return

        # Получение названия блюда из выбранной строки
        selected_row = selected_indexes[0].row()
        dish_name = self.win.dishListTableView.model().data(
            self.win.dishListTableView.model().index(selected_row, 1)  # Название блюда в столбце 1
        )

        # Получение ID блюда из базы данных
        try:
            dish_id = self.db_controller.get_dish_id_by_name(dish_name)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Не удалось найти ID блюда: {str(e)}")
            return

        # Удаление блюда и связанных записей
        try:
            success = self.db_controller.delete_dish(dish_id)
            if success:
                # Обновление таблицы
                self.refresh_dishes_table()
                QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Блюдо успешно удалено")
            else:
                raise Exception("Удаление завершилось с ошибкой.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении блюда: {str(e)}")

    def open_inspect_dish(self):
        """
        Открывает окно просмотра/редактирования блюда.
        """
        try:
            # Получение объекта выбора из QTableView
            selection_model = self.win.dishListTableView.selectionModel()

            # Проверка, есть ли выбранные строки
            if not selection_model.hasSelection():
                QtWidgets.QMessageBox.warning(self.win, "Ошибка", "Не выбрано блюдо.")
                return

            # Получение индекса текущей выбранной строки
            selected_index = selection_model.currentIndex()
            if not selected_index.isValid():
                QtWidgets.QMessageBox.warning(self.win, "Ошибка", "Не выбрано блюдо.")
                return

            # Типи в первом столбце таблицы содержится dish_id
            dish_id = self.win.dishListTableView.model().data(selected_index.siblingAtColumn(0))
            if not dish_id:
                QtWidgets.QMessageBox.warning(self.win, "Ошибка", "Не удалось получить ID блюда.")
                return

            print(f"Открывается окно для блюда с ID: {dish_id}")  # Для отладки

            # Открывает окно просмотра блюда и передаем dish_id
            self.inspect_dish_window = InspectDishWindow(dish_id)
            self.inspect_dish_window.parent = self

        except Exception as e:
            print(f"Ошибка при открытии окна: {str(e)}")  # Для логирования

    def open_add_storage(self):
        self.add_storage_window = AddStorageWindow()
        self.add_storage_window.parent = self

    def open_edit_product_window(self):
        selected = self.win.prodListTableView.currentIndex().row()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self.win, "Внимание", "Пожалуйста, выберите продукт для редактирования.")
            return

        # Получает данные о продукте из модели
        product_id = self.prod_model.index(selected, 0).data()  # ID продукта

        self.edit_prod_window = EditProductWindow(product_id)
        self.edit_prod_window.parent = self

    def edit_storage_item(self):
        # Получает выбранную строку
        selected_row = self.win.storageListTableView.currentIndex().row()

        if selected_row < 0: # != 1
            QtWidgets.QMessageBox.warning(self.win, "Внимание", "Пожалуйста, выберите продукт для редактирования.")
            return

        # Получает данные о продукте из модели
        product_id = self.storage_model.index(selected_row, 0).data()  # ID продукта
        product_name = self.storage_model.index(selected_row, 1).data()  # Имя продукта

        # Получает дату покупки из базы данных
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

        # Открывает диалог редактирования
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

        # Получает id продукта из модели
        product_id = self.storage_model.data(self.storage_model.index(index.row(), 0))

        try:

            # Обновляет отображения таблицы
            self.refresh_storage_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              "Продукт успешно удален из хранилища")
            self.refresh_storage_table()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении продукта: {str(e)}")

    def delete_product(self):
        # Получает выбранную строку
        selected_indexes = self.win.prodListTableView.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self.win, "Предупреждение",
                                          "Выберите продукт для удаления")
            return

        # Получает имя продукта из выбранной строки
        selected_row = selected_indexes[0].row()
        product_name = self.win.prodListTableView.model().data(
            self.win.prodListTableView.model().index(selected_row, 1)  # Предполагаем, что название продукта в столбце 1
        )

        # Подтверждает удаления
        reply = QtWidgets.QMessageBox.question(
            self.win,
            "Подтверждение",
            f"Вы уверены, что хотите удалить продукт \"{product_name}\"?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.No:
            return

        # Удаляет продукта из базы данных
        try:
            self.db_controller.delete_product_by_name(product_name)

            # Обновляет таблицы
            self.refresh_products_table()

            QtWidgets.QMessageBox.information(self.win, "Успех",
                                              f"Продукт \"{product_name}\" успешно удален")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при удалении продукта: {str(e)}")

    def setup_products_table(self):
        # Создает подключение к базе данных через QtSql
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('db/smart_menu.db')
        db.open()

        # Создает модель для таблицы
        self.prod_model = QSqlTableModel()
        self.prod_model.setTable('products')

        # Устанавливает заголовки столбцов
        self.prod_model.setHeaderData(1, QtCore.Qt.Horizontal, "Название продукта")

        # Выбирает только столбец с названием
        self.prod_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.prod_model.select()

        # Устанавливает модель для таблицы
        self.win.prodListTableView.setModel(self.prod_model)

        # Скрывает все столбцы кроме названия продукта
        for column in range(self.prod_model.columnCount()):
            if column != 1:  # 1 - индекс столбца name в таблице products
                self.win.prodListTableView.hideColumn(column)

        # Растягивает столбец на всю ширину таблицы
        self.win.prodListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def setup_dishes_table(self):
        # Настройка таблицы блюд
        self.dishes_model = QSqlTableModel()
        self.dishes_model.setTable("dishes")
        self.dishes_model.setFilter("")  # Показывает все блюда
        self.dishes_model.select()
        self.dishes_model.setHeaderData(1, Qt.Horizontal, "Название блюда")

        self.win.dishListTableView.setModel(self.dishes_model)
        self.win.dishListTableView.setColumnHidden(0, True)  # Скрывает id
        # Оставляет видимым только столбец с названием
        for i in range(2, self.dishes_model.columnCount()):
            self.win.dishListTableView.setColumnHidden(i, True)

        # Растягивает столбец на всю ширину таблицы
        self.win.dishListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def setup_storage_table(self):
        # Настройка таблицы запасов
        self.storage_model = QSqlTableModel()
        self.storage_model.setTable("products")
        self.storage_model.setFilter("quantity > 0")  # Показывает только продукты с ненулевым количеством
        self.storage_model.select()
        self.storage_model.setHeaderData(1, Qt.Horizontal, "Название продукта")
        self.storage_model.setHeaderData(8, Qt.Horizontal, "Кол-во")

        self.win.storageListTableView.setModel(self.storage_model)
        self.win.storageListTableView.setColumnHidden(0, True)  # Скрываем id
        # Оставляет видимыми только столбцы с названием и количеством
        for i in range(2, self.storage_model.columnCount()):
            if i != 8:  # 8 - это индекс столбца quantity
                self.win.storageListTableView.setColumnHidden(i, True)

        # Обновляет таблицы при изменении данных
        self.storage_model.dataChanged.connect(self.refresh_storage_table)

        # Растягивает столбец на всю ширину таблицы
        self.win.storageListTableView.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

    def delete_menu_today(self):
        """
        Обработчик удаления меню на сегодняшний день.
        При этом восстанавливаются ингредиенты для блюд из удаляемого меню.
        """
        try:
            # Получение блюд, входящих в меню на сегодняшний день
            today_menu = self.db_controller.get_today_menu()  # [(meal, dish_id), ...]
            print("today_menu", today_menu)

            if not today_menu:
                QtWidgets.QMessageBox.information(
                    None,
                    "Удаление невозможно",
                    "Меню на сегодня не составлено. Удаление невозможно."
                )
                return

            # Восстанавливает ингредиенты для каждого блюда
            for one_menu in today_menu:
                for dish_id in one_menu:
                    self.db_controller.restore_ingredients_by_dish_id(dish_id)

            # Удаление меню из базы данных
            result = self.db_controller.delete_today_menu()

            if result:
                QtWidgets.QMessageBox.information(
                    None,
                    "Удаление успешно",
                    "Меню на сегодня успешно удалено. Ингредиенты восстановлены."
                )

            else:
                QtWidgets.QMessageBox.critical(
                    None,
                    "Ошибка",
                    "Произошла ошибка при удалении меню. Попробуйте еще раз."
                )

            self.menu_display_controller.update_menu_display()  # Обновляем информацию о меню
            self.menu_history.load_menu_history()  # Обновляем историю меню


        except Exception as e:
            print(f"Ошибка при удалении меню: {e}")
            QtWidgets.QMessageBox.critical(
                None,
                "Ошибка",
                "Произошла ошибка при удалении меню. Попробуйте еще раз."
            )

    def export_to_csv(self):
        """
        Экспорт истории меню в CSV.
        """
        try:
            # Открываем диалоговое окно для выбора файла
            file_path, _ = QFileDialog.getSaveFileName(self.win, "Сохранить как", "", "CSV Files (*.csv)")
            if not file_path:
                return  # Пользователь отменил выбор

            # Получаем данные из базы
            data = self.db_controller.fetch_menu_history()

            # Экспортируем данные в CSV
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Дата", "Название блюда на завтрак", "Название блюда на обед", "Название блюда на ужин", "Калории",
                     "Белки", "Жиры", "Углеводы"])
                writer.writerows(data)

            QtWidgets.QMessageBox.information(self.win, "Успех", "Данные успешно экспортированы в CSV.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Ошибка экспорта в CSV: {str(e)}")

    def export_to_excel(self):
        """
        Экспорт истории меню в Excel.
        """
        try:
            # Открывает диалоговое окно для выбора файла
            file_path, _ = QFileDialog.getSaveFileName(self.win, "Сохранить как", "", "Excel Files (*.xlsx)")
            if not file_path:
                return  # Пользователь отменил выбор

            # Получает данные из базы
            data = self.db_controller.fetch_menu_history()

            # Создает DataFrame и сохраняет в Excel
            df = pd.DataFrame(data, columns=["Дата", "Название блюда на завтрак", "Название блюда на обед",
                                             "Название блюда на ужин", "Калории", "Белки", "Жиры", "Углеводы"])
            df.to_excel(file_path, index=False)

            QtWidgets.QMessageBox.information(self.win, "Успех", "Данные успешно экспортированы в Excel.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Ошибка экспорта в Excel: {str(e)}")

    def export_to_txt(self):
        self.menu_display_controller.export_today_menu_to_txt(self.win)

    def sort_products(self):
        # Сортировка по алфавиту, по столбцу с индексом 1 (название продукта)
        self.prod_model.setSort(1, QtCore.Qt.AscendingOrder)
        self.prod_model.select()  # Перезагружает данные для применения сортировки

    def sort_dishes(self):
        # Сортировка по алфавиту, по столбцу с индексом 1 (название)
        self.dishes_model.setSort(1, QtCore.Qt.AscendingOrder)
        self.dishes_model.select()  # Перезагружает данные для применения сортировки

    def sort_storage_a_z(self):
        # Сортировка по алфавиту, по столбцу с индексом 1 (название)
        self.storage_model.setSort(1, QtCore.Qt.AscendingOrder)
        self.storage_model.select()  # Перезагружает данные для применения сортировки

    def sort_storage_1_n(self):
        # Сортировка по алфавиту, по столбцу с индексом 8 (кол-во)
        self.storage_model.setSort(8, QtCore.Qt.AscendingOrder)
        self.storage_model.select()  # Перезагружает данные для применения сортировки

    def refresh_products_table(self):
        self.prod_model.select()

    def refresh_dishes_table(self):
        self.dishes_model.select()

    def refresh_storage_table(self):
        self.storage_model.select()


if __name__ == '__main__':
    MainWindow()

