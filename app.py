from flask import Flask, jsonify, send_file
import httpx
from mal import Anime
from custom_poster import CustomPoster
from dotenv import load_dotenv
from os import getenv

try:
    load_dotenv("config.env")
except:
    pass

# Create a Flask web server
app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify(
        anime_path="/anime/{mal-anime-id}",
        tv_path="/tv/{tmdb-tv-id}",
        tv_season_path="/tv/{tmdb-id}/season/{season-number}",
        movie_path="/movie/{tmdb-movie-id}",
    )


@app.route("/anime/<id>", methods=["GET"])
def mal_poster(id):
    try:
        anime = Anime(int(id))
    except:
        return jsonify(error="MAL anime id is incorrect", malID=id)

    if anime.type:
        if anime.type == "Movie":
            subtitle = f"""Movie{f' • {anime.aired.split(",")[-1].strip()}' if anime.aired else ''} • {anime.duration}"""
        else:
            subtitle = f"{f'{anime.premiered} • ' if anime.premiered else ''}{f'{anime.episodes} Episodes' if anime.episodes else anime.type or "Anime"}"
    else:
        subtitle = f"{f'{anime.premiered} • ' if anime.premiered else ''}{f'{anime.episodes} Episodes' if anime.episodes else anime.type or "Anime"}"

    poster = CustomPoster(
        {
            "subtitle": subtitle,
            "title": anime.title_english or anime.title,
            "makers": anime.studios,
            "score": f"{int(anime.score * 10)}%" if anime.score else "0%",
            "tags": anime.genres,
        },
        anime.image_url,
        None,
    )
    try:
        poster = poster.generate()
        poster.seek(0)
        return send_file(poster, mimetype="image/png")
    except:
        return jsonify(error="Something went wrong while generating poster")


@app.route("/tv/<id>", methods=["GET"])
def tmdb_serier_poster(id):
    API_KEY = str(getenv("TMDB_API_KEY", None))
    if not API_KEY:
        return jsonify(error="TMDB api key not provided")

    response = httpx.get(f"https://api.themoviedb.org/3/tv/{id}?api_key={API_KEY}")
    if response.status_code != 200:
        return response.json()

    tv_info = response.json()
    poster = CustomPoster(
        {
            "subtitle": f"{tv_info.get('status', '')} • {tv_info.get('number_of_seasons', '')} Seasons • {tv_info.get('number_of_episodes', '')} Episodes",
            "title": tv_info.get("name", None),
            "makers": [creator["name"] for creator in tv_info.get("created_by", [])],
            "score": f"{int(tv_info.get('vote_average') * 10)}%",
            "tags": [
                tag
                for genre in tv_info.get("genres", [])
                for tag in genre["name"].split(" & ")
            ],
        },
        f"https://image.tmdb.org/t/p/w500{tv_info.get('poster_path')}",
        f"https://image.tmdb.org/t/p/w500{tv_info.get('backdrop_path')}"
        if tv_info.get("backdrop_path", None)
        else None,
    )
    try:
        poster = poster.generate()
        poster.seek(0)
        return send_file(poster, mimetype="image/png")
    except:
        return jsonify(error="Something went wrong while generating poster")


@app.route("/tv/<series_id>/season/<season_number>", methods=["GET"])
def tmdb_season_poster(series_id, season_number):
    API_KEY = str(getenv("TMDB_API_KEY", None))
    if not API_KEY:
        return jsonify(error="TMDB api key not provided")

    response_season = httpx.get(
        f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?api_key={API_KEY}"
    )
    response_tv = httpx.get(
        f"https://api.themoviedb.org/3/tv/{series_id}?api_key={API_KEY}"
    )
    if response_season.status_code != 200 and response_tv.status_code != 200:
        return response_season.json()

    season_info = response_season.json()
    tv_info = response_tv.json()
    poster = CustomPoster(
        {
            "subtitle": f"{len(season_info.get('episodes', []))} Episodes",
            "title": season_info.get("name", None),
            "makers": [tv_info.get("name", "")],
            "score": f"{int(season_info.get('vote_average') * 10)}%",
            "tags": [
                tag
                for genre in tv_info.get("genres", [])
                for tag in genre["name"].split(" & ")
            ],
        },
        f"https://image.tmdb.org/t/p/w500{season_info.get('poster_path', None) or tv_info.get('poster_path', None)}",
        f"https://image.tmdb.org/t/p/w500{tv_info.get('backdrop_path')}"
        if tv_info.get("backdrop_path", None)
        else None,
    )
    try:
        poster = poster.generate()
        poster.seek(0)
        return send_file(poster, mimetype="image/png")
    except:
        return jsonify(error="Something went wrong while generating poster")


@app.route("/movie/<id>", methods=["GET"])
def tmdb_movie_poster(id):
    API_KEY = str(getenv("TMDB_API_KEY", None))
    if not API_KEY:
        return jsonify(error="TMDB api key not provided")

    response = httpx.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}")
    if response.status_code != 200:
        return response.json()

    movie_info = response.json()
    poster = CustomPoster(
        {
            "subtitle": f"{movie_info.get('release_date').split('-')[0]} • {'{:01} hour, {:02} mins'.format(*divmod(int(movie_info.get('runtime')), 60))}",
            "title": movie_info.get("title", None),
            "makers": [
                company["name"]
                for company in movie_info.get("production_companies", [])
            ],
            "score": f"{int(movie_info.get('vote_average') * 10)}%",
            "tags": [
                tag
                for genre in movie_info.get("genres", [])
                for tag in genre["name"].split(" & ")
            ],
        },
        f"https://image.tmdb.org/t/p/w500{movie_info.get('poster_path')}",
        f"https://image.tmdb.org/t/p/w500{movie_info.get('backdrop_path')}"
        if movie_info.get("backdrop_path", None)
        else None,
    )
    try:
        poster = poster.generate()
        poster.seek(0)
        return send_file(poster, mimetype="image/png")
    except:
        return jsonify(error="Something went wrong while generating poster")


# Only for testing purpose
# if __name__ == "__main__":
#     app.run(debug=True)
