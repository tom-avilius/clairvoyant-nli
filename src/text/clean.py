import spacy
import string

nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    doc = nlp(text)
    cleaned = []
    for token in doc:
        if token.is_stop or token.is_punct or token.text in string.punctuation:
            continue
        cleaned.append(token.lemma_)
    return " ".join(cleaned)
