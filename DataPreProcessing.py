import json
import re
import string
import ast
import nltk
import csv
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure required resources are downloaded
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

# Initialize lemmatizer
lemma = nltk.WordNetLemmatizer()

class TweetCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.punc_table = str.maketrans("", "", string.punctuation)  # To remove punctuation

    def remove_non_ascii_chars(self, text):
        return "".join([w if ord(w) < 128 else " " for w in text])

    def remove_hyperlinks(self, text):
        return " ".join([w for w in text.split(" ") if not "http" in w])

    def get_cleaned_text(self, text):
        cleaned_text = text.replace("\"", "").replace("\'", "").replace("-", " ")
        cleaned_text = self.remove_non_ascii_chars(cleaned_text)

        # Remove Retweet mention
        if re.match(r"RT @[_A-Za-z0-9]+:", cleaned_text):
            cleaned_text = cleaned_text[cleaned_text.index(":") + 2 :]

        cleaned_text = self.remove_hyperlinks(cleaned_text)
        cleaned_text = cleaned_text.replace("#", "HASHTAG").replace("@", "ATUSER")  # Preserve tags

        tokens = [w.translate(self.punc_table) for w in word_tokenize(cleaned_text)]
        tokens = [lemma.lemmatize(w) for w in tokens if w.lower() not in self.stop_words and len(w) > 1]

        cleaned_text = " ".join(tokens)
        cleaned_text = cleaned_text.replace("HASHTAG", "#").replace("ATUSER", "@")
        return cleaned_text

# Load JSON data
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

# Save cleaned data to JSON
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Cleaned data saved to {filename}")

# Preprocess data
def preprocess_data():
    cleaner = TweetCleaner()

    # Load news data
    news_data = load_json("news_data.json")
    twitter_data = load_json("twitter_data.json")

    cleaned_news = []
    cleaned_tweets = []

    # Clean News Data
    if news_data and "articles" in news_data:
        for article in news_data["articles"]:
            cleaned_text = cleaner.get_cleaned_text(article.get("title", "") + " " + article.get("description", ""))
            cleaned_news.append({"source": article.get("source", {}).get("name", ""), "text": cleaned_text})

    # Clean Twitter Data
    if twitter_data and "data" in twitter_data:
        for tweet in twitter_data["data"]:
            cleaned_text = cleaner.get_cleaned_text(tweet.get("text", ""))
            cleaned_tweets.append({"id": tweet.get("id", ""), "text": cleaned_text})

    # Save cleaned data
    save_json("cleaned_news.json", cleaned_news)
    save_json("cleaned_tweets.json", cleaned_tweets)

    # Convert to DataFrame
    news_df = pd.DataFrame(cleaned_news)
    twitter_df = pd.DataFrame(cleaned_tweets)

    # Merge and Save as CSV
    combined_df = pd.concat([news_df, twitter_df], ignore_index=True)
    combined_df.to_csv("processed_data.csv", index=False)
    print("Data preprocessing completed successfully!")

# Run preprocessing
if __name__ == "__main__":
    preprocess_data()
