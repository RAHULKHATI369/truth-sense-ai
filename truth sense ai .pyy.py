import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow messages
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN notifications

import cv2
import numpy as np
import pyttsx3
import speech_recognition as sr
from tensorflow import keras
import random
import time

class TruthSenseAI:
    def __init__(self):
        # Voice setup
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        # User database
        self.known_users = {"rahul khati": {"role": "boss", "voice_id": None}}
        self.current_user = None
        
        # Mock AI models (replace with real trained models)
        self.emotion_model = self._create_mock_emotion_model()
        self.truth_model = self._create_mock_truth_model()
        
        # Fingerprint simulation
        self.last_scan = None

    def _create_mock_emotion_model(self):
        """Simulate emotion detection model"""
        model = keras.Sequential([keras.layers.Dense(1)])
        model.compile(loss='mse')
        return model

    def _create_mock_truth_model(self):
        """Simulate truth detection model"""
        model = keras.Sequential([keras.layers.Dense(1)])
        model.compile(loss='mse')
        return model

    def speak(self, text):
        """Text-to-speech output"""
        print(f"System: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Speech recognition with timeout"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"User: {text}")
                return text
            except:
                return ""

    def simulate_fingerprint_scan(self):
        """Generate mock fingerprint data"""
        self.speak("Please place your finger on the sensor")
        time.sleep(2)  # Simulate scanning time
        self.last_scan = np.random.rand(256, 256)  # Fake fingerprint image
        return self.last_scan

    def detect_emotion(self, fingerprint_img):
        """Mock emotion detection"""
        emotions = ["Happy", "Stressed", "Angry", "Calm", "Sad"]
        return random.choice(emotions)

    def detect_truth(self, statement):
        """Mock truth analysis"""
        return "Truth" if len(statement.split()) > 5 else "Lie"  # Simple heuristic

    def identify_user(self):
        """Voice-based user recognition"""
        self.speak("Hello! Who are you?")
        response = self.listen()
        
        for name, data in self.known_users.items():
            if name in response:
                self.current_user = name
                self.speak(f"Hello {data['role']} {name.split()[0]}, what should I do for you?")
                return True
        self.speak("User not recognized")
        return False

    def run(self):
        """Main interaction loop"""
        if not self.identify_user():
            return
            
        while True:
            command = self.listen()
            
            if not command:
                continue
                
            if "check feelings" in command:
                if self.last_scan is None:
                    self.simulate_fingerprint_scan()
                emotion = self.detect_emotion(self.last_scan)
                self.speak(f"Current emotional state: {emotion}")
                
            elif "check truth" in command:
                self.speak("Please state your claim")
                statement = self.listen()
                if statement:
                    truth_status = self.detect_truth(statement)
                    self.speak(f"Veracity analysis: {truth_status}")
                    
            elif "thank you" in command:
                self.speak("You're welcome! Session ended.")
                break
                
            self.speak("What else should I do?")

if __name__ == "__main__":
    try:
        ai = TruthSenseAI()
        ai.run()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("System shutdown")