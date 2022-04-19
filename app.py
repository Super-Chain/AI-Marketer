from re import X
import streamlit as st
st.set_page_config(page_title="AI Marketer - No Code Marketing Analysitcs", 
                page_icon=":robot_face:",
                layout="wide",
                initial_sidebar_state="expanded"
                )

from home import home
from task import task
from pipeline import pipeline
from translation import translation
from sentiment import sentiment
from summarizer import summarizer
from sidebar import *
from reviewanalysis import reviewanalysis
from cartanalysis import cartanalysis
from regression import regression
from STP import STP
from SEM import SEM
from competitor import competitor
from rfmanalysis import rfmanalysis
from clustering import clustering
from classification import classification
from priceanalysis import priceanalysis



def main():    
    nav = sidebar()
    home(nav)
    task(nav)
    pipeline(nav)
    reviewanalysis(nav)
    cartanalysis(nav)
    STP(nav)
    SEM(nav)
    competitor(nav)
    rfmanalysis(nav)
    priceanalysis(nav)


    regression(nav)
    translation(nav)
    sentiment(nav)
    summarizer(nav)
    clustering(nav)
    classification(nav)

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        
if __name__ == "__main__":
    main()
    