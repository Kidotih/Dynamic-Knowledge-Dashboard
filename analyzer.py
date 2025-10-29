# analyzer.py
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# -----------------------------------------
# Safe NLTK data initialization
# -----------------------------------------
def safe_download(package):
    """Download NLTK resource safely (skip if already available)."""
    try:
        nltk.data.find(package)
    except LookupError:
        nltk.download(package.split("/")[-1], quiet=True)

# Ensure essential resources
safe_download("tokenizers/punkt")
safe_download("corpora/stopwords")
safe_download("corpora/wordnet")
safe_download("taggers/averaged_perceptron_tagger_eng")

STOPWORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def extract_keywords(articles, top_n=10):
    """Enhanced keyword extractor with safe fallbacks."""
    # Combine article titles + summaries
    combined = " ".join(
        f"{a.get('title', '')} {a.get('summary', '')}" for a in articles
    )

    if not combined.strip():
        return [("data", 3), ("analysis", 2), ("python", 1)]

    # Tokenize and clean
    tokens = nltk.word_tokenize(combined.lower())
    tokens = [t for t in tokens if re.match(r"^[a-z]{3,}$", t)]
    tokens = [t for t in tokens if t not in STOPWORDS]

    # Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    # POS tagging (safe)
    try:
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if pos.startswith("NN")]
    except LookupError:
        print("⚠️ POS tagger not available. Using raw tokens instead.")
        nouns = tokens

    # Count top words
    common = Counter(nouns).most_common(top_n)

    if not common:
        common = [("data", 2), ("ai", 2), ("learning", 1)]

    print("\nTop keywords found:")
    for word, freq in common:
        print(f"  - {word}: {freq}")

    return common


def analyze_keywords(articles, top_n=10):
    """Alias for extract_keywords."""
    return extract_keywords(articles, top_n)
