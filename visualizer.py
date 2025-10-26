# visualizer.py
import os
import matplotlib.pyplot as plt

def plot_keywords(keywords, output_dir="data"):
    if not keywords:
        print("⚠️ No keywords found to visualize.")
        return

    os.makedirs(output_dir, exist_ok=True)

    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:10]
    words, counts = zip(*keywords)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title("Top Keywords Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "keyword_trends.png"))
    plt.close()

    print(f"✅ Keyword trend chart saved to {output_dir}/keyword_trends.png")

