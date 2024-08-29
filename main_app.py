import json
import queue
import sounddevice as sd
import vosk
from vosk import KaldiRecognizer, Model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import words
from config.skills import *

# Инициализация голосового движка
engine = pyttsx3.init()


def speak(message):
    """Произносит сообщение вслух."""
    engine.say(message)
    engine.runAndWait()


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
    trg = words.triggers.intersection(data.split())
    if not trg:
        return
    # Очистка команды от триггерного слова
    data.replace(list(trg)[0], '')
    # Векторизация входного текста
    text_vec = vectorizer.transform([data]).toarray()[0]
    # Прогнозирование действия
    answer = clf.predict([text_vec])[0]
    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ''))
    exec(func_name + '()')


def main():
    """Основная функция для настройки распознавания голоса и обработки команд."""
    # Инициализация векторизатора и классификатора
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # Запуск прослушивания аудиопотока
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                           dtype="int16", channels=1, callback=callback):
        print("Listening...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize_and_execute(data, vectorizer, clf)
            # else:
            # print(rec.PartialResult())


if __name__ == '__main__':
    main()
