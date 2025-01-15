import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt

from db_controller import DatabaseController


class AddMenuWindow:
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi("static/ui/add_menu.ui")
        self.db_controller = DatabaseController()

        # Список кнопок для блюд
        self.dish_buttons = [
            self.win.item1pushButton,
            self.win.item2pushButton,
            self.win.item3pushButton,
            self.win.item4pushButton,
            self.win.item5pushButton,
            self.win.item6pushButton
        ]

        # Подключаем обработчики нажатий к кнопкам
        for button in self.dish_buttons:
            button.clicked.connect(self.dish_button_clicked)
            button.setEnabled(False)  # Изначально все кнопки неактивны
            print("Кнопка", button)

        self.current_meal = "завтрак"
        self.selected_dishes = {}  # Словарь для хранения выбранных блюд {meal: dish_id}
        self.dish_mapping = {}  # Словарь для хранения отображения кнопок на ID блюд

        self.win.show()
        print(f"Что хотите на {self.current_meal}?")
        self.update_available_dishes()

    def get_available_dishes(self):
        """Получает список доступных блюд из БД на основе имеющихся ингредиентов"""
        return self.db_controller.get_available_dishes_with_ids()

    def update_available_dishes(self):
        try:
            """Обновляет кнопки доступными блюдами"""
            available_dishes = self.get_available_dishes()  # [(id, name), ...]
            preparable_dishes = self.db_controller.get_preparable_dishes() # [(id, name), ...]

            print("Available dishes:", available_dishes)
            print("Preparable dishes:", preparable_dishes)
            print("Number of buttons:", len(self.dish_buttons))

            # Если нет доступных блюд, восстановить ингредиенты и вывести предупреждение
            if not preparable_dishes:
                self.restore_ingredients()
                QtWidgets.QMessageBox.warning(
                    self.win,
                    "Недостаточно ингредиентов",
                    "Не хватает продуктов в наличии. Обновите запасы."
                )
                return

            # Очищаем словарь dish_mapping
            self.dish_mapping.clear()

            # Сначала делаем все кнопки неактивными и очищаем текст
            self.dish_mapping.clear()
            for button in self.dish_buttons:
                button.setText("")
                button.setEnabled(False)

            # Назначение имен блюд кнопкам
            for button, (dish_id, dish_name) in zip(self.dish_buttons, preparable_dishes):
                button.setText(dish_name)
                button.setEnabled(True)
                self.dish_mapping[button] = dish_id  # Связываем кнопку с ID блюда

            # Скрытие оставшихся кнопок, если блюд меньше 6
            for button in self.dish_buttons[len(preparable_dishes):]:
                button.setText("---")
                button.setEnabled(False)

            print("Dish mapping updated:", self.dish_mapping)
        except Exception as e:
            print(f"Error in update_available_dishes: {e}")
    def restore_ingredients(self):
        """
        Восстанавливает ингредиенты для уже выбранных блюд.
        """
        try:
            for meal, dish_id in self.selected_dishes.items():
                self.db_controller.restore_ingredients_by_dish_id(dish_id)
            print("Ингредиенты для выбранных блюд восстановлены.")
        except Exception as e:
            print(f"Ошибка при восстановлении ингредиентов: {e}")

    def dish_button_clicked(self):
        """Обработчик нажатия на кнопку с блюдом"""
        try:
            button = self.win.sender()
            if button not in self.dish_mapping:
                print("Ошибка: кнопка не связана с блюдом.")
                return

            # Получаем ID и название блюда
            selected_dish_id = self.dish_mapping[button]
            print("self.dish_mapping", self.dish_mapping)
            selected_dish_name = button.text()
            print(f"Вы выбрали блюдо: {selected_dish_name} (ID: {selected_dish_id})")

            # Сохраняем выбор блюда для текущего приема пищи
            self.selected_dishes[self.current_meal] = selected_dish_id

            # Сохраняем выбор
            # self.selected_dishes[self.current_meal] = selected_dish_id
            # Записываем выбранное блюдо в базу данных
            # self.db_controller.add_dish_to_menu(self.current_meal, selected_dish_id)
            # Обновляем количество ингредиентов в БД
            # self.db_controller.update_ingredients_after_cooking(selected_dish)

            # Обновляем количество ингредиентов в БД
            self.db_controller.update_ingredients_after_cooking_by_dish_id(selected_dish_id)
            # Обновляем таблицу в главном окне
            self.parent.refresh_storage_table()

            # Обновляем текстовые поля интерфейса
            if self.current_meal == "завтрак":
                print(f"Что хотите на {self.current_meal}?")
                self.current_meal = "обед"
                self.win.chooseMenuHeaderLabel.setText(f"Что хотите на {self.current_meal}?")
                self.win.breakfastLabel.setText(f"{selected_dish_name}")
                self.update_available_dishes()
            elif self.current_meal == "обед":
                self.current_meal = "ужин"
                self.win.chooseMenuHeaderLabel.setText(f"Что хотите на {self.current_meal}?")
                self.win.lunchLabel.setText(f"{selected_dish_name}")
                print(f"Что хотите на {self.current_meal}?")
                self.update_available_dishes()
            else:
                self.win.dinerLabel.setText(f"{selected_dish_name}")

                # Финальный этап: сохранение меню в базу данных
                self.save_menu_to_db()

                self.parent.menu_display_controller.update_menu_display()  # Обновляем информацию о меню
                self.parent.menu_history.load_menu_history()  # Обновляем историю меню

                # Выводим итоговое меню
                print("\nВаше меню на день:")
                for meal, dish_id in self.selected_dishes.items():
                    print(f"{meal.capitalize()}: {self.db_controller.get_dish_name_by_id(dish_id)}")
                self.win.close()

        except Exception as e:
            print(f"Ошибка при обработке нажатия на кнопку: {e}")

    def save_menu_to_db(self):
        """Сохраняет меню в таблицу menu"""
        try:
            # Получаем ID блюд для каждого приема пищи
            breakfast_dish_id = self.selected_dishes.get("завтрак")
            lunch_dish_id = self.selected_dishes.get("обед")
            dinner_dish_id = self.selected_dishes.get("ужин")

            # Получаем информацию о калориях, белках, жирах и углеводах для каждого блюда
            breakfast_data = self.db_controller.get_dish_nutrients(breakfast_dish_id)
            lunch_data = self.db_controller.get_dish_nutrients(lunch_dish_id)
            dinner_data = self.db_controller.get_dish_nutrients(dinner_dish_id)

            # Суммируем значения для всего меню
            total_calories = sum([breakfast_data[0], lunch_data[0], dinner_data[0]])
            total_proteins = sum([breakfast_data[1], lunch_data[1], dinner_data[1]])
            total_fats = sum([breakfast_data[2], lunch_data[2], dinner_data[2]])
            total_carbohydrates = sum([breakfast_data[3], lunch_data[3], dinner_data[3]])

            # Сохраняем данные в таблицу menu
            self.db_controller.add_menu_to_db(
                breakfast_dish_id, lunch_dish_id, dinner_dish_id,
                total_calories, total_proteins, total_fats, total_carbohydrates
            )

            print("Меню успешно сохранено в базу данных.")

        except Exception as e:
            print(f"Ошибка при сохранении меню в базу данных: {e}")


