from connection import *
from constants import *
import constants
import argparse
import billboard.data
import re
import billboard.constants
import os.path
import sys
from songs import *

def Rate():
	i = 0 

	while True:
		i = i + 1
		print(str(i) + ": ", end = "")
		connection.Get(constants.ME_URL)
		print("ok")


def Test():
	count = 0
	found = 0

	print("-------------------")

	with open(TEST_FILE) as file:
		while True:
			artistName = file.readline().rstrip()
			songName = file.readline().rstrip()

			if artistName.startswith("#"):
				continue

			if not artistName:
				break

			count = count + 1

			ss = GetSong(connection, artistName, songName)

			if ss:
				found = found + 1

	print("-------------------")
	print (f"Found {found} / {count}")
	print("-------------------")

def Randomia():
	db = billboard.data.Database()

	found = []
	notFound = []
	
	for i in range(0, 100):
		song = db.GetRandomSong()

		ss = GetSong(connection, song.artist, song.name)

		if ss:
			found.append(f'{ss["artist"]}: {ss["song"]}')
		else:
			notFound.append(song)

	print(f"Found: {len(found)}")
	print(f"Not found: {len(notFound)}")

	for s in found:
		print("Found: " + s)

	for s in notFound:
		print("Not found: " + str(s))


def Me():
	print(connection.Get(constants.ME_URL))


def GetLineCount(filename):
	result = 0

	with open(filename, "r") as f:
		for line in f:
			result = result + 1

	return result

def MakePlaylistFile(inFilename, outFilename):
	print("Making playlist from " + inFilename + " to " + outFilename)

	notFound = []

	old = sys.stdout
	logFilename = outFilename + ".log"

	with open(logFilename, "w") as log:
		sys.stdout = log
		
		with open(outFilename, "w") as f:
			i = 0

			count = round(GetLineCount(inFilename) / 2)

			with open(inFilename, "r") as inp:
				while True:
					i = i + 1

					artist = inp.readline().rstrip()
					song = inp.readline().rstrip()

					if not artist:
						break

					ss = GetSong(connection, artist, song)

					if ss:
						f.write(ss["uri"] + "\n")
						old.write(f'{i}/{count} {ss["artist"]}: {ss["song"]}')
						
						if ss["cached"]:
							old.write(" [CACHED]")

					else:
						stringi = artist + ": " + song
						notFound.append(stringi)
						old.write("\t"+ str(i) + " NOT FOUND: " + stringi)

					old.write("\n")
					old.flush()

	sys.stdout = old

	print("----------------------------")

	nn = len(notFound)
	nf = count - nn
	prse = round(100 * nf / count)

	stuff = f"Found {nf}/{count} = {prse}%\n"
	stuff = stuff + f"{nn} not found: \n"

	for s in notFound:
		stuff = stuff + s + "\n"

	print(stuff)

	with open("temp.tmp", "w") as temp:
		temp.write(stuff)

		temp.write("--------- log -----------")

		with open(logFilename, "r") as log:
			temp.write(log.read())

	os.rename("temp.tmp", logFilename)

	result = {"total": count, "found": nf}
	return result

def Retry():
	os.rename(constants.NOT_FOUND_FILE, "temp.tmp")

	total = 0
	found = 0

	with open("temp.tmp", "r") as f:
		while True:
			artist = f.readline().rstrip()
			song = f.readline().rstrip()

			if not artist:
				break

			total = total + 1

			ss = GetSong(connection, artist, song)

			if ss:
				found = found + 1

	os.remove("temp.tmp")

	print(f"Found {found}/{total}")


def MakePlaylistFiles():
	total = 0
	found = 0

	for i in range(1, 101):
		result = MakePlaylistFile(billboard.constants.PEAK_DIR + f"/{i}_raw.txt", constants.PLAYLIST_DIR + f"/{i}.txt")

		total = total + result["total"]
		found = found + result["found"]
		
		prse = round(100 * found / total)

	print("------------------- MakePlayLists done --------------------")

	print(f"Found {found}/{total} = {prse}%\n")
	print(f"{total - found} not found.\n")

def main():
	global connection
	print("\nSpotify megatool 3000")
	print("---------------------\n")

	parser = argparse.ArgumentParser(description='Do the jorma!')
	parser.add_argument('-t', '--test', action='store_true', help = "run tests from testfile")
	parser.add_argument('-ra', '--random', action='store_true', help = "make 100 random queries")
	parser.add_argument('-re', '--retry', action='store_true', help = "retry stuff that was previously not found")
	parser.add_argument('-m', '--me', action='store_true', help = "test connection")
	parser.add_argument('-c', '--clear_cache', action='store_true', help = "clear cache")
	parser.add_argument('-plf', '--playlist_files', action='store_true', help = "make all playlist files from peak files")
	parser.add_argument('-pl', '--playlists', action='store_true', help = "make all playlists from playlist files")

	args = parser.parse_args()

	global connection

	if args.test or args.random or args.retry or args.me or args.playlist_files or args.playlists:
		connection = Connection()

	if args.test:
		Test()
	elif args.random:
		Randomia()
	elif args.retry:
		Retry()
	elif args.me:
		Me()
	elif args.clear_cache:
		if os.path.isfile(CACHE_FILE):
			print("Removing " + CACHE_FILE)
			os.remove(CACHE_FILE)
		else:
			print(CACHE_FILE + " does not exist")
	elif args.playlist_files:
		MakePlaylistFiles()
	elif args.playlists:
		MakePlaylists()
	else:
		parser.print_help()
		
if __name__ == "__main__":
	main()
