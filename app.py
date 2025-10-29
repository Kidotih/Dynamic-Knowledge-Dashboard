import os
import streamlit as st
from scraper import fetch_articles
from summarizer import summarize_articles
from keywords import extract_keywords
from visualizer import plot_keywords, plot_sentiments
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="🧠 Dynamic Knowledge Dashboard", layout="wide")

st.title("🧠 Dynamic Knowledge Dashboard")
st.markdown("Scrape, summarize, and visualize trending topics — all in one place.")

# --- Input Section ---
topic = st.text_input("Enter a topic to explore (e.g., Artificial Intelligence, Climate Change, Finance):")

if st.button("Analyze Topic") and topic:
    with st.spinner("Fetching and analyzing articles..."):
        # Fetch articles
        articles = fetch_articles(topic)
        summaries = summarize_articles(articles)

        # Create output directory
        run_id = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join("data", run_id)
        os.makedirs(output_dir, exist_ok=True)

        # Extract and visualize keywords
        keywords = extract_keywords([s["summary"] for s in summaries])
        keyword_chart = plot_keywords(keywords, output_dir)

        # Sentiment visualization
        sentiment_chart = plot_sentiments(summaries, output_dir)

        st.success("✅ Dashboard run complete!")

        # --- Articles Section ---
        st.header("📰 Latest Articles")
        for s in summaries:
            st.markdown(f"**{s['title']}**")
            st.markdown(f"Sentiment: {s['sentiment']} ({s['polarity']})")
            with st.expander("📝 Read Summary"):
                st.write(s["summary"])

        # --- Keyword Visualization ---
        st.header("🔠 Top Keywords Extracted")
        for word, count in keywords[:10]:
            st.markdown(f"• **{word}** — {count} mentions")

        # --- Charts Section ---
        st.header("📊 Visual Insights")

        if os.path.exists(keyword_chart):
            st.image(Image.open(keyword_chart), caption="Keyword Trends", use_container_width=True)
        else:
            st.warning("⚠️ Keyword trend chart not found.")

        if os.path.exists(sentiment_chart):
            st.image(Image.open(sentiment_chart), caption="Sentiment Distribution", use_container_width=True)
        else:
            st.warning("⚠️ Sentiment distribution chart not found.")

        # --- Download Section ---
        st.header("📂 Download Your Reports")
        st.markdown("All processed data and visual insights are available for you to download below.")
        st.markdown(f"📁 Reports saved in: `{output_dir}`")

else:
    st.info("👆 Enter a topic above and click **Analyze Topic** to start.")
