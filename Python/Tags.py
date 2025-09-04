import os
import re
import ast
from collections import Counter
import subprocess

def load_stopwords(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(word.strip() for word in f if word.strip())

def get(text):
    words = re.findall(r'\b\w+\b', text.lower())

    path = subprocess.run(
        ["find", os.path.expanduser("~"), "-name", "stopwords.txt"],
        check=True,
        text=True,
        capture_output=True
    )

    try:
        path_ = path.stdout.strip().splitlines()[0]
    except IndexError:
        raise RuntimeError("Stopwords file not found !")

    stopwords = load_stopwords(path_)

    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    common_words = Counter(filtered_words).most_common(20)

    return [word for word, count in common_words]
