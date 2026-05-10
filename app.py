from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model on startup
MODEL_PATH = 'model.pkl'
model = None

def load_model():
    """Load the trained ML model"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            logger.info("✓ Model loaded successfully")
            return True
        else:
            logger.error(f"❌ Model file '{MODEL_PATH}' not found")
            return False
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        return False

# Load model on startup
if not load_model():
    logger.warning("⚠️ Model not loaded. Please run 'python ml.py' to train the model.")

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict house price based on user input"""
    try:
        # Check if model is loaded
        if model is None:
            error_msg = "Error: Model not loaded. Please train the model first by running 'python ml.py'"
            logger.error(error_msg)
            return render_template('index.html', prediction_text=error_msg)

        # Get form inputs
        try:
            square_feet = float(request.form.get('square_feet', ''))
            bedrooms = int(request.form.get('bedrooms', ''))
            bathrooms = float(request.form.get('bathrooms', ''))
        except (ValueError, TypeError) as e:
            error_msg = f"Error: Invalid input format. Please enter valid numbers."
            logger.warning(f"Input validation error: {str(e)}")
            return render_template('index.html', prediction_text=error_msg)

        # Validate input values
        validation_errors = validate_inputs(square_feet, bedrooms, bathrooms)
        if validation_errors:
            error_msg = f"Error: {validation_errors}"
            logger.warning(f"Input validation failed: {validation_errors}")
            return render_template('index.html', prediction_text=error_msg)

        # Prepare features
        features = np.array([[square_feet, bedrooms, bathrooms]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Validate prediction
        if prediction < 0:
            error_msg = "Error: Invalid prediction result. Please try again."
            logger.error(f"Invalid prediction: {prediction}")
            return render_template('index.html', prediction_text=error_msg)

        # Format output
        prediction_text = f"Estimated Price: ${prediction:,.2f}"
        logger.info(f"✓ Prediction made: {prediction_text} (Area: {square_feet} sq ft, "
                   f"Beds: {bedrooms}, Baths: {bathrooms})")
        
        return render_template(
            'index.html',
            prediction_text=prediction_text
        )

    except Exception as e:
        error_msg = f"Error: An unexpected error occurred. Please try again later."
        logger.error(f"Prediction error: {str(e)}")
        return render_template('index.html', prediction_text=error_msg)

def validate_inputs(square_feet, bedrooms, bathrooms):
    """Validate input parameters"""
    
    # Validate square feet
    if square_feet <= 0 or square_feet > 100000:
        return "Square feet must be between 1 and 100,000"
    
    # Validate bedrooms
    if not isinstance(bedrooms, int) or bedrooms < 1 or bedrooms > 10:
        return "Bedrooms must be between 1 and 10"
    
    # Validate bathrooms
    if bathrooms < 1 or bathrooms > 10:
        return "Bathrooms must be between 1 and 10"
    
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK' if model is not None else 'ERROR',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    }), 200 if model is not None else 503

@app.errorhandler(400)
def bad_request(error):
    """Handle bad requests"""
    logger.warning(f"Bad request: {error}")
    return render_template('index.html', 
                         prediction_text="Error: Invalid request format"), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 Not found: {error}")
    return render_template('index.html', 
                         prediction_text="Error: Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('index.html', 
                         prediction_text="Error: Internal server error"), 500

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 EstateAI - House Price Prediction Server")
    print("="*60)
    
    if model is not None:
        print("✓ Model loaded successfully")
        print("🌐 Server running on http://localhost:5000")
        print("📝 Press Ctrl+C to stop the server")
    else:
        print("⚠️ WARNING: Model not loaded!")
        print("📚 Please run: python ml.py")
        print("Then restart this server")
    
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
