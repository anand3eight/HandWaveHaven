from gtts import gTTS
import os
# # Initialize the text-to-speech engine
# engine = pyttsx3.init()


# # Text to be converted to speech
text = "Hello, this is a simple text-to-speech conversion in Python."

# # Convert text to speech and play it
# engine.say(text)

# # Wait for the speech to finish
# engine.runAndWait()

def speak(text) :
    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    speech_file = 'speech.mp3'
    speech.save(speech_file)

    # Play the audio file
    os.system('afplay ' + speech_file)

if __name__ == '__main__' :
    speak(text)