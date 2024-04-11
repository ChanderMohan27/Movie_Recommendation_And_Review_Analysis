import pandas as pd
import pickle
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/API")

from logger import logging
from data_cleaning import data_cleaner
from utils import YamlReader
from text_preprocessing import TextPreprocessing
from movie_search import MovieInfo     


class Recommendation:
    def __init__(self, dataset, similarity):
        self.dataset = dataset
        self.similarity = similarity

    def recommend(self, movie):

        data = pd.read_csv(self.dataset)
        
        movie_index = data[data["title"] == movie].index[0]

        distances = self.similarity[movie_index]
        movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [data.iloc[i[0]]['title'] for i in movies_list]
        return recommended_movies


class SimilarityCalculator: 
    def __init__(self, dataset, similarity_file):
        self.reader = YamlReader()
        self.dataset = dataset
        self.similarity_file = similarity_file

    def calculate_similarity(self, movie_title):
        config = self.reader.read_param() 
        data = pd.read_csv(self.dataset)
        clean_data_path = config["artifacts"]["cleaned_data"]

        # cleaned_data = pd.read_csv(clean_data_path)
        if movie_title in data["title"].to_list():
            with open(self.similarity_file, 'rb') as file:
                similarity_matrix = pickle.load(file)

        else: 
            movie_search = MovieInfo()
            movie_info = movie_search.get_movie_info(movie_title)
            new_df = pd.DataFrame(movie_info, index=[0])
        
            dataa = pd.concat([data, new_df], ignore_index=True) 
            # print(data)
            dataa.to_csv(self.dataset, index=False)

            data_cleanerr = data_cleaner() 

            cleaned_data = data_cleanerr.cleaning(self.dataset) 

            cleaned_data.to_csv(clean_data_path, index = False)

            text_processor = TextPreprocessing(clean_data_path)
        
            similarity_matrix = text_processor.text_processing()

            print("#"*40)
            print("#"*40)
            print("#"*40) 

            with open(self.similarity_file, "wb") as file:
                pickle.dump(similarity_matrix, file)
        
        return similarity_matrix


if __name__ == "__main__":
    movie_name = "The Legend of Al, John and Jack"

    # Read configuration parameters
    reader = YamlReader()
    config = reader.read_param()

    # Extract file paths from configuration
    raw_data = config["artifacts"]["raw_data"]
    cleaned_data_path = config["artifacts"]["cleaned_data"]
    similarity_vector = config["artifacts"]["similarity"]

    # Calculate or load similarity matrix
    similarity_calculator = SimilarityCalculator(raw_data, similarity_vector) 
    similarity_matrix = similarity_calculator.calculate_similarity(movie_name) 

    # Recommend top 5 movies
    recommender = Recommendation(cleaned_data_path, similarity_matrix)

    recommended_movies = recommender.recommend(movie_name)

    # Print recommended movies
    print("#" * 40)
    print("#" * 40)
    print("#" * 40)
    print(f"Top 5 Movies based on {movie_name}:\n")
    for movie in recommended_movies:
        print(movie)
    print("#" * 40)
    print("#" * 40)
    print("#" * 40)
