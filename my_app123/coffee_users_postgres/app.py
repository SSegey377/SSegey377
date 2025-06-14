import os
import requests
import time
from random import randint
from flask import Flask, jsonify
from models import db, Coffee, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@postgres:5432/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

    for _ in range(10):   # Создание 10 сортов кофе
        for attempt in range(5):
            try:
                coffee_data = requests.get("https://random-data-api.com/api/coffee/random_coffee")
                coffee_data.raise_for_status()
                coffee_data = coffee_data.json()
                coffee = Coffee(
                    title=coffee_data['blend_name'],
                    origin=coffee_data['origin'],
                    intensifier=coffee_data['intensifier'],
                    notes=coffee_data['notes'].split(', ') if 'notes' in coffee_data else []
                )
                db.session.add(coffee)
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print("Слишком много запросов, ожидаем перед повторной попыткой...")
                    time.sleep(5)
                else:
                    print(f"Ошибка при получении данных о кофе: {e}")
                    break

    db.session.commit()

    # Создание 10 пользователей
    for _ in range(10):
        for attempt in range(5):
            try:
                address_data = requests.get("https://random-data-api.com/api/address/random_address")
                address_data.raise_for_status()
                address_data = address_data.json()
                coffee_id = randint(1, 10)
                if not Coffee.query.get(coffee_id):
                    print(f"Кофе с id {coffee_id} не найден, выбираем другой id.")
                    continue
                user = User(
                    name=f"User    {_ + 1}",
                    has_sale=bool(randint(0, 1)),
                    address=address_data,
                    coffee_id=coffee_id
                )
                db.session.add(user)
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print("Слишком много запросов, ожидаем перед повторной попыткой...")
                    time.sleep(5)
                else:
                    print(f"Ошибка при получении данных о пользователе: {e}")
                    break
            except ValueError as e:
                print(f"Ошибка декодирования JSON: {e}")
                break
    db.session.commit()

@app.route('/')
def index():
    return jsonify({"message": "Приложение работает и подключено к базе данных PostgreSQL."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


