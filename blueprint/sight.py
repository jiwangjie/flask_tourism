from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..serviceFunctions import findSightOrdersById, findSightCommentsById
from ..extensions import db
from ..models import Sight

sight_bp = Blueprint('sight', __name__)


class SightListAPI(MethodView):

    def get(self):
        """查看所有景点"""
        sights: [Sight] = Sight.query.all()
        data = []
        for sight in sights:
            data.append(sight.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    @login_required
    def post(self):
        """添加景点信息"""
        message = "success!"
        name = request.json.get("name")
        picture = request.json.get("picture")
        content = request.json.get("content")
        price = request.json.get("price")
        if name == "" or name is None:
            message = "景点不能为空！"
        elif Sight.query.filter(Sight.name == name).first() is not None:
            message = "景点已存在！"
        else:
            sight = Sight(name=name, picture=picture, content=content, price=price)
            db.session.add(sight)
            db.session.commit()
        return jsonify({
            "code": 200,
            "message": message,
            "data": ""
        })


class SightAPI(MethodView):

    def get(self, sight_id):
        """查看某一景点"""
        msg = "success!"
        data = {}
        sight: Sight = Sight.query.get(sight_id)
        if sight:
            data = sight.to_json()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    @login_required
    def put(self, sight_id):
        """修改景点信息"""
        msg = "success!"
        sight: Sight = Sight.query.get(sight_id)
        if sight:
            sight.name = request.json.get("name")
            sight.picture = request.json.get("picture")
            sight.content = request.json.get("content")
            sight.price = request.json.get("price")
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Sight.query.get(sight_id).to_json()
        })

    @login_required
    def delete(self, sight_id):
        """删除景点"""
        msg = "success!"
        sight: Sight = Sight.query.get(sight_id)
        if sight:
            db.session.delete(sight)
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


# 查看某一景点的所有订单和评论
@sight_bp.route("/sight/<int:sight_id>/orders", methods=["GET"])
@login_required
def get_sight_orders(sight_id, parameter):
    message = "success!"
    data = findSightOrdersById(sight_id)
    return jsonify({
        "code": 200,
        "message": message,
        "data": data
    })


@sight_bp.route("/sight/<int:sight_id>/comments", methods=["GET"])
def get_sight_comments(sight_id):
    message = "success!"
    data = findSightCommentsById(sight_id)
    return jsonify({
        "code": 200,
        "message": message,
        "data": data
    })


sight_bp.add_url_rule('/sight',
                      view_func=SightListAPI.as_view('sights_api'), methods=['GET', 'POST'])

sight_bp.add_url_rule('/sight/<int:sight_id>',
                      view_func=SightAPI.as_view('sight_api'), methods=['GET', 'PUT', 'DELETE'])
