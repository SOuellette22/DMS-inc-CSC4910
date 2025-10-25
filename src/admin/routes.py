# Imports needed for admin routes
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from authlib.integrations.flask_client import OAuth
from api_key import *
import pandas as pd

# Import models
from models import Admin, AIModels

# Define the admin blueprint and OAuth
admin_bp = Blueprint('admin', __name__, template_folder='templates')
oauth = OAuth(current_app)

# Register Google OAuth client
google = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

# Admin index route
@admin_bp.route("/")
def index():
    # Check if user is logged in
    if "username" not in session:
        # If not logged in, redirect to login page
        return redirect(url_for("admin.login"))
    else:
        # If logged in, render the admin dashboard
        return render_template("admin.html", content = session['username'])

@admin_bp.route("/login")
def login():
    # If already logged in, redirect to admin index
    if "username" in session:
        return redirect(url_for("admin.index"))

    # Initiate Google OAuth login
    try:
        authorize_uri = url_for("admin.authorize", _external=True)
        return google.authorize_redirect(redirect_uri=authorize_uri)
    except Exception as e:
        current_app.logger.error(f"Error during login redirect: {e}")
        return "Error during login redirect.", 500

# OAuth2 callback route
@admin_bp.route("/login/authorize")
def authorize():
    # Complete the OAuth2 authorization process
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.server_metadata['userinfo_endpoint']
    resp = oauth.google.get(user_info)
    user_info = resp.json()
    email = user_info["email"]

    # Check if the user is an admin
    admin_email = Admin.query.filter_by(email=email).first()
    if not admin_email:
        # If not an admin, deny access
        flash("Access denied: You are not an admin.", "danger")
        return redirect(url_for("core.home"))

    # Store user info in session
    session["username"] = email
    session["token"] = token

    # Welcome the admin user
    flash(f"Welcome, {email}!", "success")
    return redirect(url_for("admin.index", content=session['username']))

@admin_bp.route("/upload", methods=['GET', 'POST'])
def upload():
    # Checks in the message type is POST
    if request.method == 'POST':
        # Check if a file is part of the request
        file = request.files.get('file')

        # If file is not a CSV, flash an error message
        if file.content_type == 'text/csv':
            df = pd.read_csv(file)

            return df.to_html()
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")
            return redirect(url_for("admin.upload"))

    return render_template("upload.html")

@admin_bp.route("/logout")
def logout():
    # Log out the user by clearing the session
    username = session["username"]
    flash(f"You have been logged out, {username}", "info")
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("core.home"))