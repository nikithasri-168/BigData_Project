import requests
import tweepy  
import json

# Twitter API Credentials
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH3%2BzwEAAAAAB74gbgDmc39%2F1cZ%2FOmLPi6%2F9CL8%3DlgQ4cS6ncmzdXJq90Yt2SPNYtMkcots4Rj4zP4gwxwvhr8d5sO"

# News API Credentials
NEWS_API_KEY = "b88912251b8d40748745acaab5ecea2e"

# Function to fetch Twitter data
def fetch_twitter_data(query, count=100):
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={count}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching Twitter data:", response.text)
        return None

# Function to fetch News data
def fetch_news_data(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching News data:", response.text)
        return None

# Save data to a JSON file
def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

# Keywords
if __name__ == "__main__":
    topic = "AI OR Machine Learning OR Artificial Intelligence OR Tech Innovations OR Deep Learning OR Neural Networks OR ChatGPT OR AI Ethics OR Self-Driving Cars OR Generative AI OR Tech Breakthroughs" 
    twitter_data = fetch_twitter_data(topic)
    news_data = fetch_news_data(topic)

    if twitter_data:
        save_data("twitter_data.json", twitter_data)

    if news_data:
        save_data("news_data.json", news_data)
