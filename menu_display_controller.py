import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QMessageBox, QFileDialog
from datetime import datetime


class MenuDisplayController:
    def __init__(self, main_window, db_name):
        """
        Контроллер для отображения информации о сегодняшнем меню.

        - main_window: Ссылка на главное окно (объект MainWindow.win).
        - db_name: Имя файла базы данных SQLite.
        """
        self.main_window = main_window
        self.db_name = db_name

    def update_menu_display(self):
        """
        Обновляет отображение меню на сегодняшнюю дату.
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Извлекаем информацию о меню на текущую дату
            cursor.execute("""
                SELECT 
                    m.breakfast_dish_id, m.lunch_dish_id, m.dinner_dish_id,
                    m.total_calories, m.total_proteins, m.total_fats, m.total_carbohydrates,
                    d1.name AS breakfast_name, d1.calories AS breakfast_calories,
                    d1.proteins AS breakfast_proteins, d1.fats AS breakfast_fats, d1.carbohydrates AS breakfast_carbohydrates,
                    d2.name AS lunch_name, d2.calories AS lunch_calories,
                    d2.proteins AS lunch_proteins, d2.fats AS lunch_fats, d2.carbohydrates AS lunch_carbohydrates,
                    d3.name AS diner_name, d3.calories AS diner_calories,
                    d3.proteins AS diner_proteins, d3.fats AS diner_fats, d3.carbohydrates AS diner_carbohydrates
                FROM menu m
                LEFT JOIN dishes d1 ON m.breakfast_dish_id = d1.id
                LEFT JOIN dishes d2 ON m.lunch_dish_id = d2.id
                LEFT JOIN dishes d3 ON m.dinner_dish_id = d3.id
                WHERE m.date = ?
            """, (today,))
            menu_data = cursor.fetchone()
            conn.close()

            if not menu_data:
                # Если меню на сегодня отсутствует
                print("Меню на сегодняшнюю дату отсутствует.")
                self.main_window.infoMenuLabel.setText("На сегодня у вас не составлено меню. \nДля составления меню нажмите кнопку ниже")
                return

            self.main_window.infoMenuLabel.setText("Вот ваше меню на сегодня!\nПриятного аппетита!")

            # Распаковываем данные из запроса
            (breakfast_id, lunch_id, diner_id,
             total_calories, total_proteins, total_fats, total_carbohydrates,
             breakfast_name, breakfast_calories, breakfast_proteins, breakfast_fats, breakfast_carbohydrates,
             lunch_name, lunch_calories, lunch_proteins, lunch_fats, lunch_carbohydrates,
             diner_name, diner_calories, diner_proteins, diner_fats, diner_carbohydrates) = menu_data

            # Обновляем виджеты для завтрака
            self._update_label("menuTableLabel_dish_breakfast", breakfast_name)
            self._update_label("menuTableLabel_kalories_breakfast", breakfast_calories)
            self._update_label("menuTableLabel_proteins_breakfast", breakfast_proteins)
            self._update_label("menuTableLabel_fats_breakfast", breakfast_fats)
            self._update_label("menuTableLabel_carboh_breakfast", breakfast_carbohydrates)

            # Обновляем виджеты для обеда
            self._update_label("menuTableLabel_dish_lunch", lunch_name)
            self._update_label("menuTableLabel_kalories_lunch", lunch_calories)
            self._update_label("menuTableLabel_proteins_lunch", lunch_proteins)
            self._update_label("menuTableLabel_fats_lunch", lunch_fats)
            self._update_label("menuTableLabel_carboh_lunch", lunch_carbohydrates)

            # Обновляем виджеты для ужина
            self._update_label("menuTableLabel_dish_diner", diner_name)
            self._update_label("menuTableLabel_kalories_diner", diner_calories)
            self._update_label("menuTableLabel_proteins_diner", diner_proteins)
            self._update_label("menuTableLabel_fats_diner", diner_fats)
            self._update_label("menuTableLabel_carboh_diner", diner_carbohydrates)

            # Обновляем суммарные показатели за день
            self._update_label("menuTableLabel_AllKPFC_kalories", total_calories)
            self._update_label("menuTableLabel_AllKPFC_proteins", total_proteins)
            self._update_label("menuTableLabel_AllKPFC_fats", total_fats)
            self._update_label("menuTableLabel_AllKPFC_carbons", total_carbohydrates)

            print("Информация о меню успешно обновлена.")

        except Exception as e:
            QMessageBox.critical(self.main_window, "Ошибка", f"Ошибка при обновлении меню: {e}")

    def _update_label(self, label_name, value):
        """
        Обновляет текст QLabel.

        :param label_name: Имя QLabel в интерфейсе.
        :param value: Значение, которое нужно установить.
        """

        try:
            label = self.main_window.findChild(QLabel, label_name)
            if label:
                label.setText(str(value))
            else:
                print(f"Label {label_name} не найден.")
        except Exception as e:
            print(f"Ошибка при обновлении {label_name}: {e}")

    def export_today_menu_to_txt(self, parent):

        """
        Экспортирует меню на текущую дату в текстовый файл.
        """
        try:
            # Получение текущей даты
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Извлекаем информацию о меню на текущую дату
            cursor.execute("""
                SELECT 
                    m.breakfast_dish_id, m.lunch_dish_id, m.dinner_dish_id,
                    m.total_calories, m.total_proteins, m.total_fats, m.total_carbohydrates,
                    d1.name AS breakfast_name, d1.calories AS breakfast_calories,
                    d1.proteins AS breakfast_proteins, d1.fats AS breakfast_fats, d1.carbohydrates AS breakfast_carbohydrates,
                    d2.name AS lunch_name, d2.calories AS lunch_calories,
                    d2.proteins AS lunch_proteins, d2.fats AS lunch_fats, d2.carbohydrates AS lunch_carbohydrates,
                    d3.name AS dinner_name, d3.calories AS dinner_calories,
                    d3.proteins AS dinner_proteins, d3.fats AS dinner_fats, d3.carbohydrates AS dinner_carbohydrates
                FROM menu m
                LEFT JOIN dishes d1 ON m.breakfast_dish_id = d1.id
                LEFT JOIN dishes d2 ON m.lunch_dish_id = d2.id
                LEFT JOIN dishes d3 ON m.dinner_dish_id = d3.id
                WHERE m.date = ?
            """, (today,))

            # Извлекаем данные
            menu_data = cursor.fetchone()

            if not menu_data:
                QtWidgets.QMessageBox.warning(None, "Нет данных", "На сегодня меню отсутствует.")
                return

            (breakfast_id, lunch_id, dinner_id,
             total_calories, total_proteins, total_fats, total_carbohydrates,
             breakfast_name, breakfast_calories, breakfast_proteins, breakfast_fats, breakfast_carbohydrates,
             lunch_name, lunch_calories, lunch_proteins, lunch_fats, lunch_carbohydrates,
             dinner_name, dinner_calories, dinner_proteins, dinner_fats, dinner_carbohydrates) = menu_data


            # Формируем текстовый контент с выравниванием колонок
            content = (
                "| Прием пищи   | Блюдо            | Ккал  | Белки | Жиры  | Углеводы |\n"
                "|--------------|------------------|-------|-------|-------|----------|\n"
                f"| Завтрак      | {breakfast_name or '---':<16} | {str(breakfast_calories or '---'):<5} | {str(breakfast_proteins or '---'):<5} | {str(breakfast_fats or '---'):<5} | {str(breakfast_carbohydrates or '---'):<8} |\n"
                f"| Обед         | {lunch_name or '---':<16} | {str(lunch_calories or '---'):<5} | {str(lunch_proteins or '---'):<5} | {str(lunch_fats or '---'):<5} | {str(lunch_carbohydrates or '---'):<8} |\n"
                f"| Ужин         | {dinner_name or '---':<16} | {str(dinner_calories or '---'):<5} | {str(dinner_proteins or '---'):<5} | {str(dinner_fats or '---'):<5} | {str(dinner_carbohydrates or '---'):<8} |\n"
                "|--------------|------------------|-------|-------|-------|----------|\n"
                f"| Итого        |                  | {str(total_calories or '---'):<5} | {str(total_proteins or '---'):<5} | {str(total_fats or '---'):<5} | {str(total_carbohydrates or '---'):<8} |\n"
            )

            # Открываем диалог для выбора пути сохранения файла
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Сохранить меню как TXT",
                f"Меню_{today}.txt",
                "Text Files (*.txt)",
                options=options
            )

            if not file_path:
                return  # Пользователь закрыл диалог или отменил выбор

            # Сохраняем данные в выбранный файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            QtWidgets.QMessageBox.information(parent, "Успех", f"Меню успешно экспортировано в {file_path}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(parent, "Ошибка", f"Ошибка при экспорте меню: {str(e)}")
