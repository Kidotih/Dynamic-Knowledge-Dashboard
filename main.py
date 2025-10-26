# main.py
import os
import datetime
from scraper import scrape_articles
from summarizer import summarize_articles
from analyzer import extract_keywords
from visualizer import plot_keywords
from reporter import save_report

# === Create a timestamped data folder ===
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
data_dir = f"data/run_{timestamp}"
os.makedirs(data_dir, exist_ok=True)

def run_dashboard():
    print("Scraping articles...")
    articles = scrape_articles()

    print("Summarizing articles...")
    articles = summarize_articles(articles)

    print("Analyzing keywords...")
    keywords = extract_keywords(articles)

    print("\nTop keywords found:")
    for word, freq in keywords:
        print(f"  - {word}: {freq}")

    print("Visualizing data...")
    plot_keywords(keywords, output_dir=data_dir)

    print("Saving reports...")
    save_report(articles, keywords, output_dir=data_dir)

    print("\n✅ Dynamic Knowledge Dashboard run complete!")
    print(f"📁 All files saved in: {data_dir}")

if __name__ == "__main__":
    run_dashboard()
