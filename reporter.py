# reporter.py
import os
import pandas as pd

def save_report(articles, keywords, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    # Save articles summaries
    articles_df = pd.DataFrame(articles)
    articles_df.to_csv(os.path.join(output_dir, "articles_report.csv"), index=False)

    # Save keywords
    keywords_df = pd.DataFrame(keywords, columns=["Keyword", "Count"])
    keywords_df.to_csv(os.path.join(output_dir, "keywords_report.csv"), index=False)

    print(f"✅ Reports saved in {output_dir}/")

