import pandas as pd 
from pycaret.clustering import *
import os
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.text('')
st.title('🌗Clustering')
st.text('')
st.markdown(":white_check_mark:Clustering is a technique used in machine learning to group data points into clusters. Clustering can be used to find patterns in data, and to predict future events.")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #st.write(bytes_data)
        # Can be used wherever a "file-like" object is accepted:
        data = pd.read_csv(uploaded_file,  encoding= 'unicode_escape')
        st.write(data.head(10))

        s = setup(data, normalize = True, silent=True)
        kmeans = create_model('kmeans')
        plot_model(kmeans,plot='2d',display_format='streamlit')
        plot_model(kmeans,plot='elbow',display_format='streamlit')

        kmeans_results = assign_model(kmeans)
        # Inspect Clusters 
        st.title('Clusters')
        st.dataframe(kmeans_results)

        #Cluster info
        st.title("Cluster Info")
        cluster_options = list(kmeans_results['Cluster'].unique())
        cluster = st.radio('Select the cluster to check the info', cluster_options)
        cluster = str(cluster)
        st.write('You selected', cluster)
        cluster_info = kmeans_results.loc[kmeans_results['Cluster'] == cluster]
        st.dataframe(cluster_info.describe().T)
        
        @st.cache
        def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

        csv = convert_df(cluster_info.describe().T)

        st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='clustering.csv',
                mime='text/csv',
            )
