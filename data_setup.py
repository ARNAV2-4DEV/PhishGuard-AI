import pandas as pd

# Let's create a curated list of real-world safe and phishing URLs
data = {
    "url": [
        # --- SAFE / BENIGN URLS (Label 0) ---
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com/trending",
        "https://www.amazon.in/electronics",
        "https://vit.ac.in/admissions",
        "https://www.netflix.com/browse",
        "https://www.linkedin.com/feed/",
        "https://www.microsoft.com/en-us",
        "https://stackoverflow.com/questions",
        "https://www.spotify.com/premium",
        
        # --- PHISHING / MALICIOUS URLS (Label 1) ---
        "http://login-google-security-verify.com/account",
        "http://secure-paypal-login-update.net/signin",
        "http://amaz0n-giftcard-free.com/win",
        "http://verify-identity-sbi-banking.in/login.php",
        "http://netflix-free-trial-activation.xyz",
        "http://sign-in-microsoft-access-checkpoint.co",
        "http://update-your-instagram-password.icu/secure",
        "http://free-pubg-skins-generator.net/claim",
        "http://walmart-shopping-reward.top/index.html",
        "http://apple-icloud-security-alert.cc/auth"
    ],
    # 0 = Safe, 1 = Phishing
    "label": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

# Convert this dictionary into a clean Pandas DataFrame
df = pd.DataFrame(data)

# Save it to a CSV file in your folder
df.to_csv("urls.csv", index=False)

print("🎉 Success! 'urls.csv' has been created with 20 sample URLs.")
print(df.head())