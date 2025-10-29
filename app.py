# app.py
import streamlit as st
import os
import datetime
import urllib.parse

from scraper import scrape_articles
from summarizer import summarize_articles
from analyzer import analyze_keywords
from visualizer import plot_keywords, plot_sentiments
from reporter import save_report
from textblob import TextBlob

# -------------------------------
# Streamlit App Config
# -------------------------------
st.set_page_config(
    page_title="🧠 Dynamic Knowledge Dashboard",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Dynamic Knowledge Dashboard")
st.caption("Scrape, summarize, and visualize trending topics — now with sentiment insight.")

st.divider()

# -------------------------------
# Topic Input Section
# -------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "Enter a topic to explore (e.g., Artificial Intelligence, Climate Change, Finance):"
    )
with col2:
    run_dashboard = st.button("🚀 Run Dashboard", use_container_width=True)

# -------------------------------
# Main Logic
# -------------------------------
if run_dashboard:
    if topic:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        data_dir = f"data/run_{timestamp}"
        os.makedirs(data_dir, exist_ok=True)

        # 1️⃣ Scraping
        with st.spinner("🔍 Fetching recent articles..."):
            articles = scrape_articles(topic)

        if not articles:
            st.warning("No articles found for this topic.")
            st.stop()

        # 2️⃣ Summarizing
        with st.spinner("🧾 Summarizing articles..."):
            summaries = summarize_articles(articles)

        # 3️⃣ Sentiment Analysis
        with st.spinner("💭 Analyzing sentiment..."):
            for item in summaries:
                summary_text = item.get("summary", "")
                if summary_text:
                    blob = TextBlob(summary_text)
                    polarity = blob.sentiment.polarity
                    if polarity > 0.1:
                        sentiment = "😊 Positive"
                    elif polarity < -0.1:
                        sentiment = "☹️ Negative"
                    else:
                        sentiment = "😐 Neutral"
                    item["sentiment"] = sentiment
                    item["polarity"] = round(polarity, 3)
                else:
                    item["sentiment"] = "N/A"
                    item["polarity"] = 0.0

        # 4️⃣ Keyword Extraction
        with st.spinner("🔎 Extracting keywords..."):
            keywords = analyze_keywords(summaries)

        # 5️⃣ Display Articles
        st.divider()
        st.subheader("📰 Latest Articles")
        for article in summaries:
            title = article.get("title", "Untitled")
            url = article.get("url", "#")
            summary = article.get("summary", "")
            sentiment = article.get("sentiment", "N/A")
            polarity = article.get("polarity", 0.0)

            st.markdown(f"### [{title}]({url})")
            st.markdown(f"**Sentiment:** {sentiment} ({polarity})")
            with st.expander("Read Summary"):
                st.write(summary)
            st.markdown("---")

        # 6️⃣ Keyword Visualization
        if keywords:
            st.subheader("🔠 Top Keywords Extracted")
            cols = st.columns(2)
            for i, (word, freq) in enumerate(keywords):
                encoded = urllib.parse.quote(word)
                news_url = f"https://news.google.com/search?q={encoded}"
                with cols[i % 2]:
                    st.markdown(f"• **[{word}]({news_url})** — {freq} occurrences")

            with st.spinner("📊 Generating visualizations..."):
                keyword_chart = plot_keywords(keywords, output_dir=data_dir)
                st.image(keyword_chart, caption="Keyword Trends", use_container_width=True)

                sentiment_chart = plot_sentiments(summaries, output_dir=data_dir)
                st.image(sentiment_chart, caption="Sentiment Distribution", use_container_width=True)
        else:
            st.warning("No meaningful keywords found.")

        # 7️⃣ Save Report
        with st.spinner("💾 Saving report..."):
            save_report(summaries, keywords, output_dir=data_dir)

        st.success("✅ Dashboard run complete!")
        st.info(f"📂 Reports saved in `{data_dir}`")

    else:
        st.warning("Please enter a topic first.")
