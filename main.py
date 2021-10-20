from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'e55e301d88204956ba24a6c06d901250'
CLIENT_SECRET = 'ae526d028d4346d89f929488db1f3d1e'

date = input("Which year would you like to travel to? Enter a date: YYYY-MM-DD: ")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri="http://example.com",
        client_id= CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()['id']

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

billboard_page = response.text

soup = BeautifulSoup(billboard_page, 'html.parser')

song_titles = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')

song_title_texts = []

for title_tag in song_titles:
    song_title_text = title_tag.getText()
    song_title_texts.append(song_title_text)


song_uris = []

year = date.split('-')[0]

for song in song_title_texts:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

