import datetime

from flask import request, g, jsonify, current_app,render_template,session
from app import db, redis_store,mail,constants
from app.utils.commons import login_required,DateEncoder
from app.utils.response_code import RET
from app.models import Bike, Order,Location
from . import api
from flask_mail import Message,Mail
from threading import Thread
from MyQR import myqr
import os, json
from PIL import Image
from email.mime.image import MIMEImage
# @api.route("/orders/qrcode/", methods=["GET"])
def qrcode(order):
    version, level, qr_name = myqr.run(
        str(order.id),
        version=10,
        level='H',
        picture=os.getcwd()+"\logo.png",
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(order.id)+".png",
        save_dir=os.getcwd()
    )

# @api.route("/orders/email/", methods=["GET"])
# def email():
def email(order):
    qrcode(order)
    recipe = {"id":order.id,"start_date":order.begin_date,"end_date":order.end_date,"days":order.days,"price":order.bike_price,"amount":order.amount,"name":order.bike.title}
    msg = Message("Hi!This is your recipe of bike ",recipients=[order.user.email])
    msg.body = 'Thank you for choosing our bike\n\n Your order id is{id}\nOrder detail:\nbike name:{name}\nprice:{price}/per day\nStart date:{start_date}\tEnd date:{end_date}\ntotal days:{days} days\ntotal price:{amount}'.format(**recipe)
    msg.html = render_template('email.html',order=order,img='cid:image')

    from manage import app
    with app.open_resource(os.getcwd()+"\\"+str(order.id)+".png") as f:
        msg.attach('QRcode.png', "image/png", f.read(), 'inline', headers=[('Content-ID', 'image')])
    thread = Thread(target=send_async_email,args=[app,msg])
    thread.start()
    f.close()
    return "success"

    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="get data failed")

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

@api.route("/orders/<int:order_id>", methods=["GET"])
def get_order_detail(order_id):
    if not order_id:
        return jsonify(errno=RET.PARAMERR, errmsg="param error")

    try:
        ret = redis_store.get("order_info_%s" % order_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None
    if ret:
        current_app.logger.info("hit order info redis")
        return '{"errno":"0", "errmsg":"OK", "data":{"order":%s}}' % (ret), \
               200, {"Content-Type": "application/json"}

    try:
        order = Order.query.get(order_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="query failed")

    if not order:
        return jsonify(errno=RET.NODATA, errmsg="order not exist")
    try:
        order_data = order.to_full_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="data error")

    json_order = json.dumps(order_data,cls=DateEncoder)
    try:
        redis_store.setex("order_info_%s" % order, constants.BIKE_DETAIL_REDIS_EXPIRE_SECOND, json_order)
    except Exception as e:
        current_app.logger.error(e)

    resp = '{"errno":"0", "errmsg":"OK", "data":{"order":%s}}' % (json_order), \
           200, {"Content-Type": "application/json"}
    return resp



@api.route("/orders", methods=["POST"])
def save_order():
    """save order"""
    # user_id = g.user_id
    user_id = 1

    # get param
    order_data = request.get_json()
    if not order_data:
        return jsonify(errno=RET.PARAMERR, errmsg="param error")

    bike_id = order_data.get("bike_id")
    start_date_str = order_data.get("start_date")
    end_date_str = order_data.get("end_date")

    # check param
    if not all((bike_id, start_date_str, end_date_str)):
        return jsonify(errno=RET.PARAMERR, errmsg="param error")

    # check data format
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        assert start_date <= end_date

        days = (end_date - start_date).days + 1  # datetime.timedelta
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="data format error")

    # check if bike exist
    try:
        bike = Bike.query.get(bike_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="get data failed")
    if not bike:
        return jsonify(errno=RET.NODATA, errmsg="bike not exist")

    # filter available bike
    try:
        # query existed order
        count = Order.query.filter(Order.bike_id == bike_id, Order.begin_date <= end_date,
                                   Order.end_date >= start_date).count()
        #  select count(*) from order where ....
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="")
    if count > 0:
        return jsonify(errno=RET.DATAERR, errmsg="bike have been book")

    # total price
    amount = days * bike.price

    # save data
    order = Order(
        bike_id=bike_id,
        user_id=user_id,
        begin_date=start_date,
        end_date=end_date,
        days=days,
        bike_price=bike.price,
        amount=amount
    )
    try:
        db.session.add(order)
        db.session.commit()
        email(order)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="save failed")
    return jsonify(errno=RET.OK, errmsg="OK", data={"order_id": order.id})

