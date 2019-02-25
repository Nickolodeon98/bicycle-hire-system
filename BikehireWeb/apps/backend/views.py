from flask import Blueprint

back_bp = Blueprint("backend",__name__,url_prefix='/backend')

@back_bp.route('/')
def index():
    return ''

