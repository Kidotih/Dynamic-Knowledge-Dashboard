from collections import Counter
import re
import nltk
import streamlit as st

# NLTK Initialization
@st.cache_resource
def init_nltk():
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

    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    return set(stopwords.words("english")), WordNetLemmatizer()

STOPWORDS, lemmatizer = init_nltk()

# Extract keywords
def extract_keywords(articles, top_n=10):
    combined = " ".join(f"{a.get('title', '')} {a.get('summary', '')}" for a in articles)

    if not combined.strip():
        return [("data", 3), ("analysis", 2), ("python", 1)]

    try:
        tokens = nltk.word_tokenize(combined.lower())
    except Exception:
        tokens = re.findall(r'\b[a-z]{3,}\b', combined.lower())

    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    try:
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if pos.startswith("NN")]
    except Exception:
        nouns = tokens

    common = Counter(nouns).most_common(top_n)
    if not common:
        common = [("data", 2), ("ai", 2), ("learning", 1)]

    return common

def analyze_keywords(articles, top_n=10):
    return extract_keywords(articles, top_n)
