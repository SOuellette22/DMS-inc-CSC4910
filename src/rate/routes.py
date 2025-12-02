from flask import Blueprint, render_template, request, flash, redirect, url_for

# Blueprint for the rating page
# This maps to the "/rate" URL prefix when registered in app.py
rate_bp = Blueprint("rate", __name__, template_folder="templates")


# Helper function that converts a numeric rating into a human-readable label
def describe_condition(score: int) -> str:
    if score >= 5:
        return "S minus is in very good condition."
    elif score == 4:
        return "The culvert is in good condition with minor concerns."
    elif score == 3:
        return "The culvert is in fair condition and should be monitored."
    elif score == 2:
        return "The culvert is in poor condition and maintenance is recommended."
    else:
        return "The culvert is in critical condition and should be evaluated urgently."


# Main route for rating a culvert
# GET  → show the form
# POST → process the form and show the export summary page
@rate_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # -------------------------------
        # 1. Collect all form inputs safely
        # -------------------------------
        soil_ph = request.form.get("soil_ph")
        soil_drainage = request.form.get("soil_drainage")
        soil_moisture = request.form.get("soil_moisture")
        soil_ec = request.form.get("soil_ec")
        flood_frequency = request.form.get("flood_frequency")
        culvert_material = request.form.get("culvert_material")
        culvert_shape = request.form.get("culvert_shape")
        culvert_length = request.form.get("culvert_length")
        culvert_age = request.form.get("culvert_age")

        # Flash message (optional — useful during debugging)
        flash("Rating submitted properly", "success")

        # -------------------------------
        # 2. Placeholder model outputs — replace with ML prediction later
        # -------------------------------
        random_rating = 5
        xgb_rating = 5
        overall_rating = 5

        # Convert the final score into a readable condition description
        condition_label = describe_condition(int(overall_rating))

        # -------------------------------
        # 3. Build a row list for the input table on export_rate.html
        # -------------------------------
        input_rows = [
            ("Soil pH", soil_ph),
            ("Soil drainage class", soil_drainage),
            ("Soil moisture (%)", soil_moisture),
            ("Soil electrical conductivity", soil_ec),
            ("Flood frequency", flood_frequency),
            ("Culvert material", culvert_material),
            ("Culvert shape", culvert_shape),
            ("Culvert length (ft)", culvert_length),
            ("Culvert age (years)", culvert_age),
        ]

        # -------------------------------
        # 4. Render the results page with all computed values
        # -------------------------------
        return render_template(
            "export_rate.html",
            overall_rating=overall_rating,
            random_rating=random_rating,
            xgb_rating=xgb_rating,
            condition_label=condition_label,
            input_rows=input_rows,
        )

    # -------------------------------
    # GET request — simply show the rating form
    # -------------------------------
    return render_template("rate.html")
