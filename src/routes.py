from flask import render_template, request, session, redirect, url_for, flash
from authlib.integrations.flask_client import OAuth
from api_key import *

from models import Admin, AIModels

def register_routes(app, db):

    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'},
    )

    # This is the main page
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login")
    def login():
        try:
            authorize_uri = url_for("authorize", _external=True)
            return google.authorize_redirect(redirect_uri=authorize_uri)
        except Exception as e:
            app.logger.error(f"Error during login redirect: {e}")
            return "Error during login redirect.", 500

    @app.route("/authorize")
    def authorize():
        token = google.authorize_access_token()
        user_info = google.server_metadata['userinfo_endpoint']
        resp = google.get(user_info)
        user_info = resp.json()
        email = user_info["email"]

        admin_email = Admin.query.filter_by(email=email).first()
        app.logger.info(f"Admin email: {admin_email}")
        app.logger.info(f"Entered email: {email}")
        if not admin_email:
            flash("Access denied: You are not an admin.", "danger")
            return redirect(url_for("home"))

        session["username"] = email
        session["token"] = token

        flash(f"Welcome, {email}!", "success")
        return redirect(url_for("admin", content=session['username']))

    @app.route("/upload", methods=['GET', 'POST'])
    def upload():
        return render_template("upload.html")

    @app.route("/admin")
    def admin():
        return render_template("admin.html", content = session['username'])

    @app.route("/logout")
    def logout():
        username = session["username"]
        flash(f"You have been logged out, {username}", "info")
        session.pop("username", None)
        session.pop("password", None)
        return redirect(url_for("login"))

    @app.route("/rate", methods=["POST", "GET"])
    def rate():

        if request.method == "POST":
            soil_ph = request.form["soil_ph"]
            soil_drainage = request.form["soil_drainage"]
            soil_moisture = request.form["soil_moisture"]
            soil_ec = request.form["soil_ec"]
            flood_frequency = request.form["flood_frequency"]
            culvert_material = request.form["culvert_material"]
            culvert_shape = request.form["culvert_shape"]
            culvert_length = request.form["culvert_length"]
            culvert_age = request.form["culvert_age"]

            flash(
                f"Rating submitted: Soil PH: {soil_ph}, Soil Drainage: {soil_drainage}, Soil Moisture: {soil_moisture}, Soil EC: {soil_ec}, Flood Frequency: {flood_frequency}, Culvert Material: {culvert_material}, Culvert Shape: {culvert_shape}, Culvert Length: {culvert_length}, Culvert Age: {culvert_age}")
            return redirect(url_for("home"))

        return render_template("rate.html")