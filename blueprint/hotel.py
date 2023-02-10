from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..serviceFunctions import findHotelOrdersById, findHotelCommentsById
from ..extensions import db
from ..models import Hotel

hotel_bp = Blueprint('hotel', __name__)


class HotelListAPI(MethodView):

    def get(self):
        """查看所有酒店"""
        hotels: [Hotel] = Hotel.query.all()
        data = []
        for hotel in hotels:
            data.append(hotel.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    @login_required
    def post(self):
        """添加一个酒店"""
        message = "success!"
        name = request.json.get("name")
        picture = request.json.get("picture")
        content = request.json.get("content")
        price = request.json.get("price")
        if name == "" or name is None:
            message = "酒店不能为空！"
        elif Hotel.query.filter(Hotel.name == name).first() is not None:
            message = "酒店已存在！"
        else:
            hotel = Hotel(name=name, picture=picture, content=content, price=price)
            db.session.add(hotel)
            db.session.commit()
        return jsonify({
            "code": 200,
            "message": message,
            "data": ""
        })


class HotelAPI(MethodView):
    """酒店信息的查改删"""

    def get(self, hotel_id):
        """查看某一个酒店"""
        msg = "success!"
        data = {}
        hotel: Hotel = Hotel.query.get(hotel_id)
        if hotel:
            data = hotel.to_json()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    @login_required
    def put(self, hotel_id):
        """修改一个酒店信息"""
        msg = "success!"
        hotel: Hotel = Hotel.query.get(hotel_id)
        if hotel:
            hotel.name = request.json.get("name")
            hotel.picture = request.json.get("picture")
            hotel.content = request.json.get("content")
            hotel.price = request.json.get("price")
            db.session.commit()
        else:
            msg = "无此数据!"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Hotel.query.get(hotel_id).to_json()
        })

    @login_required
    def delete(self, hotel_id):
        """删除某一个酒店"""
        msg = "success!"
        hotel: Hotel = Hotel.query.get(hotel_id)
        if hotel:
            db.session.delete(hotel)
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


@hotel_bp.route("/hotel/<int:hotel_id>/orders", methods=["GET"])
@login_required
def get_hotel_orders(hotel_id):
    msg = "success!"
    data = []
    if Hotel.query.gey(hotel_id):
        data = findHotelOrdersById(hotel_id)
    else:
        msg = "无此数据！"
    return jsonify({
        "code": 200,
        "message": msg,
        "data": data
    })

@hotel_bp.route("/hotel/<int:hotel_id>/comments", methods=["GET"])
def get_hotel_comments(hotel_id):
    msg = "success!"
    data = []
    if Hotel.query.gey(hotel_id):
        data = findHotelCommentsById(hotel_id)
    else:
        msg = "无此数据！"
    return jsonify({
        "code": 200,
        "message": msg,
        "data": data
    })


hotel_bp.add_url_rule('/hotel',
                      view_func=HotelListAPI.as_view('hotels_api'), methods=['GET', 'POST'])

hotel_bp.add_url_rule('/hotel/<int:hotel_id>',
                      view_func=HotelAPI.as_view('hotel_api'), methods=['GET', 'PUT', 'DELETE'])
