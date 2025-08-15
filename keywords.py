from typing import List

def extract_keywords(text: str, top_k: int = 10) -> List[str]:
    """
    Uses RAKE (with NLTK stopwords) for phrase keywords.
    Falls back to a simple frequency list if RAKE isn't available.
    """
    if not text or not text.strip():
        return []

    try:
        # Ensure NLTK assets are present
        import nltk
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("stopwords")

        from rake_nltk import Rake
        r = Rake()  # uses English stopwords by default
        r.extract_keywords_from_text(text)
        phrases = r.get_ranked_phrases()[:top_k]
        return [p.strip() for p in phrases if p.strip()]
    except Exception:
        # Fallback: very simple word frequency (no stopword removal)
        words = [w.lower() for w in text.split() if w.isalpha()]
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_k]]
