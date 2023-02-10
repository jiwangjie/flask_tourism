from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..extensions import db
from ..models import Order, User, Hotel, Sight

order_bp = Blueprint('order', __name__)


class OrderListAPI(MethodView):

    decorators = [login_required]

    def get(self):
        """查看所有订单"""
        orders: [Order] = Order.query.all()
        data = []
        for order in orders:
            data.append(order.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    def post(self):
        """新增订单"""
        user_id = request.json.get("user_id")
        sight_id = request.json.get("sight_id")
        hotel_id = request.json.get("hotel_id")
        count = request.json.get("count")
        total = request.json.get("total")
        note = request.json.get("note")
        timestamp = datetime.utcnow()
        if sight_id == "":
            sight_id = None
        else:
            hotel_id = None
        order = Order(user_id=user_id, sight_id=sight_id, hotel_id=hotel_id, count=count,
                      total=total, note=note, create_time=timestamp)
        db.session.add(order)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": ""
        })


class OrderAPI(MethodView):

    decorators = [login_required]

    def get(self, order_id):
        """获取某一条订单信息，包含的外键信息有订单用户名，酒店/景点名"""
        msg = "success!"
        data = {}
        order: Order = Order.query.get(order_id)
        if order:
            data = order.to_json()
            userItem: User = User.query.get(order.user_id)
            data["username"] = userItem.username
            if order.hotel_id is not None:
                hotelItem: Hotel = Hotel.query.get(order.hotel_id)
                data["hotelName"] = hotelItem.name
                data["hotelPicture"] = hotelItem.picture
            else:
                sightItem: Sight = Sight.query.get(order.sight_id)
                data["sightName"] = sightItem.name
                data["sightPicture"] = sightItem.picture
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    def put(self, order_id):
        """修改订单信息"""
        msg = "success!"
        order: Order = Order.query.get(order_id)
        if order:
            order.user_id = request.json.get("user_id")
            order.count = request.json.get("count")
            order.total = request.json.get("total")
            order.note = request.json.get("note")
            sight_id = request.json.get("sight_id")
            hotel_id = request.json.get("hotel_id")
            if sight_id == "":
                sight_id = None
            else:
                hotel_id = None
            order.sight_id = sight_id
            order.hotel_id = hotel_id
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Order.query.get(order_id).to_json()
        })

    def delete(self, order_id):
        """删除订单"""
        msg = "success!"
        order: Order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


order_bp.add_url_rule('/order',
                      view_func=OrderListAPI.as_view('orders_api'), methods=['GET', 'POST'])

order_bp.add_url_rule('/order/<int:order_id>',
                      view_func=OrderAPI.as_view('order_api'), methods=['GET', 'PUT', 'DELETE'])
