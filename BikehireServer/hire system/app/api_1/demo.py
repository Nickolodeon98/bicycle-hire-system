from . import api
from app import db,models
import os
from flask import current_app

@api.route("/index")
def index():
    print (os.getcwd()+"\\"+str(18)+".png")
    return "index page"