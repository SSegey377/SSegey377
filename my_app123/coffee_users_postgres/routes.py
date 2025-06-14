from flask import Blueprint, request, jsonify
from models import db, Coffee, User
from sqlalchemy import text

bp = Blueprint('bp', __name__)

@bp.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.json
    if not user_data:
        return jsonify({"error": "Нет данных пользователя"}), 400
    name = user_data.get('name')
    has_sale = user_data.get('has_sale')
    address = user_data.get('address')
    coffee_id = user_data.get('coffee_id')
    if not name or coffee_id is None:
        return jsonify({"error": "Отсутствуют обязательные поля: name, coffee_id"}), 400
    coffee = Coffee.query.get(coffee_id)
    if not coffee:
        return jsonify({"error": f"Кофе с id {coffee_id} не найден"}), 404
    user = User(name=name, has_sale=has_sale, address=address, coffee_id=coffee_id)
    db.session.add(user)
    db.session.commit()
    response = {
        "id": user.id,
        "name": user.name,
        "has_sale": user.has_sale,
        "address": user.address,
        "coffee_id": user.coffee_id,
        "coffee_title": coffee.title,
        "coffee_origin": coffee.origin,
        "coffee_intensifier": coffee.intensifier,
        "coffee_notes": coffee.notes
    }
    return jsonify(response), 201


@bp.route('/search_coffee', methods=['POST'])
def search_coffee():
    data = request.json
    search_string = data.get('title') if data else None
    if not search_string:
        return jsonify({"error": "Отсутствует параметр 'title' для поиска"}), 400
    coffees = Coffee.query.filter(Coffee.title.ilike(f'%{search_string}%')).all()
    result = []
    for coffee in coffees:
        result.append({
            "id": coffee.id,
            "title": coffee.title,
            "origin": coffee.origin,
            "intensifier": coffee.intensifier,
            "notes": coffee.notes
        })
    return jsonify(result)


@bp.route('/unique_coffee_notes', methods=['GET'])
def unique_coffee_notes():
    query = text("SELECT DISTINCT unnest(notes) as note FROM coffee WHERE notes IS NOT NULL")
    result = db.session.execute(query).fetchall()
    unique_notes = [row['note'] for row in result]
    return jsonify({
        "unique_notes": unique_notes,
        "count": len(unique_notes)
    })


@bp.route('/users_from_country', methods=['POST'])
def users_from_country():
    data = request.json
    country = data.get('country') if data else None
    if not country:
        return jsonify({"error": "Отсутствует параметр 'country'"}), 400
    users = User.query.filter(User.address['country'].astext.ilike(f'%{country}%')).all()
    results = []
    for u in users:
        results.append({
            "id": u.id,
            "name": u.name,
            "has_sale": u.has_sale,
            "address": u.address,
            "coffee_id": u.coffee_id
        })
    return jsonify(results)

