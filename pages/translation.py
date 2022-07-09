import streamlit as st
import requests
import time
from google_trans_new import google_translator
import pandas as pd
from io import StringIO


st.text('')
st.title('📖Translation')
st.text('')
st.markdown(':white_check_mark:Translate the text data into your prefered language')
#Example Input
translator = google_translator()

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
    data = pd.read_csv(uploaded_file,encoding= 'unicode_escape')
    st.dataframe(data.head(10))
    example_target = 'Translate'
    target = st.text_input('Select the column that you want to translate',example_target)
    lang_example = 'zh-TW'
    input_lang = st.text_input("ISO-639-1 Code from Google :https://cloud.google.com/translate/docs/languages;e.g : Japanese =ja ; French =fr ; English =en", max_chars=5, value = lang_example)
    
    if st.button('Translate',key="csv") :
        data = data.dropna(subset=[target])
        translated_result = []
        with st.spinner('Translating...'):
            for i in list(data[target]):
                result = translator.translate(i,lang_tgt=input_lang)
                translated_result.append(result)
        translated_result = pd.DataFrame(translated_result)
        st.dataframe(translated_result.head(10))

        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(translated_result)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='translated_result.csv',
            mime='text/csv',
        )

else :
    t_example = 'Apple has released iOS 15.2.1, its latest software update for recent iPhone and iPad devices. The patch addresses a vulnerability found within the company’s HomeKit protocol for connecting disparate smart home devices. The bug allowed malicious individuals to force an iPhone or iPad to repeatedly crash and freeze by changing the name of a HomeKit-compatible device to include more than 500,000 characters. Since iOS backs up HomeKit device names to iCloud, it was possible for iOS users to get stuck in an endless loop of crashes.'
    lang_example = 'zh-TW'
    #User Input
    input_t =st.text_area("Use the example below or input your own text in English (maximum 10000 characters)", max_chars=10000, value=t_example, height=160)
    input_lang = st.text_input("ISO-639-1 Code from Google :https://cloud.google.com/translate/docs/languages;e.g : Japanese =ja ; French =fr ; English =en", max_chars=5, value = lang_example)

    #Button
    #Change Button Color by Markdown

    if st.button('Translate') :
    #If no input in the text box
        if input_t =='':
            st.error('Please enter some text')
        with st.spinner('Translating...'):
                result = translator.translate(input_t,lang_tgt=input_lang)  
                st.write(result)