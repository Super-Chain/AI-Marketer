from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import re
import plotly.express as px
from decimal import Decimal

headers = { 
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}



st.text('')
st.title('🤑Price Analysis')
st.markdown(':white_check_mark:Help you clearly understand what the right price point is for your products')

st.text('')
example_query = 'iphone'
example_country = 'HK'
query = st.text_input('Input the Product Name', example_query)
country = st.text_input('Input the Country Code',example_country)

def isalive(response):
    return response.status_code == 200

def format_price(price):

    price_num = Decimal("".join(d for d in price if d.isdigit() or d == '.'))
    return int(price_num)


if st.button("Analyze"):
    params = {"q": query, "hl": "en", 'gl': country, 'tbm': 'shop'}

    try:
        url = "https://www.google.com/search?"
        for key in params.keys():
            url += key + "=" + params[key].replace(" ", "+")+'&'
        #print(url)
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(repr(e))
        st.error("Wrong input. Try again!")

    #print(response)

    if not isalive(response):
        st.error("Service not available. Try later!")

    else:

        soup = BeautifulSoup(response.text, 'lxml')
        st.session_state['df'] = pd.DataFrame()
        #print(soup)
        all_product_details = soup.find_all("div", {"class": "xcR77"})[1:21]
        #print(all_product_details)
        for product_details in all_product_details:
            #print(product_details)
            try:
                title = product_details.find('div', {"class": "rgHvZc"}).text
            except:
                st.error("No data available.")
                break
            image = product_details.find('img')['src']
            price_offer = product_details.find_all('div', {"class": "dD8iuc"})[-1].text
            price = price_offer[:price_offer.index('from')]
            price = price.split(' ')[0]
            offered = price_offer[price_offer.index('from')+4:]
            link = product_details.find_all('a', href=True)
            #print(link)
            #print()
            source = f"https://www.google.com/{product_details.find_all('a', href=True)[-1]['href']}"

            st.session_state['df'] = st.session_state['df'].append({"Title": title, "Image": image, "Price": price, "Source": source, "Offered by": offered}, ignore_index=True)
            if len(st.session_state['df']) == 10:
                break
        image_width = 50
        #format the images list
        st.session_state['df']['Pic'] = ["<img src='" + r.Image
            + f"""' style='display:block;margin-left:auto;margin-right:auto;width:{image_width}px;border:0;'><div style='text-align:center'>""" 
            + "</div>" 
            for ir, r in st.session_state['df'].iterrows()]
        st.session_state['df'].set_index("Title", drop=True, inplace=True)
        st.session_state['df'].index.name = None

        st.write(st.session_state['df'][['Pic', 'Price', 'Offered by']].to_html(escape=False), unsafe_allow_html=True)
        
        @st.cache
        def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

        csv = convert_df(st.session_state['df'][['Source', 'Price', 'Offered by']])
        
        st.write('')

        st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='price_analysis.csv',
                mime='text/csv',
            )                
        st.title('Price Analysis')
        graph = st.session_state['df'][['Price', 'Offered by']]
        graph['Price'] = graph['Price'].apply(format_price)
        graph = graph.sort_values(by='Price')

        fig = px.line(graph, y="Price")
        st.plotly_chart(fig, use_container_width=True)
        st.title('Price Statistics')
        st.dataframe(pd.DataFrame(graph['Price'].describe()).iloc[[1,2,3,5,7]].T, width=900)
