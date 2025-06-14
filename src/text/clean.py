import spacy
import string

# Load the English spaCy model (small version)
nlp = spacy.load("en_core_web_sm")


# WARN: Using this with semantic similarity comparisons may
# sometimes result in annomalies.
def lemmatize_text(text):
    """
    Cleans and lemmatizes input text using spaCy.

    Steps performed:
    1. Tokenizes the text using spaCy.
    2. Removes stop words, punctuation, and standalone punctuation characters.
    3. Applies lemmatization to the remaining tokens.
    4. Returns the cleaned text as a space-separated string of lemmas.

    Parameters:
        text (str): The input sentence or paragraph to clean.

    Returns:
        str: A lemmatized and cleaned version of the input text.
    """
    # Process the text with spaCy to get tokens
    doc = nlp(text)

    cleaned = []
    for token in doc:
        # Skip stop words, punctuation, and symbols explicitly in string.punctuation
        if token.is_stop or token.is_punct or token.text in string.punctuation:
            continue
        # Append the lemmatized form of the token
        cleaned.append(token.lemma_)

    return " ".join(cleaned)
