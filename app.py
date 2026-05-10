
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    square_feet = float(request.form['square_feet'])
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])

    features = np.array([[square_feet, bedrooms, bathrooms]])

    prediction = model.predict(features)

    return render_template(
        'index.html',
        prediction_text=f"Estimated Price: ${prediction[0]:,.2f}"
    )

if __name__ == "__main__":
    app.run(debug=True)