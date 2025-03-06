from yookassa import Configuration,  Payment
import requests
import json
from config import TOKEN

Configuration.account_id = "1033668"
Configuration.secret_key = "live_KJkzS4oHMLBmwM97A48bZYJQRZCNdUUWCJcFPOAf8lE"


import uuid

async def create_payment(value, description, user_id):
    idempotence_key = str(uuid.uuid4())
    customer_email = "ovikboss2016@gmail.com"
    try:
        payment = Payment.create({
            "amount": {
                "value": f"{value}",  # Значение суммы должно быть строкой
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
            "capture": True,
            "description": f"{description}",
            "receipt": {
                "email": "simonyan-ovo@mail.ru",  # Email в корне receipt
                "items": [
                    {
                        "description": f"{description}",
                        "quantity": "1.00",
                        "amount": {
                            "value": f"{value}",  # Значение суммы должно быть строкой, равно стоимости товара
                            "currency": "RUB"
                        },
                        "vat_code": "2",
                        "payment_subject": "service",# Добавлено payment_subject
                        "payment_mode": "full_payment"

                    }
                ],
                "tax_system_code": 1
            }
        }, idempotence_key)
        print(payment)
        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url  # Получаем ссылку на оплату
        print(f"Успешно создан платеж с ID: {payment_id}")
        print(f"Ссылка на оплату: {confirmation_url}{user_id}")
        return payment
        # Отправьте ссылку на оплату пользователю (например, в Telegram-боте)

    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")

def check_payment_status(payment_id: str):
    """Проверяет статус платежа по его ID."""
    try:
        payment = Payment.find_one(payment_id)
        return payment.status #  Возвращаем статус платежа (succeeded, pending, canceled)
    except Exception as e:
        print(f"Ошибка при проверке статуса платежа: {e}")
        return None


