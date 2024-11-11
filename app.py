from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

app = Flask(__name__)

# Load trained models (assume they are stored as joblib files)
random_forest_model = joblib.load('random_forest_model.joblib')
svr_model = joblib.load('svr_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Extract features from input data
    date = data['date']  # Example: '2024-11-11'
    weekday = pd.to_datetime(date).weekday()  # Convert to numeric weekday (0=Monday, ..., 6=Sunday)
    city_zone = data['city_zone']
    weather = data['weather']  # Encoded as numeric (e.g., 0 = sunny, 1 = rainy, etc.)
    temperature = data['temperature']
    
    # Prepare input for prediction
    input_features = np.array([[weekday, city_zone, weather, temperature]])

    # Make predictions
    rf_prediction = random_forest_model.predict(input_features)
    svr_prediction = svr_model.predict(input_features)
    
    # Choose the best prediction or display both
    response = {
        'random_forest_prediction': rf_prediction[0],
        'svr_prediction': svr_prediction[0]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
