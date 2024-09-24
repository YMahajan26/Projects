from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values, load_dotenv

app = Flask(__name__)
load_dotenv(".env")
env_vars = dotenv_values(".env")


def clean_text(text):
    return text.replace("\n", "").replace("\t", "")


def get_top_100_songs(date):
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
    soup = BeautifulSoup(response.text, "html.parser")

    top_99 = [clean_text(song.getText()) for song in soup.find_all(
        class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
    )]
    number_one_song = [clean_text(song.getText()) for song in soup.find_all(
        class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"
    )]

    top_100 = number_one_song + top_99
    return top_100


def get_spotify_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': env_vars["SPOTIPY_CLIENT_ID"],
        'client_secret': env_vars["SPOTIPY_CLIENT_SECRET"],
    })
    access_token = auth_response.json()['access_token']
    return access_token


def search_tracks_in_spotify(spotify, top_100, year):
    track_ids = []
    access_token = get_spotify_access_token()

    for song in top_100:
        search_query = f"{song} year:{year}-{year + 1}"
        params = {
            'q': search_query,
            'type': 'track',
            'limit': 1,
        }

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        resp = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)
        search_results = resp.json()

        try:
            if 'tracks' in search_results and search_results['tracks']['items']:
                track = search_results['tracks']['items'][0]

                if song in track['name']:
                    song_id = track['id']
                    track_ids.append(song_id)
        except KeyError:
            print(f"No results found for '{song}' in {year}.")
        except IndexError:
            print(f"No results found for '{song}' in {year}.")

    return track_ids


playlist_created = False


def check_if_playlist_exists(spotify, username, playlist_name):
    playlists = spotify.user_playlists(user=username)

    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return True

    return False


def create_playlist(spotify, username, playlist_name, track_ids):
    global playlist
    if not check_if_playlist_exists(spotify, username, playlist_name):
        playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=True)
        spotify.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
        print(f"Playlist '{playlist_name}' created successfully")
        global playlist_created
        playlist_created = True
    else:
        print(f"Playlist '{playlist_name}' already exists.")


@app.route("/", methods=["GET", "POST"])
def index():
    playlist_created = False
    playlist_link = None  # Declare the playlist_link variable

    if request.method == "POST":
        try:
            date = request.form.get("date")
            playlist_name = f"{date} Billboard Chart"
            year = int(date[:4])
        except ValueError:
            # Handle the case when an invalid date format is entered
            date = None
            playlist_name = None
            year = None

        top_100 = get_top_100_songs(date)

        scope = "playlist-modify-public"
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        username = spotify.current_user()["id"]

        track_ids = search_tracks_in_spotify(spotify, top_100, year)

        create_playlist(spotify, username, playlist_name, track_ids)

        playlist_created = True
        playlist_link = playlist["external_urls"]["spotify"]

    return render_template("index.html", playlist_created=playlist_created, playlist_link=playlist_link)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
