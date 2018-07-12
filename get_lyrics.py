import os


from retrieve_songs_name import create_songs_list
from retrieve_songs_name import SONGS_NAME_LIST
from tekstowo import download_list

SONGS_LIST_FILE = os.path.join(os.getcwd(), SONGS_NAME_LIST)
print(SONGS_LIST_FILE)


def list_from_songs_file(dir_path=SONGS_LIST_FILE):
    with open(SONGS_LIST_FILE, 'r') as f:
        _list = [line.rstrip('\n') for line in f]
        return _list


if __name__ == "__main__":
    create_songs_list()
    songs = list_from_songs_file()
    print(songs)
    download_list(songs) 
