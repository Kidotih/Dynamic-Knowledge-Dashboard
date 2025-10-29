import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def save_report(articles, keywords, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------
    # 1️⃣ Save CSV files
    # -------------------------------
    articles_df = pd.DataFrame(articles)
    articles_csv = os.path.join(output_dir, "articles_report.csv")
    articles_df.to_csv(articles_csv, index=False)

    keywords_df = pd.DataFrame(keywords, columns=["Keyword", "Count"])
    keywords_csv = os.path.join(output_dir, "keywords_report.csv")
    keywords_df.to_csv(keywords_csv, index=False)

    # -------------------------------
    # 2️⃣ Generate HTML summary
    # -------------------------------
    html_path = os.path.join(output_dir, "summary_report.html")
    keyword_chart = os.path.join(output_dir, "keyword_trends.png")
    sentiment_chart = os.path.join(output_dir, "sentiment_distribution.png")

    html_content = f"""
    <html>
    <head>
        <title>Dynamic Knowledge Dashboard Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2C3E50; }}
            h2 {{ color: #34495E; }}
            img {{ width: 100%; max-width: 600px; margin: 10px 0; border-radius: 8px; }}
            .meta {{ font-size: 12px; color: #777; }}
        </style>
    </head>
    <body>
        <h1>🧠 Dynamic Knowledge Dashboard Report</h1>
        <p class="meta">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <h2>📊 Keyword Trends</h2>
        <img src="{os.path.basename(keyword_chart)}" alt="Keyword Chart">

        <h2>💭 Sentiment Distribution</h2>
        <img src="{os.path.basename(sentiment_chart)}" alt="Sentiment Chart">

        <h2>📰 Articles Summary</h2>
        {articles_df[['title', 'sentiment', 'summary']].to_html(index=False, escape=False)}

        <h2>🔠 Keywords Extracted</h2>
        {keywords_df.to_html(index=False, escape=False)}

        <p class="meta">© Dynamic Knowledge Dashboard</p>
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # -------------------------------
    # 3️⃣ Generate PDF (optional, using reportlab)
    # -------------------------------
    pdf_path = os.path.join(output_dir, "summary_report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("🧠 Dynamic Knowledge Dashboard Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    if os.path.exists(keyword_chart):
        story.append(Image(keyword_chart, width=400, height=250))
        story.append(Spacer(1, 12))

    if os.path.exists(sentiment_chart):
        story.append(Image(sentiment_chart, width=400, height=250))
        story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Articles Summary</b>", styles["Heading2"]))
    for _, row in articles_df.iterrows():
        story.append(Paragraph(f"<b>{row.get('title', 'Untitled')}</b>", styles["Normal"]))
        story.append(Paragraph(f"Sentiment: {row.get('sentiment', 'N/A')} ({row.get('polarity', 0.0)})", styles["Normal"]))
        story.append(Paragraph(row.get('summary', ''), styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)

    # -------------------------------
    # 4️⃣ Completion message
    # -------------------------------
    print(f"✅ Reports saved in: {output_dir}/")
    print(f" - CSV: {articles_csv}, {keywords_csv}")
    print(f" - HTML: {html_path}")
    print(f" - PDF: {pdf_path}")

    return {
        "csv": [articles_csv, keywords_csv],
        "html": html_path,
        "pdf": pdf_path
    }
