import re
import nltk
from nltk.corpus import stopwords


def find_topics(text):
    stop_words = set(stopwords.words("english"))

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z]+\b",
        text.lower()
    )

    useful_words = []

    for word in words:
        if word not in stop_words and len(word) > 3:
            useful_words.append(word)

    frequency = {}

    for word in useful_words:
        frequency[word] = frequency.get(word, 0) + 1

    sorted_words = sorted(
        frequency,
        key=frequency.get,
        reverse=True
    )

    return sorted_words[:10]
