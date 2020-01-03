"""
使用谷歌语音识别和tts完成的一个任务型对话小demo
"""
import webbrowser
import time
import os
import sys
import random
from time import ctime
import playsound
import speech_recognition as sr
from gtts import gTTS

R = sr.Recognizer()


def record_audio(ask: bool = False) -> str:
    with sr.Microphone() as source:
        if ask:
            alexis_speek(ask)
        audio = R.listen(source)

        voice_data = ''
        try:
            voice_data = R.recognize_google(audio)
        except sr.UnknownValueError:
            alexis_speek("Sorry, I did not get that")
        except sr.RequestError:
            alexis_speek('Sorry, my speech service is down')
        return voice_data


def alexis_speek(audio_string: str):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data: str):
    if 'what is your name' in voice_data:
        alexis_speek('My name is Alexis')
    if 'what time is it' in voice_data:
        alexis_speek(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speek('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speek('Here is the location of ' + location)
    if 'exit' in voice_data:
        sys.exit()


if __name__ == "__main__":
    time.sleep(1)
    alexis_speek('How can I help you?')
    while 1:
        voice_data = record_audio()
        respond(voice_data)
