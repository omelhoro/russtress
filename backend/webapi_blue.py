from flask import Flask, Blueprint, render_template, request
from setstress import setup_stress

import json

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator

def setup_rs(cl=None):
    if cl == Flask:
        simple_page = Flask(__name__)
        homeroute = "/"
    else:
        simple_page = Blueprint("rust",__name__, static_folder='static',template_folder='templates')
        homeroute = "/rustress"

    @simple_page.route('/<path:path>')
    def rustress(path):
        return simple_page.send_static_file(path)

    @simple_page.route(homeroute)
    def rustressIndex():
        return simple_page.send_static_file("index.html")

    try:
        set_stress, pm = setup_stress("./rustress/dict_data")
    except (IOError):
        try:
            set_stress, pm = setup_stress("./dict_data")
        except (IOError):
            set_stress, pm = setup_stress("./mysite/rustress/dict_data")

    @simple_page.route("/stress", methods = ["POST", "OPTIONS"])
    @crossdomain(origin="*", headers=['Content-Type'])
    def stress():
        data = request.data.decode("utf8")
        jsn = json.loads(data)["words"]
        # print("Request", jsn)
        out = json.dumps({k: list(set_stress(pm, k)) for k in jsn})
        # print(out)
        return out

    return simple_page

if __name__ == "__main__":
    app = setup_rs(Flask)
    # CORS(app, resources={r"/stress/": {"origins": "*"}})
    #app.debug = True
    app.run(host='0.0.0.0', port=5001)
