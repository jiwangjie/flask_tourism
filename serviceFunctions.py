from utils import login_required
from .extensions import db
from .models import Order, Sight, Hotel, Comment, Ticket, Station, User


def findUserOrdersById(user_id):
    """查询用户的所有订单"""
    data = []
    # 景点订单
    sightOrders = db.session.query(Order, Sight.name, Sight.picture).filter(Order.user_id == user_id). \
        filter(Order.sight_id == Sight.id).all()
    for orderItem in sightOrders:
        jsonItem = orderItem[0].to_json()
        jsonItem["sightName"] = orderItem[1]
        jsonItem["sightPicture"] = orderItem[2]
        data.append(jsonItem)
    # 酒店订单
    hotelOrders = db.session.query(Order, Hotel.name, Hotel.picture).filter(Order.user_id == user_id). \
        filter(Order.hotel_id == Hotel.id).all()
    for hotelOrder in hotelOrders:
        jsonItem = hotelOrder[0].to_json()
        jsonItem["hotelName"] = hotelOrder[1]
        jsonItem["hotelPicture"] = hotelOrder[2]
        data.append(jsonItem)
    return data


def findUserCommentsById(user_id):
    """查询用户的所有评论"""
    data = []
    # 景点评论
    sightComments = db.session.query(Comment, Sight.name, Sight.picture).filter(Comment.user_id == user_id). \
        filter(Comment.sight_id == Sight.id).all()
    for sightComment in sightComments:
        jsonItem = sightComment[0].to_json()
        jsonItem["sightName"] = sightComment[1]
        jsonItem["sightPicture"] = sightComment[2]
        data.append(jsonItem)
    # 酒店评论
    hotelComments = db.session.query(Comment, Hotel.name, Hotel.picture).filter(Comment.user_id == user_id). \
        filter(Comment.hotel_id == Hotel.id).all()
    for hotelComment in hotelComments:
        jsonItem = hotelComment[0].to_json()
        jsonItem["hotelName"] = hotelComment[1]
        jsonItem["hotelPicture"] = hotelComment[2]
        data.append(jsonItem)
    return data


def findUserTicketsById(user_id):
    """查询用户的所有车票"""
    data = []
    # 用户的所有车票
    userTickets = db.session.query(Ticket, Station.start_station, Station.end_station). \
        filter(Ticket.user_id == user_id).filter(Ticket.station_id == Station.id).all()
    for userTicket in userTickets:
        jsonItem = userTicket[0].to_json()
        jsonItem["start_station"] = userTicket[1]
        jsonItem["end_station"] = userTicket[2]
        data.append(jsonItem)
    return data


def findSightOrdersById(sight_id):
    """查询景点的所有订单"""
    data = []
    sightOrders = db.session.query(Order, User.username).filter(Order.sight_id == sight_id). \
        filter(Order.user_id == User.id).all()
    for sightOrder in sightOrders:
        jsonItem = sightOrder[0].to_json()
        jsonItem["username"] = sightOrder[1]
        data.append(jsonItem)
    return data


def findSightCommentsById(sight_id):
    """查询景点的所有评论"""
    data = []
    sightComments = db.session.query(Comment, User.username).filter(Comment.sight_id == sight_id). \
        filter(Comment.user_id == User.id).all()
    for sightComment in sightComments:
        jsonItem = sightComment[0].to_json()
        jsonItem["username"] = sightComment[1]
        data.append(jsonItem)
    return data


def findHotelOrdersById(hotel_id):
    """查询酒店的所有订单"""
    data = []
    hotelOrders = db.session.query(Order, User.username).filter(Order.hotel_id == hotel_id). \
        filter(Order.user_id == User.id).all()
    for hotelOrder in hotelOrders:
        jsonItem = hotelOrder[0].to_json()
        jsonItem["username"] = hotelOrder[1]
        data.append(jsonItem)
    return data


def findHotelCommentsById(hotel_id):
    """查询酒店的所有评论"""
    data = []
    hotelComments = db.session.query(Comment, User.username).filter(Comment.hotel_id == hotel_id). \
        filter(Comment.user_id == User.id).all()
    for hotelComment in hotelComments:
        jsonItem = hotelComment[0].to_json()
        jsonItem["username"] = hotelComment[1]
        data.append(jsonItem)
    return data
