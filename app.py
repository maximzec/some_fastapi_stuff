from fastapi import FastAPI, Request
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from email_utils import send_mail
from fastapi.templating import Jinja2Templates
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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


templates = Jinja2Templates(directory="templates")


@app.post('/form')
async def form(request: Request, form: EmailForm):
    total_price = 0
    for item in form.items:
        total_price += item.count * item.price
    message = templates.TemplateResponse(
        "email_template.html", {
            "request": request,
            "name": form.name,
            "email": form.email,
            "city": form.city,
            "address": form.address,
            "phone_number": form.phone_number,
            "items": form.items,
            "total_price": total_price
        }).body.decode('utf-8')
    send_mail(message)


@app.get('/')
async def root():
    return {'message': 'OK'}
