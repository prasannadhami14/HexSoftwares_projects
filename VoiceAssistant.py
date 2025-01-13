import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
listener = sr.Recognizer()
engine=pyttsx3.init()

def input_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Optional: handles background noise
            print("Listening...")
            voice = listener.listen(source)  # Capture audio
            command = listener.recognize_google(voice)  # Transcribe audio
            command=command.lower()
            if 'jarvis' in command:
                command=command.replace('jarvis','')
    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging error output
    return command

def talk(command):
    engine.say(command)
    engine.runAndWait()

def run_jarvis():
    command=input_command()
    if 'play' in command:
        song=command.replace('song','')
        pywhatkit.playonyt(song)
    elif 'what is' in command:
        pywhatkit.search(command)
    elif 'time' in command:
        time=datetime.datetime.now().strftime('%I:%M %p')
        talk('current time is '+time)
    elif 'who is' in command:
        person=command.replace('who is','')
        try:
            info=wikipedia.summary(person,4)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("No person found in Wikipedia")
        except Exception as e:
            talk("Sorry, I couldn't fetch the information right now.")
            print(f"Error: {e}")

run_jarvis()