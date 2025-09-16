import re
import ast
from collections import Counter
import os

def load_stopwords(path):
    """
    Loads stopwords from a given file path.
    The file should contain a list of words in Python literal syntax.
    """
    with open(path, "r", encoding="utf-8") as f:
        return set(ast.literal_eval(f.read()))

def get(text):
    """
    Extracts the most common relevant keywords from the input text.
    """
    # Use regex to find all words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Get the path to stopwords.txt in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stopwords_path = os.path.join(current_dir, "stopwords.txt")
    
    # Load all stopwords from the file
    try:
        all_stopwords = load_stopwords(stopwords_path)
    except FileNotFoundError:
        raise RuntimeError(
            f"Stopwords file not found at: {stopwords_path}\n"
            "Please create stopwords.txt in the project directory."
        )
    
    # Filter words: remove stopwords and short words
    filtered_words = [
        word for word in words 
        if word not in all_stopwords and len(word) > 3
    ]
    
    # Find the 20 most common words
    common_words = Counter(filtered_words).most_common(20)
    
    # Return only the words, not the counts
    return [word for word, count in common_words]

# Example usage for testing:
if __name__ == "__main__":
    sample_text = "This is a sample text to test the tagging function with various words."
    tags = get(sample_text)
    print("Generated tags:", tags)