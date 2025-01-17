import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine=pyttsx3.init()

def input_command():
    command=""
    try:
        talk("Hi i am jarvis how can i help you?")
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source,duration=3)  # Optional: handles background noise
            print("Listening...")
            voice = listener.listen(source,timeout=5, phrase_time_limit=10)  # Capture audio
            command = listener.recognize_google(voice).lower()  # Transcribe audio
            if 'jarvis' in command:
                command=command.replace('jarvis','').strip()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        return ""

    except Exception as e:
        print(f"An unexpected error occurred: {e}")#printing output
    return command

def talk(command):
    engine.say(command)
    engine.runAndWait()

def run_command(command):
    if 'play' in command:
        song=command.replace('play','').strip()
        pywhatkit.playonyt(song)
    elif 'what is' in command:
        pywhatkit.search(command)
    elif 'time' in command:
        time=datetime.datetime.now().strftime('%I:%M %p')
        talk('current time is '+time)
    elif 'who is' in command:
        person=command.replace('who is','').strip()
        try:
            info=wikipedia.summary(person,sentences=4)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("No person found in Wikipedia")
        except Exception as e:
            talk("Sorry, I couldn't fetch the information right now.")
            print(f"Error: {e}")
    elif 'joke' in command:
        joke=pyjokes.get_joke()
        talk(joke)
        print(joke)
    elif 'bye' in command:
        talk('see you bye')
        return False
        
    else:
        talk('I did not understand what you are saying... ')
    return True

def wake_up_jarvis():
    while True:
        try:
            with sr.Microphone() as source:
                print("Say jarvis to wake me")
                listener.adjust_for_ambient_noise(source,duration=2)
                voice=listener.listen(source,timeout=None, phrase_time_limit=5)
                command=listener.recognize_google(voice).lower()
                return command
        except sr.UnknownValueError:
            print("Say jarvis to wake me")
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            break
    

while True:
    wake_up_jarvis()
    keep_running=True
    while keep_running:
        user_command=input_command()
        if user_command:
            keep_running=run_command(user_command)
    