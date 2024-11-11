import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load dataset (replace 'traffic_data.csv' with your actual dataset)
data = pd.read_csv('dataset.csv')

# Extract features and target variable
X = data[['weekday', 'city_zone', 'weather', 'temperature']]
y = data['traffic_flow']  # Replace with the column representing traffic flow

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
print("Random Forest MSE:", mean_squared_error(y_test, rf_predictions))

# Train SVR model
svr_model = SVR(kernel='rbf')
svr_model.fit(X_train, y_train)
svr_predictions = svr_model.predict(X_test)
print("SVR MSE:", mean_squared_error(y_test, svr_predictions))

# Save models
joblib.dump(rf_model, 'random_forest_model.joblib')
joblib.dump(svr_model, 'svr_model.joblib')
