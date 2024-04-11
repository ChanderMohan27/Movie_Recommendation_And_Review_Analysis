import pandas as pd
from logger import logging
from exception import CustomException
from utils import YamlReader

class data_cleaner:
    def __init__(self):
        self.reader = YamlReader()
    
    def string_to_list(self, l):
        """Converts a comma-separated string into a list."""

        a = l.split(", ")     
        return a

    def cleaning(self, raw_data):
        """
        Performs data cleaning and transformation on the raw data.
        
        Args:
            raw_data (str): File path to the raw data CSV file.
        
        Returns:
            pd.DataFrame: Cleaned DataFrame with selected columns.
        """
        logging.info("Reading the Data files")
        # Read raw data into DataFrame
        data = pd.read_csv(raw_data)

        # Drop rows with null values in specified columns
                # data.dropna(subset=['director_name', 'cast_names', "genres", "producer_name"], inplace=True)
                # logging.info("Dropping null values from the dataframe")
        data['director_name'].fillna("", inplace=True)
        data['cast_names'].fillna("", inplace=True)
        data['genres'].fillna("", inplace=True)
        data['producer_name'].fillna("", inplace=True)    
        data['tagline'].fillna('', inplace=True)

        # Drop remaining null values and reset index
        data = data.dropna().reset_index(drop=True)

        # Split overview into lists of words
        data["overview"] = data["overview"].apply(lambda x: x.split())
        # Remove spaces from each word in overview
        data["overview"] = data["overview"].apply(lambda x: [i.replace(" ", "") for i in x])

        # Convert genres from comma-separated string to list
        data["genres"] = data["genres"].apply(self.string_to_list)
        
        logging.info("Applying Data Transformation on different columns")

        # Convert cast names from comma-separated string to list
        data["cast_names"] = data["cast_names"].apply(self.string_to_list)

        # Remove spaces from each name in producer names
        data["producer_name"] = data["producer_name"].apply(lambda x: [i.replace(" ", "") for i in self.string_to_list(x)])

        # Convert director names from comma-separated string to list
        data["director_name"] = data["director_name"].apply(self.string_to_list)

        # Remove spaces from each name in director names
        data["director_name"] = data["director_name"].apply(lambda x: [i.replace(" ", "") for i in x])

        # Split tagline into lists of words
        data["tagline"] = data["tagline"].apply(lambda x: x.split())
        # Remove spaces from each word in tagline
        data["tagline"] = data["tagline"].apply(lambda x: [i.replace(" ", "") for i in x])

        # Combine tags from different columns into a single list
        data["tags"] = data["overview"] + data["genres"] + data["cast_names"] + data["director_name"] + data["producer_name"] + data["tagline"]
        logging.info("Created tag column")
        # Select only required columns 
        new_df = data[["movie_id", "title", "tags"]]
        return new_df 
    
if __name__ == "__main__":
    # Read configuration parameters
    reader = YamlReader()
    config = reader.read_param()

    # Extract file paths from configuration
    raw_data = config["artifacts"]["raw_data"]
    cleaned_data = config["artifacts"]["cleaned_data"]

    # Initialize preprocessing class
    data_transformer = data_cleaner()

    # Read CSV files into dataframes and perform preprocessing
    cleaned_data1 = data_transformer.cleaning(raw_data)
    logging.info("Saved Dataframe into csv files")
    # Save cleaned data to CSV file
    cleaned_data1.to_csv(cleaned_data, index=False)
