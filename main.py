from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    price = Column(Float)


app = FastAPI()

# Підключення до бази SQLite
engine = create_engine('sqlite:///./test.db')

Base.metadata.create_all(engine)


def get_price_from_amazon(asin: str):
    try:
        url = f'https://www.amazon.com/dp/{asin}'
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на наявність помилок під час запиту

        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find(class_='a-offscreen')
        price = price_element.text.strip() if price_element else 'Ціна не знайдена'

        return float(price.replace('$', '').replace(',', ''))

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Помилка під час отримання даних з Amazon: {str(e)}")

    except (AttributeError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Помилка при парсингу ціни: {str(e)}")


def save_price_to_db(asin: str, price: float):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        product = Product(id=asin, price=price)
        session.merge(product)
        session.commit()
        session.close()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Помилка при роботі з базою даних: {str(e)}")


@app.get("/get_price/{asin}")
def get_price(asin: str):
    try:
        price = get_price_from_amazon(asin)
        save_price_to_db(asin, price)
        return {"ASIN": asin, "price": price}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Невідома помилка: {str(e)}")
