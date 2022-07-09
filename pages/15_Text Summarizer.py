import streamlit as st
import requests
import time
import json
from transformers import pipeline


st.text('')
st.title('📋Text Summarizer')
st.text('')
st.markdown(':white_check_mark:Text Summarizer is a machine learning algorithm that extracts the most important points from a text document. Text Summarizer can be used to summarize long documents quickly and easily.')
summarizer = pipeline("summarization")

#Example Input
sum_example = 'Apple has released iOS 15.2.1, its latest software update for recent iPhone and iPad devices. The patch addresses a vulnerability found within the company’s HomeKit protocol for connecting disparate smart home devices. The bug allowed malicious individuals to force an iPhone or iPad to repeatedly crash and freeze by changing the name of a HomeKit-compatible device to include more than 500,000 characters. Since iOS backs up HomeKit device names to iCloud, it was possible for iOS users to get stuck in an endless loop of crashes.'
min_example = 30
max_example = 100
#User Input
input_sum =st.text_area("Use the example below or input your own text in English (maximum 10000 characters)", max_chars=10000, value=sum_example, height=160)
input_min = st.text_input("The minimum output of summarized text(numeric value)",key=int, value = min_example)
input_max = st.text_input("The maximum output of summarized text(numeric value)", key=int,value = max_example)

#Button

if st.button('Summarize') :
#Change Button Color by Markdown
        st.markdown(f""" <style>.css-1cpxqw2 {{backgound-color: rgb(78, 116, 255); !important}}</style> """, unsafe_allow_html=True)
    
    #If no input in the text box
        if input_sum =='':
            st.error('Please enter some text')
        else:
            with st.spinner('Wait for it...'):
                result = summarizer(input_sum,max_length=int(input_max),min_length=int(input_min))
                st.write([result][0][0]["summary_text"]) 


