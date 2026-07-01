import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Load our numeric features
df = pd.read_csv("featured_urls.csv")

# 2. Separate into Features (X) and Target Label (y)
# X = the numbers the AI looks at to make a guess
X = df[['url_length', 'dot_count', 'has_at_symbol', 'is_https']]
# y = the true answer (0 for safe, 1 for phishing)
y = df['label']

# 3. Split data: 70% for training the AI, 30% to test it later
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("Training the Random Forest model...")

# 4. Initialize and Train the Model
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

print("🎉 Model training complete! Evaluating performance...\n")

# 5. Test the model on the remaining 30% of data it hasn't seen yet
y_pred = model.predict(X_test)

# 6. Print the performance metrics
print("--- MODEL REPORT ---")
print(classification_report(y_test, y_pred))

# 7. Save the trained model to a file so we can use it in our API later
joblib.dump(model, "phishing_model.pkl")
print("💾 Model saved securely as 'phishing_model.pkl'")