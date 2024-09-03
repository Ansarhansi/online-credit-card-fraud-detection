from flask import Flask, render_template, request
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)

# Load the pre-trained machine learning model
model = pickle.load(open('fraud_detection_model.pkl', 'rb'))

# Function to predict fraud
def predict_fraud(features):
    prediction = model.predict([features])
    return prediction[0]

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    prediction = predict_fraud(features)

    # Store the transaction in the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (feature1, feature2, feature3, fraud) VALUES (?, ?, ?, ?)", (*features, prediction))
    conn.commit()
    conn.close()

    # Render the result
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
