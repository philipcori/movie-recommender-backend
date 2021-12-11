import pandas as pd
import json
import numpy as np

from ratings_recommender.helper import get_user_based_CF_pred

NUM_MOVIES = 3706
NUM_MOVIES_TO_PREDICT_ON = 100
NUM_RECS = 10
NEIGHBORHOOD_SIZE = 10
MOVIE_ID_PREFIX = "MovieID_"
FRACTION_USERS_TO_QUERY = 1

class RatingsRecommender():
    def __init__(self):
        self.user_vectors = pd.read_csv("user_vectors.csv")
        total_num_users = len(self.user_vectors)
        self.user_vectors = self.user_vectors[:int(FRACTION_USERS_TO_QUERY * total_num_users)]
        print("user vectors loaded")

        with open('pop_movies.txt') as f:
            lines = f.readlines()
            self.popular_movies = [line.rstrip() for line in lines]
            print("popular movies loaded")

        with open('movieID_to_idx.json', 'r') as fp:
            data = json.load(fp)
            self.movieID_to_idx = data
            print("movieID_to_idx loaded")



    # params: ratings - list of (movieId, rating) objs
    def get_movie_recs(self, ratings):
        user_vec = self.construct_user_vec(ratings)
        ratings_movie_ids = [MOVIE_ID_PREFIX + str(rating['movieId']) for rating in ratings]
        preds = []
        for movie in self.popular_movies[:NUM_MOVIES_TO_PREDICT_ON]:
            movie_id = MOVIE_ID_PREFIX + str(movie)
            if movie_id not in ratings_movie_ids:
                print("predicting for movie: " + str(movie))
                pred_rating = get_user_based_CF_pred(user_vec, movie_id, self.user_vectors, NEIGHBORHOOD_SIZE)
                preds.append((movie, pred_rating))
        preds.sort(key=lambda x: x[1])
        preds.reverse()
        for pred in preds[:NUM_RECS]:
            print(str(pred[0]) + ": " + str(pred[1]))
        movie_recs = [pred[0] for pred in preds]
        return movie_recs[:NUM_RECS]

    # params: ratings - list of (movieId, rating) tuples
    def construct_user_vec(self, ratings):
        vec = np.zeros(NUM_MOVIES)
        for rating in ratings:
            movie_id = MOVIE_ID_PREFIX + str(rating['movieId'])
            stars = rating['rating']
            vec[self.movieID_to_idx[movie_id]] = stars
        return vec
