import base64
import openai
import pyaudio
import speech_recognition as sr
import whisper
from readconfig import config
openai.api_key = config["openai_api_key"]

# Create a speech recognizer
recognizer = sr.Recognizer()

# Increase threshold to decrease sensitivity, default is 300
# TODO: We could consider some form of fourier transformation to calculate the surrounding decibal and auto tune this
# TODO: Alternatively, we could train the model to only respond to my voice
recognizer.energy_threshold = config["energy_threshold"] 

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
    """
    Transcribes the audio using the local whisper API, this works offline and does not
    need an openAI_API_KEY. Which means, it's completely free!

    Args:
    audio_data: The audio data to be transcribed.

    Returns:
    The transcribed text if successful, None otherwise.
    """
    try:
        print("Transcribing audio...")
        # Transcribe the audio using whisper-offline
        response = recognizer.recognize_whisper(audio_data)
        print("Debug transcription: " + response)
        
        # TODO: Add a timeout, when engaged in back and forth conversations within
        # a certain timeframe, no need to start with prefix
        if any(prefix in response for prefix in config["speech_prefix"]):
            return response
        return None
    
    
    except Exception as e:
        print("Error transcribing audio:", str(e))
        return ""
    
def generate_response_openai(transcription):
    try:
        # Generate response using OpenAI GPT-3.5 model with role description
        prompt = f"{config['role_desc']}\n{transcription}"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 2048,
        )   
        return response.choices[0].text
    except Exception as e:
        print("Error generating response:", str(e))
        return ""

def main():
    # Initialize audio stream
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while True:
            try:
                audio_data = recognizer.listen(source)
                transcription = transcribe_audio_whisper_local(audio_data)
                # transcription = transcribe_audio_whisperAPI(audio_data)
                if transcription is not None:
                    print("You said:", transcription)
                    response = generate_response_openai(transcription)
                    print("Assistant replied: " + response)
            except sr.WaitTimeoutError:
                print("...")
                pass
            
if __name__ == "__main__":
    main()
