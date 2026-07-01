import pandas as pd

# 1. Load the dataset we created in the last step
df = pd.read_csv("urls.csv")

print("Transforming URLs into numbers...")

# 2. Define our feature extraction functions
def get_url_length(url):
    return len(str(url))

def count_dots(url):
    return str(url).count('.')

def has_at_symbol(url):
    if '@' in str(url):
        return 1
    else:
        return 0

def is_https(url):
    if str(url).startswith("https"):
        return 1
    else:
        return 0

# 3. Apply these functions to create new numerical columns
df['url_length'] = df['url'].apply(get_url_length)
df['dot_count'] = df['url'].apply(count_dots)
df['has_at_symbol'] = df['url'].apply(has_at_symbol)
df['is_https'] = df['url'].apply(is_https)

# 4. Save this new numeric data into a separate file
df.to_csv("featured_urls.csv", index=False)

print("\n🎉 Success! 'featured_urls.csv' has been created.")
print("Here is what the AI will actually see now:")
# Show only the numeric features and the label for a clean preview
print(df[['url_length', 'dot_count', 'has_at_symbol', 'is_https', 'label']].head())