from flask import Blueprint, render_template

core_bp = Blueprint('core', __name__, template_folder='templates')

# This is the main page
@core_bp.route("/")
def home():
    return render_template("index.html")