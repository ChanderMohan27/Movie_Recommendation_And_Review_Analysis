import numpy as np 
import pandas as pd
import sys

sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
from logger import logging
from utils import YamlReader
import string
string.punctuation
import nltk
nltk.download('stopwords')
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer


class text_cleaner():
    def __init__(self):
        self.reader = YamlReader()
    
    def remove_tags_stopword(self, text):
        logging.info("Using remove_tags_stopword function to do review text cleaning")
        cleaned_text = text.replace('<br />', '')
        nopunc = [x for x in cleaned_text if x not in string.punctuation]
        nopunc = ''.join(nopunc)
        from nltk.corpus import stopwords
        stpwrd = [char for char in nopunc if char not in stopwords.words('english')]
        stpwrd = ''.join(stpwrd)
        return stpwrd
    
    def convert_slang(self, text):
        words = word_tokenize(text)
        converted_words = []
        logging.info("Replacing words with there synonyms words")
        for word in words:
            # Get synonyms for the current word
            synonyms = wordnet.synsets(word)
            
            # Use the first synonym as replacement (if available)
            replacement = synonyms[0].lemmas()[0].name() if synonyms else word
            converted_words.append(replacement)

        converted_text = " ".join(converted_words)

        return converted_text
    

if __name__ == "__main__":
    # Read configuration parameters

    reader = YamlReader()
    config = reader.read_param()

    review_data_path = config["source_data"]["imdb_data"]

    cleaned_data_path = config["artifacts"]["imdb_review"]

    a = text_cleaner() 

    df = pd.read_csv(review_data_path)
    df = df[0:10000]
    df["cleaned_review"] = df["review"].apply(a.remove_tags_stopword)

    # df["cleaned_review"] = df["cleaned_review"].apply(a.convert_slang)

    df.to_csv(cleaned_data_path, index=False)


