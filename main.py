from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Функція для отримання ціни товару з Amazon за його ASIN
def get_price_from_amazon(asin: str):
    # URL для запиту на Amazon
    url = f'https://www.amazon.com/dp/{asin}'

    # Отримання вмісту сторінки
    response = requests.get(url)

    # Парсинг сторінки за допомогою Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Здійснення логіки для отримання елемента з класом 'a-offscreen' та aria-hidden="true"
    price_element = soup.find(class_='a-offscreen')
    price = price_element.text.strip() if price_element else 'Ціна не знайдена'

    return price

@app.get("/get_price/{asin}")
def get_price(asin: str):
    price = get_price_from_amazon(asin)
    return {"ASIN": asin, "price": price}
