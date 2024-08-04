# tts_service.py

import pyttsx3
import io

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Optional: Adjust voice, rate, and volume
        # self.engine.setProperty('rate', 150)  # Speed of speech
        # self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    def text_to_speech(self, text, language="en"):
        try:
            # Convert text to speech and save as a file
            self.engine.save_to_file(text, 'temp_speech.mp3')
            self.engine.runAndWait()
            
            # Read the file into a buffer
            with open('temp_speech.mp3', 'rb') as f:
                audio_bytes = f.read()
            
            # Create a BytesIO object
            buffer = io.BytesIO(audio_bytes)
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return None