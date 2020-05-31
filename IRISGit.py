import os
user = os.getlogin()

import json
import datetime

#change this section if you don't use firefox
import webbrowser
firefoxPath = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefoxPath))
webbrowser = webbrowser.get('firefox')

#for windows 10, you will need these packages installed in your machine for IRIS to run correctly
os.system('pip install python requests wolframalpha pywin32 pyaudio wikipedia SpeechRecognition pyttsx3')

import wolframalpha
client = wolframalpha.Client('WolframAlpha API Key goes here')

#dependants
import requests
import sys
import pyaudio
import wikipedia #pip install wikipedia
import speech_recognition as sr #pip install speechRecognition
import pyttsx3 #pip install pyttsx3

#lists
affirm = ['yes', 'yeah', 'yea', 'hell yeah', 'ja', 'yup', 'yep', 'absolutely', 'definitely', 'without a doubt', 'beyond the shadow of a doubt', 'for sure']
negate = ['no', 'nei', 'nope', 'nah', 'not this time', 'not today', 'hell no']
revert = ['go back', 'forget it', 'nevermind', 'revert', 'tilbakke', 'stop', 'stop it']
quit = ['thanks', 'thanks bud', 'thanks buddy', 'thanks iris', 'bye', 'bye iris', 'bye bud', 'bye buddy', 'goodbye iris', 'goodbye bud', 'goodbye', 'close', 'quit', 'close program', 'iris go away', 'go away', 'thank you', 'iris close', 'iris quit']
iris = ['open iris', 'open your code', 'show iris', 'show me your code', 'show me your guts', 'what do you look like', 'show me yourself', 'show me iris', 'show me your insides']
projectIris = ['open project iris', 'open project iris for me', 'show me project iris', 'show project iris', 'pull up your project', 'pull up project iris', 'project iris']
code = ['open code', 'show me code', 'show me my coding folder', 'show me my code', 'open my code', 'open my coding folder', 'code', 'show me my code folder', 'open my code folder', 'pull up my code folder', 'pull up code', 'pull up my coding folder', 'pull up my code']

#variables
API_KEY = 'Google Custom Search Engine API Key goes here'
SEARCH_ENGINE_ID = 'Google Custom Search Engine ID goes here'
rootUrl = 'https://customsearch.googleapis.com/customsearch/v1?key={}&cx={}&q={}'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("What can I do for you?")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

        if 'please' in query:
            query = query.replace('please', '')

    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query

