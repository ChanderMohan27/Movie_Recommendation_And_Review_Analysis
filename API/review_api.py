import requests
import pandas as pd

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

df = pd.read_csv("cleaned_movies.csv")

movie_ids = df["id"][0:2000].to_list()


all_reviews = []

counter = 0
# Iterate over each movie ID
for movie_id in movie_ids:
    # Construct the URL to fetch reviews for the current movie
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"

    # Set up the headers for the API request
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send the API request to fetch review data
    response = requests.get(url, headers=headers)

        # Extract review data from the API response
    data = response.json()
    reviews = data.get('results', [])

        # Process each review and add it to the list of all reviews
    for review in reviews:
        review_info = {
            'content': review.get('content', ''),
            'rating': review['author_details'].get('rating', None),
            'movie_id': movie_id
        }
        all_reviews.append(review_info)
    counter +=1
    print(counter)

# Convert the list of dictionaries to a DataFrame
    
df_reviews = pd.DataFrame(all_reviews)

# Display the DataFrame
df_reviews.to_csv("movie_tmdb_reviews.csv", index=False)

