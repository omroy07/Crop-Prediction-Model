from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)

# Load your dataset
data = pd.read_csv('Crop_recommendation.csv')

# Prepare your features and labels
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Train a model (or load a pre-trained model)
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, 'crop_model.pkl')

# Load the model
model = joblib.load('crop_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    features = [[
        input_data['N'],
        input_data['P'],
        input_data['K'],
        input_data['temperature'],
        input_data['humidity'],
        input_data['ph'],
        input_data['rainfall']
    ]]
    prediction = model.predict(features)
    return jsonify({'recommended_crop': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)