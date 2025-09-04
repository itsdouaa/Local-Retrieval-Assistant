import re
import ast
from collections import Counter

def load_stopwords(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(ast.literal_eval(f.read()))

def get(text):
    words = re.findall(r'\b\w+\b', text.lower())

    stopwords = load_stopwords("/home/douaa/assistant/stopwords.txt")

    filtered_words = [word for word in words if word not in french_stopwords and word not in english_stopwords and word not in arabic_stopwords and len(word) > 3]
    common_words = Counter(filtered_words).most_common(20)

    return [word for word, count in common_words]
