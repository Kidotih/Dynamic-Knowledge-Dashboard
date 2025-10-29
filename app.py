import streamlit as st
import os
import datetime
import urllib.parse
import shutil
import zipfile

from auth import login, signup
from scraper import scrape_articles
from summarizer import summarize_articles
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
# Authentication / Guest Access
# -------------------------------
if "user" not in st.session_state:
    st.sidebar.title("Authentication")
    choice = st.sidebar.selectbox("Choose:", ["Login", "Sign Up", "Continue as Guest"])

    if choice == "Login":
        login()
        st.stop()
    elif choice == "Sign Up":
        signup()
        st.stop()
    else:
        # Guest access
        st.session_state["user"] = {"guest": True}

user_info = st.session_state["user"]
if isinstance(user_info, dict) and user_info.get("guest", False):
    st.sidebar.info("👤 You are using Guest Access")
else:
    st.sidebar.success(f"✅ Logged in as {user_info.get('email')}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

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
    if not topic:
        st.warning("⚠️ Please enter a topic before running the dashboard.")
        st.stop()

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
    if isinstance(user_info, dict) and user_info.get("guest", False):
        st.info("Guest users cannot download reports. Log in to access full features.")
    else:
        with st.spinner("💾 Generating reports..."):
            save_report(summaries, keywords, output_dir=data_dir)

        st.success("✅ Dashboard run complete!")

        # -------------------------------
        # Download Buttons
        # -------------------------------
        st.divider()
        with st.container():
            st.markdown(f"📁 Reports saved in: `{data_dir}`")
            col_a, col_b, col_c = st.columns(3)

            # Articles CSV
            articles_file = os.path.join(data_dir, "articles_report.csv")
            if os.path.exists(articles_file):
                with col_a:
                    st.download_button(
                        label="⬇️ Download Articles CSV",
                        data=open(articles_file, "rb").read(),
                        file_name="articles_report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

            # Keywords CSV
            keywords_file = os.path.join(data_dir, "keywords_report.csv")
            if os.path.exists(keywords_file):
                with col_b:
                    st.download_button(
                        label="⬇️ Download Keywords CSV",
                        data=open(keywords_file, "rb").read(),
                        file_name="keywords_report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

            # ZIP of data folder
            zip_path = f"{data_dir}.zip"
            shutil.make_archive(data_dir, 'zip', data_dir)
            with col_c:
                st.download_button(
                    label="📦 Download Data Folder",
                    data=open(zip_path, "rb").read(),
                    file_name=os.path.basename(zip_path),
                    mime="application/zip",
                    use_container_width=True
                )
