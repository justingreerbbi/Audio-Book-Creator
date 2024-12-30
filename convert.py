from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover
import os

def merge_mp3_files(mp3_files, output_file, cover_image, metadata):
    # Create an empty AudioSegment
    audiobook = AudioSegment.empty()

    # Merge all MP3 files
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(mp3_file)
        audiobook += audio

    # Export the merged audio as M4B
    audiobook.export(output_file, format="mp4", codec="aac")

    # Add metadata and cover image
    audio = MP4(output_file)

    # Add metadata
    audio["\xa9nam"] = metadata['title']
    audio["\xa9ART"] = metadata['author']
    audio["\xa9alb"] = metadata['album']
    audio["\xa9gen"] = metadata['genre']
    audio["\xa9day"] = metadata['year']
    audio["trkn"] = [(int(metadata['track']), 0)]

    # Add cover image
    with open(cover_image, 'rb') as img:
        audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)]

    # Save the changes
    audio.save()

if __name__ == "__main__":
    mp3_files = ["chapter1.mp3", "chapter2.mp3"]
    output_file = "audiobook.m4b"
    cover_image = "cover.jpg"
    metadata = {
        'title': 'My Audio Book',
        'author': 'Author Name',
        'album': 'Audio Book Album',
        'genre': 'Audiobook',
        'year': '2023',
        'track': '1'
    }

    merge_mp3_files(mp3_files, output_file, cover_image, metadata)
