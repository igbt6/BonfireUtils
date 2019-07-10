import glob
import os
import re

SONGS_DIR = os.path.join(os.getcwd(), "Songs/OGNISKO_14_07_2018")
SONGS_NAME_LIST = "songs.txt"


print(SONGS_DIR)

def create_songs_list(songs_dir=SONGS_DIR):
    with open(SONGS_NAME_LIST, "w+") as f:
        os.chdir(songs_dir)
        for song in glob.glob("*.mp3"):
            song = song.replace(".mp3", "")
            #re.sub('Góraleczka', '', song)
            splitted = re.split(r"\s*-\s*", song)
            print(song)
            if len(splitted) > 1:
                f.write(splitted[0]+'-')
                f.write(splitted[1])
                f.write('\n')
            else:
                splitted = re.split(r"\s+", song)
                if len(splitted) > 1:
                    f.write(splitted[0]+'-')
                    f.write(splitted[1])
                    f.write('\n')
                else:
                    print("cannot split song: {}".format(song))


if __name__ == "__main__":
    create_songs_list()
