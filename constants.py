import os
from secret_constants import CLIENT_SECRET

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SCOPE = "playlist-modify-public"
REDIRECT_URL = "https://example.com/callback"
CLIENT_ID = "ab817804d47f4f0894f01d5fad7fbb25"
AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
ME_URL = "https://api.spotify.com/v1/me"
REFRESH_TOKEN_FILE_NAME = "refresh.token"
SEARCH_URL = "https://api.spotify.com/v1/search"
NOT_FOUND_FILE = "not_found.txt"
PLAYLIST_DIR = ROOT_DIR + "/playlists"
CACHE_FILE = "cache.txt"
TEST_FILE = "testit.txt"
PLAYLIST_ID_FILE = PLAYLIST_DIR + "/ids.txt"
PLAYLIST_URL = "https://api.spotify.com/v1/playlists/"
PLAYLIST_FILE = "playlist_ids.txt"
USERS_URL = "https://api.spotify.com/v1/users/"
TOTAL_FILE = "total.txt"
HTML_FILE = "playlists.html"
PUBLIC_PLAYLIST_URL = "https://open.spotify.com/playlist/"