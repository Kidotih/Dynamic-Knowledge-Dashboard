# summarizer.py
import re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure NLTK resources are downloaded only once
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

def summarize_text(text, max_sentences=3):
    if not text or len(text.split()) < 50:
        return text  # Return original if too short

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())

    # Calculate word frequency
    freq = {}
    for word in words:
        if word.isalpha() and word not in stop_words:
            freq[word] = freq.get(word, 0) + 1

    # Normalize frequencies
    max_freq = max(freq.values(), default=1)
    for w in freq:
        freq[w] /= max_freq

    # Score sentences
    sentences = sent_tokenize(text)
    scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    # Pick top sentences
    summary_sents = heapq.nlargest(max_sentences, scores, key=scores.get)
    summary = " ".join(summary_sents)
    return summary

def summarize_articles(articles):
    summarized = []
    for article in articles:
        content = article.get("content", "")
        summary = summarize_text(content)
        summarized.append({
            "title": article.get("title", ""),
            "summary": summary
        })
    return summarized
