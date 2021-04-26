from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from email_utils import send_mail
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    volume: int
    price: int
    vendor_code: int
    count: int


class EmailForm(BaseModel):
    email: EmailStr
    phone_number: str
    name: str
    city: str
    address: str
    items: List[Item]


@app.post('/form')
async def form(form: EmailForm):
    message = f"Заказ от : {form.name}\nГород / Регион : {form.city}\nАдрес доставки: {form.address}\nТелефон : {form.phone_number}\nEmail : {form.email}\nКоличество товаров {len(form.items)}:\n"
    list_message = ""
    total_price = 0
    for item in form.items:
        list_message += f"\t{item.name}\n\t\tОбъем в мл - {item.volume}\n\t\tЦена за шт. - {item.price}\n\t\tКоличество - {item.count}\n\t\tАртикул - {item.vendor_code}\n"
        total_price = item.price * item.count
    price_message = f"Итоговая цена : {total_price}₽"
    send_mail(message+list_message+price_message)


@app.get('/')
async def root():
    return {'message': 'OK'}
