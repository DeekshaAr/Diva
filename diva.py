import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import time

# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)

engine = pyttsx3.init('sapi5')  # Microsoft Speech API
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use ZIRA voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

user_name = "Deeksha"

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Good Morning {user_name}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon {user_name}")
    else:
        speak(f"Good Evening {user_name}")
    speak("I am Diva. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    try:
        email_user = config['email_user']
        email_password = config['email_password']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Could not send email")
    
def getWeather(city):
    try:
        api_key = config['weather_api_key']
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "q=" + city + "&appid=" + api_key
        response = requests.get(complete_url)
        response.raise_for_status()
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(f"Temperature in {city} is {current_temperature - 273.15:.2f} degrees Celsius with {weather_description}.")
        else:
            speak("City Not Found")
    except requests.exceptions.RequestException as e:
        speak("Unable to retrieve weather information")
        print(e)

def getNews():
    try:
        api_key = config['news_api_key']
        main_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
        news = requests.get(main_url).json()
        articles = news["articles"]
        headlines = [article["title"] for article in articles[:5]]
        for headline in headlines:
            speak(headline)
    except requests.exceptions.RequestException as e:
        speak("Unable to retrieve news information")
        print(e)

def tellJoke():
    try:
        joke = requests.get('https://official-joke-api.appspot.com/random_joke').json()
        speak(joke['setup'])
        speak(joke['punchline'])
    except requests.exceptions.RequestException as e:
        speak("Unable to retrieve joke")
        print(e)
        
def setAlarm(time_str):
    alarm_time = datetime.datetime.strptime(time_str, '%H:%M').time()
    while True:
        now = datetime.datetime.now().time()
        if now >= alarm_time:
            speak("Time to wake up!")
            break
        time.sleep(1)

def setTimer(seconds):
    time.sleep(seconds)
    speak("Time is up!")

reminders = []

def addReminder(reminder_text, reminder_time):
    reminders.append((reminder_text, reminder_time))

def checkReminders():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if reminder[1] == now:
                speak(f"Reminder: {reminder[0]}")
                reminders.remove(reminder)
        time.sleep(60)

todo_list = []

def addToDoItem(item):
    todo_list.append(item)
    speak(f"Added {item} to your to-do list.")

def removeToDoItem(item):
    if item in todo_list:
        todo_list.remove(item)
        speak(f"Removed {item} from your to-do list.")
    else:
        speak(f"{item} not found in your to-do list.")

def listToDoItems():
    if todo_list:
        speak("Here are your to-do items:")
        for item in todo_list:
            speak(item)
    else:
        speak("Your to-do list is empty.")

def takeNote():
    speak("What would you like to note down?")
    note = takeCommand()
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    speak("Note taken.")



if __name__ == "__main__":
    speak("Hello Deeksha")
    wishMe()
    while True:
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'play movie' in query:
            movie_dir = "E:\\Movies"
            movie = os.listdir(movie_dir)
            if movie:
                speak("Playing the first movie in your Movies folder")
                os.startfile(os.path.join(movie_dir, movie[0]))
            else:
                speak("No movies found in your Movies folder")
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Ma'am, the time is {strTime}")
            
        elif 'open code' in query:
            codePath = "C:\\Users\\Deeksha\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
            os.startfile(codePath)
            
        elif 'email to Deeksha' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "aroradeeksha2001@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Could not send email")
                
        elif 'weather in' in query:
            city = query.split("in")[-1].strip()
            getWeather(city)

        elif 'news' in query:
            speak("Fetching the latest news headlines")
            getNews()
            
        elif 'tell me a joke' in query:
            tellJoke()
            
        elif 'open website' in query:
            speak("Please tell me the name of the website")
            website = takeCommand().lower().replace(" ", "")
            webbrowser.open(f"http://{website}.com")

        elif 'set alarm' in query:
            speak("For what time? Please say in HH:MM format.")
            alarm_time = takeCommand()
            setAlarm(alarm_time)
            
        elif 'set timer' in query:
            speak("For how many seconds?")
            timer_seconds = int(takeCommand())
            setTimer(timer_seconds)
            
        elif 'add reminder' in query:
            speak("What is the reminder?")
            reminder_text = takeCommand()
            speak("At what time? Please say in HH:MM format.")
            reminder_time = takeCommand()
            addReminder(reminder_text, reminder_time)
            
        elif 'add to do' in query:
            speak("What is the to-do item?")
            todo_item = takeCommand()
            addToDoItem(todo_item)
            
        elif 'remove to do' in query:
            speak("What is the to-do item to remove?")
            todo_item = takeCommand()
            removeToDoItem(todo_item)
            
        elif 'list to do' in query:
            listToDoItems()
            
        elif 'take note' in query:
            takeNote()