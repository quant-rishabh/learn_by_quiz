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
    data = json.load(f)
    f.close()
    return data

def writing():
    
    speech = str(input("Enter : "))

    return speech

def all_lower(my_list):
    ##filter multiple answer
    new_list = []
    for x in my_list:
        new_list.append(x.lower().replace(" ",""))    
    return new_list

def practice(question, answer):
    prGreen("\n Practicing Now : ")
    for i in range(3):
        multiple_answer = answer.copy()
           
        while multiple_answer:
                    temp = input("\n" + question + "(" + str(len(multiple_answer))+ ") : ").lower().replace(" ","")
                    if temp == "show":
                        prYellow("Remember now this : " + str(multiple_answer))
                        practice(question,multiple_answer)
                    if temp not in multiple_answer:
                        prRed("wrong Ans , Try again")
                        continue
                    multiple_answer.remove(temp)
        prGreen("Correct :) ")


def test(file_name):
    
    for obj in data:
        if 'learnt_count' in obj:
            
            continue
        prCyan("\n"+obj['question'])
        
        for key in obj:
            ## specific use cases for json file 
            if(file_name == "leetcode"):
                if key =="description":
                    continue
                
            if key != 'question' :
                multiple_answer = obj[key].split(";")
                multiple_answer = all_lower(multiple_answer)
                while multiple_answer:
                    temp = input("\n" + key + "(" + str(len(multiple_answer))+ ") : ").lower().replace(" ","")
                    if temp == "show":
                        prYellow("Remember now this : " + str(multiple_answer))
                        practice(obj['question'],multiple_answer)
                        continue
                    if temp not in multiple_answer:
                        prRed("wrong Ans , Try again")
                        continue
                    multiple_answer.remove(temp)
        prGreen("Correct :) ")
            


def learning_ver_2():
    ## new json list of object with question is compulsory
    for obj in data:
        prYellow("**************************************************************************************************************")
        if 'learnt_count' in obj:
            continue
        for i in obj:
            prCyan(i + " : ")
            prGreen("\t\t "+ obj[i])





def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
 
 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
 
 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
 
 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
 
 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
 
 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
 
 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
 
 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

        



while(1):

    print("\n \n ********************************")
    
    
    prCyan("What subject you want to learn : " + str(os.listdir())+ " : \n")
    file_name = input().lower()
    
    if file_name + '.json' not in os.listdir():
        continue
    data = getFileContent(file_name)
    big_data = getFileContent(file_name)
    
    for topic in big_data.keys():
        if 'learnt_count' not in big_data[topic][len(big_data[topic])-1]:
            big_data[topic].append({"learnt_count" :0 })
        print("\n"+topic, big_data[topic][len(big_data[topic])-1]["learnt_count"])
    topic =  input("\nSelect Topic : " )
    if(topic not in data.keys()):
        continue
    
    data = data[topic]
    random.shuffle(data)

    prCyan("\nTest or Learn ? : ")

    mode = input().lower()
    if(mode == "learn"):
        learning_ver_2()
        continue 
    test(file_name)

    big_data[topic][-1]["learnt_count"]+=1
    print("last data : ", big_data[topic][-1])
    print("learn count data : ", big_data[topic][-1]["learnt_count"])
    with open(file_name + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(big_data, json_file)

        print('JSON file updated successfully')

    
    getFileContent(file_name)
    
    
   
