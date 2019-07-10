import argparse
import collections
import requests
import sys
import os

SEARCH_BASE_URL = 'http://www.tekstowo.pl/wyszukaj.html'
SEARCH_FMT_STR = SEARCH_BASE_URL + '?search-title={title}&search-artist={artist}'

LYRICS_RESULT_FILE = "lyrics.txt"

Song = collections.namedtuple('Song', ['artist', 'title', 'url'])


class InvalidSongFormat(Exception):
    pass


class LyricsNotFound(Exception):
    pass


def fetch_page(url):
    with requests.Session() as session:
        response = session.get(url)
        return response.content


def search_song(song):
    destination_url = SEARCH_FMT_STR.format(title=song.title, artist=song.artist)
    return fetch_page(destination_url)


def fetch_lyrics(song):
    return fetch_page(song.url)


def extract_song(item):
    artist_title = item.split('title="')[1].split('">')[0]
    artist, title = map(str.strip, artist_title.split(' - ')[:2])
    url = 'http://www.tekstowo.pl{}.html' \
        .format(item.split('a href="')[1].split('.html')[0])
    return Song(artist, title, url)


def parse_search_results(results):
    results = results.decode('utf-8')
    if 'Znalezieni artyści' not in results:
        raise LyricsNotFound("Cannot find given artist")
    results = results.split('Znalezieni artyści:')[0]
    return [extract_song(item) for item in results.split('<div class="box-przeboje">')[1:]]


def parse_song_lyrics(html):
    return html.decode('utf-8') \
        .split('<h2>Tekst piosenki:</h2><br />')[1] \
        .split('<p>&nbsp;</p>')[0] \
        .replace('<br />', '\n') \
        .replace('\n\n', '\n') \
        .strip()


def retrieve_artist_and_title(song):
    if song.count('-') != 1:
        raise InvalidSongFormat('Passed song string must contain only one "-"')

    artist, title = map(str.strip, song.split('-'))
    artist = artist.replace(" ", "+")
    title = title.replace(" ", "+")
    if len(artist) == 0:
        raise InvalidSongFormat("Artist part cannot be empty")
    if len(title) == 0:
        raise InvalidSongFormat("Title part cannot be empty")

    return artist, title


def download_lyrics(song):
    search_results = search_song(song)
    try:
        song_page = parse_search_results(search_results)[0]
        return parse_song_lyrics(fetch_lyrics(song_page))
    except IndexError:
        raise LyricsNotFound("No lyrics found")


def download_list(songs):
    with open(os.path.join(os.getcwd(), LYRICS_RESULT_FILE), "w+") as f:
        for song in songs:
            print(song)
            try:
                _song = Song(*retrieve_artist_and_title(song),None)
                text = download_lyrics(_song)
                f.write("TITLE: {}\n".format(song))
                f.write(text)
                f.write("\n====================================")
                f.write("\n====================================\n")
            except Exception as e:
                print("Exception caught: {}".format(str(e)))

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("""Song to find lyrics for in format (with quotes),'"<ARTIST> - <TITLE>"'""")
        sys.exit(1)
        
    print("".join(sys.argv[1:]))
    try:
        print(download_lyrics(Song(*retrieve_artist_and_title(" ".join(sys.argv[1:])), None)))
    except (InvalidSongFormat, LyricsNotFound) as e:
        print(e)
        sys.exit(1)

