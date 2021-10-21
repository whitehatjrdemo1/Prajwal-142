from flask import Flask, jsonify, request
import csv
from demographic_filtering import output
from content_filtering import get_recommendations
from storage import all_movies, didnotwatch, not_liked_movies, liked_movies
app = Flask(__name__)


@app.route('/get-movie')
def get_movie():
    return jsonify({'data': all_movies[0], 'status': 'success'})


@app.route('/liked-movie', methods=['POST'])
def liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)
    return jsonify({'status': 'success'}), 201


@app.route('/un-liked-movie', methods=['POST'])
def unliked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_liked_movies.append(movie)
    return jsonify({'status': 'success'}), 201


@app.route('/unwatched', methods=['POST'])
def unwatched():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    didnotwatch.append(movie)
    return jsonify({'status': 'success'}), 201


@app.route('/popular-movies')
def popular_movies():
    movie_data = []
    print(output)
    for movie in output:
        _d = {'title': movie[0], 'poster_link': movie[1], 'release_date': movie[2],
              'duration': movie[3], 'rating': movie[4], 'overview': movie[5]}
        movie_data.append(_d)
    return jsonify({'data': movie_data, 'status': 'success'}), 200


@app.route('/recommended-movies')
def recommended_movies():
    all_recomended = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[19])
        for data in output:
            all_recomended.append(data)
    import itertools
    all_recomended.sort()
    all_recomended = list(all_recomended for all_recomended,
                          _ in itertools.groupby(all_recomended))
    movie_data = []
    for recomended in all_recomended:
        _d = {'title': recomended[0], 'poster_link': recomended[1], 'release_date': recomended[2]
              or 'N/A', 'duration': recomended[3], 'rating': recomended[4], 'overview': recomended[5]}
        movie_data.append(_d)
    return jsonify({'data': movie_data, 'status': 'success'}), 200


if (__name__ == '__main__'):
    app.run()
