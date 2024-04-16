import pandas as pd
from logger import logging
from exception import CustomException
from utils import YamlReader

class Preprocessing:
    def __init__(self):
        self.reader = YamlReader()

    def read_csv(self, csv_file):
        df = pd.read_csv(csv_file)
        return df

    def csv_to_df(self, movie_csv, extra_movie_csv, cast_csv, crew_csv):
        logging.info("Reading different Movie detail files from different CSVs")
        movie_df = self.read_csv(movie_csv)
        extra_movie_df = self.read_csv(extra_movie_csv)
        cast_df = self.read_csv(cast_csv)
        crew_df = self.read_csv(crew_csv)

        return movie_df, extra_movie_df, cast_df, crew_df

    def preprocess(self, movie_df, extra_movie_df, cast_df, crew_df):
        
        # Preprocessing of movie Dataset 
        logging.info("start working with movie dataframes to combine them into one")

        df_needed = movie_df[["id","title","overview"]]

        df_needed.rename(columns={'id': 'movie_id'}, inplace=True)

        logging.info("Start working with crew Dataframe")

        crew_df = crew_df.drop_duplicates()

        # Filter rows for Producer 

        producers_df = crew_df[crew_df['job'] == 'Producer']

        # Group by movie_id 
        grouped = producers_df.groupby('movie_id')

        # Get the first producer for each movie
        first_producer_per_movie = grouped.first().reset_index()

        # Filter rows for Producer
        Director_df = crew_df[crew_df['job'] == 'Director']

        # Group by movie_id
        grouped = Director_df.groupby('movie_id')

        # Get the first producer for each movie

        first_Director_per_movie = grouped.first().reset_index()

        first_Director_per_movie.rename(columns={'name': 'director_name'}, inplace=True)

        first_producer_per_movie.rename(columns={'name': 'producer_name'}, inplace=True)

        merged_df = pd.merge(first_Director_per_movie,first_producer_per_movie, on='movie_id',how='left')

        final_crew_df = merged_df[["movie_id","director_name", "producer_name"]]

        logging.info("Start working with cast Dataframe")

        # Cast Data Fittering and preprocessing 

        combined_cast_df = cast_df.groupby('movie_id')['name'].apply(', '.join).reset_index()


        # Rename the column to 'combined_cast'
        combined_cast_df.rename(columns={'name': 'cast_names'}, inplace=True)


        # concate all dataframe with the help of movie_id column 

        detailed_df = pd.merge(extra_movie_df, df_needed, on='movie_id')

        final_df = pd.merge(detailed_df, combined_cast_df , on='movie_id', how = "left")

        final_df = pd.merge(final_df, final_crew_df , on='movie_id', how = "left")

        final_df = final_df[["movie_id", "title", "overview", "genres", "cast_names", "director_name", "producer_name", "tagline"]]
        
        logging.info("Successfully combine all the movie data into raw dataframe")
        return final_df

if __name__ == "__main__":
    # Read configuration parameters
    reader = YamlReader()
    config = reader.read_param()

    # Extract file paths from configuration
    movie_csv = config["source_data"]["movies_data"]
    extra_movie_csv = config["source_data"]["movie_detail_data"]
    cast_csv = config["source_data"]["cast_data"]
    crew_csv = config["source_data"]["crew_data"]

    combined_csv = config["artifacts"]["raw_data"]

    # Initialize preprocessing class
    processor = Preprocessing()

    # Read CSV files into dataframes
    movie_df, extra_movie_df, cast_df, crew_df = processor.csv_to_df(movie_csv, extra_movie_csv, cast_csv, crew_csv)

    # Perform preprocessing
    final_df = processor.preprocess(movie_df, extra_movie_df, cast_df, crew_df)

    final_df.to_csv(combined_csv, index=False)

    logging.info("Preprocessing Done store the cleaned data in Raw CSV file")
