from pycaret.regression import *
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests
import time
import json
from io import StringIO
import plotly.express as px

st.text('')
st.title('📈Regression')
st.text('')
st.markdown(':white_check_mark:Regression is a technique used to find relationships between variables in data. It can be used to predict future values of one variable based on the values of another variable.')    
uploaded_file = st.file_uploader("Choose a file",key=regression)
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
    st.session_state['data']   = pd.read_csv(uploaded_file,encoding= 'unicode_escape')
    st.dataframe(st.session_state['data'].head(10))
    #Spliting data for prediciton
    st.write('We use 70% of your data as training set, and 30% of the data to validate the model')

    
    #Plot linear regression graph
    #Finding Correlation by Linear Regression 
    st.title('Graph')
    st.write('Check out the correlation between different factors')

    example_factor = 'TV'
    factor=st.text_input('Input the column name of factor vs target ',example_factor)

    #Let user inpnut to choose the target value
    example_target = 'Sales'
    target = st.text_input('Input the target value',example_target)

    if st.button('Generate') :
        with st.spinner('Training model...'):
        #If no input in the text box
            if factor =='':
                st.error('Please enter some text')
            
            elif target =='':
                st.error('Please enter some text')
            else:
                fig = px.scatter(st.session_state['data'], x=factor, y=target,width=300,height=300,trendline="ols")

                st.plotly_chart(fig, use_container_width=True)
                #Setup training env
                    #Evalutate Model by graph
        #evaluate_model(best)
    st.title('Validate the model')
    with st.spinner('Training model...'):
        st.write('Check out the following predicted value, we named it as "Predicted Value"')
        s = setup(st.session_state['data'],target=target,silent=True)

        #Choose Best Model
        best = compare_models()

        #Predict 
        predictions = predict_model(best, data=st.session_state['data'])
        rename_predictions = predictions.rename(columns={"Label":"Predicted Value"})
        st.dataframe(rename_predictions)
        
        @st.cache
        def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

        csv = convert_df(rename_predictions)

        st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='regression.csv',
                mime='text/csv',
            )
