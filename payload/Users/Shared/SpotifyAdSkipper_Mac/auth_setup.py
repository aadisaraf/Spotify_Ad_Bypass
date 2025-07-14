import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os

SPOTIPY_CLIENT_ID = '569b06aa78e0429a8889f02319835662'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:3000'
SCOPE = "user-read-playback-state user-modify-playback-state"
CACHE_PATH = os.path.expanduser("~/.spotify_token_cache")


def main():
    auth_manager = SpotifyPKCE(
        client_id=SPOTIPY_CLIENT_ID,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH
    )

    # This will open the browser and ask for auth if needed,
    # then cache the token.
    token = auth_manager.get_access_token()
    print("Access token:", token)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user = sp.current_user()
    print("Current user:", user)

if __name__ == "__main__":
    main()
