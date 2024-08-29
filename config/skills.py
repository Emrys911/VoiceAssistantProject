import json
import os
import subprocess
import sys
import webbrowser

import pyttsx3
import requests
import speech_recognition as sr
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from vosk import Model, KaldiRecognizer

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)


def speaker(text):
    """Speak out the given text using the TTS engine."""
    engine.say(text)
    engine.runAndWait()
    print(text)


def alarm(text):
    """Trigger an alarm with the given text."""
    speaker(text)


def start_scheduler():
    """Start a background scheduler to run tasks at specific times."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: alarm("Подъем! Время вставать!"), 'cron', hour=6, minute=0)
    scheduler.start()


def fetch_weather():
    """Fetch the current weather information."""
    url = "https://api.openweathermap.org/data/2.5/weather?q=Minsk&appid=f7a51032f4c134dec171910751b38ff4&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        current_weather = weather_data['weather'][0]
        temperature = weather_data['main']['temp']
        return f"Current temperature: {temperature}°C, {current_weather['description']}"
    else:
        return "Failed to fetch weather data."


def fetch_news():
    """Fetch the latest news headlines."""
    response = requests.get('https://allnews.ng/')
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.select('h2 a')[:5]  # Adjust the selector based on the actual HTML structure
    news = [headline.text for headline in headlines]
    return news


def suggest_movie():
    """Fetch movie suggestions."""
    response = requests.get('https://www.allmovie.com/')
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('.movieTitle')[:5]  # Adjust the selector based on the actual HTML structure
    movies = [title.text for title in titles]
    return movies


def game():
    """Start a game."""
    subprocess.Popen('C:\Windows\System32\calc1.exe')



def browser():
    webbrowser.open('https://www.facebook.com/', new=2)


def play_music():
    """Open a music streaming service in the browser."""
    webbrowser.open("https://www.youtube.com/", new=3)


def offpc():
    """Shut down the computer."""
    os.system('shutdown')
    print("ноут выключен")


# Command to function mapping
data_set = {
    "weather": fetch_weather,
    "browser": lambda: webbrowser.open("https://www.google.com"),
    "game": game,
    "offpc": offpc,
    "offbot": sys.exit
}


def respond_to_command(command):
    """Respond to the given command."""
    func = data_set.get(command.lower())
    if func:
        result = func()
        if isinstance(result, str):
            print(result)
            alarm(result)
    else:
        print("Команда не распознана")
        alarm("Команда не распознана")


def online_recognition(recognizer: object, audio: object) -> object:
    """Use Google's online speech recognition to recognize the command."""
    try:
        command = recognizer.recognize_google(audio, language="ru-Eng")
        print(f"Recognized command (online): {command}")
        return command
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None


def offline_recognition(audio_data):
    """Use Vosk offline speech recognition to recognize the command."""
    model = Model("path/to/vosk-model-small-ru")  # Make sure to set the correct path to your Vosk model
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.AcceptWaveform(audio_data)
    result = json.loads(recognizer.Result())
    command = result.get('text', '')
    print(f"Recognized command (offline): {command}")
    return command


def listen_for_command(triggers):
    """Listen for commands and handle them using either online or offline recognition."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for a command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        command = online_recognition(recognizer, audio)

        if not command:
            # If online recognition failed, fall back to offline
            audio_data = audio.get_raw_data()
            command = offline_recognition(audio_data)

        if command:
            if any(trigger in command for trigger in triggers):
                command = command.replace('Siri', '').strip()
                respond_to_command(command)


def passive():
    pass


if __name__ == "__main__":
    triggers = ["Siri", "Bot Siri"]
    start_scheduler()  # Start the scheduler
    listen_for_command(triggers)
