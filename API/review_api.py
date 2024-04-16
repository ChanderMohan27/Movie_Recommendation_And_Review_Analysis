import requests
import pandas as pd

import os
import string
string.punctuation
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

class Review_info:
    def __init__(self):
        # Set up the headers for the API request
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    

    def remove_special_tags(self, text):
        # Remove 'http' if available
        cleaned_text = re.sub(r'http\S+', '', text)
        # Remove 'Rating: [Letter]' if available
        cleaned_text = re.sub(r'Rating: [A-Za-z]', '', cleaned_text)
        return cleaned_text

    def remove_tags(self, text):
        cleaned_text = text.replace('<br />', '')
        cleaned_texts = self.remove_special_tags(cleaned_text)
        nopunc = [x for x in cleaned_texts if x not in string.punctuation]
        nopunc = ''.join(nopunc)


        return nopunc 

    def get_movie_reviews(self,movie_id):
        # Construct the URL to fetch reviews for the specified movie
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"
        

        # Send the API request to fetch review data
        response = requests.get(url, headers=self.headers)

        # Extract review data from the API response
        data = response.json()
        reviews = data.get('results', [])

        # Process each review and add it to the list of all reviews
        all_reviews = []
        if reviews:
            for review in reviews:
                review_info = review.get('content', '')  

                cleaned_review= self.remove_tags(review_info)     
                all_reviews.append(cleaned_review)
        else:
            all_reviews.append("Movie Review Not Avilable")

        return all_reviews



if __name__ == "__main__":
    
    movie_id = 823464
    review_info = Review_info()

    reviews = review_info.get_movie_reviews(movie_id)

    print(reviews)


# df = pd.read_csv("cleaned_movies.csv")

# movie_ids = df["id"][0:2000].to_list()


# all_reviews = []

# counter = 0
# # Iterate over each movie ID
# for movie_id in movie_ids:
#     # Construct the URL to fetch reviews for the current movie
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"

#     # Set up the headers for the API request
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     # Send the API request to fetch review data
#     response = requests.get(url, headers=headers)

#         # Extract review data from the API response
#     data = response.json()
#     reviews = data.get('results', [])

#         # Process each review and add it to the list of all reviews
#     for review in reviews:
#         review_info = {
#             'content': review.get('content', ''),
#             'rating': review['author_details'].get('rating', None),
#             'movie_id': movie_id
#         }
#         all_reviews.append(review_info)
#     counter +=1
#     print(counter)



# Convert the list of dictionaries to a DataFrame
    
# df_reviews = pd.DataFrame(all_reviews)

# # Display the DataFrame
# df_reviews.to_csv("movie_tmdb_reviews.csv", index=False)
