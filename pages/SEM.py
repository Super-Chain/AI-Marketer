import streamlit as st
from ecommercetools import advertising
import pandas as pd


st.text('')
st.title('⌨Google AdWord Generator')
st.text('')
st.markdown(":white_check_mark:Create a list of keywords for Google AdWords")
example_product_names = 'phone case , stainless steel phone case'
product_names = st.text_input('Input the product names in list use comma to seperate the product',example_product_names)
product_names = product_names.split(',')


example_keywords_prepend = 'buy,best,cheap,reduced'
keywords_prepend = st.text_input('Input the words that you want to add before the product names',example_keywords_prepend)
keywords_prepend = keywords_prepend.split(',')


example_keywords_append = 'for sale,price,promotion'
keywords_append = st.text_input('Input the words that you want to add before the product names',example_keywords_append)
keywords_append = keywords_append.split(',')


example_campaign_name = 'phone case'
campaign_name = st.text_input('Input the campaign name',example_campaign_name)

if st.button('Submit'):
    keywords = advertising.generate_ad_keywords(product_names, keywords_prepend, keywords_append,campaign_name)
    keywords=keywords.astype(str)
    st.dataframe(keywords)
    
    @st.cache
    def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

    csv = convert_df(pd.DataFrame(keywords))

    st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='SEM.csv',
            mime='text/csv',
        )
