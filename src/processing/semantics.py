from sentence_transformers import SentenceTransformer, util

# Load sentence embedding models
# "all-MiniLM-L6-v2" is a fast and lightweight model suitable for semantic
# similarity tasks
minilm = SentenceTransformer("all-MiniLM-L6-v2")

# "all-mpnet-base-v2" is a larger, more accurate model for semantic similarity
mpnet = SentenceTransformer("all-mpnet-base-v2")


def cosine_similarity_mpnet(text1: str, text2: str) -> float:
    # NOTE: Slower but more accurate
    """
    Compute cosine similarity between two texts using the MiniLM model.

    Args:
        text1 (str): The first text string.
        text2 (str): The second text string.

    Returns:
        float: Cosine similarity score between the two texts.
               Ranges from -1.0 to 1.0 (usually between 0.0 to 1.0
               for valid inputs).
    """

    embeddings = mpnet.encode([text1, text2], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return similarity.item()  # returning the cosine similarity score


def cosine_similarity_minilm(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two texts using PyTorch backend.

    This function uses the same MiniLM model but demonstrates a slightly
    different API call.
    Note: It returns similar results as `com_sim`.

    Args:
        text1 (str): The first text input.
        text2 (str): The second text input.

    Returns:
        float: Cosine similarity score, where:
               - 0.0 means unrelated
               - 1.0 means semantically very similar
    """
    embedding1 = minilm.encode(text1, convert_to_tensor=True)
    embedding2 = minilm.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return float(similarity.item())
