import pandas as pd 
from pycaret.classification import *
import os
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


st.text('')
p_title('🎏Classification')
st.text('')
st.markdown(':white_check_mark:Classification is the task of identifying which category a given observation belongs to. In other words, it is the task of distinguishing between different groups, it is useful to handle task for marketing like event prediction.')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #st.write(bytes_data)
        # Can be used wherever a "file-like" object is accepted:
        data = pd.read_csv(uploaded_file,  encoding= 'unicode_escape')
        st.write(data.head(10))
        st.write("Received data size display in row,column" ,data.shape)
        st.write('We use 70% of your data as training set, and 30% of the data to validate the model')

        example_target = 'Clicked on Ad'
        target = st.text_input('The target column that you want to predict',example_target)

        if st.button('Submit'):
            with st.spinner('Training model...'):
                s = setup(data,target=target, silent=True)
                best = compare_models()
            plot_model(best, plot ='feature_all',display_format='streamlit')
            plot_model(best, plot ='confusion_matrix',display_format='streamlit')

            #Validation
            st.header('Validate the model by test dataset')
            predictions = predict_model(best,data=data,raw_score=True)
            rename_predictions = predictions.rename(columns={"Label":"Predicted Value","Score_0":"Possibility of predicted as 0","Score_1":"Possibility of predicted as 1"})
            st.dataframe(rename_predictions)
            
            @st.cache
            def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')

            csv = convert_df(rename_predictions)

            st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='classification.csv',
                    mime='text/csv',
                )

