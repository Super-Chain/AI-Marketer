import streamlit as st
#from sidebar import *
import requests 
import time
import json
from io import StringIO
import pandas as pd
from transformers import pipeline

st.text('')
st.title('🔥Sentiment Analysis')
st.text('')
st.markdown(':white_check_mark:Sentiment analysis is a technique used in machine learning to analyze the tone of text data. Sentiment analysis can be used to understand customer sentiment towards the product, campaign or brand.')
classifier = pipeline("sentiment-analysis")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file)

    st.dataframe(data.head(10))
    example_target = 'review'
    target = st.text_input('Select the column that you want to detect the sentiment score',example_target)
    
    if st.button('Analyze',key="csv") :
        data = data.dropna(subset=target)
        
        with st.spinner('Detecting...'):
            result = classifier(list(data[target]))
            st.write(result)
else :
    #Example Input
    p_example = 'I bought this to replace my Furbo camera that malfunctioned after only 18 months and no warranty.My dog doesnt care for the treat toss feature of the Furbo so this was a great and MUCH less expensive option. It works great and alerts me when my dog barks and I can talk to her to calm her down. Im very happy with it!'
    #User Input
    input_pa =st.text_area("Use the example below or input your own text in English (maximum 500 characters)", max_chars=500, value=p_example, height=160)
    
    if st.button('Analyze') :
        
    #If no input in the text box
        if input_pa =='':
            st.error('Please enter some text')
        else:
            with st.spinner('Wait for it...'):
                result = classifier(input_pa)
                st.write([result][0][0])