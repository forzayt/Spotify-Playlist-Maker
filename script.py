import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time

CLIENT_ID = "57e7d63ff50e46058facee08174119c7"
CLIENT_SECRET = "c8f8624cc0c245db82a065d2f8182f7c"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public"
PLAYLIST_NAME = "Popular Songs Non Stop"

# No filters
forbidden_keywords = []
instrumental_keywords = []

# Generate multi-letter search queries for broader coverage
letters = "abcdefghijklmnopqrstuvwxyz"
search_queries = [l for l in letters] + [a+b for a in letters for b in letters]

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    user_id = sp.current_user()["id"]

    # Create or get playlist
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
            description="All Spotify songs playlist!"
        )
        playlist_id = new_playlist["id"]
        print(f"✅ Created new playlist: {PLAYLIST_NAME}")

    return sp, playlist_id

def run_loop(sp, playlist_id):
    existing_track_ids = set()
    seen_queries = set()  # track which queries + offsets we already did

    # Load existing playlist tracks
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

    print(f"📊 Already have {len(existing_track_ids)} tracks in playlist.")

    try:
        while True:
            search_query = random.choice(search_queries)
            search_limit = 50
            max_offset = 1000  # Spotify limit per query
            offset_choices = [i for i in range(0, max_offset, search_limit)]

            # pick an offset not used yet for this query
            random.shuffle(offset_choices)
            for offset in offset_choices:
                query_key = f"{search_query}_{offset}"
                if query_key in seen_queries:
                    continue
                seen_queries.add(query_key)

                results = sp.search(q=search_query, type="track", limit=search_limit, offset=offset)
                tracks = results["tracks"]["items"]

                new_track_ids = [t["id"] for t in tracks if t["id"] not in existing_track_ids]

                if new_track_ids:
                    sp.playlist_add_items(playlist_id, new_track_ids)
                    existing_track_ids.update(new_track_ids)
                    print(f"✅ Added {len(new_track_ids)} new tracks from query '{search_query}' offset {offset}")
                else:
                    print(f"⚠️ No new tracks for query '{search_query}' offset {offset}")

                time.sleep(1)  # avoid hitting rate limits

            # Optional pause between cycles
            print("🔄 Cycle complete. Restarting new queries...\n")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Loop stopped manually by user.")

if __name__ == "__main__":
    sp, playlist_id = main()
    run_loop(sp, playlist_id)
