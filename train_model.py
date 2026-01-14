import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load the dataset
df = pd.read_csv('food_nutrition_data.csv')

# Select features
features = ['FoodType', 'Quantity', 'Protein', 'Carbs', 'Fat']
target = 'Calories'

# Encode categorical features
food_type_mapping = {
    'Rice': 0, 'Chicken': 1, 'Broccoli': 2, 'Banana': 3, 'Egg': 4,
    'Fish': 5, 'Carrot': 6, 'Milk': 7, 'Apple': 8, 'Spinach': 9
}
df['FoodType'] = df['FoodType'].map(food_type_mapping)

# Prepare X and y
X = df[features]
y = df[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Save the model and feature columns
joblib.dump(model, 'food_nutrition_model.pkl')
joblib.dump(features, 'food_feature_columns.pkl')

print('Model and feature columns saved successfully.')
