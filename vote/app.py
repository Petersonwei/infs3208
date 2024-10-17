from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    if request.method == 'POST':
        review = {
            'movie_title': request.form['movie_title'],
            'reviewer_name': request.form['reviewer_name'],
            'review_text': request.form['review_text'],
            'rating': request.form['rating']
        }
        redis = get_redis()
        redis.rpush('reviews', json.dumps(review))

    # Fetch recent reviews
    reviews = get_recent_reviews()
    
    return render_template('index.html', reviews=reviews)

def get_recent_reviews():
    redis = get_redis()
    reviews = redis.lrange('reviews', 0, 9)  # Get last 10 reviews
    return [json.loads(review) for review in reviews]
