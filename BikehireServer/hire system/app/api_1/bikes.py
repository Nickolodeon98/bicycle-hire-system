from . import api
from app.utils.commons import login_required,staff_login_required
from flask import g, current_app, jsonify, request,session
from app.utils.response_code import RET
from app.utils.image_storage import storage
from app.models import Location,Bike,BikeImage,Order
from app import db, constants, redis_store
import json
from datetime import datetime


@api.route("/locations")
def get_location():
    try:
        resp_json = redis_store.get("location")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            current_app.logger.info("hit redis location")
            return resp_json,200,{"Content-Type":"application/json"}
    #get location info from database
    try:
        location_list = Location.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="database error")
    location_dict_list = []
    #convert object to dict
    for location in location_list:
        location_dict_list.append(location.to_dict())

    # convert dict to json
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=location_dict_list)
    resp_json = json.dumps(resp_dict)

    # save data into redis
    try:
        redis_store.setex("location", constants.LOCATION_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}

@api.route("/bikes/info", methods=["POST"])
#@staff_login_required
def save_bike_info():
    """
    bike info from front end
    {
        "location_id":"",
        "title":"",
        "price":"",
        "deposit":"",
        "comment":"",
        "type":"",
    }
    """
    #staff_id = g.staff_id
    bike_data = request.get_json()

    title = bike_data.get("title")
    location_id = bike_data.get("location_id")
    price = bike_data.get("price")
    # check param
    if not all([title, price, location_id, price,]):
        return jsonify(errno=RET.PARAMERR, errmsg="parament not enough")

    # check price
    try:
        price = int(float(price) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="parament error")

    # check location
    try:
        location = Location.query.get(location_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="database error")

    if location is None:
        return jsonify(errno=RET.NODATA, errmsg="location error")
    bike = Bike(
        location_id=location_id,
        title = title,
        price = price,
    )
    try:
        db.session.add(bike)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="save data error")

    # save success
    return jsonify(errno=RET.OK, errmsg="OK", data={"bike_id": bike.id})

@api.route("/bikes/image", methods=["POST"])
#@staff_login_required
def save_bike_image():
    image_file = request.files.get("bike_image")
    bike_id = request.form.get("bike_id")

    if not all([image_file,bike_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="param error")
    # check bike id
    try:
        bike = Bike.query.get(bike_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="db error")

    if bike is None:
        return jsonify(errno=RET.NODATA, errmsg="bike not exist")

    image_data = image_file.read()

    #save image into qiniu storage
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="save failed")

    # save image into database
    bike_image = BikeImage(bike_id=bike_id, url=file_name)
    db.session.add(bike_image)

    if not bike.index_image_url:
        bike.index_image_url = file_name
        db.session.add(bike)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="save error")

    image_url = constants.QINIU_URL_DOMAIN + file_name

    return jsonify(errno=RET.OK, errmsg="OK", data={"image_url": image_url})

@api.route("/bikes/index", methods=["GET"])
def get_bike_index():
    try:
        ret = redis_store.get("home_page_data")
    except Exception as e:
        current_app.logger.error(e)
        ret = None

    if ret:
        current_app.logger.info("hit bike index info redis")
        return '{"errno":0, "errmsg":"OK", "data":%s}' % ret, 200, {"Content-Type": "application/json"}
    else:
        try:
            bikes = Bike.query.order_by(Bike.order_count.desc()).limit(constants.HOME_PAGE_MAX_BIKES)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="query failed")

        if not bikes:
            return jsonify(errno=RET.NODATA, errmsg="no data")

        bikes_list = []
        for bike in bikes:
            # if there is no image, ignore it
            if not bike.index_image_url:
                continue
            bikes_list.append(bike.to_basic_dict())

        json_bikes = json.dumps(bikes_list)  # "[{},{},{}]"
        try:
            redis_store.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_bikes)
        except Exception as e:
            current_app.logger.error(e)

        return '{"errno":0, "errmsg":"OK", "data":%s}' % json_bikes, 200, {"Content-Type": "application/json"}

