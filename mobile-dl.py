"""
mobile-dl.py
Author: Scott Jackson (http://scottjackson.org)

Exit codes:
1 = Error logging in to Simplenote.
2 = Error getting URLs from Simplenote.
3 = Error updating the note.
4 = No note found containing your unique phrase.
5 = More than 1 note found containing your unique phrase.
"""


import simplenote
from subprocess import call
import time
import sys
from datetime import tzinfo, timedelta, datetime

# Put *your* values here!
email = "your_name_here"	# Simplenote email.
password = "your_password_here"	# Simplenote password.
uniquePhrase = "your_phrase_here"
directoryToDownloadTo = "/Your/Directory/Here" # This has to be a full path, not "~/Downloads" or whatever. Don't ask why.
interval = 1800	# Number of seconds between checks (1800 = half an hour)


verbose = 0

if len(sys.argv) == 2:
	if sys.argv[1] == "-v" or sys.argv[1] == "-verbose" or sys.argv[1] == "-noisy":
		verbose = 1

if verbose:
	print str(datetime.now()) + " Logging into Simplenote"
try:
	simplenoteApi = simplenote.Simplenote(email, password)
except simplenote.SimplenoteAuthError:
	print str(datetime.now()) + " Error logging into Simplenote. Incorrect credentials or network issues?"
	sys.exit(1)

while True:
	if verbose:
		print str(datetime.now()) + " Checking Simplenote for new URLs"
	try:
		searchResults = simplenoteApi.search(uniquePhrase)['results']
	except simplenote.SimplenoteError:
		print str(datetime.now()) + " Error getting URLs from Simplenote"
		sys.exit(2)

	if len(searchResults) == 1:
		note = searchResults[0]
		noteString = str(note['content'])
		noteKey = note['key']
		lines = str.split(noteString, "\n")
		updatedLines = []
		urlsInNote = False

		for line in lines:
			if line != uniquePhrase and line != "":
				if verbose:
					print str(datetime.now()) + " Downloading " + line
				urlsInNote = True
				call (["bash", "mobile-dl.sh", directoryToDownloadTo, line, "&"])
			
		if urlsInNote:
			if verbose:
				print str(datetime.now()) + " Updating the note"
			try:
				simplenoteApi.update_note(noteKey, uniquePhrase + "\n")
			except simplenote.SimplenoteError:
				print str(datetime.now()) + " Error updating the note"
				sys.exit(3)

		if verbose:
			print str(datetime.now()) + " Sleeping for " + str(interval) + " seconds"
		time.sleep(interval)

	elif len(searchResults) == 0:
		print str(datetime.now()) + " No note containing '" + uniquePhrase + "' was found."
		sys.exit(4)

	else:
		print str(datetime.now()) + " More than one note found containing '" + uniquePhrase + "'. This whole shindig kinda hinges on you only having one note with your unique phrase in it."
		sys.exit(5)
	
	


