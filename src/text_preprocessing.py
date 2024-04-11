import pandas as pd
import logging
import pickle
from utils import YamlReader
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextPreprocessing:
    def __init__(self, dataset):
        self.reader = YamlReader()
        self.ps = PorterStemmer()
        self.dataset = dataset
    
    def string_to_list(self, s):
        """Convert a string representation of a list to a Python list."""
        return ast.literal_eval(s)
    
    def stemming(self, text):
        """Apply stemming to text."""
        words = [self.ps.stem(i) for i in text.split()]
        return " ".join(words)
    
    def text_processing(self):
        """Perform text preprocessing and calculate similarity matrix."""
        data = pd.read_csv(self.dataset)

        # Convert string representation of lists to actual lists
        data["tags"] = data["tags"].apply(self.string_to_list)

        # Convert lists to string, lowercase, and apply stemming
        data["tags"] = data["tags"].apply(lambda x: " ".join(x))
        data["tags"] = data["tags"].str.lower()
        data["tags"] = data["tags"].apply(self.stemming)

        # Vectorize text data
        cv = CountVectorizer(max_features=5000, stop_words="english")
        vectors = cv.fit_transform(data["tags"]).toarray()

        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(vectors)

        return similarity_matrix
    
if __name__ == "__main__":

    # Read configuration parameters
    reader = YamlReader()
    config = reader.read_param()

    # Extract file paths from configuration
    cleaned_data = config["artifacts"]["cleaned_data"]
    similarity_path = config["artifacts"]["similarity"]

    # Initialize text preprocessing class 
    text_preprocessor = TextPreprocessing(cleaned_data)

    # Perform text processing and calculate similarity matrix
    similarity_matrix = text_preprocessor.text_processing()

    # Save similarity matrix to file
    with open(similarity_path, "wb") as file:
        pickle.dump(similarity_matrix, file)

    logging.info("Similarity matrix saved successfully.")
