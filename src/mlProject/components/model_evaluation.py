import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from mlProject.utils.common import save_json
from urllib.parse import urlparse
import numpy as np
import joblib
from mlProject.entity.config_entity import ModelEvaluationConfig
from pathlib import Path


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        #mae = mean_absolute_error(actual, pred)
        #r2 = r2_score(actual, pred)
        #return rmse, mae, r2
        return rmse


    def save_results(self):

        data = pd.read_csv(self.config.data_path)
        data.drop('Unnamed: 0', axis=1, inplace=True)
        data['Date'] = pd.to_datetime(data['Date']) # Convert 'Date' column to datetime format
        data = data.set_index('Date')

        # Initialize forecast results DataFrame
        forecast_results = pd.DataFrame(columns=['Date', 'Cow', 'Predicted Body Weight (kg)'])

        # Define the date to split the data (adjust the date as needed)
        split_date = pd.to_datetime('2022-02-15')

        # Extract unique cow IDs from the DataFrame
        unique_cows = data['Cow'].unique()
        

        forecast_results = pd.read_csv(self.config.test_data_path) #importing forecast.csv
        

        # Extract unique cow IDs from the DataFrame
        unique_cows = data['Cow'].unique()
        actual_values = []
        predicted_values = []

        for cow in unique_cows:
            cow_data = data[data['Cow'] == cow]

            # Split the data into train and test based on the split_date
            cow_test_data = cow_data[cow_data.index >= split_date]

            # Extract actual values for the test set
            actual_values.extend(cow_test_data['Body Weight (kg)'].values)

            # Extract predicted values for the test set from forecast_results
            cow_predictions = forecast_results[forecast_results['Cow'] == cow]['Predicted Body Weight (kg)'].values
            predicted_values.extend(cow_predictions)

        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
        print(f"RMSE for ETS Model: {rmse}")


        
        # Saving metrics as local
        #scores = {"rmse": rmse, "mae": mae, "r2": r2}
        scores = {"rmse": rmse}
        save_json(path=Path(self.config.metric_file_name), data=scores)
