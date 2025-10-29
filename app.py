import streamlit as st
from scraper import scrape_articles
from summarizer import summarize_articles
from analyzer import analyze_keywords
from visualizer import plot_keywords
from reporter import save_report

import os
import datetime

# ----------------------------------------
# Streamlit App Configuration
# ----------------------------------------
st.set_page_config(page_title="Dynamic Knowledge Dashboard", layout="wide")

st.title("🧠 Dynamic Knowledge Dashboard")
st.write("Automatically scrape, summarize, and visualize trending topics from the web.")

# ----------------------------------------
# User Input
# ----------------------------------------
topic = st.text_input("Enter a topic to explore (e.g., Artificial Intelligence, Climate Change, Finance):")

# ----------------------------------------
# Main Process
# ----------------------------------------
if st.button("Run Dashboard"):
    if topic:
        # Step 1: Scrape Articles
        with st.spinner("🔍 Scraping articles..."):
            articles = scrape_articles(topic)

        if not articles:
            st.warning("⚠️ No articles found for this topic. Try another keyword.")
        else:
            # Step 2: Summarize Articles
            with st.spinner("🧾 Summarizing articles..."):
                summaries = summarize_articles(articles)

            # Step 3: Analyze Keywords
            with st.spinner("🔎 Analyzing keywords..."):
                keywords = analyze_keywords(summaries)

            if not keywords:
                st.warning("⚠️ No keywords could be extracted from the summaries.")
            else:
                # Step 4: Visualize Data
                with st.spinner("📊 Visualizing data..."):
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    data_dir = f"data/run_{timestamp}"
                    os.makedirs(data_dir, exist_ok=True)

                    plot_path = plot_keywords(keywords, output_dir=data_dir)

                    if os.path.exists(plot_path):
                        st.image(plot_path, caption="Keyword Trends", use_container_width=True)
                    else:
                        st.warning("⚠️ Trend plot could not be displayed (missing or invalid image).")

            # Step 5: Save Report
            with st.spinner("💾 Saving report..."):
                save_report(articles, keywords, output_dir=data_dir)

            st.success("✅ Dashboard run complete!")
            st.info(f"📂 Reports saved in `{data_dir}`")

    else:
        st.warning("⚠️ Please enter a topic first.")
