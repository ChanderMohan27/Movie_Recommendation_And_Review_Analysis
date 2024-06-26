import requests
import pandas as pd
import os
from dotenv import load_dotenv
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
from logger import logging

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

df = pd.read_csv("cleaned_movies.csv")

movie_ids = df["id"].to_list()

# List to accumulate data for all movies
movie_data = []
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

write_header = True
counter = 0

logging.info("collecting Extra Movie details info through api")
for movie_id in movie_ids:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url, headers=headers)
    data = response.json()
    # Extract required data
    budget = data['budget']
    genres = ', '.join([genre['name'] for genre in data['genres']])
    imdb_id = data['imdb_id']
    runtime = data['runtime']
    tagline = data['tagline']
    
    # Append movie data to the list
    movie_data.append({
        'budget': budget,
        'genres': genres,
        'imdb_id': imdb_id,
        'movie_id': movie_id,
        'runtime': runtime,
        'tagline': tagline
    })
    
    counter += 1
    print(counter)

# Creating DataFrame from accumulated data
df = pd.DataFrame(movie_data)

# # Writing DataFrame to CSV
df.to_csv("Data/movie_details.csv", header=write_header, mode='a', index=False)

logging.info("Stored extra movie info in csv file collecting data thorugh api")