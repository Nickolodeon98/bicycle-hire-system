from . import api
from flask import request, jsonify, current_app, session
from app.utils.response_code import RET
from app import db,constants,redis_store
from app.models import User
from sqlalchemy.exc import IntegrityError


@api.route("/users", methods=["POST"])
def register():
    """
    register
    :param
    name password password2 {JSON}
    :returns
    dict
    """
    req_dict = request.get_json()

    name = req_dict.get("name")
    email = req_dict.get("email")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    if not all([name,email, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="missing parameters")

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="password not match")

    user = User(name=name,email=email)
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="name exited")

    session["name"] = name
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="register success")

@api.route("/sessions", methods=["POST"])
def login():
    req_dict = request.get_json()
    name = req_dict.get("name")
    password = req_dict.get("password")

    if not all([name, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="missing parameters ")
        # check the number of error
        user_ip = request.remote_addr
        try:
            access_nums = redis_store.get("access_num_%s" % user_ip)
        except Exception as e:
            current_app.logger.error(e)
        else:
            if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
                return jsonify(errno=RET.REQERR, errmsg="over login error times")

    try:
        user = User.query.filter_by(name=name).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="get user data failed")

        # check password with database
    if user is None or not user.check_password(password):

        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg="name or password incorrect")
     # login success
    session["name"] = user.name
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="login success")

@api.route("/session",methods = ["GET"])
def check_login():
    name = session.get("name")
    if name is not None:
        return jsonify(error=RET.OK,errmsy="true",data={"name":name})
    else:
        return jsonify(errno=RET.SESSIONERR,errmsg="false")

@api.route("/session",methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(errno=RET.OK,errmsg="OK")