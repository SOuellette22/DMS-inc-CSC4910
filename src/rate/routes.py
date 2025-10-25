from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..models import AIModels

rate_bp = Blueprint("rate", __name__, template_folder="templates")

@rate_bp.route("/", methods=["POST", "GET"])
def index():
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