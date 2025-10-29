# visualizer.py
import matplotlib.pyplot as plt
import os

def plot_keywords(keywords, output_dir="data"):
    words, freqs = zip(*keywords[:15])
    plt.figure(figsize=(10, 5))
    plt.barh(words, freqs)
    plt.gca().invert_yaxis()
    plt.title("Top Keywords Frequency")
    plt.xlabel("Frequency")
    plt.tight_layout()

    path = os.path.join(output_dir, "keyword_trends.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_sentiments(summaries, output_dir="data"):
    sentiments = [s.get("sentiment", "N/A") for s in summaries]
    counts = {
        "😊 Positive": sentiments.count("😊 Positive"),
        "😐 Neutral": sentiments.count("😐 Neutral"),
        "☹️ Negative": sentiments.count("☹️ Negative"),
    }

    plt.figure(figsize=(6, 6))
    plt.pie(
        counts.values(),
        labels=counts.keys(),
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Sentiment Distribution")
    plt.tight_layout()

    path = os.path.join(output_dir, "sentiment_distribution.png")
    plt.savefig(path)
    plt.close()
    return path