@api.route("/bikes/<int:bike_id>", methods=["GET"])
def get_bike_detail(bike_id):

    if not bike_id:
        return jsonify(errno=RET.PARAMERR, errmsg="param error")


    try:
        ret = redis_store.get("bike_info_%s" % bike_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None
    if ret:
        current_app.logger.info("hit bike info redis")
        return '{"errno":"0", "errmsg":"OK", "data":{"bike":%s}}' % (ret), \
               200, {"Content-Type": "application/json"}

    try:
        bike = Bike.query.get(bike_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="query failed")

    if not bike:
        return jsonify(errno=RET.NODATA, errmsg="bike not exist")
    try:
        bike_data = bike.to_full_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="data error")

    json_bike = json.dumps(bike_data)
    try:
        redis_store.setex("bike_info_%s" % bike_id, constants.BIKE_DETAIL_REDIS_EXPIRE_SECOND, json_bike)
    except Exception as e:
        current_app.logger.error(e)

    resp = '{"errno":"0", "errmsg":"OK", "data":{"bike":%s}}' % (json_bike), \
           200, {"Content-Type": "application/json"}
    return resp


@api.route("/bikes")
def get_bike_list():
    """GET BIKE LIST FOR SEARCH PAGE"""
    start_date = request.args.get("sd", "")
    end_date = request.args.get("ed", "")
    location_id = request.args.get("lid", "")
    sort_key = request.args.get("sk", "new")  # sort key
    page = request.args.get("p")

    # deal with time data
    try:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date and end_date:
            assert start_date <= end_date
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="data param error")

    # check location id
    if location_id:
        try:
            location = Location.query.get(location_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="location param error")

    # page
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    redis_key = "bike_%s_%s_%s_%s" % (start_date, end_date, location_id, sort_key)
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return resp_json, 200, {"Content-Type": "application/json"}

    # filter list
    filter_params = []

    # \conflict time compared with exited order
    conflict_orders = None

    try:
        if start_date and end_date:
            conflict_orders = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
        elif start_date:
            conflict_orders = Order.query.filter(Order.end_date >= start_date).all()
        elif end_date:
            conflict_orders = Order.query.filter(Order.begin_date <= end_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="database error1")

    if conflict_orders:

        conflict_bike_ids = [order.bike_id for order in conflict_orders]


        if conflict_bike_ids:
            filter_params.append(Bike.id.notin_(conflict_bike_ids))


    if location_id:
        filter_params.append(Bike.location_id == location_id)

    if sort_key == "price-inc":
        bike_query = Bike.query.filter(*filter_params).order_by(Bike.price.asc())
    elif sort_key == "price-des":
        bike_query = Bike.query.filter(*filter_params).order_by(Bike.price.desc())
    else:
        bike_query = Bike.query.filter(*filter_params).order_by(Bike.create_time.desc())

    try:
        page_obj = bike_query.paginate(page=page, per_page=constants.BIKE_LIST_PAGE_CAPACITY, error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="database error2")

    bike_li = page_obj.items
    bikes = []
    for bike in bike_li:
        bikes.append(bike.to_basic_dict())

    total_page = page_obj.pages

    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"total_page": total_page, "bikes": bikes, "current_page": page})
    resp_json = json.dumps(resp_dict)

    if page <= total_page:

        redis_key = "bike_%s_%s_%s_%s" % (start_date, end_date, location_id, sort_key)

        try:
            # redis_store.hset(redis_key, page, resp_json)
            # redis_store.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

            pipeline = redis_store.pipeline()

            pipeline.multi()

            pipeline.hset(redis_key, page, resp_json)
            pipeline.expire(redis_key, constants.BIKE_LIST_PAGE_REDIS_CACHE_EXPIRES)

            pipeline.execute()
        except Exception as e:
            current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}