# visualizer.py
import os
import matplotlib.pyplot as plt

def plot_keywords(keywords, output_dir="data"):
    """Visualize top keyword frequencies as a bar chart."""
    if not keywords:
        print("⚠️ No keywords found to visualize.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:10]
    words, counts = zip(*keywords)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="#5B8FF9", edgecolor="black", linewidth=0.8)
    plt.title("Top Keywords Frequency", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plot_path = os.path.join(output_dir, "keyword_trends.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"✅ Keyword trend chart saved to {plot_path}")
    return plot_path


def plot_sentiments(summaries, output_dir="data"):
    """
    Visualize sentiment distribution (Positive / Neutral / Negative).
    summaries: list of dicts containing {'sentiment': label, 'polarity': float}
    """
    os.makedirs(output_dir, exist_ok=True)

    # Count sentiment labels
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for s in summaries:
        sentiment = s.get("sentiment", "Neutral")
        if sentiment in counts:
            counts[sentiment] += 1

    total = sum(counts.values())
    plot_path = os.path.join(output_dir, "sentiment_distribution.png")

    if total == 0:
        # Handle empty sentiment data gracefully
        plt.figure(figsize=(6, 6))
        plt.text(0.5, 0.5, "No sentiment data", ha="center", va="center", fontsize=14, color="gray")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        print("⚠️ No sentiment data to plot.")
        return plot_path

    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(
        counts.values(),
        labels=[f"{k} ({v})" for k, v in counts.items()],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#4CAF50", "#FFC107", "#F44336"],  # Green, Yellow, Red
    )
    plt.title("Sentiment Distribution", fontsize=14)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    print(f"✅ Sentiment chart saved to {plot_path}")
    return plot_path
