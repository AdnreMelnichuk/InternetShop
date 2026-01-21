# Мини-система сбора и анализа данных интернет-магазина

Система для генерации, хранения и анализа данных о заказах интернет-магазина.

## Компоненты

- **PostgreSQL** — хранит все заказы
- **Generator** — Python-скрипт, пишет в БД 1 заказ/сек
- **Redash** — дашборды и визуализации
- **Jupyter Notebook** — анализ данных

## Структура данных

Таблица `orders`:

| Поле | Тип | Описание |
|------|-----|----------|
| id | SERIAL | Уникальный идентификатор |
| created_at | TIMESTAMP | Время создания заказа |
| product_name | VARCHAR(100) | Название товара |
| category | VARCHAR(50) | Категория (Электроника, Одежда, Продукты, Книги, Спорт) |
| price | DECIMAL(10,2) | Цена за единицу |
| quantity | INTEGER | Количество |
| city | VARCHAR(50) | Город доставки |
| customer_age | INTEGER | Возраст покупателя |
| payment_method | VARCHAR(20) | Способ оплаты |

## Быстрый старт

### 1. Запуск системы

```bash
docker-compose up -d
```

### 2. Инициализация Redash

При первом запуске необходимо создать базу данных Redash:

```bash
docker-compose exec redash python /app/manage.py database create_tables
```

### 3. Проверка работы

Проверить, что генератор работает:
```bash
docker-compose logs -f generator
```

Проверить данные в PostgreSQL:
```bash
docker-compose exec postgres psql -U shop -d shopdb -c "SELECT COUNT(*) FROM orders;"
```

### 4. Настройка Redash

1. Открыть http://localhost:8080
2. Создать аккаунт администратора
3. Добавить источник данных:
   - Тип: PostgreSQL
   - Host: `postgres`
   - Port: `5432`
   - Database: `shopdb`
   - User: `shop`
   - Password: `shoppass`

### 5. Создание визуализаций в Redash

Примеры запросов для дашборда:

**Заказы по категориям:**
```sql
SELECT category, COUNT(*) as orders_count, SUM(price * quantity) as revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;
```

**Топ городов:**
```sql
SELECT city, COUNT(*) as orders_count
FROM orders
GROUP BY city
ORDER BY orders_count DESC
LIMIT 10;
```

**Продажи по времени:**
```sql
SELECT DATE_TRUNC('hour', created_at) as hour, COUNT(*) as orders
FROM orders
GROUP BY hour
ORDER BY hour;
```

**Средний чек по способу оплаты:**
```sql
SELECT payment_method,
       COUNT(*) as orders_count,
       ROUND(AVG(price * quantity)::numeric, 2) as avg_check
FROM orders
GROUP BY payment_method;
```

## Скриншоты дашборда

### Общий вид дашборда
![Дашборд](screenshots/dashboard.png)

### Выручка по категориям
![Категории](screenshots/categories.png)

### Топ городов по заказам
![Города](screenshots/cities.png)

### Продажи по времени
![Продажи по времени](screenshots/sales_timeline.png)

---

### 6. Jupyter Notebook

Установка зависимостей:
```bash
pip install -r requirements.txt
```

Запуск:
```bash
jupyter notebook analysis.ipynb
```

## Остановка

```bash
docker-compose down
```

Для удаления данных:
```bash
docker-compose down -v
```

## Порты

| Сервис | Порт |
|--------|------|
| PostgreSQL | 5432 |
| Redash | 8080 |
