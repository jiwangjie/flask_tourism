from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..extensions import db
from ..models import Ticket, User, Station

ticket_bp = Blueprint('ticket', __name__)


class TicketListAPI(MethodView):

    decorators = [login_required]

    def get(self):
        """查看所有车票"""
        tickets: [Ticket] = Ticket.query.all()
        data = []
        for ticket in tickets:
            data.append(ticket.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    def post(self):
        """新增加车票"""
        user_id = request.json.get("user_id")
        station_id = request.json.get("station_id")
        count = request.json.get("count")
        total = request.json.get("total")
        note = request.json.get("note")
        timestamp = datetime.utcnow()
        ticket = Ticket(user_id=user_id, station_id=station_id, count=count,
                        total=total, note=note, create_time=timestamp)
        db.session.add(ticket)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": ""
        })


class TicketAPI(MethodView):

    decorators = [login_required]

    def get(self, ticket_id):
        """查看某一车票信息，包含的外键信息有，购买车票的用户名，车站起始站"""
        msg = "success！"
        data = {}
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            data = ticket.to_json()
            userItem: User = User.query.get(ticket.user_id)  # 冒号后跟类，表示冒号前面的参数类型
            data["username"] = userItem.username
            stationItem: Station = Station.query.get(ticket.station_id)
            data["start_station"] = stationItem.start_station
            data["end_station"] = stationItem.end_station
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    def put(self, ticket_id):
        """修改某一车票信息"""
        msg = "success！"
        ticket: Ticket = Ticket.query.get(ticket_id)
        if ticket:
            ticket.user_id = request.json.get("user_id")
            ticket.station_id = request.json.get("station_id")
            ticket.count = request.json.get("count")
            ticket.total = request.json.get("total")
            ticket.note = request.json.get("note")
            db.session.commit()
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Ticket.query.get(ticket_id).to_json()
        })

    def delete(self, ticket_id):
        """删除某一车票"""
        msg = "success！"
        ticket: Ticket = Ticket.query.get(ticket_id)
        if ticket:
            db.session.delete(ticket)
            db.session.commit()
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


ticket_bp.add_url_rule('/ticket',
                       view_func=TicketListAPI.as_view('tickets_api'), methods=['GET', 'POST'])

ticket_bp.add_url_rule('/ticket/<int:ticket_id>',
                       view_func=TicketAPI.as_view('ticket_api'), methods=['GET', 'PUT', 'DELETE'])
