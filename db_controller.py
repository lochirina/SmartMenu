import sqlite3
from datetime import datetime

from PyQt5 import QtWidgets, QtCore


class DatabaseController:
    def __init__(self):
        self.db_name = 'db/smart_menu.db'

    def add_product(self, name, unit, carbohydrates, fats, calories, proteins, shelf_life):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Получаем ID единицы измерения
            cursor.execute('SELECT id FROM measurement_units WHERE name = ?', (unit,))
            unit_id = cursor.fetchone()[0]

            # Добавляем продукт
            cursor.execute('''
                INSERT INTO products (name, measurement_unit_id, carbohydrates, fats, 
                                    calories, proteins, shelf_life_days)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, unit_id, carbohydrates, fats, calories, proteins, shelf_life))

            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении продукта: {e}")
            return False
        finally:
            conn.close()

    def update_product(self, product_id, name, unit, carbohydrates, fats, calories, proteins, shelf_life):
        try:
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products
                SET name = ?, measurement_unit_id = ?, carbohydrates = ?, fats = ?, calories = ?, proteins = ?, shelf_life_days = ?
                WHERE id = ?
            ''', (name, unit, carbohydrates, fats, calories, proteins, shelf_life, product_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении продукта: {e}")
            return False

    def add_dish(self, name, description, auto_calorie_calc, calories, proteins, fats, carbs):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Добавляем блюдо
            cursor.execute('''
                INSERT INTO dishes (name, description, auto_calorie_calc, calories, proteins, 
                                    fats, carbohydrates)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, description,auto_calorie_calc, calories, proteins, fats, carbs))

            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении блюда: {e}")
            return False
        finally:
            conn.close()

    def add_dish_ingredients_from_ui(self, win, dish_id, ingredients):
        """Добавляет ингредиенты блюда из UI элементов в базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Получаем все ComboBox с ингредиентами
            ingredient_combos = win.findChildren(QtWidgets.QComboBox,
                                                      QtCore.QRegExp("ingredientComboBox_\d+"))

            # Получаем все SpinBox с количеством
            count_spinboxes = win.findChildren(QtWidgets.QSpinBox,
                                                    QtCore.QRegExp("countIngredientsSpinBox_\d+"))


            # Создаем список пар (ингредиент, количество)
            for ingredient, quantity in ingredients:
                print("Создаем список пар (ингредиент, количество)", ingredient, quantity)

                # Пропускаем пустые значения и "---"
                if ingredient != "---" and quantity > 0:
                    # Получаем ID продукта
                    cursor.execute('SELECT id FROM products WHERE name = ?',
                                   (ingredient,))
                    product_id = cursor.fetchone()[0]

                    # Добавляем связь между блюдом и ингредиентом
                    cursor.execute('''
                        INSERT INTO dish_ingredients (dish_id, product_id, quantity)
                        VALUES (?, ?, ?)
                    ''', (dish_id, product_id, quantity))
                    print("Добавляем связь между блюдом и ингредиентом", dish_id, product_id, quantity)

            conn.commit()
            return True

        except Exception as e:
            print(f"Ошибка при добавлении ингредиентов: {e}")
            return False
        finally:
            conn.close()

    def calculate_nutrition(self, ingredients):
        """
        Расчет пищевой ценности на основе ингредиентов
        Args:
            ingredients (list): Список кортежей (название_продукта, количество)
        Returns:
            tuple: (калории, белки, жиры, углеводы)
        """
        calories = proteins = fats = carbs = 0

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            for ingredient_name, amount in ingredients:
                cursor.execute('''
                    SELECT calories, proteins, fats, carbohydrates
                    FROM products
                    WHERE name = ?
                ''', (ingredient_name,))

                product = cursor.fetchone()
                if product:
                    # Пересчитываем пищевую ценность
                    calories += (product[0] * amount)
                    proteins += (product[1] * amount)
                    fats += (product[2] * amount)
                    carbs += (product[3] * amount)

        return calories, proteins, fats, carbs
    def update_product_quantity(self, product_id, quantity):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Обновляет количество продукта в базе данных
        try:
            cursor.execute('''
                UPDATE products 
                SET quantity = ? 
                WHERE id = ?
            ''', (quantity, product_id))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при обновлении количества продукта: {e}")
            raise e

    def get_available_dishes(self):
        """Получает список доступных для приготовления блюд"""
        available_dishes = []

        # Получаем все блюда из БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM dishes")
        all_dishes = cursor.fetchall()

        for dish in all_dishes:
            dish_name = dish[0]
            print(dish_name)
            # Проверяем, хватает ли ингредиентов для приготовления
            if self.can_prepare_dish(dish_name):
                available_dishes.append(dish_name)

        return available_dishes

    def get_dish_id_by_name(self, dish_name):
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id 
            FROM dishes 
            WHERE name = ?
        ''', (dish_name,))

        result = cursor.fetchone()
        print("айди =", result, result[0])
        conn.close()
        return result[0]

    def get_dish_name_by_id(self, dish_id):
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM dishes WHERE id = ?', (dish_id,))
        dish_name = cursor.fetchone()
        conn.close()
        return dish_name[0] if dish_name else None

    def add_dish_to_menu(self, meal, dish_id):
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO menu (meal, dish_id) VALUES (?, ?)
        ''', (meal, dish_id))
        conn.commit()
        conn.close()

    def get_available_dishes_with_ids(self):
        conn = sqlite3.connect('db/smart_menu.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM dishes')
        dishes = cursor.fetchall()  # [(id, name), ...]
        conn.close()
        return dishes
    def get_preparable_dishes(self):
        """
        Возвращает список блюд, которые можно приготовить из имеющихся ингредиентов.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # SQL-запрос для получения блюд, которые можно приготовить
            query = """
            SELECT DISTINCT d.id, d.name
            FROM dishes d
            JOIN dish_ingredients di ON d.id = di.dish_id
            JOIN products p ON di.product_id = p.id
            WHERE p.quantity >= di.quantity
            GROUP BY d.id
            HAVING COUNT(di.id) = (
                SELECT COUNT(*)
                FROM dish_ingredients
                WHERE dish_id = d.id
            )
            """
            cursor.execute(query)
            # preparable_dishes = [row[1] for row in cursor.fetchall()]
            preparable_dishes = cursor.fetchall()  # [(id, name), ...]
            return preparable_dishes
        except sqlite3.Error as e:
            print(f"Ошибка при получении доступных блюд: {e}")
            return []
        finally:
            conn.close()

    def update_ingredients_after_cooking(self, dish_name):
        """Обновляет количество ингредиентов после приготовления блюда"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Получаем список ингредиентов и их количество для блюда
        cursor.execute("""
            SELECT p.id, di.quantity
            FROM dish_ingredients di
            JOIN products p ON di.product_id = p.id
            JOIN dishes d ON di.dish_id = d.id
            WHERE d.name = ?
        """, (dish_name,))

        ingredients = cursor.fetchall()

        # Обновляем количество каждого ингредиента
        for product_id, amount in ingredients:
            cursor.execute("""
                UPDATE products 
                SET quantity = quantity - ?
                WHERE id = ?
            """, (amount, product_id))

        conn.commit()

    def delete_dish(self, dish_id):
        """Удаляет блюдо и его ингредиенты из базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Начинаем транзакцию
            conn.execute('BEGIN')

            # Удаляем записи из таблицы dish_ingredients
            cursor.execute('''
                DELETE FROM dish_ingredients 
                WHERE dish_id = ?
            ''', (dish_id,))

            # Удаляем само блюдо
            cursor.execute('''
                DELETE FROM dishes 
                WHERE id = ?
            ''', (dish_id,))

            # Фиксируем изменения
            conn.commit()
            return True

        except Exception as e:
            # Откатываем изменения в случае ошибки
            conn.rollback()
            print(f"Ошибка при удалении блюда: {e}")
            return False

        finally:
            conn.close()

    def delete_product_by_name(self, product_name):
        """Удаляет продукт из таблицы products по имени"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM products
                WHERE name = ?
            ''', (product_name,))

            conn.commit()
            print(f"Продукт \"{product_name}\" успешно удален из базы данных")
        except Exception as e:
            print(f"Ошибка при удалении продукта \"{product_name}\": {e}")
            raise e
        finally:
            conn.close()

    def update_product_quantity_by_name(self, product_name, quantity):
        """Обновляет количество продукта в базе данных по имени"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Обновляем количество продукта по имени
            cursor.execute('''
                    UPDATE products 
                    SET quantity = ? 
                    WHERE name = ?
                ''', (quantity, product_name))
            conn.commit()
            print(f"Количество продукта \"{product_name}\" обновлено до {quantity}")
        except Exception as e:
            print(f"Ошибка при обновлении количества продукта: {e}")
            raise e
        finally:
            conn.close()

    def get_dish_nutrients(self, dish_id):
        """Возвращает данные о калориях, белках, жирах и углеводах для указанного блюда"""
        try:
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT calories, proteins, fats, carbohydrates 
                FROM dishes WHERE id = ?
            ''', (dish_id,))
            nutrients = cursor.fetchone()
            conn.close()

            if nutrients:
                return nutrients  # (calories, proteins, fats, carbohydrates)
            else:
                raise ValueError(f"Блюдо с ID {dish_id} не найдено.")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных при получении данных блюда: {e}")
            raise

    def add_menu_to_db(self, breakfast_dish_id, lunch_dish_id, dinner_dish_id,
                       total_calories, total_proteins, total_fats, total_carbohydrates):
        """Добавляет меню в таблицу menu"""
        try:
            conn = sqlite3.connect('db/smart_menu.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO menu (breakfast_dish_id, lunch_dish_id, dinner_dish_id,
                                  total_calories, total_proteins, total_fats, total_carbohydrates)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (breakfast_dish_id, lunch_dish_id, dinner_dish_id,
                  total_calories, total_proteins, total_fats, total_carbohydrates))
            conn.commit()
            conn.close()
            print("Меню успешно добавлено в базу данных.")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных при добавлении меню: {e}")
            raise

    def update_ingredients_after_cooking_by_dish_id(self, dish_id):
        """
        Обновляет количество ингредиентов после приготовления блюда по dish_id.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Получаем список ингредиентов и их количество для блюда
            cursor.execute("""
                SELECT p.id, di.quantity
                FROM dish_ingredients di
                JOIN products p ON di.product_id = p.id
                WHERE di.dish_id = ?
            """, (dish_id,))

            ingredients = cursor.fetchall()

            # Обновляем количество каждого ингредиента
            for product_id, amount in ingredients:
                cursor.execute("""
                    UPDATE products 
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (amount, product_id))
                print(f"Ингредиент {product_id}: вычтено {amount}.")

            conn.commit()
            print("Количество ингредиентов обновлено успешно.")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных при обновлении ингредиентов: {e}")
            raise
        finally:
            conn.close()

    def restore_ingredients_by_dish_id(self, dish_id):
        """
        Восстанавливает ингредиенты, использованные для приготовления блюда по dish_id.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Получаем список ингредиентов и их количество для блюда
            cursor.execute("""
                SELECT p.id, di.quantity
                FROM dish_ingredients di
                JOIN products p ON di.product_id = p.id
                WHERE di.dish_id = ?
            """, (dish_id,))

            ingredients = cursor.fetchall()

            # Восстанавливаем количество каждого ингредиента
            for product_id, amount in ingredients:
                cursor.execute("""
                    UPDATE products 
                    SET quantity = quantity + ?
                    WHERE id = ?
                """, (amount, product_id))
                print(f"Ингредиент {product_id}: восстановлено {amount}.")

            conn.commit()
            print("Ингредиенты восстановлены успешно.")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных при восстановлении ингредиентов: {e}")
            raise
        finally:
            conn.close()