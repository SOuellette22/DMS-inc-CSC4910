from flask import Blueprint, render_template

core_bp = Blueprint('core', __name__, template_folder='templates')

# This is the main page
@core_bp.route("/")
def home():
    return render_template("index.html")

@core_bp.route("/why")
def why():
    return render_template("why.html")

@core_bp.route("/info")
def info():
    return render_template("info.html")

@core_bp.route("/conversions")
def conversions():
    return render_template("conversions.html")