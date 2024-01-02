import json
from gtts import gTTS
import pygame
from io import BytesIO
from googletrans import Translator
import speech_recognition
import pyttsx3
from rapidfuzz import fuzz
import random
from time import sleep
import os

pygame.init()
big_data = {}
data ={}
questions = []
 
def getFileContent(file_name):
    f = open(file_name+'.json')
    global data
    global big_data
    data = json.load(f)
    big_data = data
    f.close()

def speak():
    print("Speak Now : " )
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
    print(text)
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

def writing():
    
    speech = str(input("Enter : "))

    return speech

def ans_check(question, speech):
    print("\nYou said : " + speech,"\nCorrect way : " +data[question],"\nScore : " + str(fuzz.ratio(data[question].lower(), speech)))
    if(fuzz.ratio(data[question], speech) < 80):
        print("wrong answer")
        return False
    return True

def practice(question,sp, lang='en'):
    for i in range(3):
        write=""
        if(sp=='speak'):
            if(lang=='hi'):
                ask(trans(question) + " ,  " +  data[question])
            else:
                 ask(question + " ,  " +  data[question])
            write = speak()
        else:
            print(question)
            write=writing()
        ans = ans_check(question, write)


def test(sp,lang = 'en'):
    for question in questions:
        if question=='learnt_count':
            continue
        if str(data[question])=='learnt_count':
            continue

        print('\n')
        write=""
        if(sp=='speak'):
            if(lang=='hi'):
                ask(trans(question))
            else:
                
                ask(question)
            write = speak()
        else:
            print(question)
            write=writing()
        
        ans = ans_check(question, write)
        if(ans == False):
            practice(question,sp,lang)
            questions.append(question)

def learning(sp):
    for question in questions:
        if question=='learnt_count':
            continue
        if str(data[question])=='learnt_count':
            continue
        
        print('\n'+question + " ,  " +  data[question])

def learning_speak(sp):
    for question in questions:
        
        if question=='learnt_count':
            continue
        if str(data[question])=='learnt_count':
            continue
        for i in range(3):
            ask(question + " ,  " +  data[question])
            if(sp=='speak'):
                write = speak()
            else:
                write=writing()
            
            ans_check(question, write)



while(1):

    print("\n \n ********************************")
    
    

    file_name = input("What subject you want to learn : \n" + str(os.listdir())+ " : ").lower()
    
    if file_name + '.json' not in os.listdir():
        continue
    getFileContent(file_name)

   
    
    for topic in data.keys():
        if 'learnt_count' not in data[topic]:
            big_data[topic]['learnt_count'] =0
        print("\n"+topic, big_data[topic]['learnt_count'])
    
    topic =  input("\nSelect Topic : " )
    if(topic not in data.keys()):
        continue
    data = data[topic]

    isReverseData = input("\nmeaning-first? : ").lower()

    if( isReverseData == 'yes'):

        data = {v: k for k, v in data.items()}
    
    questions = list(data.keys())
    random.shuffle(questions)
    mode = input("\n Test , Learn : ").lower()
    sp = input("\nWrite, Speak : " ).lower()
    print("\n\n********************************\n****************************")
    match mode:
        case 'learn':
             learning(sp)
        case 'test':
            if file_name=='speaking':
                test(sp,'hi')
            else:
                test(sp)
        case _:
            print("wrong input")
            continue
    big_data[topic]['learnt_count'] +=1
    with open(file_name + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(big_data, json_file)

        print('JSON file updated successfully')

    
    getFileContent(file_name)



#task

    # learnt_count of every variable and show which you learnt less
    # include sentences also
    # include file at run time that is vocab and sentence
