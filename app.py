from flask import Flask, render_template, request, redirect, url_for, session
import sys
sys.path.append("/Users/chandermohan/Desktop/Football_Project/src")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/API")
sys.path.append("/Users/chandermohan/Desktop/Football_Project/movie_recommendation")
from logger import logging
from data_cleaning import data_cleaner
from utils import YamlReader
from text_preprocessing import TextPreprocessing
from movie_search import MovieInfo     
import yaml 
from recommendation import Recommendation, SimilarityCalculator 
# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Read configuration parameters from YAML file
reader = YamlReader()
config = reader.read_param()

# Define paths to your dataset and similarity vector
raw_data = config["artifacts"]["raw_data"]
cleaned_data_path = config["artifacts"]["cleaned_data"]
similarity_vector = config["artifacts"]["similarity"]


# Initialize SimilarityCalculator with dataset and similarity vector
similarity_calculator = SimilarityCalculator(raw_data, similarity_vector)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'show_details' in request.form:

            selected_movie = request.form['movie_name']
            # Redirect to the show_details route
            # session["movie_name_info"] = selected_movie


            return redirect(url_for('show_details'), movie_name=selected_movie)
        else:
            selected_movie = request.form['movie_name']

            similarity_matrix = similarity_calculator.calculate_similarity(selected_movie)
            recommender = Recommendation(raw_data, similarity_matrix)
            # Call the recommend method of the Recommendation object
            recommended_movie_names, recommended_movie_posters, recommended_movie_details = recommender.recommend(selected_movie)
            # Store recommended movie information and details in session variables
            session["movie_name"] = selected_movie
            session['recommended_movie_names'] = recommended_movie_names
            session['recommended_movie_posters'] = recommended_movie_posters
            session['recommended_movie_details'] = recommended_movie_details 
            return redirect(url_for('recommendations')) 

    return render_template('index.html')

@app.route('/show_details')

def show_details():
    movie_detail = []
    movie_poster = []
    movie_title = []

    movie_namee = session.get('movie_name')

    print("#"*40)
    print("#"*40)
    print("#"*40)

    print(movie_namee)
    movie_info = MovieInfo()
    recomentation = Recommendation(raw_data, similarity_vector)
    dataa = movie_info.get_movie_info(movie_namee)
    movie_name_id = dataa["movie_id"]
    poster_url = recomentation.fetch_poster(movie_name_id)
    if poster_url:
        movie_poster.append(poster_url)
        details = recomentation.fetch_movie_details(movie_name_id)
        movie_detail.append(details)
        movie_title.append(movie_namee) 
    movies_data = zip(movie_title, movie_poster, movie_detail)
    print("#"*40)
    print("#"*40)
    print("#"*40)
    print(movie_detail)
    print(movie_poster)
    # Pass the fetched movie info to the template
    return render_template('show_details.html', movie_name=movie_namee, recommended_movies_data=movies_data)


@app.route('/recommendations')
def recommendations():
    movie_namee = session.get('movie_name')
    recommended_movie_names = session.get('recommended_movie_names')
    recommended_movie_posters = session.get('recommended_movie_posters')
    recommended_movie_details = session.get('recommended_movie_details')

    recommended_movies_data = zip(recommended_movie_names, recommended_movie_posters, recommended_movie_details)
    return render_template('recommendations.html', movie_name = movie_namee, recommended_movies_data=recommended_movies_data)


if __name__ == '__main__':
    app.run(debug=True)
