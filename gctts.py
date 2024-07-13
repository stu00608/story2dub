from google.cloud import texttospeech


def tts(text, lang, voice_name, output_path, speed=1.0, audio_format='MP3'):
    """
    Synthesize speech from the input string of text.

    Args:
    text (str): The text to synthesize.
    lang (str): The language code (e.g., 'ja-JP').
    voice_name (str): The name of the voice (e.g., 'ja-JP-Wavenet-C').
    output_path (str): The path to save the output audio file.
    audio_format (str): The audio format (default is 'MP3').

    Returns:
    None
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code=lang,
        ssml_gender=texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED
    )

    # Select the type of audio file you want returned
    audio_encoding = getattr(texttospeech.AudioEncoding, audio_format)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding, speaking_rate=speed)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_path}"')


if __name__ == "__main__":
    # Example usage
    tts(
        text="あっ！なんかスパイシーな香りがしてきた！",
        lang="ja-JP",
        voice_name="ja-JP-Neural2-B",
        output_path="output.mp3"
    )
