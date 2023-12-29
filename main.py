from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

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
    url = f'https://www.amazon.com/dp/{asin}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_element = soup.find(class_='a-offscreen')
    price = price_element.text.strip() if price_element else 'Ціна не знайдена'

    Session = sessionmaker(bind=engine)
    session = Session()

    product = Product(id=asin, price=float(price.replace('$', '').replace(',', '')))
    session.add(product)
    session.commit()
    session.close()

    return price

@app.get("/get_price/{asin}")
def get_price(asin: str):
    price = get_price_from_amazon(asin)
    return {"ASIN": asin, "price": price}
