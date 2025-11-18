import pandas as pd
import os

def css_for_table():
    '''
    This function will return the CSS styling for the table that is used to preview the dataset
    :return: The CSS styling for the table
    '''
    css = """
    <style type="text/css" media="screen" style="width:100%">
        table, th, td {
            background-color: #0; 
            padding: 10px;
        }
        th {
            background-color: #0b0b0f; 
            shadow: 0 10px 30px rgba(0, 0, 0, 0.35); 
            color: white; 
            font-family: Tahoma;
            font-size : 13; 
            text-align: center;
        }
        td {
            background-color: #0b0b0f; 
            shadow:0 10px 30px rgba(0, 0, 0, 0.35); 
            color: white; 
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

    rates = new_df['Cul_rating'].unique()
    rates.sort()
    for rate in rates:
        df = new_df['Age'][new_df.Cul_rating == rate]
        q1 = df.quantile(q=0.25, interpolation='linear')
        q3 = df.quantile(q=0.75, interpolation='linear')
        new_df = new_df.drop(new_df[(new_df['Cul_rating'] == rate) & (new_df['Age'] < q1)].index)
        new_df = new_df.drop(new_df[(new_df['Cul_rating'] == rate) & (new_df['Age'] > q3)].index)

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

    return new_df

def train_model(name, path, X_train, y_train):
    '''
    This function will train a model based on the name provided
    :param name: This is the name of the model to be trained
    :param X_train: This is the training features
    :param X_test: This is the testing features
    :param y_train: This is the training labels
    :param y_test: This is the testing labels
    :return: The trained model and its accuracy score on the test set
    '''
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    import pickle

    if name == "Random Forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        file = "." + path # Prepend a dot to make it a relative path

        # Check if the specified path exists
        if os.path.exists(file):

            # Save the trained model to the specified path
            with open(file, 'wb') as f:
                pickle.dump(model, f)

            return True

        return False


    elif name == "XGBoost":
        model = XGBClassifier(random_state=42)
        model.fit(X_train, y_train)

        file = "." + path # Prepend a dot to make it a relative path

        # Check if the specified path exists
        if os.path.exists(file):

            # Save the trained model to the specified path
            with open(file, 'wb') as f:
                pickle.dump(model, f)

            return True

        return False
    else:
        return "Model type not supported."

