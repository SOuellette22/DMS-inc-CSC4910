# Imports needed for admin routes
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app, jsonify
from authlib.integrations.flask_client import OAuth

from src.api_key import *
from sklearn.model_selection import train_test_split

# Import models
from src.app import db
from src.models import Admin, AIModels
from src.admin.functions import *

from datetime import datetime

# Define the correct columns for the dataset
correct_column_list = ['latitude', 'longitude', 'length',
                       'cul_matl', 'cul_type', 'Soil_Drainage_Class',
                       'Soil_Moisture', 'Soil_pH', 'Soil_Elec_Conductivity',
                       'Soil_Surface_Texture','Flooding_Frequency',
                       'State', 'Age', 'Cul_rating']

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
    if "username" in session:

        username = session["username"]

        if not Admin.query.filter_by(email=username).first():
            # If not an admin, log out and redirect to home
            flash("Access denied: You are not an admin.", "danger")
            session.pop("username", None)

            current_app.logger.error("Non-admin user had session active, logging out. Email: %s", username)

            return redirect(url_for("core.home"))

        # If not logged in, redirect to login page
        return render_template("admin.html")
    else:
        # If logged in, render the admin dashboard
        return redirect(url_for("admin.login"))

# Admin POST route to handle form submissions
@admin_bp.route("/", methods=['POST'])
def admin_post():

    if not "username" in session:

        # If not an admin, log out and redirect to home
        flash("Access denied: You are not an admin.", "danger")

        return redirect(url_for("core.home"))

    username = session["username"]

    if not Admin.query.filter_by(email=username).first():
        # If not an admin, log out and redirect to home
        flash("Access denied: You are not an admin.", "danger")
        session.pop("username", None)

        current_app.logger.error("Non-admin user had session active, logging out. Email: %s", username)

        return redirect(url_for("core.home"))

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
            return css_for_table() + f"<p style='color: black;'>The Number of Rows: {num_rows}</p>" + correct_csv + preview_html

    # Handles dataset swapping
    elif "dataset-swap" in request.form:

        db_path = current_app.instance_path

        string = save_models(db_path) # Saves the current models before swapping datasets

        # Checks if the models were saved successfully
        if string != "Models saved":
            flash("Error saving models before dataset swap.", "danger")
            return redirect(url_for("admin.index"))

        # Updates the date_updated and updated_by fields for all AI models
        for model in AIModels.query.all():
            model.date_updated = datetime.now()
            model.updated_by = session["username"]

            db.session.commit()

        # The dataset swap process was completed successfully
        flash("Dataset swapped successfully.", "success")
        return redirect(url_for("admin.index"))

    elif "modelConfirm" in request.form:

        temp = request.form.get("model_name")

        # This makes it so that the file path is formatted correctly
        path = "/"
        tempSlit = temp.split(" ")
        for i in range(len(tempSlit)):
            if i == 0:
                path += tempSlit[i].lower()
            else:
                path += tempSlit[i]
                if i != len(tempSlit) - 1:
                    path += ""
                    
        # Gets the model details from the form
        model_name = request.form.get("model_name")
        file_path = path + ".pkl"
        admin_email = session["username"]
        description = request.form.get("description")

        # Creates a new AI model entry in the database
        new_model = AIModels(model_name, file_path, admin_email, description)
        db.session.add(new_model)
        db.session.commit()

        return redirect(url_for("admin.index"))

    flash("No valid action specified.", "danger")

    return redirect(url_for("admin.index"))

@admin_bp.route("/test_training", methods=['POST'])
def test_training():

    if not "username" in session:

        # If not an admin, log out and redirect to home
        flash("Access denied: You are not an admin.", "danger")

        return redirect(url_for("core.home"))

    username = session["username"]

    if not Admin.query.filter_by(email=username).first():
        # If not an admin, log out and redirect to home
        flash("Access denied: You are not an admin.", "danger")
        session.pop("username", None)

        current_app.logger.error("Non-admin user had session active, logging out. Email: %s", username)

        return redirect(url_for("core.home"))

    # This route is for testing purposes to evaluate model accuracy
    file = request.files.get('file')

    string = "Accuracy Results:\n" # Initialize the string to hold accuracy results

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
            return jsonify("Error: Incorrect columns in dataset.")

        # Process the dataset and create training and testing splits
        processed_df = process_dataset(df)

        # Gets the features and labels from the processed dataframe
        dataset_label = processed_df['Cul_rating']
        dataset_features = processed_df.drop(columns=['Cul_rating'], axis=1)

        # Creates the training and testing splits
        X_train, X_test, y_train, y_test = train_test_split(
            dataset_features, dataset_label, test_size=0.2, random_state=42
        )

        db_path = current_app.instance_path

        # Update all AI models with the new dataset splits
        ai_models = AIModels.query.all()
        for model in ai_models:
            # Gets the path to the model dataset file
            path = model.file_path

            flag = train_model(model.model_name, path, db_path, X_train, X_test, y_train, y_test)  # Train the model and saves them

            string += f"{model.model_name}: {flag}\n" # Append the accuracy result to the string

    return jsonify(string) # Return the accuracy results as JSON


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
    if "username" not in session:
        return redirect(url_for("core.home"))

    username = session["username"]
    flash(f"You have been logged out, {username}", "info")
    session.pop("username", None)
    return redirect(url_for("core.home"))