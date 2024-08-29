# !/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from main_app import speak


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def data_set():
    """Returns a dictionary mapping voice commands to their respective actions."""
    return {
        'привет': lambda: speak('и тебе, привет'),
        'какая сейчас погода': lambda: speak('weather сейчас скажу'),
        'какая погода на улице': lambda: speak('weather боишься замерзнуть?'),
        'что там на улице': lambda: speak('weather сейчас гляну'),
        'сколько градусов': lambda: speak('weather можешь выглянуть в окно, но сейчас проверю'),
        'запусти браузер': lambda: speak('browser запускаю браузер'),
        'открой браузер': lambda: speak('browser открываю браузер'),
        'открой интернет': lambda: speak('browser интернет активирован'),
        'играть': lambda: speak('game лишь бы баловаться'),
        'хочу поиграть в игру': lambda: speak('game а нам лишь бы баловаться'),
        'запусти игру': lambda: speak('game запускаю, а нам лишь бы баловаться'),
        'посмотреть фильм': lambda: speak('browser сейчас открою браузер'),
        'выключи компьютер': lambda: speak('offpc отключаю'),
        'отключись': lambda: speak('offbot отключаюсь'),
        'как у тебя дела': lambda: speak('passive работаю в фоне, не переживай'),
        'что делаешь': lambda: speak('passive жду очередной команды, мог бы и сам на кнопку нажать'),
        'работаешь': lambda: speak('passive как видишь'),
        'расскажи анекдот': lambda: speak('passive вчера помыл окна, теперь у меня рассвет на 2 часа раньше'),
        'ты тут': lambda: speak('passive вроде, да'),
        'how are you doing today': lambda: speak('passive nice, and what about you'),
        'good night': lambda: speak('passive bye, bye'),
        'пока': lambda: speak('passive Пока')
    }


def triggers():
    """Returns a set of voice command triggers."""
    return {'привет', 'какая сейчас погода', 'какая погода на улице', 'что там на улице', 'сколько градусов',
            'запусти браузер', 'открой браузер', 'открой интернет', 'играть', 'хочу поиграть в игру',
            'запусти игру', 'посмотреть фильм', 'выключи компьютер', 'отключись', 'как у тебя дела',
            'что делаешь', 'работаешь', 'расскажи анекдот', 'ты тут', 'how are you doing today',
            'good night', 'пока'}


# Пример вызова функций
if __name__ == '__main__':
    # Пример использования
    data = data_set()
    print("Voice Commands and Actions:")
    for command, action in data.items():
        print(f"Command: {command} -> Action: {action}")
        action()  # Вызываем функцию, которая произносит ответ голосом

    print("\nVoice Command Triggers:")
    print(triggers())
