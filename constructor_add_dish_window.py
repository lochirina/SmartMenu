from PyQt5 import QtWidgets, uic
import sqlite3

from PyQt5.QtWidgets import QApplication

from db_controller import DatabaseController

class AddDishWindow:
    def __init__(self):
        # Инициализация окна добавления блюда
        self.win = uic.loadUi("static/ui/add_dish.ui")
        self.db = DatabaseController()

        # Инициализируем ComboBox с продуктами
        self.initialize_ingredient_comboboxes()

        # Подключаем обработчик для чекбокса
        self.win.calculateAutoNutritValuecheckBox.stateChanged.connect(
            self.handle_auto_calculate_toggle
        )

        # Подключаем обработчик изменения значения в ComboBox
        for i in range(self.win.verticalLayout_2.count()):
            item = self.win.verticalLayout_2.itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                combo = item.itemAt(0).widget()
                if isinstance(combo, QtWidgets.QComboBox):
                    self.load_products_to_combobox(combo)
                    combo.currentTextChanged.connect(self.handle_ingredient_change)

        # # Добавляем обработчик изменения значения в ComboBox
        # for combo in self.win.findChildren(QtWidgets.QComboBox):
        #     if combo.objectName().startswith('ingredientComboBox'):
        #         combo.currentTextChanged.connect(
        #             lambda text, cb=combo: self.update_unit_label(cb)
        #         )

        self.win.addDishPushButton.clicked.connect(self.action_add_dish)
        self.win.show()

    def load_products_to_combobox(self, combobox):
        """
        Загружает список продуктов из базы данных в указанный ComboBox
        """
        # Подключение к базе данных
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        # Получение всех продуктов
        cursor.execute('SELECT name FROM products ORDER BY name')
        products = cursor.fetchall()

        # Очистка comboBox и добавление значения по умолчанию
        combobox.clear()
        combobox.addItem("---")

        # Добавление продуктов в comboBox
        for product in products:
            combobox.addItem(product[0])

        conn.close()

    def initialize_ingredient_comboboxes(self):
        """
        Инициализирует все существующие ComboBox с продуктами
        """
        # Находим все ComboBox в окне, начинающиеся с 'ingredientComboBox'
        for widget in self.win.findChildren(QtWidgets.QComboBox):
            if widget.objectName().startswith('ingredientComboBox'):
                self.load_products_to_combobox(widget)

    def handle_ingredient_change(self, text):
        """
        Обработчик изменения значения в ComboBox ингредиентов
        """
        # Проверяем, является ли отправитель последним ComboBox
        sender = self.win.sender()
        if text != "---" and sender == self.get_last_combobox():
            # Создаем новый HorizontalLayout
            new_layout = QtWidgets.QHBoxLayout()
            layout_num = self.get_next_layout_number()
            new_layout.setObjectName(f"ingrHorizontalLayout{layout_num}")

            # Создаем новый ComboBox
            new_combo = QtWidgets.QComboBox()
            new_combo.setObjectName(f"ingredientComboBox{layout_num}")
            self.load_products_to_combobox(new_combo)
            new_combo.currentTextChanged.connect(self.handle_ingredient_change)

            # Создаем новый SpinBox
            new_spin = QtWidgets.QSpinBox()
            new_spin.setObjectName(f"countIngredientsSpinBox{layout_num}")

            # Создаем новый Label
            new_label = QtWidgets.QLabel()
            new_label.setObjectName(f"unitIngredLoabel{layout_num}")

            # Добавляем виджеты в layout
            new_layout.addWidget(new_combo)
            new_layout.addWidget(new_spin)
            new_layout.addWidget(new_label)

            # Находим индекс кнопки "Добавить"
            add_button_index = -1
            for i in range(self.win.verticalLayout_2.count()):
                if isinstance(self.win.verticalLayout_2.itemAt(i).widget(), QtWidgets.QPushButton):
                    add_button_index = i
                    break

            # Вставляем новый layout перед кнопкой
            if add_button_index != -1:
                self.win.verticalLayout_2.insertLayout(add_button_index, new_layout)
            else:
                self.win.verticalLayout_2.addLayout(new_layout)

            # Применяем стили после добавления в layout
            new_combo.setStyleSheet("""
                QComboBox {
                    border: 2px solid rgba(100, 100, 100, 25);
                    color: #2d2c2c;
                    border-radius: 4%;
                    padding: 1px 18px 1px 3px;
                    max-height: 32px;
                    min-height: 32px;
                    font-size: 14px; 
                    font-family: Inter; 
                    padding-left: 8px;
                }
                QComboBox::drop-down {
                    border-left-width: 1px;
                    border-left-color: gray;
                    border-left-style: none;
                    border-top-right-radius: 4%;
                    border-bottom-right-radius: 4%;
                    font-size: 14px; 
                    font-family: Inter;
                    padding-left: 8px; 
                }
            """)

            new_spin.setStyleSheet("""
                QSpinBox {
                    border: 2px solid rgba(100, 100, 100, 25);
                    color: #2d2c2c;
                    border-radius: 4%;
                    padding: 1px 18px 1px 3px;
                    height: 32px;
                    min-width: 56px;
                    max-width: 56px;
                    font-size: 14px; 
                    font-family: Inter; 
                    padding-left: 8px;
                }
            """)

            new_label.setStyleSheet("""
                QLabel {
                    background-color: none;
                    color: #2d2c2c;
                    border:none;
                    margin-top: 8px;
                    margin-bottom:8px;

                    text-align:left;
                    vertical-align:text-top;
                    font-size:14px;
                    font-family:Inter;
                    line-height:auto;
                    border-style:hidden;
                    outline:none;

                    min-width: 56px;
                    max-width: 56px;
                }
            """)

            # Увеличиваем высоту окна
            # current_height = self.win.height()
            # self.win.setFixedHeight(current_height + 32)
            self.update_frame_and_window_height()

            # Обеновление стилей
            QApplication.style().polish(new_combo)

    def handle_auto_calculate_toggle(self, state):
        """
        Обработчик изменения состояния чекбокса автоматического расчета
        Args:
            state (bool): Состояние чекбокса
        """
        # Список полей для блокировки
        fields = [
            self.win.kaloriesLineEdit,
            self.win.proteinsLineEdit,
            self.win.fatsLineEdit,
            self.win.carbohLineEdit
        ]

        # Блокируем или разблокируем поля
        for field in fields:
            field.setEnabled(not state)
            # Очищаем поля при включении автоматического расчета
            if state:
                field.clear()

    def update_frame_and_window_height(self, increase=True):
        """
        Обновляет высоту verticalFrame и окна
        Args:
            increase (bool): True для увеличения, False для уменьшения
        """
        # Получаем текущую высоту фрейма
        frame = self.win.findChild(QtWidgets.QFrame, "verticalFrame")
        current_frame_height = frame.height()

        # Изменяем высоту на 32 пикселя
        delta = 32 if increase else -32
        frame.setFixedHeight(current_frame_height + delta)

        # Изменяем высоту окна
        current_window_height = self.win.height()
        self.win.setFixedHeight(current_window_height + delta)

    def add_ingredient_row(self):
        # Создаем новый горизонтальный layout
        self.ingr_layout_counter += 1
        new_horiz_layout = QtWidgets.QHBoxLayout()
        new_horiz_layout.setObjectName(f"ingrHorizontalLayout{self.ingr_layout_counter}")

        # Создаем и настраиваем новый ComboBox
        new_combo = QtWidgets.QComboBox()
        new_combo.setObjectName(f"ingredientComboBox_{self.ingr_layout_counter}")
        # Применяем такой же стиль как у остальных ComboBox
        new_combo.setStyleSheet(self.win.ingredientComboBox.styleSheet())
        self.load_products_to_combobox(new_combo)
        new_combo.currentTextChanged.connect(self.check_and_add_ingredient_row)

        # Создаем и настраиваем новый SpinBox
        new_spin = QtWidgets.QSpinBox()
        new_spin.setObjectName(f"countIngredientsSpinBox_{self.ingr_layout_counter}")

        print(f"countIngredientsSpinBox_{self.ingr_layout_counter}")

        # Применяем такой же стиль как у остальных SpinBox
        new_spin.setStyleSheet(self.win.countIngredientsSpinBox.styleSheet())

        # Добавляем виджеты в layout
        new_horiz_layout.addWidget(new_combo)
        new_horiz_layout.addWidget(new_spin)

        # Находим индекс кнопки "Добавить"
        add_button_index = -1
        for i in range(self.win.verticalLayout_2.count()):
            if self.win.verticalLayout_2.itemAt(i).widget() == self.win.addDishPushButton:
                add_button_index = i
                break

        # Вставляем новый layout перед кнопкой
        if add_button_index != -1:
            self.win.verticalLayout_2.insertLayout(add_button_index, new_horiz_layout)
        else:
            # Если кнопка не найдена, добавляем в конец
            self.win.verticalLayout_2.addLayout(new_horiz_layout)

        # Увеличиваем высоту окна
        current_height = self.win.height()
        self.win.setFixedHeight(current_height + 32)

    def get_last_combobox(self):
        """
        Получает ссылку на последний ComboBox в verticalLayout_2
        """
        last_combo = None
        for i in range(self.win.verticalLayout_2.count()):
            item = self.win.verticalLayout_2.itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                combo = item.itemAt(0).widget()
                if isinstance(combo, QtWidgets.QComboBox):
                    last_combo = combo
        return last_combo

    def get_next_layout_number(self):
        """
        Получает следующий порядковый номер для layout
        """
        max_num = 0
        for i in range(self.win.verticalLayout_2.count()):
            item = self.win.verticalLayout_2.itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                name = item.objectName()
                if name.startswith("ingrHorizontalLayout"):
                    num = int(name.replace("ingrHorizontalLayout", ""))
                    max_num = max(max_num, num)
        return max_num + 1

    def action_add_dish(self):
        """Обработчик нажатия кнопки Добавить"""
        # Получаем данные из полей ввода
        name = self.win.nameOfDishLineEdit.text()
        description = self.win.infoDishPlainTextEdit.toPlainText()
        auto_calculate = self.win.calculateAutoNutritValuecheckBox.isChecked() # Булевое значение

        # Проверяем обязательные поля
        if not name:
            QtWidgets.QMessageBox.warning(self.win, "Ошибка",
                                          "Введите название блюда")
            return

        try:
            # Собираем ингредиенты
            ingredients = []
            for i in range(self.win.verticalLayout_2.count()):
                item = self.win.verticalLayout_2.itemAt(i)
                if isinstance(item, QtWidgets.QHBoxLayout):
                    combo = item.itemAt(0).widget()
                    spin = item.itemAt(1).widget()
                    if isinstance(combo, QtWidgets.QComboBox) and combo.currentText() != "---":
                        ingredients.append((combo.currentText(), spin.value()))
                        print(ingredients)

            # Получаем пищевую ценность
            if auto_calculate:
                # Автоматический расчет на основе ингредиентов
                calories, proteins, fats, carbs = self.db.calculate_nutrition(ingredients)
            else:
                # Берем значения из полей ввода
                calories = float(self.win.kaloriesLineEdit.text() or 0)
                proteins = float(self.win.proteinsLineEdit.text() or 0)
                fats = float(self.win.fatsLineEdit.text() or 0)
                carbs = float(self.win.carbohLineEdit.text() or 0)

            # Добавляем блюдо в базу данных
            dish_id = self.db.add_dish(name, description, auto_calculate, calories,
                                       proteins, fats, carbs)

            # Проверка, добавилось ли блюдо
            if dish_id:
                # Получаем ID добавленного блюда
                conn = sqlite3.connect('db/smart_menu.db')
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM dishes WHERE name = ?', (name,))
                dish_id = cursor.fetchone()[0]
                conn.close()

                # Добавляем ингредиенты
                self.db.add_dish_ingredients_from_ui(self.win, dish_id, ingredients)

                QtWidgets.QMessageBox.information(self.win, "Успех",
                                                  "Блюдо успешно добавлено")

                # self.win.close()

            # Очищаем форму
            self.clear_form()

            # Обновляем таблицу в главном окне
            self.parent.refresh_dishes_table()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.win, "Ошибка",
                                           f"Ошибка при добавлении блюда: {str(e)}")

    def clear_form(self):
        """Очищает все поля формы"""
        self.win.nameOfDishLineEdit.clear()
        self.win.infoDishPlainTextEdit.clear()
        self.win.kaloriesLineEdit.clear()
        self.win.proteinsLineEdit.clear()
        self.win.fatsLineEdit.clear()
        self.win.carbohLineEdit.clear()

        # Очищаем все ComboBox и SpinBox ингредиентов
        for i in range(self.win.verticalLayout_2.count()):
            item = self.win.verticalLayout_2.itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                combo = item.itemAt(0).widget()
                spin = item.itemAt(1).widget()
                if isinstance(combo, QtWidgets.QComboBox):
                    combo.setCurrentIndex(0)
                if isinstance(spin, QtWidgets.QSpinBox):
                    spin.setValue(0)

        # Сбрасываем чекбокс автоматического расчета
        self.win.calculateAutoNutritValuecheckBox.setChecked(False)

