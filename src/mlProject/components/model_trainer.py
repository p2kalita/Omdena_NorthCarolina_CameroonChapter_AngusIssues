import pandas as pd
import os
from mlProject import logger
import joblib
from mlProject.entity.config_entity import ModelTrainerConfig
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):

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
        

        # Continue with the forecasting logic
        for cow in unique_cows:
            cow_data = data[data['Cow'] == cow]

            # Ensure that the index is a DatetimeIndex
            cow_data.index = pd.to_datetime(cow_data.index)

            # Split the data into train and test based on the split_date
            cow_train_data = cow_data[cow_data.index < split_date]
            cow_test_data = cow_data[cow_data.index >= split_date]

            # Fit the model and make predictions
            model_ETS = ETSModel(cow_train_data['Body Weight (kg)'], error='add', trend=None, seasonal=None)
            model_fit = model_ETS.fit()

            # Make predictions for the test set
            cow_predictions = model_fit.predict(start=len(cow_train_data), end=len(cow_train_data) + len(cow_test_data) - 1)

            # Store the predictions
            cow_forecast_df = pd.DataFrame({
                'Date': cow_test_data.index,
                'Cow': cow,
                'Predicted Body Weight (kg)': cow_predictions
            })

            forecast_results = pd.concat([forecast_results, cow_forecast_df])

        forecast_results.reset_index(drop=True, inplace=True)
        print(forecast_results)

        # Ensure the directory exists
        model_dir = os.path.join(self.config.root_dir, 'model_trainer')
        os.makedirs(model_dir, exist_ok=True)

        forecast_results.to_csv(os.path.join(self.config.root_dir, 'forecast_results.csv'), index=False)

        joblib.dump(model_fit, os.path.join(self.config.root_dir, self.config.model_name))