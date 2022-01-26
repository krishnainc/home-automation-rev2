import speech_recognition as sr
from nltk import word_tokenize
import tensorflow as tf
from modelFile import *


model=tf.keras.models.load_model('model1.h5')
device=['fan','light']
command=['on','off']
wake_up=['lambo','rambo','jumbo','lumbo','gumball','number','gumbo','dumbo','bumble']
def speech(check):
    r=sr.Recognizer()
    
    
    with sr.Microphone() as source:
        if(check):
            print('Speak anything : ')
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            #print(text)
            if(check):
                print('You said: {}'.format(text))
                main(text)
            words=word_tokenize(text.lower())
            for i in wake_up:
                if(i in words):        
                    return True
        except:
            speech(False)

from contractions import CONTRACTION_MAP # make sure copy contraction.py in the same folder as this file
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

from nltk.stem.snowball import SnowballStemmer
englishStemmer=SnowballStemmer("english")
def stemming(text):
    text_stemming=[]
    words=word_tokenize(text)
    for word in words:
        text_stem=englishStemmer.stem(word)
        text_stemming.append(text_stem)
    
    return (" ".join(text_stemming))


from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatization(text):
    text_lemma=[]
    words=word_tokenize(text)
    for word in words:
        lemma=wordnet_lemmatizer.lemmatize(word, pos="v")
        text_lemma.append(lemma)
    return (" ".join(text_lemma))


import re
#from serpapi import GoogleSearch

def main(text):
    #print('hello')
    words=word_tokenize(text)
    text_lower=text.lower()
    #print(text_lower)
    text_contra=expand_contractions(text_lower)
    if any(word in text_contra for word in device):
    
        #print(text_contra)
        text_stem=stemming(text_contra)
        #print(stemming(text_contra))
        text_lemma=lemmatization(text_stem)
        words=word_tokenize(text)

        for i in device:
            if(i in words):
                for y in command:
                    if(y in words):
                        print(i+" "+y)
                        speak(i+" "+y)
    
    
    else :

        z=runApp1(text_contra)

        speak(z)
        
                    
    
    #print(date_born)

import pyttsx3
def speak(date_born):
    
    text_speech=pyttsx3.init()
    text_speech.say(date_born)
    text_speech.runAndWait()
    return False
def run():
    check=False
    while True:
        check=False
        print('Sleeping')
        check=speech(False)
        if(check):
            print('Wake Up')
            speech(True)

run()