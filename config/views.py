from django.http import JsonResponse
from django.shortcuts import render
import pyttsx3
import os
import webbrowser
import sys
import requests
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)


def speaker(text):
    """Speak out the given text using the TTS engine."""
    engine.say(text)
    engine.runAndWait()


def index(request):
    """Render the command input form."""
    return render(request, 'voiceassistant/index.html')


def alarm_clock(text):
    """Trigger an alarm with the given text."""
    engine.say(text)
    engine.runAndWait()


def start_scheduler():
    """Start a background scheduler to run tasks at specific times."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: alarm_clock("Подъем! Время вставать!"), 'cron', hour=6, minute=0)
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
    subprocess.Popen('D:\\Proekti\\snake2_3D\\dist\\main_snake_game.exe')


def play_music():
    """Open a music streaming service in the browser."""
    webbrowser.open("https://www.spotify.com")


def offpc():
    """Shut down the computer."""
    os.system('shutdown /s /t 1')
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
            alarm_clock(result)
    else:
        print("Команда не распознана")
        alarm_clock("Команда не распознана")


def voice_command_view(request):
    """Handle voice commands from the web interface."""
    if request.method == "POST":
        command = request.POST.get('command', '')
        print(f"Received command: {command}")
        if command:
            respond_to_command(command)
            return JsonResponse({"status": "success", "message": f"Executed command: {command}"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
