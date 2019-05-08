from werkzeug.routing import BaseConverter
from flask import session, jsonify,g
from app.utils.response_code import RET
import functools
# Custom regular expression converter
class ReConverter(BaseConverter):
    """"""
    def __init__(self, url_map, regex):
        super(ReConverter, self).__init__(url_map)
        self.regex = regex

def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args,**kwargs):
        # check user whether login
        user_id = session.get("user_id")
        if user_id is not None:
            #save id in object g for view func using
            g.user_id = user_id
            return view_func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR,errmsg="user not login")
    return wrapper

def staff_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args,**kwargs):
        # check user whether login
        staff_id = session.get("staff_id")
        if staff_id is not None:
            #save id in object g for view func using
            g.staff_id = staff_id
            return view_func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR,errmsg="staff not login")
    return wrapper


import json
import  datetime

class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return  json.JSONEncoder.default(self,obj)
