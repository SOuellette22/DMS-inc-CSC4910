from flask import Blueprint, render_template, request, flash, redirect, url_for

rate_bp = Blueprint("rate", __name__, template_folder="templates")


@rate_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Safely get form data
        soil_ph = request.form.get("soil_ph")
        soil_drainage = request.form.get("soil_drainage")
        soil_moisture = request.form.get("soil_moisture")
        soil_ec = request.form.get("soil_ec")
        flood_frequency = request.form.get("flood_frequency")
        culvert_material = request.form.get("culvert_material")
        culvert_shape = request.form.get("culvert_shape")
        culvert_length = request.form.get("culvert_length")
        culvert_age = request.form.get("culvert_age")

        # You can keep these flashes for debugging if you want
        flash("Rating submitted properly", "success")

        # ==== PLACEHOLDER MODEL OUTPUTS ====
        # TODO: plug your real model here
        random_rating = 5
        xgb_rating = 5
        overall_rating = 5
        condition_label = "S minus is in very good condition."
        # ===================================

        # Rows for the input table on export_rate.html
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

        return render_template(
            "export_rate.html",
            overall_rating=overall_rating,
            random_rating=random_rating,
            xgb_rating=xgb_rating,
            condition_label=condition_label,
            input_rows=input_rows,
        )

    # GET: just show the form
    return render_template("rate.html")
