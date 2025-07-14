
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyPKCE
from mod import wait_until_near_end, monitor_and_handle_ad  # make sure these are in mod.py

import os
from dotenv import load_dotenv

SPOTIPY_CLIENT_ID='569b06aa78e0429a8889f02319835662'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:3000'
SCOPE = "user-read-playback-state user-modify-playback-state"
CACHE_PATH = os.path.expanduser("~/.spotify_token_cache")

auth_manager = SpotifyPKCE(
            client_id=SPOTIPY_CLIENT_ID,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE_PATH
        )
sp = spotipy.Spotify(auth_manager=auth_manager)

def is_spotify_running():
    try:
        subprocess.check_output(["pgrep", "-x", "Spotify"])
        return True
    except subprocess.CalledProcessError:
        return False

def main_loop():
    print("starting main loop...")
    # sp = None
    
    while True:  # Infinite loop to keep the script running forever
        print("Waiting for Spotify to open...")
        
        # Wait until Spotify is running
        while not is_spotify_running():
            time.sleep(15)  # Check every 5 seconds instead of 200 for quicker response

        print("Spotify is open. Starting ad detection logic...")

        # Authenticate with Spotipy (do this after Spotify opens)
       

        # While Spotify is running, run your ad detection
        while is_spotify_running():
            try:
                wait_until_near_end(sp)
                monitor_and_handle_ad(sp)
            except KeyboardInterrupt:
                print("Stopped by user.")
                return
            except Exception as e:
                print(f"Error: {e}.\nRetrying in 5 seconds...")
                time.sleep(5)

        print("Spotify closed. Waiting for it to open again...")

if __name__ == "__main__":
    main_loop()
