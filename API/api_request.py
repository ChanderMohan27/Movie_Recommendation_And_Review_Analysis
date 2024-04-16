import requests 
import pandas as pd

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")


# List to store all data from all pages
all_data = []

# Api to get the movie detail...

for page in range(1, 1001):  # Assuming you want to fetch data from pages 1 to 2
    
    url = f"https://api.themoviedb.org/3/trending/movie/week?language=en-US&page={page}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)
    json_data = response.json()

    # Extract data from the current page

    data = json_data.get("results", [])
    
    # Columns that we do not need in our data 
    data_to_exclude = ["adult", "media_type", "video", "original_language"]

    # Filter and store data from current page
    filtered_data = []
    for d in data:
        filtered_dict = {k: v for k, v in d.items() if k not in data_to_exclude}
        filtered_data.append(filtered_dict)

    # Append data from current page to the list
    all_data.extend(filtered_data)


# Create DataFrame
df = pd.DataFrame(all_data)

df.to_csv("movies.csv", index= False)