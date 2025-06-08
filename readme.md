# Spotify Slowed + Reverb Playlist Generator

A Python script that automatically creates and maintains a curated Spotify playlist of slowed + reverb songs while filtering out unwanted genres and instrumental tracks.

## Features

- 🎵 **Automatic Playlist Creation**: Creates a public Spotify playlist if it doesn't exist
- 🔍 **Smart Filtering**: Filters out unwanted genres (phonk, trap, metal, etc.)
- 🎤 **Vocals Only**: Excludes instrumental tracks and beats
- 📊 **Detailed Reporting**: Shows filtering statistics after each run
- 🔄 **Multi-field Detection**: Checks track names, album names, and artist names
- ⏱️ **Duration-based Filtering**: Catches short instrumental beats

## Prerequisites

- Python 3.6 or higher
- Spotify Developer Account
- Spotify Premium (recommended for best experience)

## Installation

1. **Install required packages:**
   ```bash
   pip install spotipy requests
   ```

2. **Set up Spotify Developer Account:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new app
   - Note down your `Client ID` and `Client Secret`
   - Add `http://127.0.0.1:8888/callback` to your app's redirect URIs

3. **Update credentials in the script:**
   ```python
   CLIENT_ID = "your_client_id_here"
   CLIENT_SECRET = "your_client_secret_here"
   ```

## Configuration

### Playlist Settings
- **Playlist Name**: "Slowed + Reverb Global Playlist"
- **Visibility**: Public
- **Description**: "Slowed + reverb songs across the spotify server Auto-Updates Daily!"

### Filtering Options

**Forbidden Genres** (automatically excluded):
- Electronic: phonk, trap, dubstep, EDM, hardstyle, hyperpop
- Metal: death metal, black metal, metalcore, deathcore
- Regional: k-pop, j-pop, reggaeton, latin trap
- Ambient: lofi, chillwave, meditation music, nature sounds
- And many more...

**Instrumental Detection** (automatically excluded):
- Tracks with "instrumental", "beat", "type beat" in title
- Producer tags like "(prod", "[prod", "prod by"
- Covers and karaoke versions
- Short tracks (<2 minutes) with suspicious terms

## Usage

1. **Run the script:**
   ```bash
   python spotify_playlist_generator.py
   ```

2. **First-time authentication:**
   - Browser will open for Spotify login
   - Authorize the application
   - You'll be redirected to a callback URL
   - Copy the entire URL and paste it back in the terminal

3. **Subsequent runs:**
   - Authentication token is cached
   - Script runs automatically without browser interaction

## Output Example

```
✅ Created new playlist: Slowed + Reverb Global Playlist
✅ Added 23 filtered slowed + reverb songs to your playlist!
📊 Filtered out 15 tracks with forbidden keywords
🎵 Filtered out 8 instrumental tracks
📈 Total tracks processed: 50
```

## Customization

### Adding/Removing Genres
Edit the `forbidden_keywords` list to customize which genres to exclude:
```python
forbidden_keywords = [
    "phonk", "trap", "metal",  # Add or remove genres here
    # ... rest of the list
]
```

### Modifying Instrumental Detection
Update the `instrumental_keywords` list to catch different types of instrumental tracks:
```python
instrumental_keywords = [
    "instrumental", "beat", "karaoke",  # Add terms here
    # ... rest of the list
]
```

### Changing Search Parameters
Modify search settings:
```python
search_query = "slowed reverb"  # Change search terms
search_limit = 50  # Adjust number of tracks to process
```

## Troubleshooting

### Common Issues

**"Invalid client" error:**
- Double-check your `CLIENT_ID` and `CLIENT_SECRET`
- Ensure redirect URI is set correctly in Spotify Developer Dashboard

**"Insufficient client scope" error:**
- Make sure `SCOPE = "playlist-modify-public"` is set correctly
- Clear cached tokens and re-authenticate

**No tracks found:**
- Check your internet connection
- Verify Spotify API is accessible
- Try adjusting search terms

**Too many tracks filtered:**
- Review your `forbidden_keywords` list
- Consider reducing instrumental detection strictness

### Debug Mode
Add debugging to see what's being filtered:
```python
print(f"Checking track: {track['name']} by {track['artists'][0]['name']}")
```

## Rate Limits

- Spotify API has rate limits
- Script includes basic error handling
- If you hit limits, wait a few minutes and retry

## Security Notes

- Never commit your credentials to version control
- Consider using environment variables for sensitive data:
  ```python
  import os
  CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
  CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
  ```

## License

This project is for educational purposes. Respect Spotify's Terms of Service and API usage guidelines.

## Contributing

Feel free to submit issues or pull requests to improve the filtering logic or add new features!

---

**Note**: This script is designed to run manually. For automated daily updates, consider setting up a cron job (Linux/Mac) or Task Scheduler (Windows).