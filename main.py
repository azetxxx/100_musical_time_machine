from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import datetime as dt
import os
import requests
import spotipy


# Constants
BASE_URL = 'https://www.billboard.com/charts/hot-100/'
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


# Function to get a valid date from user
def get_valid_date():
    while True:
        picked_date = input("\n📅 Pick a date in the past for time traveling! \
            \nHint: Use the following format (YYYY-MM-DD) ➡️ ")
        if is_date_format_valid(picked_date):
            return picked_date
        else:
            print("\n❌ Invalid date format or future date. Try again! \n")


# Function to validate date formate
def is_date_format_valid(date_input):
    try:
        dt_input_obj = dt.datetime.strptime(date_input, "%Y-%m-%d")
        return dt_input_obj.date() <= dt.date.today()
    except ValueError:
        return False


# Add a list of items (URI) to a playlist (URI)
def add_songs_to_playlist(playlist_name, list_of_songs):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                client_secret=SPOTIFY_CLIENT_SECRET,
                                                redirect_uri="http://example.com",
                                                scope = "playlist-modify-public playlist-modify-private"
                                                ))
    # Iterate through the list of song titles and search for each one
    list_of_song_ids = []
    for title in list_of_songs:
        results = sp.search(q=title, type="track", limit=1)  # Limit the search to one result per title
        if results and results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_id = track['id']
            list_of_song_ids.append(track_id)
            print(f"✅ Title: {title}, Spotify Track ID: {track_id}")
        else:
            print(f"❌ Title: {title}, Spotify Track ID not found")

    # Create a new playlist
    user = sp.current_user()
    playlist = sp.user_playlist_create(user['id'], playlist_name, public=True)

    # Add songs to the created playlist
    sp.playlist_add_items(playlist['id'], list_of_song_ids, position=None)

    print("\n😇 Playlist created! Have fun! 💃🕺\n")


def main():
    picked_date = get_valid_date()
    print(f"\n✅ Picked date: {picked_date}\n")

    response = requests.get(BASE_URL + picked_date)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return

    chart_page = response.text
    soup = BeautifulSoup(chart_page, 'html.parser')

    # song_titles = soup.select(selector='div.o-chart-results-list-row-container ul li:nth-of-type(4) ul li:first-of-type span')
    song_titles = soup.select(selector='li ul li h3')

    list_of_songs = []

    for song in song_titles:
        for string in song.stripped_strings:
            list_of_songs.append(string)

    playlist_name = f"🎵 Musical Time Machine {picked_date}\n"

    print('\n' + playlist_name)

    add_songs_to_playlist(playlist_name, list_of_songs)



if __name__ == '__main__':
    main()
