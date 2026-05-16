from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, List

WORD_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str | None) -> List[str]:
    """Convert text into lowercase searchable tokens."""
    if text is None:
        return []
    return WORD_PATTERN.findall(text.lower())


def calculate_document_frequency(document_tokens: List[List[str]]) -> Dict[str, int]:
    """Count how many documents contain each token."""
    document_frequency: Dict[str, int] = {}

    for tokens in document_tokens:
        for token in set(tokens):
            document_frequency[token] = document_frequency.get(token, 0) + 1

    return document_frequency


def tf_idf_vector(
    tokens: List[str],
    document_frequency: Dict[str, int],
    total_documents: int,
) -> Dict[str, float]:
    """Create a small TF-IDF style vector for a list of tokens."""
    if not tokens:
        return {}

    term_frequency = Counter(tokens)
    vector: Dict[str, float] = {}

    for token, count in term_frequency.items():
        tf = count / len(tokens)
        df = document_frequency.get(token, 0)
        idf = math.log((1 + total_documents) / (1 + df)) + 1
        vector[token] = tf * idf

    return vector


def cosine_similarity(vector_a: Dict[str, float], vector_b: Dict[str, float]) -> float:
    """Calculate cosine similarity between two sparse vectors."""
    common_tokens = set(vector_a) & set(vector_b)
    dot_product = sum(vector_a[token] * vector_b[token] for token in common_tokens)

    magnitude_a = math.sqrt(sum(value * value for value in vector_a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
