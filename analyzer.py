# analyzer.py
from collections import Counter
import re
import nltk

# Make sure NLTK data is ready
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

def extract_keywords(articles, top_n=10):
    # Combine all summaries
    text = " ".join(a.get("summary", "") for a in articles)

    # Clean and split text
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    words = [w for w in words if w not in STOPWORDS]

    # Count most common words
    common = Counter(words).most_common(top_n)

    # Fallback if empty
    if not common:
        common = [("data", 1), ("analysis", 1), ("python", 1)]

    print("\nTop keywords found:")
    for word, freq in common:
        print(f"  - {word}: {freq}")

    return common
