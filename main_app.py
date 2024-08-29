import pyttsx3
import json
import queue
import sounddevice as sd
import vosk
from vosk import KaldiRecognizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Инициализация голосового движка
engine = pyttsx3.init()


def speak(message):
    """Произносит сообщение вслух."""
    engine.say(message)
    engine.runAndWait()


def data_set():
    """Возвращает словарь, сопоставляющий голосовые команды с соответствующими действиями."""
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
    """Возвращает набор триггеров голосовых команд."""
    return set(data_set().keys())


# Инициализация очереди для аудиоданных
q = queue.Queue()

# Загрузка модели Vosk
model = vosk.Model('vosk-model')

# Настройка устройств ввода и вывода
device = sd.default.device = (0, 4)  # Настройте индексы устройств ввода и вывода по необходимости
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

# Инициализация распознавателя Vosk
rec = KaldiRecognizer(model, samplerate)


def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}", flush=True)
    q.put(bytes(indata))


def recognize_and_execute(data, vectorizer, clf):
    """Распознает команду из аудио и выполняет соответствующую функцию."""
    trg = triggers().intersection(data.split())
    if not trg:
        return
    # Очистка команды от триггерного слова
    data = data.replace(list(trg)[0], '')
    # Векторизация входного текста
    text_vec = vectorizer.transform([data]).toarray()[0]
    # Прогнозирование действия
    answer = clf.predict([text_vec])[0]
    # Выполнение действия
    func_name = answer.split()[0]
    if func_name in data_set():
        data_set()[func_name]()


def main():
    """Основная функция для настройки распознавания голоса и обработки команд."""
    # Инициализация векторизатора и классификатора
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(data_set().keys()))
    clf = LogisticRegression()
    clf.fit(vectors, list(data_set().keys()))

    # Запуск прослушивания аудиопотока
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0],
                           dtype="int16", channels=1, callback=callback):
        print("Listening...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize_and_execute(data, vectorizer, clf)
                print(data)
            else:
                print(rec.PartialResult())


if __name__ == '__main__':
    main()