@api.route("/user/orders", methods=["GET"])
def get_user_orders():
    user_id = request.args.get("user_id")
    try:
        orders = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc()).all()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="query error")

    orders_dict_list = []
    if orders:
        for order in orders:
            orders_dict_list.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg="OK", data={"orders": orders_dict_list})


@api.route("/user/orders", methods=["PUT"])
def pickup_return():
    order_id= request.args.get("order_id")

    # get param
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="param error")


    action = req_data.get("action")
    if action not in ("pickup", "return","cancel"):
        return jsonify(errno=RET.PARAMERR, errmsg="param error")

    try:
        order = Order.query.filter(Order.id == order_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="query order failed")
    if action == "pickup":
        order.status = "PICKED"
        try:
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(errno=RET.DBERR, errmsg="commit failed")
    if action == "return":
        order.status = "COMPLETED"
        try:
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(errno=RET.DBERR, errmsg="commit failed")
    if action == "cancel":
        try:
            db.session.delete(order)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(errno=RET.DBERR, errmsg="commit failed")
    return jsonify(errno=RET.OK, errmsg="OK")



@api.route("locations/orders/income", methods=["GET"])
def order_income():
    start_date = request.args.get("sd", "")
    end_date = request.args.get("ed", "")

    try:
        if start_date and end_date:
            assert start_date <= end_date
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="data param error")

    redis_key = "location_orders_income_%s_%s" % (start_date, end_date)
    try:
        resp_json = redis_store.hget(redis_key)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return resp_json, 200, {"Content-Type": "application/json"}

    locations = Location.query.all()
    income_list=[]
    overall = 0
    for location in locations:
        income = 0
        orders = Order.query.join(Bike).filter(Bike.location_id == location.id).all()
        for order in orders:
            income = income + order.amount
        income_dict = {"location_id": location.id, "location_name": location.name, "order_income": income}
        income_list.append(income_dict)
        overall = overall+income

    resp_dict = dict(errno=RET.OK, errmsg="OK",data={"overall": overall, "income_list": income_list})
    resp_json = json.dumps(resp_dict, cls=DateEncoder)

    try:
        redis_store.setex("location_orders_amount_%s_%s" % (start_date, end_date),
                          constants.LOCATION_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}


@api.route("locations/orders/amount", methods=["GET"])
def order_amount():
    start_date = request.args.get("sd", "")
    end_date = request.args.get("ed", "")

    try:
        if start_date and end_date:
            assert start_date <= end_date
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="data param error")

    redis_key = "location_orders_amount_%s_%s"% (start_date, end_date)
    try:
        resp_json = redis_store.hget(redis_key)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return resp_json, 200, {"Content-Type": "application/json"}

    locations = Location.query.all()
    amount_list=[]
    for location in locations:
        amount = Order.query.join(Bike).filter(Bike.location_id == location.id).count()
        # amount = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date, order.bike.location_id==location.id).count()
        amount_dict = {"location_id":location.id,"location_name":location.name,"order_amount": amount}
        amount_list.append(amount_dict)

    resp_dict = dict(errno=RET.OK, errmsg="OK", data=amount_list)
    resp_json = json.dumps(resp_dict,cls=DateEncoder)

    try:
        redis_store.setex("location_orders_amount_%s_%s"% (start_date, end_date), constants.LOCATION_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}

