from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..extensions import db
from ..models import Station

station_bp = Blueprint('station', __name__)


class StationListAPI(MethodView):

    def get(self):
        """查看所有车站"""
        stations: [Station] = Station.query.all()
        data = []
        for station in stations:
            data.append(station.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    @login_required
    def post(self):
        """添加车次信息"""
        message = "success!"
        start_station = request.json.get("start_station")
        end_station = request.json.get("end_station")
        price = request.json.get("price")
        if start_station == "" or start_station is None:
            message = "出发站不能为空！"
        elif end_station == "" or end_station is None:
            message = "终点站不能为空！"
        elif Station.query.filter(Station.start_station == start_station,
                                  Station.end_station == end_station).first() is not None:
            message = "车站班次已存在！"
        else:
            station = Station(start_station=start_station, end_station=end_station, price=price)
            db.session.add(station)
            db.session.commit()
        return jsonify({
            "code": 200,
            "message": message,
            "data": ""
        })


class StationAPI(MethodView):

    def get(self, station_id):
        """获取某一个车次"""
        msg = "success！"
        data = {}
        station: Station = Station.query.get(station_id)
        if station:
            data = station.to_json()
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    @login_required
    def put(self, station_id):
        """修改车次信息"""
        msg = "success！"
        station: Station = Station.query.get(station_id)
        if station:
            station.start_station = request.json.get("start_station")
            station.end_station = request.json.get("end_station")
            station.price = request.json.get("price")
            db.session.commit()
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Station.query.get(station_id).to_json()
        })

    @login_required
    def delete(self, station_id):
        """删除车次"""
        msg = "success！"
        station: Station = Station.query.get(station_id)
        if station:
            db.session.delete(station)
            db.session.commit()
        else:
            msg = "无此数据"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


station_bp.add_url_rule('/station',
                        view_func=StationListAPI.as_view('stations_api'), methods=['GET', 'POST'])

station_bp.add_url_rule('/station/<int:station_id>',
                        view_func=StationAPI.as_view('station_api'), methods=['GET', 'PUT', 'DELETE'])
