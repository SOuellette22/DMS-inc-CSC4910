import pandas as pd
import os
import time

def test_process_dataset_function():
    from src.admin.functions import process_dataset

    # Create a data frame based on the small actual dataset
    data = {
        'latitude': [34.05, 36.16, 25.16],
        'longitude': [-118.24, -115.15, -119.70],
        'length': [100, 150, 200],
        'cul_matl': ['Concrete', 'Steel', 'Wood'],
        'cul_type': ['Box', 'Pipe', 'Circle'],
        'Soil_Drainage_Class': ['Well drained', 'Poorly drained', 'Moderately well Drained'],
        'Soil_Moisture': [20.5, 30.2, 25.3],
        'Soil_pH': [6.5, 7.0, 5.8],
        'Soil_Elec_Conductivity': [1.2, 0.8, 1.5],
        'Flooding_Frequency': ['No', 'rare', 'Frequent'],
        'State': ['CA', 'NV', 'CA'],
        'Soil_Surface_Texture': ['Loam', 'Clay', 'Sandy'],
        'Cul_rating': ['5', '3', '3'],
        'Age': [10, 20, 30]
    }

    df = pd.DataFrame(data)

    # Process the dataset
    processed_df = process_dataset(df)

    # Check that the processed dataframe has the expected columns
    expected_columns = [
        'length', 'Soil_Drainage_Class', 'Soil_Moisture', 'Soil_pH',
        'Soil_Elec_Conductivity', 'Age', 'Cul_rating',
        'type_Box', 'mat_Concrete'
    ]

    for col in expected_columns:
        assert col in processed_df.columns.to_list(), f"Missing expected column: {col}"

    # Check that there are no missing values in the processed dataframe
    assert not processed_df.isnull().values.any(), f"Processed dataframe contains missing values in this column: {processed_df.columns[processed_df.isnull().any()].tolist()}"

    # Make sure all culomns have correct data types
    assert processed_df['Cul_rating'].dtype == 'int64', "Cul_rating column is not of type integer"
    assert processed_df['Soil_Drainage_Class'].dtype == 'int64', "Soil_Drainage_Class column is not of type integer"
    assert processed_df['Flooding_Frequency'].dtype == 'int64', "Flooding_Frequency column is not of type integer"
    assert processed_df['length'].dtype in ['int64', 'float64'], "length column is not of type integer or float"
    assert processed_df['Soil_Moisture'].dtype in ['int64', 'float64'], "Soil_Moisture column is not of type integer or float"
    assert processed_df['Soil_pH'].dtype in ['int64', 'float64'], "Soil_pH column is not of type integer or float"
    assert processed_df['Soil_Elec_Conductivity'].dtype in ['int64', 'float64'], "Soil_Elec_Conductivity column is not of type integer or float"
    assert processed_df['Age'].dtype in ['int64', 'float64'], "Age column is not of type integer or float"

def test_train_model_function():
    from src.admin.functions import process_dataset, train_model
    from sklearn.model_selection import train_test_split

    os.mkdir("./src/tests/admin/instance")
    os.mkdir("./src/tests/admin/instance/current")

    # Create a data frame based on the small actual dataset
    data = {
        'latitude': [34.05, 36.16, 25.16, 40.71, 34.05],
        'longitude': [-118.24, -115.15, -119.70, -74.00, -118.24],
        'length': [100, 150, 200, 250, 120],
        'cul_matl': ['Concrete', 'Steel', 'Wood', 'Concrete', 'Steel'],
        'cul_type': ['Box', 'Pipe', 'Circle', 'Box', 'Pipe'],
        'Soil_Drainage_Class': ['Well drained', 'Poorly drained', 'Moderately well Drained', 'Well drained', 'Poorly drained'],
        'Soil_Moisture': [20.5, 30.2, 25.3, 22.1, 28.4],
        'Soil_pH': [6.5, 7.0, 5.8, 6.9, 7.2],
        'Soil_Elec_Conductivity': [1.2, 0.8, 1.5, 1.1, 0.9],
        'Flooding_Frequency': ['No', 'rare', 'Frequent', 'No', 'rare'],
        'State': ['CA', 'NV', 'CA', 'NY', 'NV'],
        'Soil_Surface_Texture': ['Loam', 'Clay', 'Sandy', 'Loam', 'Clay'],
        'Cul_rating': ['5', '3', '3', '4', '2'],
        'Age': [10, 20, 30, 15, 25]
    }

    df = pd.DataFrame(data)

    # Process the dataset
    processed_df = process_dataset(df)

    # Gets the features and labels from the processed dataframe
    dataset_label = processed_df['Cul_rating']
    dataset_features = processed_df.drop(columns=['Cul_rating'], axis=1)

    # Creates the training and testing splits
    X_train, X_test, y_train, y_test = train_test_split(
        dataset_features, dataset_label, test_size=0.2, random_state=42
    )

    db_path = "./src/tests/admin/instance"  # Use current directory for testing
    model_name = "Random Forest"
    path = "/test_model.pkl"
    accuracy = train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)

    # Check that the accuracy is a float between 0 and 1
    assert isinstance(accuracy, float), f"Accuracy is not a float it is {type(accuracy)} + {accuracy}"
    assert 0.0 <= accuracy <= 1.0, f"Accuracy is not between 0 and 1 it is {accuracy}"

    # Make sure the model file got saved
    assert os.path.exists(db_path + "/tmp" + path), f"Model file was not saved at {db_path + path}"

    os.remove(db_path + "/tmp" + path)
    os.rmdir(db_path + "/tmp")  # Clean up the created directory after test

