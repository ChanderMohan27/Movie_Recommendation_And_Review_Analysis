import pandas as pd
import pickle
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src/review_analysis_pipeline")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/API")
import requests
from logger import logging
from utils import YamlReader
from text_cleaning import text_cleaner
from text_vectorization import model_trainer
import pickle
import os
class sentiment_prediction:
    def __init__(self):
        self.reader = YamlReader()

    def prediction(self,text):
        
        logging.info("Doing Sentiment Analysis for Movie Review")
        config = self.reader.read_param()
        model_path = config["artifacts"]["review_pipeline"]

        # Loading Sentiment analysis prediction model 

        with open(model_path, 'rb') as file:
            saved_pipeline = pickle.load(file)

        # Cleaning Review by using text cleaning functions 

        data_cleaner = text_cleaner()
        logging.info("Doing Review's text preprocessing by removing stop words and other text preprocessing")
        remove_punctuation = data_cleaner.remove_tags_stopword(text)

        # clean_text = data_cleaner.convert_slang(remove_punctuation)

        clean_text_series = pd.Series(remove_punctuation)
        # Doing prediction on the basis of sentiment analysis model 
        
        prediction = saved_pipeline.predict(clean_text_series)

        prediction = prediction[0]
        logging.info("Getting Review's Sentiment Analysis")

        return prediction 
    
if __name__ == "__main__":
    text = "_Four Weddings and a Funeral Except the Weddings Were Actually Just Extra Funerals.__Final rating:★★½ - Had a lot that appealed to me, didn’t quite work as a whole._"
    reader = YamlReader()    
    config = reader.read_param()
    model_path = config["artifacts"]["review_pipeline"]


    predict_pipeline = sentiment_prediction()

    predicted_text = predict_pipeline.prediction(text)

    print(predicted_text)






