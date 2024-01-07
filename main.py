import base64
import openai

openai.api_key = "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"
import pyaudio
import speech_recognition as sr
import whisper

# Initialize OpenAI API with your API key

# Create a speech recognizer
recognizer = sr.Recognizer()

def transcribe_audio_whisperAPI(audio_data):
    try:
      # Convert the audio to FLAC format for Whisper API
        audio_data = audio_data.get_flac_data()
        
        # Encode the audio data as base64
        audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")
        
        # Transcribe the audio using Whisper API
        response = openai.Completion.create(
            model="Whisper",
            prompt=f"Transcribe the following audio: \n{audio_data_base64}\n",
            content_type="text/plain",
        )
        
        return response.choices[0].text
    
    except Exception as e:
        print("Error transcribing audio:", str(e))
        return ""
    
def transcribe_audio_whisper_local(audio_data):
    try:
        # Transcribe the audio using whisper-offline
        response = recognizer.recognize_whisper(audio_data)
        response = recognizer.recognize_whisper(audio_data)
        print("Offline whisper thinks you said " + response)
        return response
    
    
    except Exception as e:
        print("Error transcribing audio:", str(e))
        return ""
    

def main():
    # Initialize audio stream
    with sr.Microphone() as source:
        print("Listening...")
        while True:
            try:
                audio_data = recognizer.listen(source)
                transcription = transcribe_audio_whisper_local(audio_data)
                print("You said:", transcription)
            except sr.WaitTimeoutError:
                pass

if __name__ == "__main__":
    main()
