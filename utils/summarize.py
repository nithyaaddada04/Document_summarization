from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extractive_summary(text: str, sentences: int = 5) -> str:
    """
    Robust, lightweight extractive summary using LexRank (Sumy).
    No GPUs or heavy models required.
    """
    if not text or not text.strip():
        return "No text to summarize."

    # Guard against extremely short content
    words = text.split()
    if len(words) < 40:
        return text.strip() if len(words) <= sentences * 20 else " ".join(words[: sentences * 20])

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    sents = summarizer(parser.document, sentences)
    return " ".join(str(s) for s in sents) or "Summary could not be generated."
