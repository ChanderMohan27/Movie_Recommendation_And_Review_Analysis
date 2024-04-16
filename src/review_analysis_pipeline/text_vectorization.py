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
from text_cleaning import text_cleaner
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pickle 
class model_trainer():

    def __init__(self):
        self.reader = YamlReader()

    
    def vectorization_model_training(self,data):
        

        df = pd.read_csv(data)
        reviews = df["cleaned_review"]
        
        logging.info("implimenting CountVectorizer on cleaned Review list")
        bow_transformer = CountVectorizer(analyzer='word').fit(reviews)

        reviews_bow = bow_transformer.transform(reviews)

        sparsity = (100.0 * reviews_bow.nnz / (reviews_bow.shape[0] * reviews_bow.shape[1]))

        tfidf_transformer = TfidfTransformer().fit(reviews_bow)

        #To transform the entire bag-of-words corpus into TF-IDF corpus at once
        logging.info("Transforming Count Vectors into tfidf corpus")
        reviews_tfidf = tfidf_transformer.transform(reviews_bow)

        model = MultinomialNB().fit(reviews_tfidf, df['sentiment'])

        msg_train, msg_test, label_train, label_test = train_test_split(reviews,df['sentiment'], test_size=0.2)
        
        logging.info("Creating Pipeline to do classification of Review (Sentiment Analysis)")
        pipeline = Pipeline([
                    ('bow', CountVectorizer(analyzer='word')),  # strings to token integer counts
                    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
                    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
                            ])
        
        # Training the pipeline on the training Data 
        
        pipeline.fit(msg_train,label_train)

        logging.info("Pipeline Created....")

        return pipeline
    
if __name__=="__main__":

    reader = YamlReader()

    config = reader.read_param()

    data_path = config["artifacts"]["imdb_review"]
    pipeline_path = config["artifacts"]["review_pipeline"]
    train = model_trainer()

    prediction_pipeline = train.vectorization_model_training(data_path)
    
    with open(pipeline_path, 'wb') as file:
        pickle.dump(prediction_pipeline, file)





