from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import os
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from random import shuffle
from flask_caching import Cache




# Flash configuration
app = Flask(__name__)
app.static_folder = 'static'
# Cache instance
cache = Cache(app, config={'CACHE_TYPE': 'simple',
                           'SEND_MAX_FILE_MAX_AGE_DEFAULT': '0'})



# load evn vars
load_dotenv()
clientId = os.environ.get("SPOTIPY_CLIENT_ID")
clientSecret = os.environ.get("SPOTIPY_CLIENT_SECRET")
uri = os.environ.get("SPOTIPY_REDIRECT_URI")
scope = "user-library-read, user-top-read, user-follow-read, playlist-read-private, user-read-recently-played"

# brings up a window prompt, accept its conditions to continue
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId,
                                               client_secret=clientSecret,
                                               redirect_uri=uri,
                                               scope=scope))


@app.route('/', methods=['GET', 'POST'])
def frontpage():
    user_playlists = []
    user = sp.current_user()
    following = sp.current_user_followed_artists(limit=50)
    recent_played = sp.current_user_recently_played(limit=1)
    # playlists_name = sp.current_user_playlists(limit=10)['items']
    playlists = sp.current_user_playlists()
    for items in playlists['items']:
        if items['owner']['display_name'] == str(user['display_name']):
            user_playlists.append(items['name'])
    return render_template('index.html', 
                            user=user,
                            playlists=playlists,
                            following=following,
                            recent_played=recent_played)

@app.route('/artists')
def get_top_artists():
    cache.clear()
    artists_images = []
    artists = sp.current_user_top_artists(limit=50, offset=1, time_range="long_term")
    for artist in artists['items']:
        for image in artist['images']:
            if image['width'] == 160:
                artists_images.append(image['url'])
    shuffle(artists_images)
    generate_collage(artists_images)
    
    with app.app_context():
        cache.clear()
    return render_template("artists.html", 
                           artists=artists, 
                           images=artists_images)

@app.route('/tracks')
def get_top_tracks():
    tracks_images = []
    tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")
    for track in tracks['items']:
        for image in track['album']['images']:
            if image['width'] == 640:
                tracks_images.append(image['url'])
    shuffle(tracks_images)
    generate_collage(tracks_images)
    
    with app.app_context():
        cache.clear()
    return render_template("tracks.html", tracks=tracks)






def generate_collage(images):
    # TODO: If len of image lst is small, generate new empty image of appropriate size
    
    # Reduce the width if less than 50 images
    ratio = 1.0
    num_images = 50
    if len(images) != 50:
        ratio = float(str(len(images)/50)[0:3])
        num_images = 50*ratio
    # Creating a new empty image, RGB mode with size thats subject to change 
    width = int(ratio * 1600)
    height = 800    
    collage = Image.new("RGBA", (width,height), color=(255,255,255,255))
    # Iterate through grid with no spacing, to place image
    idx = 0
    while idx < num_images-1:
        for i in range(0,width,160):
            for j in range(0,height,160):
                if idx > num_images-1:
                    break
                else:
                    # Requesting image url
                    response = requests.get(images[idx])
                    # Getting the in-memory info to save the image with BytesIO
                    photo = Image.open(BytesIO(response.content)).convert("RGBA")
                    # Resize image to fit
                    photo_resized = photo.resize((160, 160))
                    # Paste image at loc i,j
                    collage.paste(photo_resized, (i,j))
                    idx += 1
    # Create file if non-existent
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    collage.save(r'static/images/collage.png')
    
    
    




@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()