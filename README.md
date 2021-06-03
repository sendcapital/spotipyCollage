# Spotify PhotoCollage Gen

Generates a photocollage of your top listened artists and tracks. Designed with this [webpage color pallete](https://colorhunt.co/palette/14114). 

Built with Flask, Spotipy and Pillow.


## Screenshots


<p align="center">
<img src="https://github.com/EatSleepBeatMeat/spotipyCollage/blob/main/screenshots/Frontpage.PNG?raw=true" alt=" " width="700"/>
</p>

<p align="center">
<img src="https://github.com/EatSleepBeatMeat/spotipyCollage/blob/main/screenshots/page2.PNG?raw=true" alt=" " width="700"/>
</p>

<p align="center">
<img src="https://github.com/EatSleepBeatMeat/spotipyCollage/blob/main/screenshots/page3.PNG?raw=true" alt=" " width="700"/>
</p>

<p align="center">
    <img src="https://github.com/EatSleepBeatMeat/spotipyCollage/blob/main/screenshots/page3alt.PNG?raw=true" alt=" " width="700" />
</p>

## Setup 

### Libraries required

```python
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
```

### Integrating with spotipy

To run the webpage, user authorization is required. Register your app at [My Dashboard](https://developer.spotify.com/dashboard/applications) to get the credentials necessary to make autorized calls (a `client id` and `client secret`)

Your spotipy `redirect uri` can be `http://example.com`, `http://localhost` or `http://127.0.0.1:9090`. Whichever you'd prefer. For me, I could only use `http://127.0.0.1:9090` for reasons that I can't be bothered to discover.

### Loading environment variables

Use a `.env` file and [python-dotenv](https://github.com/theskumar/python-dotenv) to load your env variables into `album.py`


### Making Changes

Every change made will be reflected in your terminal 

```
 * Detected change in 'C:\\Users\\sendm\\Mooncake\\Kyoto\\albumCover\\album.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 336-424-228
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

To reflect the change to the webpage, refresh the page with `ctrl + shift + r` (Windows 10).

## Going Further

[Intended design](https://github.com/EatSleepBeatMeat/spotipyCollage/blob/main/screenshots/Intended.png?raw=true)

Actually intended to do a [photo collage](https://github.com/adrienverge/PhotoCollage) [like this](https://github.com/adrienverge/PhotoCollage/raw/master/screenshots/photocollage-1.4-preview.png) where the bigger cells would be assigned to your most listened artist but I couldn't understand how to implement it into my code and spotipy didn't have a function to grab number of times listened per artist, or at least I couldn't find it. Had a couple problems installing packages on windows too. 
