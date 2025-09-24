import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import requests.exceptions
import random
import time

# Replace with your actual credentials
CLIENT_ID = "57e7d63ff50e46058facee08174119c7"
CLIENT_SECRET = "c8f8624cc0c245db82a065d2f8182f7c"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public"
PLAYLIST_NAME = "Popular Songs Non Stop"

# No forbidden or instrumental filters
forbidden_keywords = []
instrumental_keywords = []

# No custom search queries – placeholder to fetch everything
search_queries = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    user_id = sp.current_user()["id"]

    playlist_id = None
    playlists = sp.current_user_playlists(limit=50)["items"]
    for playlist in playlists:
        if playlist["name"] == PLAYLIST_NAME:
            playlist_id = playlist["id"]
            break
    if not playlist_id:
        new_playlist = sp.user_playlist_create(
            user=user_id,
            name=PLAYLIST_NAME,
            public=True,
            description="Best playlist on SPOTIFY __ Jesus Loves You <3 !"
        )
        playlist_id = new_playlist["id"]
        print(f"✅ Created new playlist: {PLAYLIST_NAME}")

    return sp, playlist_id

def run_loop(sp, playlist_id):
    try:
        existing_track_ids = set()
        results = sp.playlist_items(playlist_id, fields='items.track.id,total', additional_types=['track'])
        while results:
            for item in results["items"]:
                track = item.get("track")
                if track:
                    existing_track_ids.add(track["id"])
            if results.get("next"):
                results = sp.next(results)
            else:
                break

        while True:
            print("🔄 Starting a new search cycle...")

            search_query = random.choice(search_queries)
            search_limit = 50
            max_offset = 1000  # Spotify's limit
            random_offset = random.randint(0, max_offset // search_limit - 1) * search_limit

            results = sp.search(q=search_query, type="track", limit=search_limit, offset=random_offset)
            tracks = results["tracks"]["items"]

            new_track_ids = []
            filtered_count = 0
            instrumental_filtered = 0
            duplicate_skipped = 0

            for track in tracks:
                track_id = track["id"]
                name = track["name"].lower()
                album = track["album"]["name"].lower()
                artist_names = " ".join([artist["name"].lower() for artist in track["artists"]])

                if track_id in existing_track_ids:
                    duplicate_skipped += 1
                    continue

                if any(bad in name for bad in forbidden_keywords) or \
                   any(bad in album for bad in forbidden_keywords) or \
                   any(bad in artist_names for bad in forbidden_keywords):
                    filtered_count += 1
                    continue

                if any(instr in name for instr in instrumental_keywords) or \
                   any(instr in album for instr in instrumental_keywords) or \
                   any(instr in artist_names for instr in instrumental_keywords):
                    instrumental_filtered += 1
                    continue

                if "music" in name and ("only" in name or "version" in name):
                    instrumental_filtered += 1
                    continue

                duration_ms = track.get("duration_ms", 0)
                if duration_ms < 120000 and any(term in name for term in ["beat", "type", "(prod", "[prod", "loop"]):
                    instrumental_filtered += 1
                    continue

                new_track_ids.append(track_id)

            if new_track_ids:
                sp.playlist_add_items(playlist_id, new_track_ids)
                existing_track_ids.update(new_track_ids)
                print(f"✅ Added {len(new_track_ids)} new tracks to the playlist!")
            else:
                print("⚠️ No new tracks passed the filter this cycle.")

            print(f"📊 Forbidden keyword filters: {filtered_count}")
            print(f"🎵 Instrumental filters: {instrumental_filtered}")
            print(f"♻️ Duplicate tracks skipped: {duplicate_skipped}")
            print(f"📈 Total searched this cycle: {len(tracks)}\n")

         #   time.sleep(3600)  # Wait 1 hour before next search

    except KeyboardInterrupt:
        print("\n🛑 Loop stopped manually by user.")
    except (SpotifyException, requests.exceptions.RequestException) as e:
        print(f"❌ Error occurred: {e}")
        print("Retrying...")
        run_loop(sp, playlist_id)

if __name__ == "__main__":
    sp, playlist_id = main()
    run_loop(sp, playlist_id)
