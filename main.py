import speech_recognition as sr
import playsound 
from gtts import gTTS 
import random
from time import ctime respo
import webbrowser
import time
import os

with open('./data.json') as f:
  dialogue = json.load(f)

class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True
        
r = sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak(random.choice(dialogue['UnknownResponse']))
        except sr.RequestError:
            speak(dialogue['RequestError']) 
        print(f">> {voice_data.lower()}")
        return voice_data.lower()
    
def speak(audio_string):
    text_to_speech = gTTS(text=audio_string, lang='en') 
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    text_to_speech.save(./audio_file) 
    playsound.playsound(audio_file) 
    print(f": {audio_string}") 
    os.remove(./audio_file) 
    
def respond(voice_data):
    # greeting
    if there_exists(dialogue['BotToUserGreetings']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

    # name
    if there_exists(dialogue['AskName']):
        if person_obj.name:
            speak(dialogue['ReplyAskName'])

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f" {dialogue['ReplyAfterName']} {person_name}")
        person_obj.setName(person_name) 

    # greeting
    if there_exists(dialogue['UserToBotGreetings']):
        speak(f"{dialogue['ReplyUserToBotGreetings']}{person_obj.name}")

    # time
    if there_exists(dialogue['AskTime']):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    # google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'I found {search_term} for you')

    # youtube
    if there_exists(dialogue['GoogleSearchYouTube']):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'I found {search_term} for you')

    if there_exists(dialogue['Exit']):
        speak(random.choice(dialogue['Exit']))
        exit()
        
time.sleep(1)

person_obj = person()
while(1):
    voice_data = record_audio() 
    respond(voice_data) 