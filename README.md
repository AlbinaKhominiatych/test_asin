# Amazon Price Scraper

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/yourrepository/blob/master/LICENSE)

## Опис

Цей проєкт реалізує простий API для отримання ціни товарів на Amazon за їх ASIN (Amazon Standard Identification Number). Використовуючи FastAPI для створення API та SQLAlchemy для роботи з базою даних, код дозволяє отримувати ціни товарів з Amazon та зберігати їх у базі даних SQLite.

## Функції та ендпойнти

### 1. `GET /get_price/{asin}`
   - **Опис:** Ендпойнт API для отримання ціни товару з Amazon та зберігання її в базі даних.
   - **Параметри:**
       - `asin` (строка): Amazon Standard Identification Number товару.
   - **Повертає:**
       - JSON об'єкт з полями ASIN та price.

### Обробка помилок

Код має обробку помилок під час взаємодії з Amazon, парсингу даних та роботи з базою даних. Це дозволяє виводити зрозумілі повідомлення про помилки відповідно до ситуацій, що виникають.

### Масштабованість та розширюваність

Код розділений на функції для роботи з Amazon, базою даних та обробки запитів API, що дозволяє легко додавати новий функціонал або оновлювати існуючий без змін у вже існуючому коді.

## Технології

- Python
- FastAPI
- SQLAlchemy
- BeautifulSoup
- SQLite
- requests

## Встановлення та запуск

1. Клонуйте репозиторій:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```
2. Встановіть залежності:
    ```bash
    pip install -r requirements.txt
    ```
3. Запустіть сервер:
    ```bash
    uvicorn main:app --reload
    ```

## Ліцензія

Цей проект ліцензовано під [MIT License](https://opensource.org/licenses/MIT).
