from . import api
from flask import request, jsonify, current_app, session
from app.utils.response_code import RET
from app import db
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
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    if not all([name, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="paraments incompleted")

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="Inconsistent secondary password")

    user = User(name=name)
    user.password = password

    db.session.add(user)
    db.session.commit()
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