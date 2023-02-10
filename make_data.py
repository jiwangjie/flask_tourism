from datetime import datetime

from .extensions import db
from .models import User, Sight, Order, Hotel, Comment, Station, Ticket


def make_data():
    # user
    user_1 = User(username="admin", encrypt_password="admin", phone="18949297060",
                  gender=True, avatar="avatar", user_role=True)
    user_2 = User(username="admin1", encrypt_password="admin", phone="18949297061",
                  gender=False, avatar="avatar", user_role=False)
    # sight
    sight_1 = Sight(name="sight_name_1", picture="sight_picture", content="sight_content", price=12.99)
    sight_2 = Sight(name="sight_name_2", picture="sight_picture", content="sight_content", price=12.99)

    # hotel
    hotel_1 = Hotel(name="hotel_name_1", picture="hotel_picture", content="hotel_content", price=12.99)
    hotel_2 = Hotel(name="hotel_name_1", picture="hotel_picture", content="hotel_content", price=12.99)

    # station
    station_1 = Station(start_station="HangZhou", end_station="HeFei", price=12.99)
    station_2 = Station(start_station="HeFei", end_station="HangZhou", price=12.99)

    # order
    order_1 = Order(user_id=1, sight_id=1, count=1, total=1, note="order_note",
                    create_time=datetime.utcnow())
    order_2 = Order(user_id=1, sight_id=1, count=1, total=9, note="order_note",
                    create_time=datetime.utcnow())
    order_3 = Order(user_id=1, sight_id=2, count=1, total=99, note="order_note",
                    create_time=datetime.utcnow())
    order_4 = Order(user_id=1, hotel_id=1, count=1, total=1, note="order_note",
                    create_time=datetime.utcnow())
    order_5 = Order(user_id=1, hotel_id=1, count=1, total=1, note="order_note",
                    create_time=datetime.utcnow())
    order_6 = Order(user_id=1, hotel_id=2, count=1, total=9, note="order_note",
                    create_time=datetime.utcnow())
    order_7 = Order(user_id=2, sight_id=2, count=1, total=99, note="order_note",
                    create_time=datetime.utcnow())
    order_8 = Order(user_id=2, hotel_id=1, count=1, total=1, note="order_note",
                    create_time=datetime.utcnow())

    # comment
    comment_1 = Comment(content="comment_content", user_id=1, sight_id=1, create_time=datetime.utcnow())
    comment_2 = Comment(content="comment_content", user_id=1, hotel_id=1, create_time=datetime.utcnow())

    # ticket
    ticket_1 = Ticket(user_id=1, station_id=1, count=1, total=12.99, note="ticket_note", create_time=datetime.utcnow())
    ticket_2 = Ticket(user_id=1, station_id=2, count=1, total=12.99, note="ticket_note", create_time=datetime.utcnow())

    db.session.add(user_1)
    db.session.add(user_2)

    db.session.add(sight_1)
    db.session.add(sight_2)

    db.session.add(hotel_1)
    db.session.add(hotel_2)

    db.session.add(station_1)
    db.session.add(station_2)

    db.session.add(order_1)
    db.session.add(order_2)
    db.session.add(order_3)
    db.session.add(order_4)
    db.session.add(order_5)
    db.session.add(order_6)
    db.session.add(order_7)
    db.session.add(order_8)

    db.session.add(comment_1)
    db.session.add(comment_2)

    db.session.add(ticket_1)
    db.session.add(ticket_2)

    db.session.commit()
