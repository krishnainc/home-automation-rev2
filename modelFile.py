import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk
import string
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D,Flatten
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

def runApp1(text_contra):
    
    with open('dataText.json') as content:

        detail=json.load(content)

    tags=[]
    inputs=[]
    response={}
    for intent in detail['intents'][0:5000]:
        response[intent['tag'][0:5000]]=intent['responses'][0:5000]
        for lines in intent['patterns'][0:5000]:
            inputs.append(lines)
            tags.append(intent['tag'])

    data=pd.DataFrame({"inputs":inputs,"tags":tags})

    data['inputs']=data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
    data['inputs']=data['inputs'].apply(lambda wrd:''.join(wrd))


    
    tokenizer=Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(data['inputs'])
    train=tokenizer.texts_to_sequences(data['inputs'])

    
    x_train =pad_sequences(train)

    
    le=LabelEncoder()
    le.fit_transform(data['tags'])

    input_shape=20
    text_p=[]
    prediction_input=text_contra
    prediction_input=[letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input=''.join(prediction_input)
    text_p.append(prediction_input)

    prediction_input=tokenizer.texts_to_sequences(text_p)
    prediction_input=np.array(prediction_input).reshape(-1)
    prediction_input=pad_sequences([prediction_input],input_shape)
        

    new_model=tf.keras.models.load_model('model2.h5')

    output=new_model.predict(prediction_input)

    output=output.argmax()

    vocabulary=len(tokenizer.word_index)

    output_length=le.classes_.shape[0]

    response_tag=le.inverse_transform([output])[0]

    print('Going Merry :',response[response_tag])
    return response[response_tag]