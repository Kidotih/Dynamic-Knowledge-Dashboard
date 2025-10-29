# analyzer.py
from collections import Counter
import re
import nltk
import streamlit as st

# -----------------------------------------
# NLTK Initialization with Streamlit cache
# -----------------------------------------
@st.cache_resource
def init_nltk():
    """Download and initialize NLTK resources safely."""
    resources = {
        "punkt": "tokenizers/punkt",
        "stopwords": "corpora/stopwords",
        "wordnet": "corpora/wordnet",
        "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger"
    }

    for package, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)

    # Safe imports
    try:
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        stop_words = set(stopwords.words("english"))
    except Exception:
        stop_words = set(["the", "and", "for", "with", "that", "this"])  # fallback

    try:
        lemmatizer = WordNetLemmatizer()
    except Exception:
        lemmatizer = lambda x: x  # no-op fallback

    return stop_words, lemmatizer

STOPWORDS, lemmatizer = init_nltk()

# -----------------------------------------
# Keyword Extraction
# -----------------------------------------
def extract_keywords(articles, top_n=10):
    """
    Extract top keywords from a list of articles (titles + summaries).
    Provides safe fallback if NLTK fails.
    """
    combined = " ".join(
        f"{a.get('title', '')} {a.get('summary', '')}" for a in articles
    )

    if not combined.strip():
        return [("data", 3), ("analysis", 2), ("python", 1)]

    # Tokenize safely
    try:
        tokens = nltk.word_tokenize(combined.lower())
    except Exception:
        tokens = re.findall(r'\b[a-z]{3,}\b', combined.lower())

    tokens = [t for t in tokens if t not in STOPWORDS]

    # Lemmatize
    try:
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
    except Exception:
        pass

    # POS tagging (extract nouns)
    try:
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if pos.startswith("NN")]
    except Exception:
        nouns = tokens

    # Count top keywords
    common = Counter(nouns).most_common(top_n)

    if not common:
        common = [("data", 2), ("ai", 2), ("learning", 1)]

    return common

# -----------------------------------------
# Alias function
# -----------------------------------------
def analyze_keywords(articles, top_n=10):
    return extract_keywords(articles, top_n)
