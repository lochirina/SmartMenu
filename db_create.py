import sqlite3
from datetime import datetime


def create_database():
    # Подключение к базе данных (создается, если не существует)
    conn = sqlite3.connect('db/smart_menu.db')
    cursor = conn.cursor()

    # Создание таблицы "Набор ед. измерения"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS measurement_units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    # Создание таблицы "Продукты"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        proteins INTEGER NOT NULL,
        fats INTEGER NOT NULL,
        carbohydrates INTEGER NOT NULL,
        calories INTEGER NOT NULL,
        measurement_unit_id INTEGER,
        shelf_life_days INTEGER,
        quantity INTEGER DEFAULT 0,
        purchase_date DATE,
        FOREIGN KEY (measurement_unit_id) REFERENCES measurement_units (id)
    )
    ''')

    # Создание таблицы "Блюда"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT DEFAULT 0,
        description TEXT,
        auto_calorie_calc BOOLEAN DEFAULT TRUE,
        calories INTEGER,
        proteins INTEGER,
        fats INTEGER,
        carbohydrates INTEGER
    )
    ''')

    # Создание таблицы "Ингредиенты блюд"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dish_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (dish_id) REFERENCES dishes (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    # Создание таблицы "Меню"

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE DEFAULT CURRENT_DATE,
        breakfast_dish_id INTEGER,
        lunch_dish_id INTEGER,
        dinner_dish_id INTEGER,
        total_calories INTEGER,
        total_proteins INTEGER,
        total_fats INTEGER,
        total_carbohydrates INTEGER,
        FOREIGN KEY (breakfast_dish_id) REFERENCES dishes (id),
        FOREIGN KEY (lunch_dish_id) REFERENCES dishes (id),
        FOREIGN KEY (dinner_dish_id) REFERENCES dishes (id)
    )
    ''')

    # Создание индексов для оптимизации
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_dishes_name ON dishes(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_menu_date ON menu(date)')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


def insert_default_measurement_units():
    conn = sqlite3.connect('db/smart_menu.db')
    cursor = conn.cursor()

    # Список стандартных единиц измерения
    default_units = ["шт.", "ед.", "гр.", "мл."]

    # Добавление каждой единицы измерения
    for unit in default_units:
        cursor.execute('INSERT OR IGNORE INTO measurement_units (name) VALUES (?)', (unit,))
        print("Дабавлен", unit)

    conn.commit()
    conn.close()

def insert_default_product():
    conn = sqlite3.connect('db/smart_menu.db')
    cursor = conn.cursor()

    # Список стандартных единиц измерения
    default_none_prod = "---"

    # Добавление каждой единицы измерения
    cursor.execute('INSERT OR IGNORE INTO products (name, proteins, fats, carbohydrates, calories, measurement_unit_id) VALUES (?, ?, ?, ?, ?, ?)', (default_none_prod, 0, 0, 0, 0, 0))
    print("Добавлен")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    insert_default_measurement_units()
    # insert_default_product()