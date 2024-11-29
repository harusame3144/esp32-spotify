import time
import spotipy
import requests

from geekmagic import set_image_theme, set_weather_forecast, upload_image_from_bytes, set_photo_album_image
from image import convert_and_resize_to_jpeg, draw_information
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# Spotify API credentials
SPOTIFY_CLIENT_ID = "[REDACTED]"
SPOTIFY_CLIENT_SECRET = "[REDACTED]"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope,
))

def update_track_image(image_url, title, artist, pg):
    resized_image = convert_and_resize_to_jpeg(requests.get(image_url).content)
    converted_image = draw_information(resized_image.read(), title, artist, position=(10, 160), font_size=22, pg=pg)
    
    upload_image_from_bytes(converted_image.read(), "spotify.jpg")
    set_photo_album_image("spotify.jpg")
    set_image_theme()

def detect_song_change():
    previous_track = None
    
    while True:
        try:
            playback = sp.current_playback()
            if playback and playback['is_playing']:
                current_track = playback['item']['name']
                artist_name = playback['item']['artists'][0]['name']
                progress = (playback['progress_ms'] / 1000) / (playback['item']['duration_ms'] / 1000)
                update_track_image(
                        playback['item']['album']['images'][0]['url'],
                        current_track,
                        artist_name,
                        progress)
                    
                if current_track != previous_track:
                    print(f"Now playing: {current_track} - {artist_name}")
                    previous_track = current_track
            else:
                set_weather_forecast()
                print("No song is playing.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    detect_song_change()
