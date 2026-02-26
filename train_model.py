import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load market_data.csv to get all categories and some training points
market_df = pd.read_csv("market_data.csv")

# Create training data from market_data.csv
# We have Today (Day 0) and After 7 Days (Day 7)
train_data = []
for _, row in market_df.iterrows():
    # Day 0
    train_data.append([row['district'], row['crop'], row['market'], 0, row['price_today']])
    # Day 7
    train_data.append([row['district'], row['crop'], row['market'], 7, row['price_after_7_days']])

data = pd.DataFrame(train_data, columns=["District", "Crop", "Market", "Day", "Price"])

# Convert text to numbers
le_d = LabelEncoder()
le_c = LabelEncoder()
le_m = LabelEncoder()

# Fit encoders on ALL possible values from the csv
le_d.fit(market_df["district"].unique())
le_c.fit(market_df["crop"].unique())
le_m.fit(market_df["market"].unique())

data["District"] = le_d.transform(data["District"])
data["Crop"] = le_c.transform(data["Crop"])
data["Market"] = le_m.transform(data["Market"])

# Inputs and output
X = data[["District", "Crop", "Market", "Day"]]
y = data["Price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model and encoders
joblib.dump(model, "price_model.pkl")
joblib.dump(le_d, "district.pkl")
joblib.dump(le_c, "crop.pkl")
joblib.dump(le_m, "market.pkl")

print("Model trained and saved")
