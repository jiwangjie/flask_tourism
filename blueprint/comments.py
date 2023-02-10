from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from utils import login_required
from ..extensions import db
from ..models import Comment, Hotel, Sight, User

comment_bp = Blueprint('comment', __name__)


class CommentListAPI(MethodView):

    decorators = [login_required]

    def get(self):
        comments: [Comment] = Comment.query.all()
        data = []
        for comment in comments:
            data.append(comment.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    def post(self):
        """添加一条评论"""
        msg = "success!"
        content = request.json.get("content")
        user_id = request.json.get("user_id")
        sight_id = request.json.get("sight_id")
        hotel_id = request.json.get("hotel_id")
        timestamp = datetime.utcnow()
        if sight_id == "":
            sight_id = None
        else:
            hotel_id = None
        if content == "":
            msg = "评论内容不能为空！"
        else:
            sight = Comment(content=content, user_id=user_id, sight_id=sight_id, hotel_id=hotel_id, create_time=timestamp)
            db.session.add(sight)
            db.session.commit()
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


class CommentAPI(MethodView):

    def get(self, comment_id):
        """获取某一条评论"""
        data = {}
        msg = "success!"
        comment: Comment = Comment.query.get(comment_id)  # 冒号后跟类，表示冒号前面的参数类型
        if comment:
            data = comment.to_json()
            userItem: User = User.query.get(comment.user_id)
            data["username"] = userItem.username
            if comment.hotel_id is not None:
                hotelItem: Hotel = Hotel.query.get(comment.hotel_id)
                data["hotelName"] = hotelItem.name
                data["hotelPicture"] = hotelItem.picture
            else:
                sightItem: Sight = Sight.query.get(comment.sight_id)
                data["hotelName"] = sightItem.name
                data["hotelPicture"] = sightItem.picture
        else:
            msg = "无此评论"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    @login_required
    def put(self, comment_id):
        """修改评论信息"""
        msg = "success!"
        comment: Comment = Comment.query.get(comment_id)
        if comment:
            comment.content = request.json.get("content")
            comment.user_id = request.json.get("user_id")
            sight_id = request.json.get("sight_id")
            hotel_id = request.json.get("hotel_id")
            if sight_id == "":
                sight_id = None
            else:
                hotel_id = None
            comment.sight_id = sight_id
            comment.hotel_id = hotel_id
            db.session.commit()
        else:
            msg = "无此评论！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": Comment.query.get(comment_id).to_json()
        })

    @login_required
    def delete(self, comment_id):
        """删除一条评论"""
        msg = "success!"
        comment: Comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
        else:
            msg = "无此评论！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


comment_bp.add_url_rule('/comment',
                        view_func=CommentListAPI.as_view('comments_api'), methods=['GET', 'POST'])

comment_bp.add_url_rule('/comment/<int:comment_id>',
                        view_func=CommentAPI.as_view('comment_api'), methods=['GET', 'PUT', 'DELETE'])
