import os
import time
import random
import psycopg2
from psycopg2 import OperationalError

# Конфигурация подключения к БД (значения из переменных окружения)
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Данные для генерации заказов
CATEGORIES = {
    'Электроника': {
        'products': ['Смартфон', 'Ноутбук', 'Наушники', 'Планшет', 'Умные часы', 'Телевизор', 'Колонка'],
        'price_range': (5000, 150000)
    },
    'Одежда': {
        'products': ['Футболка', 'Джинсы', 'Куртка', 'Платье', 'Кроссовки', 'Свитер', 'Шапка'],
        'price_range': (500, 15000)
    },
    'Продукты': {
        'products': ['Молоко', 'Хлеб', 'Сыр', 'Кофе', 'Чай', 'Шоколад', 'Фрукты'],
        'price_range': (50, 2000)
    },
    'Книги': {
        'products': ['Роман', 'Учебник', 'Детектив', 'Фантастика', 'Биография', 'Комикс', 'Словарь'],
        'price_range': (200, 3000)
    },
    'Спорт': {
        'products': ['Гантели', 'Коврик', 'Мяч', 'Велосипед', 'Скакалка', 'Ракетка', 'Бутсы'],
        'price_range': (300, 50000)
    }
}

# Города с весами (более крупные города чаще)
CITIES = [
    ('Москва', 25),
    ('Санкт-Петербург', 15),
    ('Новосибирск', 8),
    ('Екатеринбург', 7),
    ('Казань', 6),
    ('Нижний Новгород', 5),
    ('Челябинск', 5),
    ('Самара', 5),
    ('Ростов-на-Дону', 5),
    ('Уфа', 4),
    ('Красноярск', 4),
    ('Воронеж', 4),
    ('Пермь', 3),
    ('Волгоград', 3),
    ('Краснодар', 3)
]

PAYMENT_METHODS = ['Карта', 'Наличные', 'Онлайн-кошелёк']


def get_weighted_city():
    """Выбор города с учётом веса (населения)."""
    cities, weights = zip(*CITIES)
    return random.choices(cities, weights=weights)[0]


def generate_order():
    """Генерация одного заказа."""
    category = random.choice(list(CATEGORIES.keys()))
    cat_data = CATEGORIES[category]

    product = random.choice(cat_data['products'])
    price = round(random.uniform(*cat_data['price_range']), 2)
    quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
    city = get_weighted_city()
    customer_age = random.randint(18, 70)
    payment_method = random.choice(PAYMENT_METHODS)

    return {
        'product_name': product,
        'category': category,
        'price': price,
        'quantity': quantity,
        'city': city,
        'customer_age': customer_age,
        'payment_method': payment_method
    }


def wait_for_db(max_retries=30, delay=2):
    """Ожидание доступности БД."""
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("База данных доступна!")
            return True
        except OperationalError:
            print(f"Ожидание БД... попытка {i + 1}/{max_retries}")
            time.sleep(delay)
    return False


def insert_order(conn, order):
    """Вставка заказа в БД."""
    query = """
        INSERT INTO orders (product_name, category, price, quantity, city, customer_age, payment_method)
        VALUES (%(product_name)s, %(category)s, %(price)s, %(quantity)s, %(city)s, %(customer_age)s, %(payment_method)s)
    """
    with conn.cursor() as cur:
        cur.execute(query, order)
    conn.commit()


def main():
    """Основной цикл генерации данных."""
    print("Запуск генератора данных...")

    if not wait_for_db():
        print("Не удалось подключиться к БД!")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    print("Подключение к БД установлено. Начинаю генерацию заказов...")

    order_count = 0
    try:
        while True:
            order = generate_order()
            insert_order(conn, order)
            order_count += 1

            total = order['price'] * order['quantity']
            print(f"[{order_count}] {order['product_name']} ({order['category']}) - "
                  f"{order['quantity']} шт. x {order['price']}₽ = {total:.2f}₽ | "
                  f"{order['city']}")

            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\nОстановка. Всего сгенерировано заказов: {order_count}")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
