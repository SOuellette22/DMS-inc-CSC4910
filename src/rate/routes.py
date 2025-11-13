from flask import Blueprint, render_template, request, flash, redirect, url_for

rate_bp = Blueprint("rate", __name__, template_folder="templates")

@rate_bp.route("/", methods=["POST", "GET"])
def index():
    # Handle form submission
    if request.method == "POST":
        # Get form data
        soil_ph = request.form["soil_ph"]
        soil_drainage = request.form["soil_drainage"]
        soil_moisture = request.form["soil_moisture"]
        soil_ec = request.form["soil_ec"]
        flood_frequency = request.form["flood_frequency"]
        culvert_material = request.form["culvert_material"]
        culvert_shape = request.form["culvert_shape"]
        culvert_length = request.form["culvert_length"]
        culvert_age = request.form["culvert_age"]
        

        # TODO: David this is where you will process the data and output it to the user
        flash(f"Rating Submitted Properly", "success")
        flash(f"Soil pH: {soil_ph}", "info")
        flash(f"Soil Drainage: {soil_drainage}", "info")
        flash(f"Soil Moisture: {soil_moisture}", "info")
        flash(f"Soil Eclectic Conductivity: {soil_ec}", "info")
        flash(f"Flood Frequency: {flood_frequency}", "info")
        flash(f"Culvert Material: {culvert_material}", "info")
        flash(f"Culvert Shape: {culvert_shape}", "info")
        flash(f"Culvert Length: {culvert_length}", "info")
        flash(f"Culvert Age: {culvert_age}", "info")

        return redirect(url_for("core.home")) # TODO: Change this to the results page when available

    return render_template("rate.html")