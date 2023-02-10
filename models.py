from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(db.Model):
    """用户信息"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    phone = db.Column(db.String(11), unique=True)
    gender = db.Column(db.Boolean, default=True)
    avatar = db.Column(db.String)
    user_role = db.Column(db.Boolean, default=True)
    # 表间关系
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    tickets = db.relationship('Ticket', back_populates='user', cascade='all, delete-orphan')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    @property
    def encrypt_password(self):
        return self.password

    @encrypt_password.setter
    def encrypt_password(self, value):
        self.password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)


class Sight(db.Model):
    """景点"""
    __tablename__ = 'sight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    picture = db.Column(db.String)
    content = db.Column(db.String)
    price = db.Column(db.Float(2), nullable=False)
    # 这里不做人员类型分类，前端可以根据不同人员对价格进行计算
    # 表间关系
    comments = db.relationship('Comment', back_populates='sight')
    orders = db.relationship('Order', back_populates='sight')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Hotel(db.Model):
    """酒店"""
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    picture = db.Column(db.String)
    content = db.Column(db.String)
    price = db.Column(db.Float(2), nullable=False)
    # type = db.Column(db.String)
    # 这里不做房间类型分类，前端可以根据不同房间对价格进行计算
    # 表间关系
    comments = db.relationship('Comment', back_populates='hotel')
    orders = db.relationship('Order', back_populates='hotel')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Station(db.Model):
    """车站"""
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_station = db.Column(db.String)
    end_station = db.Column(db.String)
    price = db.Column(db.Float(2), nullable=False)
    # 表间关系
    tickets = db.relationship('Ticket', back_populates='station')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Ticket(db.Model):
    """车票"""
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    station_id = db.Column(db.Integer, db.ForeignKey(Station.id))
    count = db.Column(db.Integer)
    total = db.Column(db.Float)
    note = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())  # 字段拼写错误
    # 表间关系
    user = db.relationship('User', back_populates='tickets')
    station = db.relationship('Station', back_populates='tickets')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Order(db.Model):
    """酒店和景点订单"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sight_id = db.Column(db.Integer, db.ForeignKey(Sight.id))
    hotel_id = db.Column(db.Integer, db.ForeignKey(Hotel.id))
    count = db.Column(db.Integer)  # 票数
    total = db.Column(db.Float)  # 总价
    note = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    # 表间关系
    user = db.relationship('User', back_populates='orders')
    sight = db.relationship('Sight', back_populates='orders')
    hotel = db.relationship('Hotel', back_populates='orders')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Comment(db.Model):
    """酒店和景点评论"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sight_id = db.Column(db.Integer, db.ForeignKey(Sight.id))
    hotel_id = db.Column(db.Integer, db.ForeignKey(Hotel.id))
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    # 表间关系
    user = db.relationship('User', back_populates='comments')
    sight = db.relationship('Sight', back_populates='comments')
    hotel = db.relationship('Hotel', back_populates='comments')

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
