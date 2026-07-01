import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

print("Loading saved model and data features...")
# 1. Load the frozen model brain and the featured data
model = joblib.load("phishing_model.pkl")
df = pd.read_csv("featured_urls.csv")

# Extract just the numeric columns the model expects
X = df[['url_length', 'dot_count', 'has_at_symbol', 'is_https']]

print("Analyzing AI decisions using SHAP (TreeExplainer)...")
# 2. Hook up the SHAP explainer to our Random Forest trees
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# 3. Create a clean canvas for our plot
plt.figure(figsize=(10, 5))

# If shap_values is a list (common for Random Forest), index [1] represents Phishing impact
if isinstance(shap_values, list):
    shap.summary_plot(shap_values[1], X, show=False)
else:
    # Handle newer SHAP version format
    shap.summary_plot(shap_values[:, :, 1], X, show=False)

# 4. Save the plot as a PNG image in your project folder
plt.title("SHAP Feature Importance: What Flags a Phishing URL?", fontsize=14, pad=20)
plt.savefig("shap_importance.png", bbox_inches='tight')

print("\n🎉 Success! 'shap_importance.png' has been saved to your folder.")
print("Open the image from your sidebar to see exactly how your AI thinks!")