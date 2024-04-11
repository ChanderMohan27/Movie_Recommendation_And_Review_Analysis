import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

class MovieInfo:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    def get_movie_info(self,movie_name):
            

            # Search for the movie by name
            url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
            response = requests.get(url, headers=self.headers)
            data = response.json()

            # Get movie ID
            movie_id = data['results'][0]['id']

            # Get movie overview and title
            overview = data["results"][0]["overview"]
            title = data["results"][0]["title"]

            # Get cast names
            url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
            response = requests.get(url, headers=self.headers)
            data = response.json()
            cast_names = ', '.join([cast['name'] for cast in data['cast'][:4]])

            # Get crew details
            crew_data = data.get("crew", [])
            crew_df = pd.DataFrame(crew_data)
            filtered_crew_df = crew_df[ 
                ((crew_df['department'] == 'Production') & (crew_df['job'] == 'Producer')) |
                ((crew_df['department'] == 'Directing') & (crew_df['job'] == 'Director'))
            ]
            filtered_crew_df['movie_id'] = movie_id
            filtered_crew_df = filtered_crew_df[["name", "department", "job", "movie_id"]]
            filtered_crew_df = filtered_crew_df.drop_duplicates()
            producers_df = filtered_crew_df[filtered_crew_df['job'] == 'Producer']
            directors_df = filtered_crew_df[filtered_crew_df['job'] == 'Director']
            producer_name = producers_df.iloc[0]['name'] if not producers_df.empty else ""
            director_name = directors_df.iloc[0]['name'] if not directors_df.empty else ""

            # Get movie genres and tagline
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
            response = requests.get(url, headers=self.headers)
            data = response.json()
            genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
            tagline = data['tagline'] if 'tagline' in data else " "

            # Construct the movie dictionary
            movie_info = {
                "movie_id": movie_id,
                "title": str(title),
                "overview": str(overview),
                "genres": str(genres),
                "cast_names": str(cast_names),
                "director_name": str(director_name),
                "producer_name": str(producer_name),
                "tagline" : str(tagline)
            }

            return movie_info
    

if __name__ == "__main__":
     
    movie = MovieInfo()
    dataa = movie.get_movie_info("Late Night with the Devil")



