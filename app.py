from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # путь до файла БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    """The view to get all users and creating new user"""
    if request.method == 'GET':
        users_list = db.session.query(User).all()
        result = []
        for user in users_list:
            result.append(user.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        try:
            new_user = json.loads(request.data)
            new_user_object = User(
                id=new_user['id'],
                first_name=new_user['first_name'],
                last_name=new_user['last_name'],
                age=new_user['age'],
                email=new_user['email'],
                role=new_user['role'],
                phone=new_user['phone']
            )
            db.session.add(new_user_object)
            db.session.commit()
            return f"Новый пользователь добавлен в базу данных с id #{new_user['id']}", 200
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id: int):
    """The view to get one user by user_id, to update/delete user"""
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if user is None:
            return f'Пользователя с id {user_id} не существует'
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user_to_update = db.session.query(User).get(user_id)
        if user_to_update is None:
            return f'Пользователя с id {user_id} не существует'
        user_to_update.first_name = user_data['first_name']
        user_to_update.last_name = user_data['last_name']
        user_to_update.age = user_data['age']
        user_to_update.email = user_data['email']
        user_to_update.role = user_data['role']
        user_to_update.phone = user_data['phone']

        db.session.add(user_to_update)
        db.session.commit()
        return f'Пользователь с id {user_id} изменен'

    elif request.method == 'DELETE':
        user_to_del = db.session.query(User).get(user_id)
        if user_to_del is None:
            return f'Пользователя с id {user_id} не существует'
        db.session.delete(user_to_del)
        db.session.commit()
        return f'Пользователь с id {user_id} удален'


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    """The view to get all orders and creating new order"""
    if request.method == 'GET':
        orders_list = db.session.query(Order).all()
        result = []
        for order in orders_list:
            result.append(order.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        try:
            new_order = json.loads(request.data)
            new_order_object = Order(
                id=new_order['id'],
                name=new_order['name'],
                description=new_order['description'],
                start_date=new_order['start_date'],
                end_date=new_order['end_date'],
                address=new_order['address'],
                price=new_order['price'],
                customer_id=new_order['customer_id'],
                executor_id=new_order['executor_id']
            )
            db.session.add(new_order_object)
            db.session.commit()
            return f"Новый заказ добавлен в базу данных с id #{new_order['id']}", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id: int):
    """The view to get one order by id, to update/delete order"""
    if request.method == 'GET':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return f'Заказ с id {order_id} не существует'
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order_to_update = db.session.query(Order).get(order_id)
        if order_to_update is None:
            return f'Заказа с id {order_id} не существует'
        order_to_update.name = order_data['name']
        order_to_update.description = order_data['description']
        order_to_update.start_date = order_data['start_date']
        order_to_update.end_date = order_data['end_date']
        order_to_update.address = order_data['address']
        order_to_update.price = order_data['price']
        order_to_update.customer_id = order_data['customer_id']
        order_to_update.executor_id = order_data['executor_id']

        db.session.add(order_to_update)
        db.session.commit()
        return f'Заказ с id {order_id} изменен'

    elif request.method == 'DELETE':
        user_to_del = db.session.query(Order).get(order_id)
        if user_to_del is None:
            return f'Заказа с id {order_id} не существует'
        db.session.delete(user_to_del)
        db.session.commit()
        return f'Заказ с id {order_id} удален'


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    """The The view to get all offers and creating new offer"""
    if request.method == 'GET':
        offers_list = db.session.query(Offer).all()
        result = []
        for offer in offers_list:
            result.append(offer.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        try:
            new_offer = json.loads(request.data)
            new_offer_object = Order(
                id=new_offer['id'],
                order_id=new_offer['order_id'],
                executor_id=new_offer['executor_id']
            )
            db.session.add(new_offer_object)
            db.session.commit()
            return f"Новый оффер добавлен в базу данных с id #{new_offer['id']}", 200
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id: int):
    if request.method == 'GET':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return f'Предложения с id {offer_id} не существует'
        return jsonify(offer.to_dict())

    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer_to_update = db.session.query(Offer).get(offer_id)
        if offer_to_update is None:
            return f'Оффера с id {offer_id} не существует'
        offer_to_update.order_id = offer_data['order_id']
        offer_to_update.executor_id = offer_data['executor_id']

        db.session.add(offer_to_update)
        db.session.commit()
        return f'Оффер с id {offer_id} изменен'

    elif request.method == 'DELETE':
        user_to_del = db.session.query(Order).get(offer_id)
        if user_to_del is None:
            return f'Оффера с id {offer_id} не существует'
        db.session.delete(user_to_del)
        db.session.commit()
        return f'Оффер с id {offer_id} удален'


if __name__ == '__main__':
    app.run(debug=True)
