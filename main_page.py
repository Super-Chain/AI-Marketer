import streamlit as st
st.set_page_config(page_title="AI Marketer - No Code Marketing Analysitcs", 
                page_icon=":robot_face:",
                layout="wide",
                initial_sidebar_state="expanded"
                )
from re import X
from pages.home import home
from pages.task import task
from pages.pipeline import pipeline
from pages.translation import translation
from pages.sentiment import sentiment
from pages.summarizer import summarizer
from pages.sidebar import *
from pages.reviewanalysis import reviewanalysis
from pages.cartanalysis import cartanalysis
from pages.regression import regression
from pages.STP import STP
from pages.SEM import SEM
from pages.competitor import competitor
from pages.rfmanalysis import rfmanalysis
from pages.clustering import clustering
from pages.classification import classification
from pages.priceanalysis import priceanalysis
