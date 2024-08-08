import pyttsx3
import io
import os

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 130)  # Default speech rate

    def get_voices(self):
        return [{"id": voice.id, "name": voice.name} for voice in self.voices]

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def text_to_speech(self, text, voice_id=None):
        try:
            if voice_id:
                self.engine.setProperty('voice', voice_id)

            temp_file = 'temp_speech.mp3'
            self.engine.save_to_file(text, temp_file)
            self.engine.runAndWait()

            with open(temp_file, 'rb') as f:
                audio_bytes = f.read()

            buffer = io.BytesIO(audio_bytes)
            buffer.seek(0)

            os.remove(temp_file)

            return buffer
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return None
