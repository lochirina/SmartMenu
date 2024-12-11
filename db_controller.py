import sqlite3
from datetime import datetime

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

    def add_dish_ingredients(self, dish_id, ingredients):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            for ingredient_name, amount in ingredients:
                # Получаем ID продукта
                cursor.execute('SELECT id FROM products WHERE name = ?',
                               (ingredient_name,))
                product_id = cursor.fetchone()[0]

                # Добавляем связь блюда и ингредиента
                cursor.execute('''
                    INSERT INTO dish_ingredients (dish_id, product_id, quantity)
                    VALUES (?, ?, ?)
                ''', (dish_id, product_id, amount))
        except Exception as e:
            print(f"Ошибка при добавлении ингредиента: {e}")
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

    def can_prepare_dish(self, dish_name):

        """Проверяет, достаточно ли ингредиентов для приготовления блюда"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Получаем необходимые ингредиенты и их количество для блюда
        cursor.execute("""
            SELECT p.name, di.quantity
            FROM dish_ingredients di
            JOIN products p ON di.product_id = p.id
            JOIN dishes d ON di.dish_id = d.id
            WHERE d.name = ?
        """, (dish_name,))

        # # Получаем необходимые ингредиенты и их количество для блюда
        # cursor.execute('''
        #     SELECT p.name, di.quantity, mu.name
        #     FROM dishes d
        #     JOIN dish_ingredients di ON d.id = di.dish_id
        #     JOIN products p ON di.product_id = p.id
        #     JOIN measurement_units mu ON p.measurement_unit_id = mu.id
        #     WHERE d.id = ?
        #     ORDER BY p.name
        # ''', (dish_name,))

        # dish_id = self.get_dish_id_by_name(dish_name)
        # cursor.execute('''
        #     SELECT di.product_id
        #     FROM dish_ingredients di
        #     WHERE di.dish_id = ?;
        # ''', (dish_id,))

        # results = cursor.fetchall()
        # print("all ingred", results)
        # conn.close()

        # Разделяем результаты на два списка
        # ingredient_names = [row[0] for row in results]
        # ingredient_quantities = [row[1] for row in results]
        # print("all ingred", ingredient_names)
        # print("all ingred", ingredient_quantities)

        required_ingredients = cursor.fetchall()
        print("Блюдо", dish_name, "ингредиенты:", required_ingredients)

        # Проверяем наличие каждого ингредиента
        for ingredient_name, required_amount in required_ingredients:
            cursor.execute("SELECT quantity FROM products WHERE name = ?", (ingredient_name,))
            available_amount = cursor.fetchone()[0]

            if available_amount < required_amount:
                return False

        return True

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

