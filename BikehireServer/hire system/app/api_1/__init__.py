from flask import Blueprint

#create blueprint object

api = Blueprint("api_1",__name__)


from . import demo, passport,bikes,orders