import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pickle
import numpy as np

print("\n" + "="*60)
print("🤖 EstateAI - House Price Prediction Model Training")
print("="*60 + "\n")

try:
    # Load dataset
    print("📂 Loading dataset...")
    data = pd.read_csv("housing_price_dataset.csv")
    print(f"✓ Dataset loaded successfully!")
    print(f"   Records: {len(data)}")
    print(f"   Columns: {list(data.columns)}\n")

    # Validate data
    print("🔍 Validating data...")
    if data.isnull().sum().sum() > 0:
        print(f"⚠️ Found {data.isnull().sum().sum()} missing values")
        data = data.dropna()
        print(f"✓ Removed missing values, remaining records: {len(data)}\n")
    else:
        print("✓ No missing values found\n")

    # Check for outliers and basic stats
    print("📊 Dataset Statistics:")
    print(data[['SquareFeet', 'Bedrooms', 'Bathrooms', 'Price']].describe())
    print()

    # Prepare features
    print("📊 Preparing features...")
    X = data[['SquareFeet', 'Bedrooms', 'Bathrooms']]
    y = data['Price']
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}\n")

    # Split dataset
    print("✂️ Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples\n")

    # Train model
    print("🚀 Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("✓ Model training completed!\n")

    # Evaluate model
    print("📈 Model Evaluation:")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    print(f"   Training R² Score:  {train_r2:.4f}")
    print(f"   Test R² Score:      {test_r2:.4f}")
    print(f"   Training RMSE:      ${train_rmse:,.2f}")
    print(f"   Test RMSE:          ${test_rmse:,.2f}\n")

    # Display coefficients
    print("🔢 Model Coefficients:")
    coefficients = {
        'Square Feet': model.coef_[0],
        'Bedrooms': model.coef_[1],
        'Bathrooms': model.coef_[2],
        'Intercept': model.intercept_
    }
    
    for feature, coef in coefficients.items():
        if feature == 'Intercept':
            print(f"   - {feature:15} ${coef:,.2f}")
        else:
            print(f"   - {feature:15} {coef:.4f}")
    print()

    # Save model
    print("💾 Saving model...")
    pickle.dump(model, open('model.pkl', 'wb'))
    print("✓ Model saved successfully as 'model.pkl'\n")

    print("="*60)
    print("✅ Model Training Complete!")
    print("="*60 + "\n")

except FileNotFoundError:
    print("❌ ERROR: Dataset file 'housing_price_dataset.csv' not found!")
    print("   Please ensure the CSV file is in the same directory.\n")
except KeyError as e:
    print(f"❌ ERROR: Required column '{e}' not found in dataset!")
    print("   Expected columns: 'SquareFeet', 'Bedrooms', 'Bathrooms', 'Price'\n")
except Exception as e:
    print(f"❌ ERROR: {str(e)}\n")
    raise
