import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

recogniser=sr.Recognizer()
newsapi="d142ff8fe1da4e398ed9cab3740b6dbf"

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get("https://newsapi.org/v2/everything?q=keyword&apiKey=d142ff8fe1da4e398ed9cab3740b6dbf")
        data=r.json()
        if data.get("status") == "ok":
           articles = data.get("articles", [])

        if not articles:
            print("No news articles found.")
            speak("No news articles found.")
        else:
            speak("Here are the top news headlines")
            for i, article in enumerate(articles[:5], start=1):  # Limit to 5 articles
                title = article.get('title')
                desc = article.get('description')
                url = article.get('url')
                print(f"\n📰 News {i}")
                print(f"Title: {article.get('title')}")
                print(f"Description: {article.get('description')}")
                print(f"URL: {article.get('url')}")
                speak(f"News {i}. {title}")
    else:
        #let openai handle the request
        pass

if __name__=="__main__":
    speak("Initialising jarvis")
    while True:
        r = sr.Recognizer()

        print("recognising...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=4)
            word=r.recognize_google(audio)
            if (word.lower()=="jarvis"):
                speak("Tell me, how can I help you?")

                with sr.Microphone() as source:
                    print("jarvis active...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error;{0}".format(e))
