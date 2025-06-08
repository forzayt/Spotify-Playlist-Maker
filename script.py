import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import requests.exceptions

# Replace with your actual credentials
CLIENT_ID = "57e7d63ff50e46058facee08174119c7"
CLIENT_SECRET = "c8f8624cc0c245db82a065d2f8182f7c"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public"
PLAYLIST_NAME = "Global Slowed + Reverb Playlist"

# List of keywords to skip
forbidden_keywords = ["phonk", "funk", "sigma", "sped up", "nightcore", "bass boosted"]

try:
    # Step 1: Auth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    # Step 2: Get current user
    user_id = sp.current_user()["id"]

    # Step 3: Check for existing playlist
    playlist_id = None
    playlists = sp.current_user_playlists(limit=50)["items"]
    for playlist in playlists:
        if playlist["name"] == PLAYLIST_NAME:
            playlist_id = playlist["id"]
            break

    # Step 4: Create playlist if not found
    if not playlist_id:
        new_playlist = sp.user_playlist_create(
            user=user_id,
            name=PLAYLIST_NAME,
            public=True,
            description="Auto-filled slowed + reverb songs"
        )
        playlist_id = new_playlist["id"]
        print(f"✅ Created new playlist: {PLAYLIST_NAME}")

    # Step 5: Search for slowed + reverb songs
    search_query = "slowed reverb"
    search_limit = 20

    results = sp.search(q=search_query, type="track", limit=search_limit)
    tracks = results["tracks"]["items"]

    # Step 6: Filter & collect track IDs
    track_ids = []
    for track in tracks:
        name = track["name"].lower()
        album = track["album"]["name"].lower()
        if any(bad in name for bad in forbidden_keywords):
            continue
        if any(bad in album for bad in forbidden_keywords):
            continue
        track_ids.append(track["id"])

    # Step 7: Add to playlist
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)
        print(f"✅ Added {len(track_ids)} filtered slowed + reverb songs to your playlist!")
    else:
        print("⚠️ No slowed + reverb tracks passed the filter.")

except (SpotifyException, requests.exceptions.RequestException) as e:
    print(f"❌ Error occurred: {e}")
