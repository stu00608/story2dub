# story2dub

story2dub is a Python tool that generates audio files and subtitles from a CSV file containing story content. It uses Google Cloud Text-to-Speech to create voice recordings and combines them into a single audio file with customizable intervals between lines. The tool also generates an SRT subtitle file for the created audio.

## Features

- Converts text to speech using Google Cloud TTS
- Supports multiple speakers (male and female voices)
- Allows customization of pause duration between lines
- Generates SRT subtitles synchronized with the audio
- Supports various audio output formats (MP3, WAV, FLAC, OGG)
- Allows adjustment of speech speed

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- pip (Python package installer)
- Google Cloud account with Text-to-Speech API enabled
- Google Cloud credentials set up on your machine

## Installation

1. Clone this repository or download the script:

   ```
   git clone https://github.com/yourusername/story2dub.git
   cd story2dub
   ```

2. Install the required Python packages:

   ```
   pip install google-cloud-texttospeech pydub
   ```

3. Set up your Google Cloud credentials. Follow the [Google Cloud documentation](https://cloud.google.com/docs/authentication/getting-started) for instructions.

## Usage

To use story2dub, follow these steps:

1. Prepare your story CSV file with the following columns:

   - Content: The text to synthesize
   - Language: The language code (e.g., 'JP')
   - Gender: The gender of the TTS voice actor ('M' or 'F')
   - EndWaitTime: How long to pause after each line (in seconds)
   - Odor: The odor label for the current subtitle (optional)

2. Run the script with the following command:

   ```
   python story2dub.py --story_path your_story.csv --output_path output_audio.mp3 [--speed 1.0] [--overwrite]
   ```

   - `--story_path`: Path to your input CSV file (required)
   - `--output_path`: Path for the output audio file (required)
   - `--speed`: Speech speed factor (optional, default is 1.0)
   - `--overwrite`: Flag to overwrite existing files in the output folder (optional)

3. The script will generate:
   - An audio file at the specified output path
   - An SRT subtitle file with the same name as the audio file
   - A working directory named after your input CSV file, containing individual audio clips and an updated CSV file

## Example

Assuming you have a CSV file named `my_story.csv`:

```
python story2dub.py --story_path my_story.csv --output_path my_story_audio.mp3 --speed 1.2
```

This command will:

- Read `my_story.csv`
- Generate an audio file named `my_story_audio.mp3`
- Create an SRT file named `my_story_audio.srt`
- Set the speech speed to 1.2x normal speed

## Notes

- The script creates a working directory named after your input CSV file. This directory contains individual audio clips for each line and an updated CSV file with additional information.
- If you run the script multiple times with the same input file, use the `--overwrite` flag to replace existing files in the working directory.
- Adjust the `--speed` parameter to change the pace of the speech and the duration of pauses between lines. Values greater than 1.0 will speed up the audio, while values less than 1.0 will slow it down.

## Troubleshooting

- If you encounter errors related to Google Cloud authentication, ensure your credentials are correctly set up and the Text-to-Speech API is enabled for your project.
- For issues with audio processing, make sure you have the necessary audio codecs installed on your system for pydub to work correctly.
