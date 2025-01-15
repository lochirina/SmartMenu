from PyQt5 import QtWidgets, uic, QtCore, QtGui
from datetime import datetime
import sqlite3

from PyQt5.QtSql import QSqlTableModel

from db_controller import DatabaseController

class InspectDishWindow:
    def __init__(self, dish_id):
        self.win = uic.loadUi("static/ui/ispect_dish.ui")
        self.db = DatabaseController()
        self.dish_id = dish_id

        # Подгрузка данных блюда
        self.load_dish_data(dish_id)

        # Подключение обработчиков
        self.win.calculateAutoNutritValuecheckBox.stateChanged.connect(self.handle_auto_calculate_toggle)
        self.win.addDishPushButton.clicked.connect(self.save_dish_changes)

        self.win.show()

    def load_dish_data(self, dish_id):
        """
        Загружает данные блюда из базы данных и отображает их в интерфейсе.
        """
        try:
            dish = self.db.get_dish_by_id(dish_id)
            if dish:
                # Имя и описание блюда
                self.win.nameOfDishLineEdit.setText(dish['name'])
                self.win.infoDishPlainTextEdit.setPlainText(dish['description'])

                # Автоматический расчет пищевой ценности
                auto_calculate = dish['auto_calorie_calc']
                self.win.calculateAutoNutritValuecheckBox.setChecked(auto_calculate)

                # Калории, белки, жиры, углеводы
                if not auto_calculate:
                    self.win.kaloriesLineEdit.setText(str(dish['calories']))
                    self.win.proteinsLineEdit.setText(str(dish['proteins']))
                    self.win.fatsLineEdit.setText(str(dish['fats']))
                    self.win.carbohLineEdit.setText(str(dish['carbohydrates']))
                else:
                    self.handle_auto_calculate_toggle(True)

                # Подгрузка ингредиентов в таблицу
                print(1)
                self.load_ingredients_to_table(dish_id)
                print(2)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Ошибка загрузки данных блюда: {str(e)}")

    def load_ingredients_to_table(self, dish_id):
        """
        Загружает ингредиенты блюда в таблицу QTableView.
        """
        try:
            # Создаем соединение с базой данных
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()

            # Выполняем SQL-запрос для получения данных
            query = '''
            SELECT
                p.name AS ingredient_name,
                di.quantity AS ingredient_quantity,
                mu.name AS unit_name
            FROM dish_ingredients di
            JOIN products p ON di.product_id = p.id
            JOIN measurement_units mu ON p.measurement_unit_id = mu.id
            WHERE di.dish_id = ?
            '''
            cursor.execute(query, (dish_id,))
            ingredients = cursor.fetchall()
            print(ingredients)

            # Закрываем соединение
            conn.close()

            # Настройка модели таблицы
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["Название ингредиента", "Количество", "Ед. изм."])

            # Заполнение модели данными
            for row in ingredients:
                items = [
                    QtGui.QStandardItem(str(row[0])),  # Название ингредиента
                    QtGui.QStandardItem(str(row[1])),  # Количество
                    QtGui.QStandardItem(str(row[2])),  # Ед. изм.
                ]
                model.appendRow(items)

            # Установка модели в QTableView
            self.win.prodListTableView.setModel(model)

            # Настройка отображения
            self.win.prodListTableView.horizontalHeader().setStretchLastSection(True)
            self.win.prodListTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.win.prodListTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Ошибка загрузки ингредиентов: {str(e)}")

    def handle_auto_calculate_toggle(self, state):
        """
        Обработчик изменения состояния чекбокса автоматического расчета.
        """
        fields = [
            self.win.kaloriesLineEdit,
            self.win.proteinsLineEdit,
            self.win.fatsLineEdit,
            self.win.carbohLineEdit
        ]

        for field in fields:
            field.setEnabled(not state)
            if state:
                # Если авторасчет включен, пересчитываем значения
                ingredients = self.db.get_ingredients_by_dish_id(self.dish_id)
                nutrition = self.db.calculate_nutrition([(i['name'], i['quantity']) for i in ingredients])
                self.win.kaloriesLineEdit.setText(str(nutrition[0]))
                self.win.proteinsLineEdit.setText(str(nutrition[1]))
                self.win.fatsLineEdit.setText(str(nutrition[2]))
                self.win.carbohLineEdit.setText(str(nutrition[3]))

    def save_dish_changes(self):
        """
        Сохраняет изменения в данные блюда.
        """
        try:
            name = self.win.nameOfDishLineEdit.text()
            description = self.win.infoDishPlainTextEdit.toPlainText()
            auto_calculate = self.win.calculateAutoNutritValuecheckBox.isChecked()

            if not name:
                QtWidgets.QMessageBox.warning(self.win, "Ошибка", "Название блюда не может быть пустым.")
                return

            if not auto_calculate:
                calories = float(self.win.kaloriesLineEdit.text() or 0)
                proteins = float(self.win.proteinsLineEdit.text() or 0)
                fats = float(self.win.fatsLineEdit.text() or 0)
                carbs = float(self.win.carbohLineEdit.text() or 0)
            else:
                calories = proteins = fats = carbs = None

            # Сохранение в базу данных
            self.db.update_dish(self.dish_id, name, description, auto_calculate, calories, proteins, fats, carbs)
            QtWidgets.QMessageBox.information(self.win, "Успех", "Изменения успешно сохранены.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка", f"Ошибка сохранения данных: {str(e)}")