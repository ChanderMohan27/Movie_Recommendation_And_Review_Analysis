import pandas as pd
import pickle
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/API")
import requests
from logger import logging
from data_cleaning import data_cleaner
from utils import YamlReader
from text_preprocessing import TextPreprocessing
from movie_search import MovieInfo     
import os
from dotenv import load_dotenv 
from sentiment import sentiment_prediction
from review_api import Review_info
# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

class Recommendation:
    def __init__(self, dataset, similarity):
        self.dataset = dataset 
        self.similarity = similarity
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        

 
    
    def fetch_movie_details(self, movie_id): 
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return { 
            'release_date': data.get('release_date', ''),
            'overview': data.get('overview', ''),
            'vote_average': data.get('vote_average', ''),
            'vote_count': data.get('vote_count', ''),
            'popularity': data.get('popularity', ''),
            'original_language': data.get('original_language', '')
        } 
    
    def fetch_poster(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        data = requests.get(url, headers=self.headers)
        data = data.json()
        poster_path = data['poster_path'] 
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path 

    def get_review_list(self, movie_id):

        review = Review_info()
        review_prediction = []
     
        all_reviews = review.get_movie_reviews(movie_id)

        sentiment_analysis = sentiment_prediction()
        
        for review in all_reviews:

            if review != "Movie Review Not Avilable":
                # Getting sentiment analysis for each review by user
                predict = sentiment_analysis.prediction(review)
                review_prediction.append((review,predict))

            else:
                review_prediction.append((review,""))

        return review_prediction 

    def recommend(self, movie):
        data = pd.read_csv(self.dataset)
        recommended_movies = [] 
        recommended_posters = []
        recommended_details = []
        all_movie_reviews = [] 
        movie_search = MovieInfo() 
        movie_info = movie_search.get_movie_info(movie) 
        movie_name_id = movie_info["movie_id"] 
        movie_index = data[data["movie_id"] == movie_name_id].index[0] 
        moive_review = self.get_review_list(movie_name_id)
        poster_url = self.fetch_poster(movie_name_id) 
        if poster_url: 
            recommended_posters.append(poster_url)
        else:
            pass
        recommended_movies.append(movie_info['title'])
        details = self.fetch_movie_details(movie_name_id) 
        recommended_details.append(details)
        all_movie_reviews.append(moive_review) 

        # Calucalting distance according to the movie index 

        distances = self.similarity[movie_index] 
        movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
        for i in movies_list:   
            movie_id = data.iloc[i[0]].movie_id 
            poster_url = self.fetch_poster(movie_id)
            moive_review = self.get_review_list(movie_id)
            if poster_url:
                recommended_posters.append(poster_url)
            else:
                pass
            recommended_movies.append(data.iloc[i[0]]['title'])
            details = self.fetch_movie_details(movie_id)
            recommended_details.append(details)
            all_movie_reviews.append(moive_review) 
        return recommended_movies, recommended_posters, recommended_details, all_movie_reviews
    
    


class SimilarityCalculator: 

    def __init__(self, dataset, similarity_file):
        self.reader = YamlReader()
        self.dataset = dataset
        self.similarity_file = similarity_file

        
    def calculate_similarity(self, movie_title):
        config = self.reader.read_param() 
        data = pd.read_csv(self.dataset) 
        clean_data_path = config["artifacts"]["cleaned_data"]
        movie_search = MovieInfo()
        movie_info = movie_search.get_movie_info(movie_title) 
        movie_name_id = movie_info["movie_id"]

        # cleaned_data = pd.read_csv(clean_data_path)
        if movie_name_id in data["movie_id"].to_list(): 
            with open(self.similarity_file, 'rb') as file:
                similarity_matrix = pickle.load(file) 

        else: 

            # movie_info = movie_search.get_movie_info(movie_title) 
            new_df = pd.DataFrame(movie_info, index=[0])
        
            dataa = pd.concat([data, new_df], ignore_index=True) 
            # print(data)
            dataa.to_csv(self.dataset, index=False)

            data_cleanerr = data_cleaner() 

            cleaned_data = data_cleanerr.cleaning(self.dataset) 

            cleaned_data.to_csv(clean_data_path, index = False)

            text_processor = TextPreprocessing(clean_data_path)
        
            similarity_matrix = text_processor.text_processing()


            with open(self.similarity_file, "wb") as file:
                pickle.dump(similarity_matrix, file)
        
        return similarity_matrix


if __name__ == "__main__":
    movie_name = "Welcome to the Jungle"

    # Read configuration parameters
    reader = YamlReader()
    config = reader.read_param()

    # Extract file paths from configuration
    raw_data = config["artifacts"]["raw_data"]
    cleaned_data_path = config["artifacts"]["cleaned_data"]
    similarity_vector = config["artifacts"]["similarity"]
    model_path = config["artifacts"]["review_pipeline"]

    # Calculate or load similarity matrix
    similarity_calculator = SimilarityCalculator(raw_data, similarity_vector) 
    similarity_matrix = similarity_calculator.calculate_similarity(movie_name) 

    # Recommend top 5 movies
    recommender = Recommendation(cleaned_data_path, similarity_matrix)

    recommended_movies,b,c, movie_review = recommender.recommend(movie_name)

    # Print recommended movies
    # print("#" * 40)
    # print("#" * 40)
    # print("#" * 40)
    # print(movie_review)
    # print(f"Top 5 Movies based on {movie_name}:\n")
    # # for recommended_movie in recommended_movies:
    #     print(recommended_movie)
    print("#" * 40)
    print("#" * 40)
    print("#" * 40)
