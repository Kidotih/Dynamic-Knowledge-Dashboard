import streamlit as st
from scraper import scrape_articles
from summarizer import summarize_articles
from analyzer import analyze_keywords
from visualizer import plot_keywords
from reporter import save_report

import os
import datetime

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Dynamic Knowledge Dashboard", layout="wide")

st.title("🧠 Dynamic Knowledge Dashboard")
st.write("Automatically scrape, summarize, and visualize trending topics from the web.")

# Topic Input
topic = st.text_input("Enter a topic to explore (e.g., Artificial Intelligence, Climate Change, Finance):")

if st.button("Run Dashboard"):
    if topic:
        with st.spinner("🔍 Scraping articles..."):
            articles = scrape_articles(topic)
        
        if not articles:
            st.warning("No articles found for this topic.")
        else:
            with st.spinner("🧾 Summarizing articles..."):
                summaries = summarize_articles(articles)

            with st.spinner("🔎 Analyzing keywords..."):
                keywords = analyze_keywords(summaries)

            if not keywords:
                st.warning("No keywords extracted.")
            else:
                with st.spinner("📊 Visualizing data..."):
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    data_dir = f"data/run_{timestamp}"
                    os.makedirs(data_dir, exist_ok=True)
                    
                    plot_path = plot_keywords(keywords, output_dir=data_dir)
                    st.image(plot_path, caption="Keyword Trends", use_column_width=True)

            with st.spinner("💾 Saving reports..."):
                save_reports(articles, keywords, output_dir=data_dir)

            st.success("✅ Dashboard run complete!")
            st.info(f"Reports saved in `{data_dir}`")
    else:
        st.warning("Please enter a topic first.")
