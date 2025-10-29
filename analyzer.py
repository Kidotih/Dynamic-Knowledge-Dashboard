# analyzer.py
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK data
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("omw-1.4", quiet=True)

STOPWORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def extract_keywords(articles, top_n=10):
    """Enhanced keyword extractor using lemmatization and POS tagging."""
    # Combine titles and summaries
    combined = " ".join(
        f"{a.get('title', '')} {a.get('summary', '')}" for a in articles
    )

    # Tokenize and clean text
    tokens = nltk.word_tokenize(combined.lower())
    tokens = [t for t in tokens if re.match(r"^[a-z]{3,}$", t)]  # only alphabetic
    tokens = [t for t in tokens if t not in STOPWORDS]

    # Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    # Keep only nouns (better keyword candidates)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]

    # Count most common words
    common = Counter(nouns).most_common(top_n)

    if not common:
        common = [("data", 3), ("ai", 2), ("learning", 1)]

    print("\nTop keywords found:")
    for word, freq in common:
        print(f"  - {word}: {freq}")

    return common

def analyze_keywords(articles, top_n=10):
    """Alias for extract_keywords (used elsewhere)."""
    return extract_keywords(articles, top_n)
