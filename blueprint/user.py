from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session
from flask.views import MethodView

from utils import login_required
from ..serviceFunctions import findUserOrdersById, findUserCommentsById, findUserTicketsById
from ..extensions import db
from ..models import User

user_bp = Blueprint('user', __name__)


class UserListAPI(MethodView):
    """查询所有用户，新增用户"""

    decorators = [login_required]

    def get(self):
        users: [User] = User.query.all()
        data = []
        for user in users:
            data.append(user.to_json())
        return jsonify({
            "code": 200,
            "message": "success!",
            "data": data
        })

    def post(self):
        """用户注册"""
        message = "success!"
        username = request.json.get("username")
        password = request.json.get("password")
        phone = request.json.get("phone")
        if username == "" or username is None:
            message = "用户名不能为空！"
        elif User.query.filter(User.username == username).first() is not None:
            message = "用户名已存在！"
        elif password == "" or password is None:
            message = "密码不能为空！"
        elif phone == "" or phone is None:
            message = "手机号不能为空！"
        elif User.query.filter(User.phone == phone).first() is not None:
            message = "手机号已被注册！"
        else:
            gender = eval(request.json.get("gender"))
            avatar = request.json.get("avatar")
            user_role = eval(request.json.get("user_role"))
            user = User(username=username, encrypt_password=password, phone=phone, gender=gender,
                        avatar=avatar, user_role=user_role)
            db.session.add(user)
            db.session.commit()
        return jsonify({
            "code": 200,
            "message": message,
            "data": ""
        })


class UserAPI(MethodView):

    decorators = [login_required]

    def get(self, user_id):
        """查看用户信息"""
        msg = "success!"
        data= {}
        user: User = User.query.get(user_id)
        if user:
            data = user.to_json()
        else:
            msg = "无此数据!"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": data
        })

    def put(self, user_id):
        """修改用户信息"""
        msg = "success!"
        user: User = User.query.get(user_id)
        if user:
            user.encrypt_password = request.json.get("password")
            user.phone = request.json.get("phone")
            user.gender = eval(request.json.get("gender"))
            user.avatar = request.json.get("avatar")
            user.user_role = eval(request.json.get("user_role"))
            db.session.commit()
        else:
            msg = "无此数据！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": User.query.get(user_id).to_json()
        })

    def delete(self, user_id):
        """删除账户"""
        msg = "success!"
        user: User = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            msg = "无此用户！"
        return jsonify({
            "code": 200,
            "message": msg,
            "data": ""
        })


@user_bp.route("/login", methods=["POST", "GET"])
def login():
    """登录"""
    msg = "success!"
    if request.method == "GET":
        return render_template('login.html')  # 返回登录页面
    else:
        username = request.json.get("username")
        password = request.json.get("password")
        user_role = eval(request.json.get("user_role"))
        if username == "" or username is None:
            msg = "用户名不能为空！"
        elif password == "" or password is None:
            msg = "密码不能为空！"
        else:
            user = User.query.filter(User.username == username,
                                     User.user_role == user_role).first()
            if user is not None:
                if user.check_password(password):
                    session['user'] = user.to_json()
                    if user_role is True:
                        redirect(url_for('index.index', message="重定向来的"))  # 普通用户
                    redirect(url_for('index.admin'))  # 管理员
                else:
                    msg = "密码错误！"
            else:
                msg = "账号不存在！"
    return jsonify({
        "code": 200,
        "message": msg,
        "data": ""
    })


@user_bp.route("/logout", methods=["POST"])
def logout():
    """退出"""
    msg = "success!"
    user = session.get('user')
    if not user:
        msg = "用户尚未登录！"
    else:
        session["user"] = None
    return jsonify({
        "code": 200,
        "message": msg,
        "data": ""
    })


@user_bp.route("/register", methods=["GET"])
def register():
    """注册"""
    if request.method == "GET":
        return render_template("register.html")  # 返回注册页面
    else:
        return redirect(url_for('/user', _method='POST'))


# 查看某一用户的订单，评论，车票
# 想要查看用户的酒店订单，可在前端直接选择sight_id == NULL，想看景点订单选择hotel_id== NULL。
# 查看评论同理
@user_bp.route("/user/<int:user_id>/<string:parameter>", methods=["GET"])
@login_required
def get_user_parameter(user_id, parameter):
    msg = "success!"
    data = []
    if parameter == "orders":  # 查询某一用户的所有订单
        if User.query.get(user_id):
            data = findUserOrdersById(user_id)
        else:
            msg = "无此数据！"
    elif parameter == "comments":  # 查询某一用户的所有评论
        if User.query.get(user_id):
            data = findUserCommentsById(user_id)
        else:
            msg = "无此数据！"
    elif parameter == "tickets":  # 查询某一用户的所有车票
        if User.query.get(user_id):
            data = findUserTicketsById(user_id)
        else:
            msg = "无此数据！"
    else:
        msg = "参数错误！"
    return jsonify({
        "code": 200,
        "message": msg,
        "data": data
    })


user_bp.add_url_rule('/user',
                     view_func=UserListAPI.as_view('users_api'), methods=['GET', 'POST'])

user_bp.add_url_rule('/user/<int:user_id>',
                     view_func=UserAPI.as_view('user_api'), methods=['GET', 'PUT', 'DELETE'])
