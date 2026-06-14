import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        return ""

def wish():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Pradeep")
    elif hour < 18:
        speak("Good afternoon Pradeep")
    else:
        speak("Good evening Pradeep")

wish()
speak("I am your personal AI assistant. How can I help you?")

while True:
    query = listen()

    if "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("Current time is " + time)

    elif "date" in query:
        date = datetime.date.today()
        speak("Today's date is " + str(date))

    elif "wikipedia" in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    elif "your name" in query:
        speak("My name is your personal AI assistant")

    elif "exit" in query or "stop" in query:
        speak("Goodbye Pradeep")
        break

    elif query != "":
        speak("Sorry, I did not understand")
