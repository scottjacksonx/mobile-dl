#mobile-dl

mobile-dl is kinda like [Instapaper](http://instapaper.com) for media other than text.

So you're out and about and you see on your iPhone (maybe on Twitter, maybe somewhere on the internet) that someone made a video you want to watch. You can't watch it right now, but you want to save it for later.

All you do is paste the URL of the video file (or audio file, or *anything* -- any valid URL is fine) into a specific note in Simplenote -- when you get home, your video is there on your computer for you to watch.

##Setup

First, here's what you need. Most people already have this stuff, but I just want to be clear. You need:

- a home computer with a Unix-y environment ([Cygwin](http://www.cygwin.com/) will do if you're on Windows)
- [Python](http://python.org) 2.6 or above
- [`curl`](http://en.wikipedia.org/wiki/Curl_(Unix))
- A [Simplenote](http://simplenoteapp.com/) account
- an iPhone with Simplenote installed (the iPhone is optional, but it's kinda the whole reason I built mobile-dl)

OK, so here's how to set mobile-dl up. There's two parts -- the "client" and the "server."

###The "Client" (Your iPhone)

1. Choose a *unique* word or phrase you want to identify your note. This should be something quick to type, as well as something that **isn't going to appear in any of your other notes**. I use "qqqq" as my unique phrase because [it's a great hack](http://www.kungfugrippe.com/post/453204090/q-trick).
2. In Simplenote, make a new note and type your unique phrase into the note. Let Simplenote sync.

###The "Server" (Your Home Computer)

1. Download the source onto your home computer.
2. Edit the user-specific values at the top of `mobile-dl.py` (your Simplenote credentials, your unique phrase, the directory you want your files to be downloaded to, and how often you want your home computer to check for new files).
3. Run `mobile-dl.py`. Your home computer is now watching your note for changes.

By default, mobile-dl runs silently -- it won't print anything. This is so you can run it in the background and not have it disturb you. If you want mobile-dl to print to the terminal when it does anything, run `mobile-dl.py` with the `-v` switch (`-verbose` and `-noisy` also work).

##Adding a File

On your iPhone, copy the URL of the file you want to download.

Open up Simplenote on your iPhone.

Open the note that contains your unique phrase.

Paste the URL into a blank line in note.

Now, if `mobile-dl.py` is running on your home computer, it will check your note and download any URLs you put in there. Once it's started downloading the files, it will clear the note, leaving only your unique phrase so you can use the note again.

##That's it. Well, almost.

There's one rule you have to follow:

##One URL per line.

URLs have to be separated by newlines. It can be as many newlines as you like, but you can't have two URLs on the same line.

Put simply, a single line can be `[nothing (so, just a newline) | a URL | your unique phrase]`.

##Credits

I used [samuel](http://github.com/samuel)'s [python-simplenote](http://github.com/samuel/python-simplenote) wrapper for the Simplenote API, though I had to tweak his code a little bit. Doing a `diff` on his `simplenote.py` and my `simplenote.py` will show you the changes.