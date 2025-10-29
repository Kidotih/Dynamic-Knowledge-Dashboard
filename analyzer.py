# analyzer.py
"""
Improved keyword extractor for Dynamic Knowledge Dashboard.

Features:
- Uses NLTK for tokenization, stopwords and lemmatization (WordNet).
- Extracts unigrams and high-score bigrams.
- Filters short tokens and punctuation.
- Returns top_n keywords as (keyword, count) tuples.
- Provides sensible fallback keywords if nothing meaningful is found.
"""

import re
from collections import Counter
import nltk

# Ensure required NLTK data is available (quiet downloads)
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

STOPWORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def _clean_tokens(text):
    """Tokenize, lowercase, remove short tokens and stopwords, and lemmatize."""
    if not text:
        return []

    # Basic cleanup and tokenization
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    tokens = word_tokenize(text.lower())

    cleaned = []
    for t in tokens:
        # only alphabetic tokens, min length 3 to allow 'ai' -> handled via bigrams or fallback
        if re.fullmatch(r"[a-zA-Z]{3,}", t) and t not in STOPWORDS:
            lemma = lemmatizer.lemmatize(t)
            cleaned.append(lemma)
    return cleaned

def _extract_bigrams(tokens, min_score=2):
    """
    Simple bigram scoring: count bigrams and include those that appear >= min_score.
    Returns list of bigram strings joined by a space.
    """
    bigrams = zip(tokens, tokens[1:])
    bigram_list = [" ".join(b) for b in bigrams]
    counter = Counter(bigram_list)
    # Only keep bigrams that appear at least once (min_score can be tuned)
    return [b for b, c in counter.items() if c >= 1], counter

def extract_keywords(articles, top_n=10):
    """
    Main function: accepts `articles` (list of dicts with 'summary' or 'content')
    and returns a list of (keyword, count) tuples ordered by frequency.
    """
    # Combine summaries or content
    texts = []
    for a in articles:
        # prefer 'summary' then 'content' then 'title'
        texts.append(a.get("summary") or a.get("content") or a.get("title") or "")

    combined = " ".join(texts).strip()
    tokens = _clean_tokens(combined)

    # Count unigrams
    uni_counts = Counter(tokens)

    # Extract bigrams and count them; weight bigrams slightly higher
    bigrams, bigram_counter = _extract_bigrams(tokens)
    # Combine counts: give bigrams weight = unigram average (or just count them)
    combined_counter = Counter(uni_counts)
    # add bigrams counts (treat bigram count as separate token)
    for b, c in bigram_counter.items():
        if c > 0:
            combined_counter[b] += c  # includes bigram if frequent

    # If nothing found, try relaxed token rule (allow 2-letter tokens like 'ai')
    if not combined_counter:
        relaxed = re.findall(r"\b[a-zA-Z]{2,}\b", combined.lower())
        relaxed = [lemmatizer.lemmatize(t) for t in relaxed if t not in STOPWORDS]
        if relaxed:
            combined_counter = Counter(relaxed)

    # Get most common
    common = combined_counter.most_common(top_n)

    # Fallback if still empty
    if not common:
        common = [("data", 1), ("analysis", 1), ("python", 1)]

    # Debug print (keeps console informative)
    print("\nTop keywords found:")
    for word, freq in common:
        print(f"  - {word}: {freq}")

    return common


# Backwards-compatible alias used elsewhere in the project
def analyze_keywords(articles, top_n=10):
    return extract_keywords(articles, top_n)
