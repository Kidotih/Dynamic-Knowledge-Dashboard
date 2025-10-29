# nltk_setup.py
import nltk

def download_nltk_resources():
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
            print(f"Downloading NLTK resource: {package}")
            nltk.download(package, quiet=True)

if __name__ == "__main__":
    download_nltk_resources()
    print("✅ All NLTK resources are ready.")

