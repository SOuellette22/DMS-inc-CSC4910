from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from authlib.integrations.flask_client import OAuth
from api_key import *
import pandas as pd

from ..models import Admin, AIModels

admin_bp = Blueprint('admin', __name__, template_folder='templates')
oauth = OAuth(current_app)

@admin_bp.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("admin.login"))
    else:
        return render_template("admin.html", content = session['username'])

@admin_bp.route("/login")
def login():
    if "username" in session:
        return redirect(url_for("admin.index"))

    google = oauth.register(
        name='google',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'},
    )
    try:
        authorize_uri = url_for("admin.authorize", _external=True)
        return google.authorize_redirect(redirect_uri=authorize_uri)
    except Exception as e:
        current_app.logger.error(f"Error during login redirect: {e}")
        return "Error during login redirect.", 500

@admin_bp.route("/login/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.server_metadata['userinfo_endpoint']
    resp = oauth.google.get(user_info)
    user_info = resp.json()
    email = user_info["email"]

    admin_email = Admin.query.filter_by(email=email).first()
    if not admin_email:
        flash("Access denied: You are not an admin.", "danger")
        return redirect(url_for("core.home"))

    session["username"] = email
    session["token"] = token

    flash(f"Welcome, {email}!", "success")
    return redirect(url_for("admin.index", content=session['username']))

@admin_bp.route("/upload", methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']

        if file.content_type == 'text/csv':
            df = pd.read_csv(file)

            return df.to_html()
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")
            return redirect(url_for("admin.upload"))

    return render_template("upload.html")

@admin_bp.route("/logout")
def logout():
    username = session["username"]
    flash(f"You have been logged out, {username}", "info")
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("core.home"))