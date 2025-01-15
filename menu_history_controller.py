from PyQt5.QtWidgets import QLabel, QFrame
from datetime import datetime
import sqlite3

class MenuHistory:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db_path = "db/smart_menu.db"  # Путь к базе данных

    def load_menu_history(self):
        # Подключение к базе данных
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Проверка, создано ли меню на сегодняшний день
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT * FROM menu WHERE date = ?", (today,))
            today_menu = cursor.fetchone()

            if today_menu:
                # Если меню создано сегодня, выбираем три предыдущих
                cursor.execute("""
                    SELECT * FROM menu
                    WHERE date < ?
                    ORDER BY date DESC
                    LIMIT 3
                """, (today,))
            else:
                # Если меню на сегодня нет, выбираем три последних
                cursor.execute("""
                    SELECT * FROM menu
                    ORDER BY date DESC
                    LIMIT 3
                """)

            menus = cursor.fetchall()
            self.populate_history_cards(menus)

            conn.close()
        except Exception as e:
            print(f"Ошибка при загрузке истории меню: {e}")

    def populate_history_cards(self, menus):
        # Словарь для отображения данных в соответствующие QFrame
        frames = {
            1: {
                "frame": self.main_window.win.history_card_frame_1,
                "date_label": "dateLabel_1",
                "breakfast_label": "breakfastLabel_1",
                "lunch_label": "lunchLabel_1",
                "diner_label": "dinerLabel_1",
                "kalories_label": "kaloriesLabel_1",
                "foodvalue_label": "foodvalueLabel_1",
            },
            2: {
                "frame": self.main_window.win.history_card_frame_2,
                "date_label": "dateLabel_2",
                "breakfast_label": "breakfastLabel_2",
                "lunch_label": "lunchLabel_2",
                "diner_label": "dinerLabel_2",
                "kalories_label": "kaloriesLabel_2",
                "foodvalue_label": "foodvalueLabel_2",
            },
            3: {
                "frame": self.main_window.win.history_card_frame_3,
                "date_label": "dateLabel_3",
                "breakfast_label": "breakfastLabel_3",
                "lunch_label": "lunchLabel_3",
                "diner_label": "dinerLabel_3",
                "kalories_label": "kaloriesLabel_3",
                "foodvalue_label": "foodvalueLabel_3",
            },
        }

        # Итерация по меню и фреймам
        for i, menu in enumerate(menus[:3], start=1):
            frame_info = frames.get(i)
            if not frame_info:
                continue

            # Извлечение данных из меню
            menu_date = menu[1]
            breakfast_id = menu[2]
            lunch_id = menu[3]
            diner_id = menu[4]
            total_calories = menu[5]
            total_proteins = menu[6]
            total_fats = menu[7]
            total_carbohydrates = menu[8]

            # Получение названий блюд
            breakfast_name = self.get_dish_name(breakfast_id)
            lunch_name = self.get_dish_name(lunch_id)
            diner_name = self.get_dish_name(diner_id)

            # Форматирование даты
            formatted_date = self.format_date(menu_date)

            # Заполнение данных в соответствующие элементы
            getattr(self.main_window.win, frame_info["date_label"]).setText(formatted_date)
            getattr(self.main_window.win, frame_info["breakfast_label"]).setText(breakfast_name)
            getattr(self.main_window.win, frame_info["lunch_label"]).setText(lunch_name)
            getattr(self.main_window.win, frame_info["diner_label"]).setText(diner_name)
            getattr(self.main_window.win, frame_info["kalories_label"]).setText(f"{total_calories} Ккал")
            getattr(self.main_window.win, frame_info["foodvalue_label"]).setText(
                f"Б: {total_proteins} Ж: {total_fats} У: {total_carbohydrates}"
            )

    def get_dish_name(self, dish_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM dishes WHERE id = ?", (dish_id,))
            dish = cursor.fetchone()
            conn.close()
            return dish[0] if dish else "Неизвестно"
        except Exception as e:
            print(f"Ошибка при получении названия блюда: {e}")
            return "Ошибка"

    def format_date(self, date_str):

        print(f"Значение даты перед форматированием: {date_str}")

        try:
            # Преобразуем дату в строку, если это число
            if isinstance(date_str, int):
                date_str = str(date_str)

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            day_of_week = date_obj.strftime("%a").capitalize()[:2]
            formatted_date = date_obj.strftime("%d.%m.%Y") + f", {day_of_week}"
            return formatted_date
        except Exception as e:
            print(f"Ошибка при форматировании даты: {e}")
            return "Неизвестно"