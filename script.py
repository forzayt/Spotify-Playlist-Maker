import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import requests.exceptions

# Replace with your actual credentials
CLIENT_ID = "57e7d63ff50e46058facee08174119c7"
CLIENT_SECRET = "c8f8624cc0c245db82a065d2f8182f7c"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public"
PLAYLIST_NAME = "Slowed + Reverb Global Playlist "

# List of keywords to skip
forbidden_keywords = [
    "phonk", "funk", "sigma", "sped up", "nightcore", "bass boosted", "hyperpop",
    "trap", "drill", "dubstep", "EDM", "hardstyle", "hardcore", "screamo", "emo",
    "punk", "metal", "deathcore", "grindcore", "industrial", "goregrind", "noisegrind",
    "pornogrind", "crust punk", "cyberpunk", "crunkcore", "electropunk", "digital hardcore",
    "glitchcore", "vaporwave", "chillwave", "lofi", "ambient", "psytrance", "reggaeton",
    "latin trap", "k-pop", "j-pop", "c-pop", "t-pop", "bossa nova", "salsa", "merengue",
    "reggae", "ska", "dub", "bluegrass", "country", "folk", "gospel", "classical", "opera",
    "jazz", "blues", "soul", "R&B", "disco", "funk rock", "boogie", "electro funk", "go-go",
    "avant-funk", "nu-funk", "synth-funk", "synthwave", "retrowave", "chiptune", "8-bit",
    "video game music", "anime music", "soundtrack", "musical theatre", "show tunes",
    "easy listening", "lounge", "flamenco", "tango", "samba", "cumbia",
    "mambo", "cha-cha", "bhangra", "kirtan", "qawwali", "sufi", "ghazal",
    "devotional", "chant", "mantra", "new age", "spiritual", "meditation", "yoga music",
    "nature sounds", "white noise", "pink noise", "brown noise", "sleep music",
    "study music", "focus music", "relaxation music", "healing music", "sound therapy",
    "brainwave entrainment", "isochronic tones", "binaural beats", "solfeggio frequencies",
    "432 Hz", "528 Hz", "639 Hz", "741 Hz", "852 Hz", "963 Hz", "delta waves", "theta waves",
    "alpha waves", "beta waves", "gamma waves", "lucid dreaming", "out-of-body experience",
    "astral projection", "remote viewing", "telepathy", "psychic", "paranormal", "occult",
    "esoteric", "mysticism", "alchemy", "alchemy music", "hermetic", "theosophy", "gnostic",
    "occult rock", "psychedelic rock", "stoner rock", "doom metal", "sludge metal", "black metal",
    "death metal", "thrash metal", "power metal", "speed metal", "prog metal", "metalcore",
    "post-metal", "hardcore punk", "anarcho-punk", "oi!", "ska punk", "street punk", 
    "pop punk", "emo pop", "post-hardcore", "mathcore", "noise rock", "experimental rock", 
    "avant-garde metal", "industrial metal", "gothic metal", "powerviolence", "doomcore", 
    "sludgecore", "deathgrind", "crustgrind", "cybergrind", "stoner metal",
    # Legitimate blackened subgenres only
    "blackened death metal", "blackened doom", "blackened thrash", "blackened hardcore",
    "blackened crust", "blackened grind", "blackened sludge", "blackened deathcore"
]

