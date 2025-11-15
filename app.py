import streamlit as st
import os
import datetime
import urllib.parse
import shutil
import requests
import feedparser
from bs4 import BeautifulSoup


from auth import login, signup
from scraper import scrape_articles
from summarizer import summarize_articles
from analyzer import analyze_keywords
from visualizer import plot_keywords, plot_sentiments
from reporter import save_report

# -------------------------------
# Streamlit Config
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
        st.session_state["user"] = {"guest": True}

user_info = st.session_state["user"]
if user_info.get("guest", False):
    st.sidebar.info("👤 Guest Access")
else:
    st.sidebar.success(f"✅ Logged in as {user_info.get('email')}")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()


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
        "Enter a topic to explore:",
        placeholder="Type a topic here..."
    )
with col2:
    run_dashboard = st.button("🚀 Run Dashboard", use_container_width=True)

# -------------------------------
# Main Logic
# -------------------------------
if run_dashboard:
    if not topic:
        st.warning("⚠️ Please enter a topic.")
        st.stop()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = f"data/run_{timestamp}"
    os.makedirs(data_dir, exist_ok=True)

    # 1️⃣ Scraping
    # 1️⃣ Scraping (deployment-safe)
with st.spinner("🔍 Fetching recent articles..."):
    # Format the topic for URL
    query = topic.replace(" ", "+")
    feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:US"

    headers = {"User-Agent": "Mozilla/5.0"}  # Google requires browser-like headers
    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
    except Exception as e:
        st.warning(f"⚠ Failed to fetch RSS feed: {e}")
        st.stop()

    if not feed.entries:
        st.warning(f"No articles found for topic '{topic}'. Try another keyword or region.")
        st.stop()

    # Process entries
    articles = []
    for entry in feed.entries[:10]:  # Limit to 10 articles
        title = entry.title
        url = entry.link
        summary = entry.get("summary", "")
        published = entry.get("published", "")
        source = getattr(entry, "source", {}).get("title", "") or url.split("/")[2]

        # Optional: fetch full content
        content = summary
        try:
            art_resp = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(art_resp.text, "html.parser")
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            if paragraphs:
                content = " ".join(paragraphs)
        except:
            content = summary

        articles.append({
            "title": title,
            "url": url,
            "summary": summary,
            "content": content,
            "published": published,
            "source": source,
            "image": None
        })


    # 2️⃣ Summarizing + Sentiment
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
    for a in summaries:
        st.markdown(f"### [{a.get('title','Untitled')}]({a.get('url','#')})")
        st.markdown(f"**Sentiment:** {a.get('sentiment','N/A')} ({a.get('polarity',0.0):.2f})")
        with st.expander("📝 Read Summary"):
            st.write(a.get("summary",""))
        st.markdown("---")

    # -------------------------------
    # Keyword Visualization
    # -------------------------------
    if keywords:
        st.subheader("🔠 Top Keywords")
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
    if user_info.get("guest", False):
        st.info("Guest users cannot download reports.")
    else:
        with st.spinner("💾 Generating reports..."):
            save_report(summaries, keywords, output_dir=data_dir)

        st.success("✅ Dashboard run complete!")
        st.divider()
        st.markdown(f"📁 Reports saved in: `{data_dir}`")
        col_a, col_b, col_c = st.columns(3)

        # Articles CSV
        articles_file = os.path.join(data_dir, "articles_report.csv")
        if os.path.exists(articles_file):
            with col_a:
                st.download_button(
                    "⬇️ Download Articles CSV",
                    data=open(articles_file, "rb").read(),
                    file_name="articles_report.csv",
                    mime="text/csv"
                )

        # Keywords CSV
        keywords_file = os.path.join(data_dir, "keywords_report.csv")
        if os.path.exists(keywords_file):
            with col_b:
                st.download_button(
                    "⬇️ Download Keywords CSV",
                    data=open(keywords_file, "rb").read(),
                    file_name="keywords_report.csv",
                    mime="text/csv"
                )

        # ZIP of data folder
        zip_path = f"{data_dir}.zip"
        shutil.make_archive(data_dir, 'zip', data_dir)
        with col_c:
            st.download_button(
                "📦 Download Data Folder",
                data=open(zip_path, "rb").read(),
                file_name=os.path.basename(zip_path),
                mime="application/zip"
            )