def test_train_model_invalid_name():
    from src.admin.functions import process_dataset, train_model
    from sklearn.model_selection import train_test_split

    # Create a data frame based on the small actual dataset
    data = {
        'latitude': [34.05, 36.16, 25.16, 40.71, 34.05],
        'longitude': [-118.24, -115.15, -119.70, -74.00, -118.24],
        'length': [100, 150, 200, 250, 120],
        'cul_matl': ['Concrete', 'Steel', 'Wood', 'Concrete', 'Steel'],
        'cul_type': ['Box', 'Pipe', 'Circle', 'Box', 'Pipe'],
        'Soil_Drainage_Class': ['Well drained', 'Poorly drained', 'Moderately well Drained', 'Well drained',
                                'Poorly drained'],
        'Soil_Moisture': [20.5, 30.2, 25.3, 22.1, 28.4],
        'Soil_pH': [6.5, 7.0, 5.8, 6.9, 7.2],
        'Soil_Elec_Conductivity': [1.2, 0.8, 1.5, 1.1, 0.9],
        'Flooding_Frequency': ['No', 'rare', 'Frequent', 'No', 'rare'],
        'State': ['CA', 'NV', 'CA', 'NY', 'NV'],
        'Soil_Surface_Texture': ['Loam', 'Clay', 'Sandy', 'Loam', 'Clay'],
        'Cul_rating': ['5', '3', '3', '4', '2'],
        'Age': [10, 20, 30, 15, 25]
    }

    df = pd.DataFrame(data)

    # Process the dataset
    processed_df = process_dataset(df)

    # Gets the features and labels from the processed dataframe
    dataset_label = processed_df['Cul_rating']
    dataset_features = processed_df.drop(columns=['Cul_rating'], axis=1)

    # Creates the training and testing splits
    X_train, X_test, y_train, y_test = train_test_split(
        dataset_features, dataset_label, test_size=0.2, random_state=42
    )

    model_name = "Not a Model"
    db_path = "./src/tests/admin/instance"
    path = "/test_model.pkl"

    accuracy = train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)

    # Check that the accuracy is None for an invalid model name
    assert isinstance(accuracy, str), f"Accuracy is not a string it is {type(accuracy)} + {accuracy}"
    assert accuracy == "Model type not supported.", f"Accuracy message is not correct it is {accuracy}"

def test_save_models_function():
    from src.admin.functions import save_models
    from src.admin.functions import process_dataset, train_model
    from sklearn.model_selection import train_test_split

    # Create a data frame based on the small actual dataset
    data = {
        'latitude': [34.05, 36.16, 25.16, 40.71, 34.05],
        'longitude': [-118.24, -115.15, -119.70, -74.00, -118.24],
        'length': [100, 150, 200, 250, 120],
        'cul_matl': ['Concrete', 'Steel', 'Wood', 'Concrete', 'Steel'],
        'cul_type': ['Box', 'Pipe', 'Circle', 'Box', 'Pipe'],
        'Soil_Drainage_Class': ['Well drained', 'Poorly drained', 'Moderately well Drained', 'Well drained',
                                'Poorly drained'],
        'Soil_Moisture': [20.5, 30.2, 25.3, 22.1, 28.4],
        'Soil_pH': [6.5, 7.0, 5.8, 6.9, 7.2],
        'Soil_Elec_Conductivity': [1.2, 0.8, 1.5, 1.1, 0.9],
        'Flooding_Frequency': ['No', 'rare', 'Frequent', 'No', 'rare'],
        'State': ['CA', 'NV', 'CA', 'NY', 'NV'],
        'Soil_Surface_Texture': ['Loam', 'Clay', 'Sandy', 'Loam', 'Clay'],
        'Cul_rating': ['5', '3', '3', '4', '2'],
        'Age': [10, 20, 30, 15, 25]
    }

    df = pd.DataFrame(data)

    # Process the dataset
    processed_df = process_dataset(df)

    # Gets the features and labels from the processed dataframe
    dataset_label = processed_df['Cul_rating']
    dataset_features = processed_df.drop(columns=['Cul_rating'], axis=1)

    # Creates the training and testing splits
    X_train, X_test, y_train, y_test = train_test_split(
        dataset_features, dataset_label, test_size=0.2, random_state=42
    )

    db_path = "./src/tests/admin/instance"  # Use current directory for testing
    model_name = "Random Forest"
    path = "/test_model.pkl"
    train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)

    # Now test the save_models function
    save_models(db_path)

    assert os.path.exists(db_path + "/current" + path) == True

    train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)
    time.sleep(1)  # Ensure a time difference for file modification
    save_models(db_path)
    train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)
    time.sleep(1)
    save_models(db_path)
    train_model(model_name, path, db_path, X_train, X_test, y_train, y_test)
    time.sleep(1)
    save_models(db_path)

    assert os.path.exists(db_path + "/current" + path) == True
    assert os.path.exists(db_path + "/tmp" + path) == False
    assert len(os.listdir(db_path)) <= 3

    os.remove(db_path + "/current" + path)  # Clean up the created file after test
    dir_list = os.listdir(db_path)
    for file in dir_list:
        if file != "current":
            os.remove(db_path + "/" + file + path)
            os.rmdir(os.path.join(db_path, file))

    os.rmdir("./src/tests/admin/instance/current")
    os.rmdir("./src/tests/admin/instance")

