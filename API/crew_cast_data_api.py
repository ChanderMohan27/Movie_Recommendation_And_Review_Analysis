import requests
import pandas as pd
import os
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
from logger import logging

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")


df = pd.read_csv("cleaned_movies.csv")

movie_ids = df["id"].to_list()

# Initialize empty lists to store dataframes
cast_dfs = []
crew_dfs = []
write_header = True
headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
counter = 0

logging.info("collecting Movie Crew and Cast info through api")
for movie_id in movie_ids:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"     

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract cast data
    cast_data = data.get('cast', [])
    # Create DataFrame for cast
    cast_df = pd.DataFrame(cast_data)
    # Filter only the rows where the order is 0, 1, or 2
    filtered_cast_df = cast_df[cast_df.get('order', pd.Series([])).isin([0, 1, 2, 3])]
    # Add movie_id column

    filtered_cast_df['movie_id'] = movie_id

    try:

        final_dataframe = filtered_cast_df[["id","name","profile_path","movie_id"]]
    except KeyError:
        pass

    final_dataframe.to_csv("cast_details.csv", mode='a',header=write_header, index=False)
    # Append to list of cast dataframes
    # cast_dfs.append(final_dataframe)

    # Extract crew data
    crew_data = data.get("crew", [])

    # Create DataFrame for crew
    crew_df = pd.DataFrame(crew_data) 

    # Filter crew data
    try:
        filtered_crew_df = crew_df[ 
            ((crew_df['department'] == 'Production') & (crew_df['job'] == 'Producer')) |
            ((crew_df['department'] == 'Writing') & (crew_df['job'] == 'Writer')) |
            ((crew_df['department'] == 'Directing') & (crew_df['job'] == 'Director'))
        ]
        # Add movie_id column
        filtered_crew_df['movie_id'] = movie_id

        filtered_crew_df1 = filtered_crew_df[["id","name","profile_path","department", "job","movie_id"]]

    except KeyError:

        pass
    
    # Appending Each row with each iteration in the CSV file

    filtered_crew_df1.to_csv("crew_details.csv", mode='a', header= write_header, index = False)
    write_header = False
    counter+=1
    print(counter)

    logging.info("saved crew csv and cast csv though api")