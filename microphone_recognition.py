#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))

# recognize speech using whisper
# try:
#     print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
# except sr.UnknownValueError:
#     print("Whisper could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Whisper")

# # recognize speech using Whisper API
OPENAI_API_KEY = "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"
try:
    print(f"Whisper API thinks you said {r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}")
except sr.RequestError as e:
    print("Could not request results from Whisper API")