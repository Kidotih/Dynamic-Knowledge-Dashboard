import streamlit as st
import os
import datetime
import urllib.parse

from scraper import scrape_articles
from summarizer import summarize_articles  # ✅ includes sentiment now
from analyzer import analyze_keywords
from visualizer import plot_keywords, plot_sentiments
from reporter import save_report

# -------------------------------
# Streamlit App Config
# -------------------------------
st.set_page_config(
    page_title="🧠 Dynamic Knowledge Dashboard",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------
st.title("🧠 Dynamic Knowledge Dashboard")
st.caption("Scrape, summarize, and visualize trending topics — all in one place.")
st.divider()

# -------------------------------
# Topic Input
# -------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "Enter a topic to explore (e.g., Artificial Intelligence, Climate Change, Finance):",
        placeholder="Type a topic here..."
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

        # 2️⃣ Summarizing + Sentiment Analysis
        with st.spinner("🧾 Summarizing and analyzing sentiment..."):
            summaries = summarize_articles(articles)

        # 3️⃣ Keyword Extraction
        with st.spinner("🔎 Extracting keywords..."):
            keywords = analyze_keywords(summaries)

        # -------------------------------
        # Display Articles
        # -------------------------------
        st.divider()
        st.subheader("📰 Latest Articles")

        for article in summaries:
            title = article.get("title", "Untitled")
            url = article.get("url", "#")
            summary = article.get("summary", "")
            sentiment = article.get("sentiment", "N/A")
            polarity = article.get("polarity", 0.0)

            st.markdown(f"### [{title}]({url})")
            st.markdown(f"**Sentiment:** {sentiment} ({polarity:.2f})")
            with st.expander("📝 Read Summary"):
                st.write(summary)
            st.markdown("---")

        # -------------------------------
        # Keyword Visualization
        # -------------------------------
        if keywords:
            st.subheader("🔠 Top Keywords Extracted")

            cols = st.columns(2)
            for i, (word, freq) in enumerate(keywords):
                encoded = urllib.parse.quote(word)
                news_url = f"https://news.google.com/search?q={encoded}"
                with cols[i % 2]:
                    st.markdown(f"• **[{word}]({news_url})** — {freq} mentions")

            with st.spinner("📊 Generating visualizations..."):
                keyword_chart = plot_keywords(keywords, output_dir=data_dir)
                st.image(keyword_chart, caption="Keyword Trends", use_container_width=True)

                sentiment_chart = plot_sentiments(summaries, output_dir=data_dir)
                st.image(sentiment_chart, caption="Sentiment Distribution", use_container_width=True)
        else:
            st.warning("No meaningful keywords found.")

        # -------------------------------
        # Save & Download Section
        # -------------------------------
        with st.spinner("💾 Generating reports..."):
            save_report(summaries, keywords, output_dir=data_dir)

        st.success("✅ Dashboard run complete!")

        # 📦 Aesthetic Download Card
        st.divider()
        with st.container():
            st.markdown(
                """
                <div style="
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
                    ">
                    <h3 style="color:#0d6efd; margin-bottom:10px;">📂 Download Your Reports</h3>
                    <p style="color:#555; margin-bottom:15px;">
                        All processed data and visual insights are available for you to download below.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("### 🧾 Articles Summary")
                st.caption("Detailed summaries and sentiment for each article.")
                st.download_button(
                    label="⬇️ Download Articles CSV",
                    data=open(os.path.join(data_dir, "articles_report.csv"), "rb").read(),
                    file_name="articles_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col_b:
                st.markdown("### 🔠 Keywords Analysis")
                st.caption("Top extracted keywords with their frequency counts.")
                st.download_button(
                    label="⬇️ Download Keywords CSV",
                    data=open(os.path.join(data_dir, "keywords_report.csv"), "rb").read(),
                    file_name="keywords_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col_c:
                st.markdown("### 🧠 Dashboard Data Folder")
                st.caption("Contains visualizations and all exported results.")
                st.download_button(
                    label="📦 Open Data Directory",
                    data="",
                    file_name=f"{data_dir}.zip",
                    mime="application/zip",
                    use_container_width=True
                )

        st.info(f"📁 Reports saved in: `{data_dir}`")

    else:
        st.warning("⚠️ Please enter a topic before running the dashboard.")
