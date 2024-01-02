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

path = "very_1"

#for key value like state capital
wrong_words = []
myvars = {}
with open(path+".txt") as myfile:
    for line in myfile:
       
        name, var = line.partition("=")[::2]
        name = name.strip().lower()
        var = var.strip().lower()
        myvars[name.strip()] = var

questions = list(myvars.keys())
random.shuffle(questions)

count = len(myvars)


def speak():
    recognizer = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as mic:
            
            
            recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            return text
        
    except speech_recognition.UnknownValueError():
        print("trying again")
        recognizer = speech_recognition.Recognizer

def ask(text):
    sleep(0.5)
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

def ask_question(question):
    
    ask(question)
    print("Speak : " , question)
    speech = str(input("Enter : "))

    return speech

def ans_check(question, speech):
    
    if(fuzz.ratio(myvars[question], speech) < 90):
        print(question ,myvars[question], speech,fuzz.ratio(myvars[question], speech))
        return False
    return True

def practice(question):
    for i in range(5):
        speech = ask_question(question + " ,  " +  myvars[question])
        ans = ans_check(question, speech)
        if( ans == False):
            print(" WRONG ANSWER ")


def test():
    count = len(myvars)
    for question in questions:
        speech = ask_question(question)
        ans = ans_check(question, speech)
        if(ans == False):
            wrong_words.append(question + '\n')
            count = count -1
            practice(question)
    total = len(myvars)
    correct_ans = count
    f = open("/test/MARKS"+path+".txt", "a")
    f.write('\n\n Correct answer : ' + str(correct_ans) + '/' + str(total) +'\n')
    f.writelines(wrong_words)
    f.close()

def learning():
    for question in questions:
        print(question, myvars[question])
        for i in range(3):
            speech = ask_question(question + " ,  " +  myvars[question])
            ans = ans_check(question, speech)

print("1. Learning    2. Test ")
ch = int(input())

match ch:
    case 1:
         learning()
    case 2:
         test()



    





