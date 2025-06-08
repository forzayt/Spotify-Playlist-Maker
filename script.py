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
    "easy listening", "lounge", "bossa nova", "flamenco", "tango", "samba", "cumbia",
    "merengue", "mambo", "cha-cha", "bhangra", "kirtan", "qawwali", "sufi", "ghazal",
    "devotional", "chant", "mantra", "new age", "spiritual", "meditation", "yoga music",
    "ambient", "nature sounds", "white noise", "pink noise", "brown noise", "sleep music",
    "study music", "focus music", "relaxation music", "healing music", "sound therapy",
    "brainwave entrainment", "isochronic tones", "binaural beats", "solfeggio frequencies",
    "432 Hz", "528 Hz", "639 Hz", "741 Hz", "852 Hz", "963 Hz", "delta waves", "theta waves",
    "alpha waves", "beta waves", "gamma waves", "lucid dreaming", "out-of-body experience",
    "astral projection", "remote viewing", "telepathy", "psychic", "paranormal", "occult",
    "esoteric", "mysticism", "alchemy", "alchemy music", "hermetic", "theosophy", "gnostic",
    "occult rock", "psychedelic rock", "stoner rock", "doom metal", "sludge metal", "black metal",
    "death metal", "thrash metal", "power metal", "speed metal", "prog metal", "metalcore",
    "post-metal", "doom metal", "sludge metal", "grindcore", "hardcore punk", "crust punk",
    "anarcho-punk", "oi!", "ska punk", "street punk", "pop punk", "emo pop", "screamo",
    "post-hardcore", "mathcore", "noise rock", "experimental rock", "avant-garde metal",
    "industrial metal", "gothic metal", "deathcore", "metalcore", "hardcore", "post-hardcore",
    "grindcore", "powerviolence", "doomcore", "sludgecore", "deathgrind", "crustgrind",
    "pornogrind", "noisegrind", "goregrind", "cybergrind", "mathcore", "post-metal",
    "sludge metal", "doom metal", "stoner metal", "blackened death metal", "blackened doom",
    "blackened crust", "blackened grind", "blackened hardcore", "blackened thrash",
    "blackened speed metal", "blackened sludge", "blackened prog", "blackened folk",
    "blackened ambient", "blackened noise", "blackened experimental", "blackened avant-garde",
    "blackened industrial", "blackened gothic", "blackened electronic", "blackened synth",
    "blackened pop", "blackened rap", "blackened hip hop", "blackened jazz", "blackened blues",
    "blackened soul", "blackened R&B", "blackened disco", "blackened funk", "blackened reggae",
    "blackened ska", "blackened dub", "blackened bossa nova", "blackened salsa", "blackened tango",
    "blackened cumbia", "blackened merengue", "blackened mambo", "blackened cha-cha", "blackened bhangra",
    "blackened kirtan", "blackened qawwali", "blackened sufi", "blackened ghazal", "blackened devotional",
    "blackened chant", "blackened mantra", "blackened new age", "blackened spiritual", "blackened meditation",
    "blackened yoga music", "blackened ambient", "blackened nature sounds", "blackened white noise",
    "blackened pink noise", "blackened brown noise", "blackened sleep music", "blackened study music",
    "blackened focus music", "blackened relaxation music", "blackened healing music", "blackened sound therapy",
    "blackened brainwave entrainment", "blackened isochronic tones", "blackened binaural beats",
    "blackened solfeggio frequencies", "blackened 432 Hz", "blackened 528 Hz", "blackened 639 Hz",
    "blackened 741 Hz", "blackened 852 Hz", "blackened 963 Hz", "blackened delta waves", "blackened theta waves",
    "blackened alpha waves", "blackened beta waves", "blackened gamma waves", "blackened lucid dreaming",
    "blackened out-of-body experience", "blackened astral projection", "blackened remote viewing",
    "blackened telepathy", "blackened psychic", "blackened paranormal", "blackened occult", "blackened esoteric",
    "blackened mysticism", "blackened alchemy", "blackened hermetic", "blackened theosophy", "blackened gnostic",
    "blackened occult rock", "blackened psychedelic rock", "blackened stoner rock", "blackened doom metal",
    "blackened sludge metal", "blackened black metal", "blackened death metal", "blackened thrash metal",
    "blackened power metal", "blackened speed metal", "blackened prog metal", "blackened metalcore",
    "blackened post-metal", "blackened doom metal", "blackened sludge metal", "blackened grindcore",
    "blackened hardcore punk", "blackened crust punk", "blackened anarcho-punk", "blackened oi!", "blackened ska punk",
    "blackened street punk", "blackened pop punk", "blackened emo pop", "blackened screamo", "blackened post-hardcore",
    "blackened mathcore", "blackened noise rock", "blackened experimental rock", "blackened avant-garde metal",
    "blackened industrial metal", "blackened gothic metal", "blackened deathcore", "blackened metalcore",
    "blackened hardcore", "blackened post-hardcore", "blackened grindcore", "blackened powerviolence",
    "blackened doomcore", "blackened sludgecore", "blackened deathgrind", "blackened crustgrind", "blackened pornogrind",
    "blackened noisegrind", "blackened goregrind", "blackened cybergrind", "blackened mathcore", "blackened post-metal",
    "blackened sludge metal", "blackened doom metal", "blackened stoner metal", "blackened blackened death metal",
    "blackened blackened thrash", "blackened blackened speed metal", "blackened blackened sludge", "blackened blackened prog",
    "blackened blackened folk", "blackened blackened ambient", "blackened blackened noise", "blackened blackened experimental",
    "blackened blackened avant-garde", "blackened blackened industrial", "blackened blackened gothic",
    "blackened blackened electronic", "blackened blackened synth", "blackened blackened pop", "blackened blackened rap",
    "blackened blackened hip hop", "blackened blackened jazz", "blackened blackened blues", "blackened blackened soul",
    "blackened blackened R&B", "blackened blackened disco", "blackened blackened funk", "blackened blackened reggae",
    "blackened blackened ska", "blackened blackened dub", "blackened blackened bossa nova", "blackened blackened salsa",
    "blackened blackened tango", "blackened blackened cumbia", "blackened blackened merengue", "blackened blackened mambo",
    "blackened blackened cha-cha", "blackened blackened bhangra", "blackened blackened kirtan", "blackened blackened qawwali",
    "blackened blackened sufi", "blackened blackened ghazal", "blackened blackened devotional", "blackened blackened chant",
    "blackened blackened mantra", "blackened blackened new age", "blackened blackened spiritual", "blackened blackened meditation",
    "blackened blackened yoga music", "blackened blackened ambient", "blackened blackened nature sounds", "blackened blackened white noise",
    "blackened blackened pink noise", "blackened blackened brown noise", "blackened blackened sleep music", "blackened blackened study music",
    "blackened blackened focus music", "blackened blackened relaxation music", "blackened blackened healing music", "blackened blackened sound therapy",
    "blackened blackened brainwave entrainment", "blackened blackened isochronic tones", "blackened blackened binaural beats",
    "blackened blackened solfeggio frequencies", "blackened blackened 432 Hz", "blackened blackened 528 Hz",
    "blackened blackened 639 Hz", "blackened blackened 741 Hz", "blackened blackened 852 Hz", "blackened blackened 963 Hz",]

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
    search_limit = 50

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
