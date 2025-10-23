from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
# TODO THIS STUFF NEEDS TO GO IN A CONFIG FILE
app.secret_key = "test" # TODO THIS NEEDS TO CHANGE
app.permanent_session_lifetime = timedelta(hours=1)

# This is the main page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods = ["POST", "GET"])
def login():
    # this checks to see if the HTTP message type is POST
    if request.method == "POST":
        # gets the password and username entered
        password = request.form["password"]
        username = request.form["username"]
        
        # checks if the entered password is correct
        if password != "password":
            return render_template("login.html")
        else:
            session["username"] = username
            session.permanent = True
            flash("Login successful!")
            return redirect(url_for("admin", usr = username))
    else: 
        if "username" in session:
            username = session["username"]
            session.permanent = True
            flash("Already Logged In!")
            return redirect(url_for("admin", usr = username))
        
        return render_template("login.html")
    

@app.route("/admin")
def admin():
    # This is a check to see if the user has logged in yet
    if "username" in session:
        return render_template("user.html", content = session["username"])
    
    # if they are not logged in
    flash("You are not logged in!")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    username = session["username"]
    flash(f"You have been logged out, {username}", "info")
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("login"))


@app.route("/rate", methods = ["POST", "GET"])
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
        
        flash(f"Rating submitted: Soil PH: {soil_ph}, Soil Drainage: {soil_drainage}, Soil Moisture: {soil_moisture}, Soil EC: {soil_ec}, Flood Frequency: {flood_frequency}, Culvert Material: {culvert_material}, Culvert Shape: {culvert_shape}, Culvert Length: {culvert_length}, Culvert Age: {culvert_age}")
        return redirect(url_for("home"))
    
    return render_template("rate.html")

if __name__ == "__main__":
    app.run(debug = True)