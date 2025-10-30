# summarizer.py
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob
import re
import heapq
import streamlit as st

# -----------------------------------------
# Ensure NLTK resources at runtime
# -----------------------------------------
@st.cache_resource
def setup_nltk():
    """Download required NLTK data if missing (safe for deployment)."""
    resources = {
        "punkt": "tokenizers/punkt",
        "punkt_tab": "tokenizers/punkt_tab",
        "stopwords": "corpora/stopwords",
    }
    for package, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)

setup_nltk()

# -----------------------------------------
# Text Cleaning
# -----------------------------------------
def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -----------------------------------------
# Summarization
# -----------------------------------------
def summarize_text(text, max_sentences=3):
    text = clean_text(text)
    if not text or len(text.split()) < 50:
        return text

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())

    freq = {}
    for word in words:
        if word.isalpha() and word not in stop_words:
            freq[word] = freq.get(word, 0) + 1

    if not freq:
        return text

    max_freq = max(freq.values())
    for w in freq:
        freq[w] /= max_freq

    sentences = sent_tokenize(text)
    scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    summary_sents = heapq.nlargest(max_sentences, scores, key=scores.get)
    return " ".join(summary_sents)

# -----------------------------------------
# Summarize Articles with Sentiment
# -----------------------------------------
def summarize_articles(articles):
    summarized = []

    for article in articles:
        raw_content = article.get("content") or article.get("summary") or ""
        summary = summarize_text(raw_content)
        clean_summary = clean_text(summary)

        if clean_summary:
            blob = TextBlob(clean_summary)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                sentiment_label = "😊 Positive"
            elif polarity < -0.1:
                sentiment_label = "☹️ Negative"
            else:
                sentiment_label = "😐 Neutral"
        else:
            sentiment_label = "😐 Neutral"
            polarity = 0.0

        summarized.append({
            "title": article.get("title", "Untitled"),
            "summary": clean_summary,
            "sentiment": sentiment_label,
            "polarity": round(polarity, 2),
            "url": article.get("url", "")
        })

    print(f"✅ Summarized and analyzed {len(summarized)} articles")
    return summarized
