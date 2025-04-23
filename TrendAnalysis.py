import pandas as pd
import ast

# Load co-occurrence data from the output file
cooccurrence_data = []

# Read co-occurrence data
with open("cooccurrence_output.txt", "r", encoding="utf-16") as file:
    for line in file:
        pair, count = line.strip().rsplit("\t", 1)
        cooccurrence_data.append({"pair": ast.literal_eval(pair), "count": int(count)})

# Create DataFrame
df = pd.DataFrame(cooccurrence_data)

# Sort by frequency (count) in descending order
df = df.sort_values(by="count", ascending=False)

# Show top 10 trending word pairs
print("Top 10 Trending Word Pairs:")
print(df.head(10))

# Save the sorted data to CSV
df.to_csv("trending_word_pairs.csv", index=False)
print("Trending word pairs saved to trending_word_pairs.csv!")
