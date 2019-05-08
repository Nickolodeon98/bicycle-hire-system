from flask import Blueprint, current_app, make_response
from flask_wtf import csrf

html = Blueprint("web_html", __name__)

@html.route("/Forstaff/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """offer html file"""
    # if file name is "" that means index
    if not html_file_name:
        html_file_name = "index.html"

    # if not favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name =  "html/"+html_file_name

    # create csrf token
    csrf_token = csrf.generate_csrf()

    # back static file
    resp = make_response(current_app.send_static_file(html_file_name))

    # set csrf to cookie
    resp.set_cookie("csrf_token", csrf_token)

    return resp