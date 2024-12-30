import os, sys
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def convert_mp3_to_m4b(directory):
    # Collect all MP3 files in the directory
    mp3_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')])
    
    if not mp3_files:
        print("No MP3 files found in the directory.")
        return

    # Create an empty list to hold segments
    segments = []

    # Load each MP3 file and add to segments
    for mp3_file in mp3_files:
        audio = AudioSegment.from_file(mp3_file, format="mp3")
        segments.append(audio)
        print(f"Loaded {os.path.basename(mp3_file)}")

    # Concatenate all segments
    combined_audio = sum(segments)

    # Export combined audio to M4B
    output_file = os.path.join(directory, "audiobook.m4b")
    combined_audio.export(output_file, format="mp4")
    print(f"Combined MP3s into audiobook file: {output_file}")

    # Add chapter information using Mutagen
    audio = MP4(output_file)
    audio.save()
    sys.exit(0)
    
    chapter_list = []
    cumulative_duration = 0
    for i, mp3_file in enumerate(mp3_files):
        mp3 = MP3(mp3_file)
        duration = mp3.info.length * 1000  # Convert to milliseconds for consistency
        start_time = cumulative_duration
        end_time = start_time + duration
        chapter_name = f"Chapter {i + 1}"

        chapter_list.append((start_time, end_time, chapter_name))

        #audio.add_tags('moov.udta.chpl.Chapter', {
        #    'start': start_time,
        #    'title': chapter_name
        #})

        cumulative_duration += duration

    audio['chpl'] = chapter_list
    #audio['moov']['udta']['chpl'] = chapter_list  # 'chpl' is the key for chapters in Mutagen

    sys.exit(0)

    # Update the file with new chapter metadata
    audio.save()

    print("Chapters added to the audiobook.")

if __name__ == "__main__":
    # Change this to the directory where your MP3 files are located
    directory = "."  # Current directory
    convert_mp3_to_m4b(directory)