import os.path
from constants import *

class Cache:
	def __init__(self):
		self.data = {}

		if not os.path.isfile(CACHE_FILE):
			return

		with open(CACHE_FILE) as f:
			while True:
				artistsong = f.readline().rstrip()

				if not artistsong:
					break

				uri = f.readline().rstrip()
				sartist = f.readline().rstrip()
				ssong = f.readline().rstrip()
				self.data[artistsong] = { "artist": sartist, "song": ssong, "uri": uri }

		print(f"Cache loaded with {len(self.data)} songs.")

	def Add(self, artist, song, uri, sartist, ssong):
		self.data[artist + song] = { "artist": sartist, "song": ssong, "uri": uri }

		with open(CACHE_FILE, "a") as file:
			file.write(artist + song + "\n")
			file.write(uri + "\n")
			file.write(sartist + "\n")
			file.write(ssong + "\n")

	def Get(self, artist, song):
		return self.data.get(artist + song)