# Keywords that indicate instrumental tracks (to exclude)
instrumental_keywords = [
    "instrumental", "instrumentals", "karaoke", "backing track", "backing tracks",
    "piano version", "guitar version", "acoustic version", "cover version", "cover",
    "beat", "beats", "track", "background music", "bgm", "soundtrack", "ost",
    "theme", "intro", "outro", "interlude", "bridge", "breakdown", "drop",
    "piano solo", "guitar solo", "drum solo", "bass solo", "violin solo", "flute solo",
    "orchestral", "symphony", "concerto", "prelude", "etude", "sonata", "nocturne",
    "waltz", "minuet", "scherzo", "rondo", "fugue", "toccata", "fantasie", "rhapsody",
    "improvisation", "jam", "live session", "studio session", "rehearsal", "practice",
    "no vocals", "without vocals", "minus vocals", "vocal removed", "vocals removed",
    "sing along", "singalong", "playback", "playalong", "music only", "melody only",
    "tune", "arrangement", "orchestration", "composition", "piece", "movement",
    "(instrumental)", "[instrumental]", "- instrumental", "instrumental -",
    "piano cover", "guitar cover", "violin cover", "flute cover", "saxophone cover",
    "harp cover", "cello cover", "drums cover", "bass cover", "organ cover",
    "music box", "lullaby version", "elevator music", "hold music", "waiting music",
    # Additional terms to catch phonk instrumentals and similar
    "type beat", "type", "(prod", "[prod", "prod by", "produced by", "freestyle beat",
    "rap beat", "hip hop beat", "trap beat", "phonk beat", "drill beat", "loop",
    "sample", "remix beat", "hard beat", "fire beat", "crazy beat", "insane beat"
]

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
            description="Slowed + reverb songs across the spotify server Auto-Updates Daily!"
        )
        playlist_id = new_playlist["id"]
        print(f"✅ Created new playlist: {PLAYLIST_NAME}")

    return sp, playlist_id

def run_loop(sp, playlist_id):
    try:
        while True:
            print("🔄 Starting a new search cycle...")

            search_query = "slowed reverb"
            search_limit = 50

            results = sp.search(q=search_query, type="track", limit=search_limit)
            tracks = results["tracks"]["items"]

            track_ids = []
            filtered_count = 0
            instrumental_filtered = 0

            for track in tracks:
                name = track["name"].lower()
                album = track["album"]["name"].lower()
                artist_names = " ".join([artist["name"].lower() for artist in track["artists"]])

                if any(bad in name for bad in forbidden_keywords):
                    filtered_count += 1
                    continue
                if any(bad in album for bad in forbidden_keywords):
                    filtered_count += 1
                    continue
                if any(bad in artist_names for bad in forbidden_keywords):
                    filtered_count += 1
                    continue

                if any(instr in name for instr in instrumental_keywords):
                    instrumental_filtered += 1
                    continue
                if any(instr in album for instr in instrumental_keywords):
                    instrumental_filtered += 1
                    continue
                if any(instr in artist_names for instr in instrumental_keywords):
                    instrumental_filtered += 1
                    continue

                if "music" in name and ("only" in name or "version" in name):
                    instrumental_filtered += 1
                    continue

                duration_ms = track.get("duration_ms", 0)
                if duration_ms > 0 and duration_ms < 120000:
                    suspicious_terms = ["beat", "type", "style", "(prod", "[prod", "freestyle", "loop"]
                    if any(term in name for term in suspicious_terms):
                        instrumental_filtered += 1
                        continue

                track_ids.append(track["id"])

            if track_ids:
                sp.playlist_add_items(playlist_id, track_ids)
                print(f"✅ Added {len(track_ids)} filtered slowed + reverb songs to your playlist!")
            else:
                print("⚠️ No slowed + reverb tracks passed the filter this cycle.")

            print(f"📊 Filtered out {filtered_count} tracks with forbidden keywords")
            print(f"🎵 Filtered out {instrumental_filtered} instrumental tracks")
            print(f"📈 Total tracks processed this cycle: {len(tracks)}")
            print()  # Just a newline for readability

    except KeyboardInterrupt:
        print("\n🛑 Loop stopped manually by user. Exiting gracefully...")

    except (SpotifyException, requests.exceptions.RequestException) as e:
        print(f"❌ Error occurred: {e}")
        print("Retrying immediately...")
        run_loop(sp, playlist_id)  # Restart loop after error

if __name__ == "__main__":
    sp, playlist_id = main()
    run_loop(sp, playlist_id)