def search(x):
    try:
        speak('Searching Wolfram Alpha')
        res = client.query(x)
        results = next(res.results).text

        if x == '':
            speak('What would you like to search for?')
            x = takeCommand().lower()

        speak('According to Wolfram Alpha')
        print(results)

    except:
        try:
            speak('Wolfram Alpha has proven unsuccessful, searching other databases.')
            wikiResult = wikipedia.summary(x, sentences=2)

            url = rootUrl.format(API_KEY, SEARCH_ENGINE_ID, query)
            jsonData = requests.get(url)
            data = jsonData.json()
            searchItems = data.get('items')

            firstResult = searchItems[0]
            secondResult = searchItems[1]
            thirdResult = searchItems[2]

            googleResult = "\n" + firstResult['title'] + "\n" + secondResult['title'] + "\n" + thirdResult['title']

            if not wikiResult:
                speak("I didn't find anything on Wikipedia. Here's what was on Google.")
                print('Google:\n' + googleResult)
                speak('Would you like any more information on any of these?')
                response = takeCommand().lower()

                if response in affirm:
                    speak('Which one?')
                    response = takeCommand().lower()

                elif 'first' in response:
                    print(firstResult['snippet'])
                    speak(firstResult['snippet'])

                elif 'II' in response:
                    print(secondResult['snippet'])
                    speak(secondResult['snippet'])

                elif 'third' in response:
                    print(thirdResult['snippet'])
                    speak(thirdResult['snippet'])

                elif 'open' in response:
                    x.replace(' ', '+')
                    webbrowser.open('https://www.google.com/search?q=' + x)

                else:
                    speak('Very well.')
                    __name__ = "__main__"

            if not googleResult:
                speak("I didn't find anything on Google. Here's what was on Wikipedia.")
                print('Wikipedia:\n' + wikiResult)
                speak("I can expand on these if you'd like.")
                response = takeCommand().lower()

                if response in affirm:
                    speak("Your native tongue sir? Or English?")
                    response = takeCommand().lower()
                    x = x.replace(' ', '_')

                    if 'Norwegian' in response:
                        webbrowser.open('https://no.wikipedia.org/wiki/' + x)
                        __name__ = "__main__"

                    if 'English' in response:
                        webbrowser.open('https://en.wikipedia.org/wiki/' + x)
                        __name__ = "__main__"

                else:
                    speak('Very well.')
                    __name__ = "__main__"

            speak("Here's what I found on Google and Wikipedia.")
            print('Google:\n' + googleResult + '\n\nWikipedia:\n' + wikiResult)

            speak('Would you like any more information on any of these?')
            response = takeCommand().lower()

            if response in affirm:
                speak('Which one sir?')
                response = takeCommand().lower()

                if 'google' in response:

                    if 'first' in response:
                        print(firstResult['snippet'])
                        speak(firstResult['snippet'])

                    elif 'II' in response:
                        print(secondResult['snippet'])
                        speak(secondResult['snippet'])

                    elif 'third' in response:
                        print(thirdResult['snippet'])
                        speak(thirdResult['snippet'])

                    elif 'open' in response:
                        x.replace(' ', '+')
                        webbrowser.open('https://www.google.com/search?q=' + x)

                if 'wiki' in response:
                    x.replace(' ', '_')
                    webbrowser.open('https://en.wikipedia.org/wiki/' + x)

            if response in negate:
                speak('Very well.')
                __name__ = "__main__"

        except:
            webbrowser.open(x)
            speak("I'm sorry sir, I can't find anything on that topic.")

if __name__ == "__main__":
    greet()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'search' in query:
            query = query.replace('search', '')

            if 'for' in query:
                query.replace('for', '')

            search(query)

        elif 'youtube' in query:
            webbrowser.open("youtube.com")
            __name__ = "__main__"

        elif 'google' in query:
            webbrowser.open("google.com")
            __name__ = "__main__"

        elif 'github' in query:
            webbrowser.open("github.com")
            __name__ = "__main__"

        elif 'wikipedia' in query:
            webbrowser.open('wikipedia.com')
            __name__ = "__main__"

        elif 'gmail' in query:
            webbrowser.open('gmail.com')
            __name__ = "__main__"

        #local commands
        elif 'guild wars' in query:
            codePath = "C:\\Guild Wars 2\\Gw2-64.exe"
            os.startfile(codePath)
            speak('Enjoy')
            break

        elif 'discord' in query:
            codePath = "C:\\Users\\" + user + "\\AppData\\Local\\Discord\\app-0.0.306\\Discord.exe"
            os.startfile(codePath)
            break

        elif 'i love you' in query:
            speak('Aw thanks, if I was capable of producing serotonin at the sight of a human, I am sure it would be you.')
            __name__ = "__main__"

        elif 'how are you' in query:
            speak("I'm well. Thank you for asking. How are you?")
            __name__ = "__main__"

        elif "what's up" in query:
            speak('That would be the atmosphere.')
            __name__ = "__main__"

        elif "how goes it" in query:
            speak("It goes well, thank you.")
            __name__ = "__main__"

        elif query == 'is the world going to end':
            speak('Yes, eventually.')
            __name__ = "__main__"

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            __name__ = "__main__"

        elif query in code:
            try:
                codePath = "C:\\Users\\" + user + "\\OneDrive\\Documents\\code"
                os.startfile(codePath)
                __name__ = "__main__"

            except:
                os.mkdir(codePath)
                os.startfile(codePath)
                __name__ = "__main__"

        elif query in iris:
            cwd = os.getcwd()
            os.startfile(cwd + "\\IRIS.py")

        elif 'make me laugh' in query:
            speak("No.")
            __name__ = "__main__"

        elif 'tell me a joke' in query:
            speak("Have you heard of the AI that can take off all of your clothes and give you a whole new outfit? I've seen it change people.")
            __name__ = "__main__"

        elif query in quit:
            speak("Farewell")
            break
