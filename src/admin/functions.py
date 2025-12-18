import pandas as pd
import os
from datetime import datetime

from sklearn.metrics import accuracy_score


def css_for_table():
    '''
    This function will return the CSS styling for the table that is used to preview the dataset
    :return: The CSS styling for the table
    '''
    css = """
    <style type="text/css" media="screen" style="width:100%">
        table, th, td {
            background-color: #FFFFFF;
            padding: 10px;
        }
        th {
            background-color: #0; 
            shadow: 0 10px 30px rgba(0, 0, 0, 0.35); 
            color: black; 
            font-family: Tahoma;
            font-size : 13; 
            text-align: center;
        }
        td {
            background-color: #0; 
            shadow:0 10px 30px rgba(0, 0, 0, 0.35); 
            color: black; 
            padding: 10px; 
            font-family: Calibri; 
            font-size : 12; 
            text-align: center;
        }
    </style>
    """
    return css

def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function will process the dataset into the form that is needed to train the models and create a training and testing split
    :param df: This is the dataframe that is to be processed
    :return: This is the new processed dataframe
    '''
    # Preprocess the dataset by dropping rows with any missing values and removing unnecessary columns
    new_df = df.copy().dropna(axis=0)
    new_df.drop(columns=['latitude', 'longitude','State','Soil_Surface_Texture'], axis=1, inplace=True)
    new_df = new_df.fillna(new_df.mode().iloc[0])

    # This makes sure that the Cul_rating column is of type integer
    new_df = new_df[new_df.Cul_rating != "Unknown"]
    new_df["Cul_rating"] = new_df["Cul_rating"].astype(int)

    # This converts the cul_type column into one hot encoded columns
    new_df = new_df[new_df.cul_type != "UNKNOWN"]
    new_df_temp = pd.get_dummies(new_df["cul_type"], prefix='type')
    new_df = pd.merge(left=new_df, right=new_df_temp, left_index=True, right_index=True)
    new_df.drop(["cul_type"], axis=1, inplace=True)

    # This converts the cul_matl column into one hot encoded columns
    new_df = new_df[new_df.cul_matl != "UNKNOWN"]
    new_df_temp = pd.get_dummies(new_df["cul_matl"], prefix='mat')
    new_df = pd.merge(left=new_df, right=new_df_temp, left_index=True, right_index=True)
    new_df.drop(["cul_matl"], axis=1, inplace=True)

    # This makes sure that all the numerical columns don't have any missing values
    new_df.dropna(subset=["Age"], axis=0, inplace=True)
    new_df.dropna(subset=["Soil_Elec_Conductivity"], axis=0, inplace=True)
    new_df.dropna(subset=["Soil_Moisture"], axis=0, inplace=True)
    new_df.dropna(subset=["Soil_pH"], axis=0, inplace=True)
    new_df.dropna(subset=["length"], axis=0, inplace=True)

    # This maps the Soil_Drainage_Class column to numerical values
    new_df.dropna(subset=['Soil_Drainage_Class'], axis=0, inplace=True)
    new_df['Soil_Drainage_Class'] = new_df['Soil_Drainage_Class'].map(
        {'Very poorly drained': 0,
         'Poorly drained': 1,
         'Somewhat poorly drained': 2,
         'Moderately well drained': 3,
         'Well drained': 4,
         'High': 5,
         'Somewhat excessively drained': 6,
         'Excessively drained': 7, })

    # This maps the Flooding_Frequency column to numerical values
    new_df.dropna(subset=['Flooding_Frequency'], axis=0, inplace=True)
    new_df['Flooding_Frequency'] = new_df['Flooding_Frequency'].map(
        {'No': 0,
         'very rare': 1,
         'rare': 2,
         'Occasional': 3,
         'Frequent': 4, })
    new_df.dropna(subset=['Flooding_Frequency'], axis=0, inplace=True)

    # This removes outliers from the Age column based on the Cul_rating`
    rates = new_df['Cul_rating'].unique()
    rates.sort()
    for rate in rates:
        df = new_df['Age'][new_df.Cul_rating == rate]
        q1 = df.quantile(q=0.25, interpolation='linear')
        q3 = df.quantile(q=0.75, interpolation='linear')
        new_df = new_df.drop(new_df[(new_df['Cul_rating'] == rate) & (new_df['Age'] < q1)].index)
        new_df = new_df.drop(new_df[(new_df['Cul_rating'] == rate) & (new_df['Age'] > q3)].index)

    # Order the columns in alphabetical order except for the target column which should be first
    target_col = 'Cul_rating'
    cols = [col for col in new_df.columns if col != target_col]
    cols.sort()
    cols = [target_col] + cols
    new_df = new_df[cols]

    return new_df

def train_model(name, path, db_path, X_train, Xtest, y_train, y_test):
    '''
    This function will train a model based on the name provided.
    :param name: This is the name of the model to be trained.
    :param path: The filename (relative or absolute) where the trained model will be saved.
    :param db_path: The base directory path where the model and temporary files will be stored.
    :param X_train: This is the training features.
    :param X_test: This is the testing features.
    :param y_train: This is the training labels.
    :param y_test: This is the testing labels.
    :return: The trained model's accuracy score on the test set.
    '''
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    import pickle

    db_dir = db_path + "/tmp"

    # Create the temp directory if it does not exist
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    else:
        # remove existing file if it exists
        full_path = os.path.join(db_dir, path)
        if os.path.exists(full_path):
            os.remove(full_path)

    # Train the model based on the name provided
    if name == "Random Forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
    elif name == "XGBoost":
        model = XGBClassifier(random_state=42)
        model.fit(X_train, y_train)
    else:
        return "Model type not supported."

    # Save the trained model to the specified path
    with open(db_dir + path, 'wb') as f:
        pickle.dump(model, f)

    # Return the accuracy score of the model on the test set
    return round(accuracy_score(y_test, model.predict(Xtest)),3)

def save_models(db_path):
    '''
    This function will save the trained models to the instance/current directory
    '''

    temp_dir = db_path + "/tmp/"
    current_dir = db_path + "/current/"

    # If the current directory does not exist, create it
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)

    # If the temp directory does not exist, there are no models to save
    if not os.path.exists(temp_dir):
        return "No models to save."

    # Checks if the current directory exists and moves all files to a new directory called the current time stamp
    if os.listdir(current_dir):
        time_stamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S") # Format: YYYY-MM-DD_HH.MM.SS
        new_dir = os.path.join(db_path, time_stamp) # New directory path
        os.mkdir(new_dir) # Create the new directory

        # Moves all files from the current directory to the new time stamp directory
        for file_name in os.listdir(current_dir):
            full_file_name = os.path.join(current_dir, file_name)
            if os.path.isfile(full_file_name):
                os.replace(full_file_name, os.path.join(new_dir, file_name))

    # Moves all files from the temp directory to the current directory
    for file_name in os.listdir(temp_dir):
        full_file_name = os.path.join(temp_dir, file_name)
        if os.path.isfile(full_file_name):
            os.replace(full_file_name, os.path.join(current_dir, file_name))

    os.rmdir(temp_dir)

    # This removes the third-oldest time stamp directory if there are more than 2
    time_stamp_dirs = [d for d in os.listdir(db_path) if os.path.isdir(os.path.join(db_path, d))]  # List of time stamp directories
    if len(time_stamp_dirs) > 3:
        time_stamp_dirs.sort()
        dir_to_remove = os.path.join(db_path, time_stamp_dirs[0])  # Get the oldest directory
        for file_name in os.listdir(dir_to_remove):
            full_file_name = os.path.join(dir_to_remove, file_name)
            if os.path.isfile(full_file_name):
                os.remove(full_file_name)
        os.rmdir(dir_to_remove)

    return "Models saved"

