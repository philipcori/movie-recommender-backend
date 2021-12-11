import pandas as pd

def get_popularity_score(v, m, R, C):
    m = int(m)
    return v / (v + m) * R + m / (v + m) * C

def get_most_popular_movies(num, genre, popularity_importance, ratings):
    ratings = ratings[ratings[genre] == 1]
    movie_vote_counts = ratings.groupby("MovieID").count().sort_values(by="Rating", ascending=False)["Rating"]
    movie_avg_ratings = ratings.groupby("MovieID").mean().sort_values(by="Rating", ascending=False)["Rating"]
    C = movie_avg_ratings.mean()
    m = popularity_importance
    movie_df = pd.concat([movie_vote_counts, movie_avg_ratings], axis=1)
    movie_df.columns = ["Rating_Count", "Rating_Mean"]
    movie_df["Score"] = movie_df.apply(lambda row: get_popularity_score(row["Rating_Count"], m, row["Rating_Mean"], C), axis=1)
    movie_df = movie_df.sort_values(by="Score", ascending=False).reset_index()
    return movie_df["MovieID"][:num].values.tolist()