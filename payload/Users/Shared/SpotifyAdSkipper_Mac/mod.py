import os
import time
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import subprocess



SCOPE = "user-read-playback-state user-read-currently-playing"


def check_ads():
    if is_ad_playing():
        print("Ad detected")
    else:
        print("No ad detected")

def is_ad_playing(sp):
    """
    Check if an ad is currently playing on Spotify.
    Returns True if an ad is playing, False otherwise.
    """
    current = sp.current_playback()

    if not current:
        print("Nothing is playing")
        return False
    
    item = current.get("item")
    if item is None:
        print("Likely an ad (no track metadata returned)")
        return True

    track_name = item.get("name","").lower()
    artists = [artist["name"].lower() for artist in item.get("artists",[])]
    uri = item.get("uri","").lower()

    if "Ad" in item.get("name","") or "advertisement" in track_name or "spotify" in artists:
        print(f"Likely and ad - Track: {track_name}, Arists: {artists}")
        return True
    
    if "spotify:ad:" in uri :
        print("Likely an ad - URI contains 'spotify:ad:")
        return True
    
    print(f"Not and ad - Track: {track_name}, Artists: {artists}, URI: {uri}")
    return False


def restart_spotify():
    print("Restarting Spotify...")
    subprocess.run(["osascript", "-e", 'quit app "Spotify"']) 
    print("Waiting for Spotify to quit...")
    subprocess.run(["osascript", "-e", 'delay 2'])  # Wait for 2 seconds
    
    #restarting Spotify and pushing spotify to the back of the system, to ensure it doesnt mess with current setup
    subprocess.run(["osascript","-e",'''
                    tell application "Spotify" to launch
                    delay 1
                    tell application "System Events" to set frontmost of process "Spotify" to false
                    '''])
    print("Waiting 3 seconds before continuing...")
    time.sleep(3)

    #playing the song
    subprocess.run(["osascript", "-e", 'tell application "Spotify" to play'])
    
    
    

def getRemainingTime(sp):
    playback = sp.current_playback()
    if not playback or not playback.get("item"):
        return None
    
    duration_ms = playback["item"]["duration_ms"]
    progress_ms = playback["progress_ms"]
    print(duration_ms)
    print(progress_ms)
    
    remaining = (duration_ms - progress_ms)/1000.0
    return(max(0, remaining-10))

def wait_until_near_end(sp):
    remaining_time = getRemainingTime(sp)
    if remaining_time is None:
        print("Could not retrieve playback information.")
        return
    
    print(f"Remaining time: {remaining_time} seconds...")
    time.sleep(remaining_time)


def monitor_and_handle_ad(sp):
    print("Monitoring Spotify for ads...")
    prev_track_id = sp.current_playback()["item"]["id"] if sp.current_playback().get("item") else None
    ad_found = False
    seconds_monitored = 0

    while seconds_monitored < 30:
        if is_ad_playing(sp):
            if is_ad_playing(sp):
                ad_found = True
            break


        curr = sp.current_playback()
        if not curr or not curr.get("item"):
            break
        curr_track_id = curr["item"]["id"]


        #Ecit if a new track starts playing
        if curr_track_id != prev_track_id:
            print("New track started playing, exiting ad monitoring.")
            break

        time.sleep(1)
        seconds_monitored += 1
    

    if ad_found:
        restart_spotify()



# if __name__ == "__main__":
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = SCOPE))


#     while True:
#         try:
#             wait_until_near_end(sp)
#             monitor_and_handle_ad(sp)

#         except KeyboardInterrupt:
#             print("Stopped by user.")
#             break
#         except Exception as e:
#             print(f"Error: {e}.\nRetrying in 5 seconds...")
#             time.sleep(5)

