# Imports needed for admin routes
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from authlib.integrations.flask_client import OAuth
from api_key import *
import pandas as pd

# Import models
from models import Admin, AIModels
from admin.functions import *

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
        return render_template("admin.html")

# Admin POST route to handle form submissions
@admin_bp.route("/", methods=['POST'])
def admin_post():
    correct_column_list = ['latitude', 'longitude', 'length',
                           'cul_matl', 'cul_type', 'Soil_Drainage_Class',
                           'Soil_Moisture', 'Soil_pH', 'Soil_Elec_Conductivity',
                           'Soil_Surface_Texture','Flooding_Frequency',
                           'State', 'Age', 'Cul_rating']

    # Handles the preview of the dataset
    if "dataset-preview" in request.form:
        file = request.files.get('file') # saves the file uploaded

        # Checks to make sure that the file is a CSV
        if file and file.content_type == 'text/csv':
            # Reads the CSV into a DataFrame, generates a preview, and counts the number of rows
            df = pd.read_csv(file)
            preview_html = df.head().to_html()
            num_rows = len(df)

            # Checks if the columns are correct and sets the flag accordingly
            flag = True
            for col in correct_column_list:
                if col not in df.columns.to_list():
                    flag = False
                    break

            # Checks if the columns are correct and generates the appropriate message
            correct_csv = "<p style='color: red; margin-bottom: 2px; margin-top: -10px'>This dataset looks to not have the right columns</p>"
            if flag:
                correct_csv = "<p style='color: green; margin-bottom: 2px; margin-top: -10px'>This dataset looks to have the right columns</p>"

            # returns the CSS styling along with the preview HTML into the IFrame
            return css_for_table() + f"<p style='color: white;'>The Number of Rows: {num_rows}</p>" + correct_csv + preview_html

    # Handles dataset swapping
    elif "dataset-swap" in request.form:
        file = request.files.get('file')

        # Checks to make sure that the file is a CSV
        if file and file.content_type == 'text/csv':
            df = pd.read_csv(file)

            # Checks if the columns are correct and sets the flag accordingly
            flag = True
            for col in correct_column_list:
                if col not in df.columns.to_list():
                    flag = False
                    break

            # If columns are incorrect, flash an error message and redirect
            if not flag:
                flash("The uploaded dataset does not have the correct columns.", "danger")
                return redirect(url_for("admin.index"))

            # TODO: Implement dataset swapping logic here
            # Todo: write a function to do this since it will be a lot easier to manage later on

            flash("Dataset swapped successfully.", "success")
            return redirect(url_for("admin.index"))

    flash("No valid action specified.", "danger")

    return redirect(url_for("admin.index"))

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
    if not Admin.query.filter_by(email=email).first():
        # If not an admin, deny access
        flash("Access denied: You are not an admin.", "danger")
        return redirect(url_for("core.home"))

    # Store user info in session
    session["username"] = email
    session["token"] = token

    # Welcome the admin user
    flash(f"Welcome, {email}!", "success")
    return redirect(url_for("admin.index"))

@admin_bp.route("/logout")
def logout():
    # Log out the user by clearing the session
    username = session["username"]
    flash(f"You have been logged out, {username}", "info")
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("core.home"))