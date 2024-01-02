from gtts import gTTS
import pygame
from io import BytesIO
from googletrans import Translator
import speech_recognition
import pyttsx3
from rapidfuzz import fuzz
import random
from time import sleep
pygame.init()

file_name = "simple_tense.txt"

def speak():
    recognizer = speech_recognition.Recognizer()

    print("Iam listening : " )
    with speech_recognition.Microphone() as mic:
         recognizer.adjust_for_ambient_noise(mic, duration = 0.4)
         audio = recognizer.listen(mic)
    try:
        text = recognizer.recognize_google(audio)
        text = text.lower()
        return text
        
    except speech_recognition.UnknownValueError():
        print("Try again iam listening again : " )
        speak()

def ask(text):
    tts = gTTS(text=text, lang='hi',tld='co.in', slow=False)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def trans(text):
    translater = Translator()
    out = translater.translate(text, dest ='hi')
    return out.text


def practice(question):
    for i in range(3):
        ask(trans(question) + ',' + question)
        sleep(0.5)
    
    

questions =[]

wrong_words = []
total = 0
count = 0



with open(file_name) as myfile:
    for question in myfile:
        questions.append(question)

random.shuffle(questions)
        

for question in questions:
    sleep(0.1)
    total = total+1
    ask(trans(question))
    
    speech = speak()
    if(fuzz.ratio(question, speech) < 80):
        practice(question)
        wrong_words.append(question)
        count = count +1
    print(question, speech,fuzz.ratio(question, speech) ,'\n')

correct_ans = total-count
f = open("score_" + file_name, "a")
f.write('\n\n Correct answer : ' + str(correct_ans) + '/' + str(total) +'\n')
f.writelines(wrong_words)
f.close()



    





