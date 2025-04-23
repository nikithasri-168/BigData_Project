import pandas as pd
import ast
import matplotlib.pyplot as plt
 
# Load the CSV
df = pd.read_csv("trending_word_pairs.csv")
 
# Parse the 'pair' column from string to list using literal_eval
def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val
 
df["pair"] = df["pair"].apply(safe_literal_eval)
 
# Sort the dataframe by 'count' to get the most frequent word pairs
df_sorted = df.sort_values(by='count', ascending=False)
 
# Select top N pairs for plotting (e.g., top 50 or top 100)
top_n = 30
df_top = df_sorted.head(top_n)
 
# Create a list of word pairs and their counts
pairs = [' - '.join(pair) for pair in df_top["pair"]]
counts = df_top["count"]
 
# Plot the bar chart
plt.figure(figsize=(12, 8))
plt.barh(pairs, counts, color='skyblue')
plt.xlabel("Frequency")
plt.ylabel("Word Pairs")
plt.title(f"Trending Words")
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()