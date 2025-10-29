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
    plt.bar(words, counts, color="#1f77b4", edgecolor="black", linewidth=0.8)
    plt.title("Top Keywords Frequency", fontsize=15, fontweight="bold")
    plt.xlabel("Keywords", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=40, ha="right", fontsize=10)
    plt.tight_layout()

    plot_path = os.path.join(output_dir, "keyword_trends.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✅ Keyword trend chart saved to {plot_path}")
    return plot_path


def plot_sentiments(summaries, output_dir="data"):
    """
    Visualize sentiment distribution (😊 Positive / 😐 Neutral / ☹️ Negative).
    Always shows a chart, even if sentiment data is incomplete.
    """
    import matplotlib.pyplot as plt
    import os

    os.makedirs(output_dir, exist_ok=True)

    counts = {"😊 Positive": 0, "😐 Neutral": 0, "☹️ Negative": 0}
    for s in summaries:
        sentiment = s.get("sentiment", "😐 Neutral")
        if sentiment not in counts:
            sentiment = "😐 Neutral"
        counts[sentiment] += 1

    # Guarantee there's at least one item to show
    total = sum(counts.values())
    if total == 0:
        counts["😐 Neutral"] = 1
        total = 1

    plot_path = os.path.join(output_dir, "sentiment_distribution.png")

    plt.figure(figsize=(6, 6))
    plt.pie(
        counts.values(),
        labels=[f"{k} ({v})" for k, v in counts.items()],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#4CAF50", "#FFC107", "#F44336"],  # Green, Yellow, Red
        wedgeprops={"edgecolor": "black"},
    )
    plt.title("Sentiment Distribution", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"✅ Sentiment chart saved to {plot_path}")
    return plot_path


    # Handle empty sentiment data
    if total == 0:
        plt.figure(figsize=(6, 6))
        plt.text(0.5, 0.5, "No sentiment data available", ha="center", va="center", fontsize=14, color="gray")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        print("⚠️ No sentiment data to plot.")
        return plot_path

    # Pie chart visualization
    plt.figure(figsize=(6, 6))
    plt.pie(
        counts.values(),
        labels=[f"{k} ({v})" for k, v in counts.items()],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#4CAF50", "#FFC107", "#F44336"],  # Green, Yellow, Red
        wedgeprops={"edgecolor": "black"}
    )
    plt.title("Sentiment Distribution", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"✅ Sentiment chart saved to {plot_path}")
    return plot_path
