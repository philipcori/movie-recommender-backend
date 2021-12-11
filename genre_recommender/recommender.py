import pandas as pd
import boto3

from genre_recommender.helper import get_most_popular_movies


class GenreRecommender():
    def __init__(self):

        self.ratings = pd.read_csv("https://movie-recommender-pcori.s3.us-west-2.amazonaws.com/ratings_with_genres.csv")
        print("ratings with genre loaded!")

    def get_movie_recs(self, num, genre, popularity_importance):
        num = int(num)
        return get_most_popular_movies(num, genre, popularity_importance, self.ratings)