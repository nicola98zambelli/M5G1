

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, classification_report, confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc
import sklearn
import joblib
import boto3
import pathlib
from io import StringIO 
import argparse
import joblib
import os
import numpy as np
import pandas as pd

# inference functions ---------------

# def input_fn(request_body, request_content_type):
#     print(request_body)
#     print(request_content_type)
#     if request_content_type == "text/csv":
#         request_body = request_body.strip()
#         try:
#             df = pd.read_csv(StringIO(request_body), header=None)
#             return df
        
#         except Exception as e:
#             print(e)
#     else:
#         return """Please use Content-Type = 'text/csv' and, send the request!!""" 
 
    
def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf

# def predict_fn(input_data, model):
#     if type(input_data) != str:
#         prediction = model.predict(input_data)
#         print(prediction)
#         return prediction
#     else:
#         return input_data
        
    
if __name__ == "__main__":

    print("[INFO] Extracting arguments")
    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script.
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--random_state", type=int, default=0)

    # Data, model, and output directories
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--bucket", type=str, default='data-remote-repository-cefriel')
    parser.add_argument("--train-file", type=str, default="gruppo-1/raw/train.csv")
    parser.add_argument("--validation-file", type=str, default="gruppo-1/raw/validation.csv")
    
    args, _ = parser.parse_known_args()

    print(os.environ.get("SM_MODEL_DIR"))
    print("SKLearn Version: ", sklearn.__version__)
    print("Joblib Version: ", joblib.__version__)

    print("[INFO] Reading data")
    print()

    s3 = boto3.resource('s3')

    train_file = args.train_file
    validation_file = args.validation_file
    bucket_name = args.bucket
    #train data
    obj = s3.Object(bucket_name, train_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    train_df = pd.read_csv(data_file, sep=";")
    
    #validation data
    obj = s3.Object(bucket_name, validation_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    validation_df = pd.read_csv(data_file, sep=";")

    # fillna with mean
    train_df['MasVnrArea'] = train_df['MasVnrArea'].fillna(train_df['MasVnrArea'].mean())
    train_df['GarageYrBlt'] = train_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].mean())
    validation_df['MasVnrArea'] = validation_df['MasVnrArea'].fillna(validation_df['MasVnrArea'].mean())
    validation_df['GarageYrBlt'] = validation_df['GarageYrBlt'].fillna(validation_df['GarageYrBlt'].mean())
    
    features = [
    'MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 
    'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 
    '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 
    'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 
    'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
    '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold'
    ]
    
    label = "SalePrice"
    
    print("Building training and testing datasets")
    print()
    X_train = train_df[features]
    X_validation = validation_df[features]
    y_train = train_df[label]
    y_validation = validation_df[label]

    print('Column order: ')
    print(features)
    print()
    
    print("Label column is: ",label)
    print()
    
    print("Data Shape: ")
    print()
    print("---- SHAPE OF TRAINING DATA (75%) ----")
    print(X_train.shape)
    print(y_train.shape)
    print()
    print("---- SHAPE OF VALIDATION DATA (25%) ----")
    print(X_validation.shape)
    print(y_validation.shape)
    print()
    
  
    print("Training RandomForest Model.....")
    print()
    model =  RandomForestRegressor(n_estimators=args.n_estimators, random_state=args.random_state, verbose = 3,n_jobs=-1)
    model.fit(X_train, y_train)
    print()
    

    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model,model_path)
    print("Model persisted at " + model_path)
    print()

    
    y_pred_val = model.predict(X_validation)
    test_acc = mean_squared_error(y_validation,y_pred_val)
    #test_rep = classification_report(y_validation,y_pred_val)

    print()
    print("---- METRICS RESULTS FOR TESTING DATA ----")
    print()
    print("Total Rows are: ", X_validation.shape[0])
    print('[TESTING] Model MSE is: ', test_acc)
    #print('[TESTING] Testing Report: ')
    #print(test_rep)
