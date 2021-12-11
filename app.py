import json

from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import logging

from genre_recommender.recommender import GenreRecommender
from ratings_recommender.recommender import RatingsRecommender

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'
logging.getLogger('flask_cors').level = logging.DEBUG

sys2_recommender = RatingsRecommender()
sys1_recommender = GenreRecommender()

@app.route('/echo', methods = ['GET'])
@cross_origin()
def echo():
    print('endpoint invoked with request:')
    print(request)
    # name = request.json['name']
    name = request.args.get('name')
    msg = 'Hello ' + str(name)
    resp = make_response(msg)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.access_control_allow_origin = "*"
    print('returning response:')
    print(resp.headers)
    return resp

# expects query param ratings - json string
@app.route('/system2/get_recs', methods = ['GET'])
@cross_origin()
def get_system2_recs():
    ratings_str = request.args.get('ratings')
    ratings = json.loads(ratings_str)
    movie_recs = sys2_recommender.get_movie_recs(ratings)
    resp = {}
    resp['recs'] = movie_recs
    return resp

@app.route('/system1/get_recs', methods = ['GET'])
@cross_origin()
def get_system1_recs():
    num = request.args.get('num')
    genre = request.args.get('genre')
    popularity_importance = request.args.get('popularityImportance')
    recs = sys1_recommender.get_movie_recs(num, genre, popularity_importance)
    print(recs)
    resp = {}
    resp['recs'] = recs
    return resp







