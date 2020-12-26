from connection import Connection
from constants import *
import billboard.data
import re
import billboard.constants
import os.path
import sys
from cache import Cache

rx = re.compile("([^\w ]|_)")
cache = Cache()

def Fix(name, artist, level):
	name = re.sub("\(.*?\)", "", name)
	name = re.sub(" feat.*", "", name, flags = re.IGNORECASE)

	if artist:
		name = re.sub(" starring.*", "", name, flags = re.IGNORECASE)
		name = re.sub(" duet with .*", "", name, flags = re.IGNORECASE)		
		name = re.sub(" with .*", "", name, flags = re.IGNORECASE)		
		name = re.sub(" and the .*", "", name, flags = re.IGNORECASE)		
		name = re.sub(" and his .*", "", name, flags = re.IGNORECASE)

		if level >= 2:
			name = re.sub(" and .*", "", name, flags = re.IGNORECASE)

	if level >= 2:
		name = re.sub("\/.*", "", name, flags = re.IGNORECASE)

		if artist:
			name = re.sub("&.*", "", name, flags = re.IGNORECASE)
			name = re.sub(" x .*", "", name, flags = re.IGNORECASE)

	if level >= 1:
		name = re.sub("the ", "", name, flags = re.IGNORECASE)

		if not artist:
			name = re.sub("-.*", "", name)

	name = rx.sub(' ', name)
	name = name.rstrip().lstrip()

	return name


def GetSong(connection, artistName_, songName_):
	print(f"\nSearching: {artistName_}: {songName_}")

	cached = cache.Get(artistName_, songName_)

	if cached:
		print("\n\t" + f'{cached["artist"]}: {cached["song"]} [cached]')
		cached["cached"] = True
		return cached

	result = None

	for level in range(0, 3):
		artistName = Fix(artistName_, True, level)
		songName = Fix(songName_, False, level)

		q = "artist:" + artistName + " NOT karaoke track:" + songName +" NOT karaoke"

		params = {"q": q, "type": "track"}

		r = connection.Get(SEARCH_URL, params = params)
		items = r["tracks"]["items"]

		if items:
			result = items[0]
			break

	if artistName != artistName_ or songName != songName_:
		print(f"=========> {artistName}: {songName}")

	if result:
		print("\n\t" + f'{result["artists"][0]["name"]}: {result["name"]}')
	else:
		with open(NOT_FOUND_FILE, "a") as file:
			file.write(artistName_ + "\n")
			file.write(songName_ + "\n")

		print("\n\t NOT FOUND")

	if not result:
		return None

	sartist = result["artists"][0]["name"]
	ssong = result["name"]
	uri = result["uri"]

	cache.Add(artistName_, songName_, uri, sartist, ssong)
	return {"artist": sartist, "song": ssong, "uri": uri, "cached": False}