import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
df = pd.read_csv('data/Fertilizer Prediction.csv')

# Print columns to verify names
print(df.columns)

# Rename for consistency (optional but helpful)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Encode categorical columns
le_soil = LabelEncoder()
le_crop = LabelEncoder()

df['soil_type'] = le_soil.fit_transform(df['soil_type'])
df['crop_type'] = le_crop.fit_transform(df['crop_type'])

# Features and target
X = df[['temperature', 'humidity', 'moisture', 'soil_type', 'crop_type', 'nitrogen', 'phosphorous', 'potassium']]
y = df['fertilizer_name']

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model and encoders
joblib.dump(model, 'fertilizer_model.pkl')
joblib.dump(le_soil, 'soil_encoder.pkl')
joblib.dump(le_crop, 'crop_encoder.pkl')
