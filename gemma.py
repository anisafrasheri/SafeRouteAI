# Python Code for Collecting and Storing SOS Alerts:
import requests
import pandas as pd

# Define your API endpoint for SOS alerts
api_url = 'https://api.yourapp.com/sos-alerts'

# Fetch SOS alerts data from your API
response = requests.get(api_url)
data = response.json()

# Convert to DataFrame for easier analysis
sos_alerts = pd.DataFrame(data)

# Sample columns: ['user_id', 'timestamp', 'latitude', 'longitude', 'context']

# Display the first few rows
print(sos_alerts.head())


# 3. Data Storage and Management
# You’ll need to store your collected data for easy querying and analysis.
# Example: Storing Data in a PostgreSQL Database

import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="gemma_db",
    user="your_username",
    password="your_password"
)

# Create a cursor object
cursor = conn.cursor()

# SQL to create a table for SOS alerts
create_table = """
CREATE TABLE IF NOT EXISTS sos_alerts (
    user_id INT,
    timestamp TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    context TEXT
)
"""
cursor.execute(create_table)
conn.commit()

# Insert data from the API into the table
for _, row in sos_alerts.iterrows():
    insert_query = """
    INSERT INTO sos_alerts (user_id, timestamp, latitude, longitude, context)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (row['user_id'], row['timestamp'], row['latitude'], row['longitude'], row['context']))

conn.commit()
cursor.close()
conn.close()

# 4. Data Analysis and Modeling
# You can now analyze the data and use machine learning models to predict safety levels.
#
# Example: Descriptive Analysis (Finding High-Frequency Areas)
# Group by location and count the number of SOS alerts per location

sos_by_location = sos_alerts.groupby(['latitude', 'longitude']).size().reset_index(name='count')

# Sort to find high-frequency alert areas
high_risk_areas = sos_by_location.sort_values(by='count', ascending=False)
print(high_risk_areas.head())

#Predictive Modeling: Time Series Forecasting with Machine Learning
#You can use time-series analysis or classification models (e.g., decision trees) to predict unsafe areas.

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Feature engineering: Convert timestamp to relevant features like hour, day of week, etc.
sos_alerts['hour'] = pd.to_datetime(sos_alerts['timestamp']).dt.hour
sos_alerts['day_of_week'] = pd.to_datetime(sos_alerts['timestamp']).dt.dayofweek

# Prepare data for classification model (safe vs unsafe area based on SOS frequency)
X = sos_alerts[['latitude', 'longitude', 'hour', 'day_of_week']]
y = (sos_alerts['count'] > threshold_value).astype(int)  # Define a threshold for 'unsafe'

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a classification model (e.g., Random Forest)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# 5. Insights Generation
# You can generate insights from the model and create visualizations to present them.
#
# Example: Visualizing High-Risk Areas Using Matplotlib

import matplotlib.pyplot as plt

# Plot high-risk areas based on SOS alert counts
plt.scatter(sos_by_location['longitude'], sos_by_location['latitude'], c=sos_by_location['count'], cmap='Reds')
plt.colorbar(label='Number of SOS Alerts')
plt.title('High-Risk Areas Based on SOS Alerts')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# 6. User Interface (UI) Development
# Build a simple web interface using Flask or Django to display the insights.
#
# Example: Flask App to Display Insights

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    # Query your database for high-risk areas
    sos_alerts = pd.read_sql("SELECT * FROM sos_alerts", conn)
    high_risk_areas = sos_alerts.groupby(['latitude', 'longitude']).size().reset_index(name='count')

    return render_template('index.html', data=high_risk_areas.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

# 7. Real-Time Notifications
# You can trigger notifications based on live data using real-time databases like Firebase.
#
# Example: Sending Notifications (using Firebase Cloud Messaging)

import firebase_admin
from firebase_admin import messaging

# Initialize Firebase SDK
firebase_admin.initialize_app()

# Define a function to send SOS alert notifications
def send_sos_notification(user_token, alert_message):
    message = messaging.Message(
        notification=messaging.Notification(
            title="SOS Alert",
            body=alert_message,
        ),
        token=user_token,
    )
    messaging.send(message)

# Example usage:
user_token = "example_firebase_token"
send_sos_notification(user_token, "You're entering a high-risk area!")

