# visualizer.py
import os
import matplotlib.pyplot as plt

def plot_keywords(keywords, output_dir="data"):
    """
    Plots a bar chart of top keywords and their frequencies.
    Returns the full path to the saved image file.
    """
    if not keywords:
        print("⚠️ No keywords found to visualize.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    # Sort and select top 10 keywords
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:10]
    words, counts = zip(*keywords)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="#4a90e2", edgecolor="black")
    plt.title("Top Keyword Frequency", fontsize=14)
    plt.xlabel("Keywords", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save and close the plot
    plot_path = os.path.join(output_dir, "keyword_trends.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"✅ Keyword trend chart saved to {plot_path}")
    return plot_path
