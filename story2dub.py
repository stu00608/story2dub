import argparse
import csv
import os
from pydub import AudioSegment
from gctts import tts

# Voice mapping
voice_mapping = {
    'M': 'ja-JP-Neural2-C',
    'F': 'ja-JP-Neural2-B'
}


def create_srt(csv_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as srt_file:
        current_time = 0
        for index, row in enumerate(csv_data, start=1):
            start_time = format_time(current_time)
            end_time = format_time(current_time + float(row['duration']))

            srt_file.write(f"{index}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{row['Content']}\n\n")

            current_time += float(row['duration']) + \
                float(row['EndWaitTime'])


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_r = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_r:02d},{milliseconds:03d}"


def main(story_path, output_path, speed=1.0, overwrite=False):
    format = output_path.split('.')[1]
    # Check if the format is valid audio format for pydub
    if format not in ['mp3', 'wav', 'flac', 'ogg']:
        raise ValueError("Invalid audio format")

    basename = os.path.basename(story_path).split('.')[0]
    os.makedirs(basename, exist_ok=True)
    work_dir = os.path.abspath(basename)

    # if basename folder is not empty, raise an error
    if os.listdir(work_dir) and not overwrite:
        csvfile = os.path.join(work_dir, 'updated_story.csv')
        # Read the csvfile to get the rows
        with open(csvfile, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    else:
        work_dir = basename

        # Read the story CSV file
        with open(story_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        # Generate audio files and update CSV data
        for index, row in enumerate(rows):
            voice_name = voice_mapping[row['Gender']]
            audio_filename = f"{index}-{row['Content'][:10]}.mp3"
            audio_path = os.path.join(work_dir, audio_filename)

            tts(row['Content'], 'ja-JP', voice_name, audio_path, speed=speed)

            # Get audio duration
            audio = AudioSegment.from_mp3(audio_path)
            duration = len(audio) / 1000.0  # Convert to seconds

            # Update row with new information
            row['audio_path'] = audio_path
            row['duration'] = str(duration)

        # Save updated CSV
        updated_csv_path = os.path.join(work_dir, 'updated_story.csv')
        with open(updated_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    # Update the EndWaiteTime based on speed
    for row in rows:
        row['EndWaitTime'] = str(float(row['EndWaitTime']) / speed)

    # Combine audio files
    combined_audio = AudioSegment.empty()
    for row in rows:
        audio = AudioSegment.from_mp3(row['audio_path'])
        combined_audio += audio
        # Update rows
        combined_audio += AudioSegment.silent(
            duration=float(row['EndWaitTime']) * 1000)

    # Export combined audio
    combined_audio.export(output_path, format=format)

    # Create SRT subtitle file
    srt_path = os.path.splitext(output_path)[0] + ".srt"
    create_srt(rows, srt_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate audio and subtitles from a story CSV file")
    parser.add_argument("--story_path", required=True,
                        help="Path to the input story CSV file")
    parser.add_argument("--output_path", required=True,
                        help="Path to save the output audio file")
    parser.add_argument("--overwrite", action='store_true',
                        help="Overwrite the existing files in the output folder")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="The speed of the audio file")
    args = parser.parse_args()

    main(args.story_path, args.output_path, args.speed, args.overwrite)
