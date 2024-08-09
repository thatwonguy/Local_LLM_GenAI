from google.cloud import texttospeech
import io

class TTSService:
    def __init__(self):
        # Initialize the Google Cloud Text-to-Speech client
        self.client = texttospeech.TextToSpeechClient()

    def get_available_voices(self, language_code="en-US"):
        try:
            # Fetch the list of available voices
            response = self.client.list_voices(language_code=language_code)
            voices = []
            for voice in response.voices:
                voices.append({
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                })
            return voices
        except Exception as e:
            print(f"Error fetching available voices: {e}")
            return []

    def text_to_speech(self, text, voice_name="en-US-Wavenet-D", language_code="en-US"):
        try:
            input_text = texttospeech.SynthesisInput(text=text)

            # Configure the voice request, e.g., language and voice name
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )

            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )

            # Save the audio to a BytesIO object
            audio_buffer = io.BytesIO(response.audio_content)
            return audio_buffer

        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return None
