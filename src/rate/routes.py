import os.path
import pickle

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from src.admin.functions import process_dataset
import pandas as pd
from src.models import AIModels

# Blueprint for the rating page
# This maps to the "/rate" URL prefix when registered in app.py
rate_bp = Blueprint("rate", __name__, template_folder="templates")

soilDrainageOptions = [
    "Excessively drained",
    "Somewhat excessively drained",
    "Well drained",
    "Moderately well drained",
    "High",
    "Somewhat poorly drained",
    "Poorly drained",
    "Very poorly drained",
]

culvertMaterialOptions = [
    "Aluminum",
    "Corrugated Steel",
    "High Density Polyethylene",
    "Poly Vinyl Chloride",
    "Steel Plate",
    "Steel plate",
    "Reinforced Concrete",
    "Unreinforced Concrete",
]

culvertShapeOptions = [
    "Arch",
    "Round",
    "Ellipse/Squashed",
    "Box",
    "Other",
]

floodFrequencyOptions = [
    "No",
    "very rare",
    "rare",
    "Occasional",
    "Frequent",
]

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

        # This checks to make sure that all fields are filled and valid
        if not (soil_ph and
                soil_drainage and
                soil_moisture and
                soil_ec and
                flood_frequency and
                culvert_material and
                culvert_shape and
                culvert_length and
                culvert_age):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("rate.index"))

        # Basic validation of numeric fields and option selections
        try:
            soil_ph = float(soil_ph)
            soil_moisture = float(soil_moisture)
            soil_ec = float(soil_ec)
            culvert_length = float(culvert_length)
            culvert_age = int(culvert_age)

            if soil_drainage not in soilDrainageOptions:
                raise ValueError("Invalid soil drainage option.")
            if flood_frequency not in floodFrequencyOptions:
                raise ValueError("Invalid flood frequency option.")
            if culvert_material not in culvertMaterialOptions:
                raise ValueError("Invalid culvert material option.")
            if culvert_shape not in culvertShapeOptions:
                raise ValueError("Invalid culvert shape option.")
        except ValueError as e:
            flash(f"Invalid input: {e}", "danger")
            return redirect(url_for("rate.index"))

        # Flash message (optional — useful during debugging)
        flash("Rating Submitted Properly", "success")

        # Process the inputs into the necessary format for the ML model
        df = pd.DataFrame([{
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moisture,
            "Soil_Elec_Conductivity": soil_ec,
            "length": culvert_length,
            "Age": culvert_age,
        }])

        # Map soil drainage to numerical values
        match soil_drainage:
            case 'Very poorly drained':
                df['Soil_Drainage_Class'] = 0
            case 'Poorly drained':
                df['Soil_Drainage_Class'] = 1
            case 'Somewhat poorly drained':
                df['Soil_Drainage_Class'] = 2
            case 'Moderately well drained':
                df['Soil_Drainage_Class'] = 3
            case 'Well drained':
                df['Soil_Drainage_Class'] = 4
            case 'High':
                df['Soil_Drainage_Class'] = 5
            case 'Somewhat excessively drained':
                df['Soil_Drainage_Class'] = 6
            case 'Excessively drained':
                df['Soil_Drainage_Class'] = 7

        # Map flood frequency tonumerical values
        match flood_frequency:
            case 'No':
                df['Flooding_Frequency'] = 0
            case 'very rare':
                df['Flooding_Frequency'] = 1
            case 'rare':
                df['Flooding_Frequency'] = 2
            case 'Occasional':
                df['Flooding_Frequency'] = 3
            case 'Frequent':
                df['Flooding_Frequency'] = 4

        # Create one-hot encodingfor culvert material
        for material in culvertMaterialOptions:
            col_name = f"mat_{material}"
            df[col_name] = 1 if culvert_material == material else 0

        # Create one-hot encoding for culvert shape
        for shape in culvertShapeOptions:
            col_name = f"type_{shape}"
            df[col_name] = 1 if culvert_shape == shape else 0

        # Order the columns alphabetically
        columns = [col for col in df.columns ]
        columns.sort()
        df = df[columns]

        ml_list = []

        # Puts all the variables into a dataframe with there column names
        for model in AIModels.query.all():
            model_path = current_app.instance_path + "/current" + model.file_path
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    ml_model = pickle.load(f)
                    prediction = ml_model.predict(df)
                    ml_list.append([model.model_name, prediction[0]])



        # -------------------------------
        # 2. Calculate the overall rating by averaging all model predictions
        # -------------------------------
        overall_rating = 0
        for ml in ml_list:
            overall_rating += ml[1]
        overall_rating = overall_rating / len(ml_list)

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
            ml_list=ml_list,
            condition_label=condition_label,
            input_rows=input_rows,
        )

    # -------------------------------
    # GET request — simply show the rating form
    # -------------------------------
    return render_template("rate.html")
