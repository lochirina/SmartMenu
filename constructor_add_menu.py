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
        self.selected_dishes = {}

        self.win.show()
        print(f"Что хотите на {self.current_meal}?")
        self.update_available_dishes()

    def get_available_dishes(self):
        """Получает список доступных блюд из БД на основе имеющихся ингредиентов"""
        return self.db_controller.get_available_dishes()

    def update_available_dishes(self):
        try:
            """Обновляет кнопки доступными блюдами"""
            available_dishes = self.get_available_dishes()

            print("Available dishes:", available_dishes)
            print("Number of buttons:", len(self.dish_buttons))

            # Сначала делаем все кнопки неактивными и очищаем текст
            for button in self.dish_buttons:
                if button is None:
                    print(f"Warning: button is None")
                    continue
                button.setText("")
                button.setEnabled(False)
            # Заполняем доступные кнопки названиями блюд
            for i, dish in enumerate(available_dishes):
                if i < len(self.dish_buttons):
                    if self.dish_buttons[i] is not None:
                        self.dish_buttons[i].setText(dish)
                        self.dish_buttons[i].setEnabled(True)
        except Exception as e:
            print(f"Error in update_available_dishes: {e}")


    def dish_button_clicked(self):
        """Обработчик нажатия на кнопку с блюдом"""

        button = self.win.sender()

        selected_dish = button.text()

        # Сохраняем выбор
        self.selected_dishes[self.current_meal] = selected_dish

        # Обновляем количество ингредиентов в БД
        self.db_controller.update_ingredients_after_cooking(selected_dish)


        # Определяем следующий прием пищи
        if self.current_meal == "завтрак":
            self.current_meal = "обед"
            print(f"Что хотите на {self.current_meal}?")
            self.win.chooseMenuHeaderLabel.setText(f"Что хотите на {self.current_meal}?")
            self.win.breakfastLabel.setText(f"{selected_dish}")
            self.update_available_dishes()
        elif self.current_meal == "обед":
            self.win.lunchLabel.setText(f"{selected_dish}")
            self.current_meal = "ужин"
            print(f"Что хотите на {self.current_meal}?")
            self.win.chooseMenuHeaderLabel.setText(f"Что хотите на {self.current_meal}?")
            self.update_available_dishes()
        else:
            self.win.dinerLabel.setText(f"{selected_dish}")
            # Выводим итоговое меню
            print("\nВаше меню на день:")
            for meal, dish in self.selected_dishes.items():
                print(f"{meal.capitalize()}: {dish}")
            self.win.close()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = AddMenuWindow()
#     sys.exit(app.exec_())