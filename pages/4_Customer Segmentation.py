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
st.title('👨‍👩‍👦‍👦Customer Segmentation')
st.text('')
st.markdown(':white_check_mark:Segment your customers and target on the prospect')
if st.button('Get Demo Data') :
    data = pd.read_csv('./dataset/Mall_Customers.csv',  encoding= 'unicode_escape')
    # if rerun by changing the file
    st.write(data.head(10))
    with st.spinner('Training model...'):

        s = setup(data, normalize = True, silent=True, ignore_features = ["CustomerID"])
        st.session_state['kmeans'] = create_model('kmeans')
        st.session_state['kmeans_results'] = assign_model(st.session_state['kmeans'])

        plot_model(st.session_state['kmeans'], plot = 'cluster',display_format="streamlit")
        
        st.write('The following graph indicates the optimum numbers of cluster, based on the number of k (k=?), you should input the number of k in "Number of Clusters you would like"')
        st.title('Elbow Graph')
        col1, col2 = st.columns(2)
        with col1 :
            plot_model(st.session_state['kmeans'],plot='elbow',display_format='streamlit')
        # Inspect Clusters 
        st.title('Clusters')
        st.dataframe(st.session_state['kmeans_results'])

        st.title("Cluster Info")
        stats = st.session_state['kmeans_results'][[i for i in st.session_state['kmeans_results'].columns if i != "CustomerID"]]
        stats = stats.groupby(['Cluster']).mean().T
        stats = stats.rename_axis(None, axis = 1)
        stats = stats.reset_index().rename(columns={'index': 'attributes'})
        fig = px.bar(stats, x="attributes", y=[i for i in stats.columns if i != 'attributes'], barmode='group')

        st.plotly_chart(fig, use_container_width=True)

else :
    uploaded_file = st.file_uploader("Choose a file")
    id_name = st.text_input("Enter the column name of the customers' ID (Optional)", 'CustomerID')
    selected_k = st.text_input("Number of Clusters you would like (If you don't know, you could leave it blank and we will determine the optimal number of clusters in the elbow graph and you could use it to rerun again)", '')

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #st.write(bytes_data)
        # Can be used wherever a "file-like" object is accepted:
        data = pd.read_csv(uploaded_file,  encoding= 'unicode_escape')
        # if rerun by changing the file
        st.write(data.head(10))

        if st.button('Cluster'):
            with st.spinner('Training model...'):
                ID = str(id_name)
                try:
                    s = setup(data, normalize = True, silent=True, ignore_features = [ID])
                except:
                    st.error("Wrong Input")
                if selected_k == '':
                    st.session_state['kmeans'] = create_model('kmeans')
                else:
                    st.session_state['kmeans'] = create_model('kmeans', num_clusters = int(selected_k))
                st.session_state['kmeans_results'] = assign_model(st.session_state['kmeans'])

        if 'kmeans_results' in st.session_state:
            plot_model(st.session_state['kmeans'], plot = 'cluster',display_format="streamlit")
            col1,col2 = st.columns(2)
            with col1:
                st.text('The following graph indicates the optimum numbers of cluster, based on the number of k (k=?), you should input the number to Number of Clusters you would like')

                plot_model(st.session_state['kmeans'],plot='elbow',display_format='streamlit')
            # Inspect Clusters 
            st.title('Clusters')
            st.dataframe(st.session_state['kmeans_results'])
        
            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

            csv = convert_df(st.session_state['kmeans_results'])

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='cluster.csv',
                mime='text/csv',
            )

            #Cluster info
            with st.spinner("Analyzing"):
                st.title("Cluster Info")
                stats = st.session_state['kmeans_results'][[i for i in st.session_state['kmeans_results'].columns if i != ID]]
                stats = stats.groupby(['Cluster']).mean().T
                stats = stats.rename_axis(None, axis = 1)
                stats = stats.reset_index().rename(columns={'index': 'attributes'})
                fig = px.bar(stats, x="attributes", y=[i for i in stats.columns if i != 'attributes'], barmode='group')

            st.plotly_chart(fig, use_container_width=True)




