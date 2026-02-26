import pandas as pd
import joblib

# Load trained model and encoders
model = joblib.load("price_model.pkl")
le_d = joblib.load("district.pkl")
le_c = joblib.load("crop.pkl")
le_m = joblib.load("market.pkl")

def predict_price(district, crop, market, day):
    # Transform labels
    d = le_d.transform([district])[0]
    c = le_c.transform([crop])[0]
    m = le_m.transform([market])[0]

    # Create DataFrame with feature names to avoid warnings
    X = pd.DataFrame([[d, c, m, day]], columns=["District", "Crop", "Market", "Day"])
    
    price = model.predict(X)
    return round(float(price[0]), 2)
