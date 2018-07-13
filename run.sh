sudo apt-get install ffmpeg

source venv/bin/activate

# install all the stuff
pip install -r requirements.txt

# download the songs from youtube
#youtube-dl -o "Songs/%(playlist)s/%(artist)s - %(track)s.%(ext)s" --download-archive downloaded.txt --no-post-overwrites -i -x --audio-format mp3 --audio-quality 0 --yes-playlist https://www.youtube.com/playlist?list=PLbba1CoobcgrOa15pbT0Psj3P4y27bNUf
youtube-dl -o "Songs/%(playlist)s/%(title)s.%(ext)s" --download-archive downloaded.txt --no-post-overwrites -i -x --audio-format mp3 --audio-quality 0 --yes-playlist https://www.youtube.com/playlist?list=PLbba1CoobcgrOa15pbT0Psj3P4y27bNUf

