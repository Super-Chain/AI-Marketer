import streamlit as st
from util import p_title
#from annotated_text import annotated_text
import html
import time
import requests
import streamlit.components.v1 as components
import spacy
from spacy import displacy
import re

nlp = spacy.blank('en')

def ner(nav):
    if nav == 'Named Entity Recognition':
        st.text('')
        p_title('Named Entity Recognition')
        st.text('')
        example_ner = 'Security Camera 2K, blurams Baby Monitor light Red Dog Camera 360-degree for Home Security w/ Smart Motion Tracking, Phone App, IR Night Vision, Siren, Works with Alexa & Google Assistant & IFTTT, 2-Way Audio'
        input_ner =st.text_area("Use the example below or input your product title in English (maximum 500 characters)", max_chars=500, value=example_ner, height=160)
        
        #Define NER Tags Color
        color_dict = {'model number': "#8ef", "brand": "#faa", "color":"#fea", "scenario": "#afa", "feature": "#d385ff", "material": "#eeff86"}
       
        # run the function when users click the button 
        #Change Button Color by Markdown
        st.markdown(f""" <style>.css-1cpxqw2 edgvbvh1 {{color: rgb(78, 116, 255);}}</style> """, unsafe_allow_html=True)

        if st.button('Analyze') :
            
        #If no input in the text box
            if input_ner =='':
                st.error('Please enter some text')
            else:
                with st.spinner('Wait for it...'):
                    time.sleep(6)
            
                url = "http://35.232.5.235:8081/ner"
                payload = {"Title":input_ner}
                headers = {
                    'content-type': "application/json",
                    }
            response = requests.request("POST", url, json=payload, headers=headers)
            result = response.json()


            doc = nlp(input_ner)
            #result = {"brand": "Security", "color": "Red"}
            color_dict = {'model number': "#8ef", "brand": "#faa", "color":"#fea", "scenario": "#afa", "feature": "#d385ff", "material": "#eeff86"}

            spans = []
            for key in result['Result'].keys():
                spans.extend([(m.start(0), m.end(0), key) for m in re.finditer(result['Result'][key], input_ner)])
            ents = []
            for span_start, span_end, label in spans:
                ent = doc.char_span(span_start, span_end, label=label)
                if ent is None:
                    continue
                ents.append(ent)

            doc.ents = ents
            html = displacy.render(doc, style="ent", jupyter=False, options={"colors": color_dict})
            html += '<style>body {background-color: #f0f2f6; font-family: "Source Sans Pro", sans-serif;}</style>'
            components.html(html)
            
