import numpy as np
import math
from scipy.stats import pearsonr

def getPearsonCorrelation(a, b, rho):
    a = a - np.mean(a)
    b = b - np.mean(b)
    sim = pearsonr(a, b)[0]
    return sim * np.abs(math.pow(sim, rho - 1))


def get_user_avg_rating(elt, ratings):
    user_id = elt['UserID']
    user_ratings = ratings[ratings['UserID'] == user_id]['Rating']
    user_ratings = [rating for rating in user_ratings if rating > 0]
    if len(user_ratings) == 0:
        return 3
    pred = np.mean(user_ratings)
    return pred


def get_movie_avg_pred(movie_id, ratings):
    movie_ratings = ratings[ratings['MovieID'] == movie_id]['Rating']
    movie_ratings = [rating for rating in movie_ratings if rating > 0]
    if len(movie_ratings) == 0:
        return 0
    return np.mean(movie_ratings)


# returns list of tuple pairs of userid,similarity for k most similar users to user userVector that have rated movieID
def getUserNeighbors(userVector, user_vecs, movieId, k, rho, sim_func):
    user_vecs = user_vecs[(user_vecs[movieId] != 0)]
    sims = user_vecs.apply(lambda x: (x[0], sim_func(userVector, x[1:], rho)), axis=1).values
    sims = list(sims)
    sims.sort(key=lambda x: x[1])
    sims.reverse()
    return sims[:k]

def get_user_neighborhood_pred(movie_id, user_vecs, neighborhood):
    sumOfSimilarities = np.sum([x[1] for x in neighborhood])
    rating = 0
    # accumulates a weighted average of user ratings based on similarity
    for elt in neighborhood:
        rating += (elt[1] / sumOfSimilarities) * user_vecs.loc[elt[0]-1, movie_id]
    return rating

def get_user_based_CF_pred(user_vec, movie_id, user_vecs, k):
    neighbor_sims = getUserNeighbors(user_vec, user_vecs, movie_id, k, 2, getPearsonCorrelation)
    pred = get_user_neighborhood_pred(movie_id, user_vecs, neighbor_sims)
    return pred