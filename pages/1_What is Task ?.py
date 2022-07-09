import streamlit as st
import streamlit.components.v1 as components


st.text('')

st.title('What is Task ?')
st.subheader('Task is a predefined marketing duties based on preset marketing tasks.')
st.write('Marketing consists of a lot of manual workload from data collection, data analytics and drawing data-driven marketing campaigns')
st.write('In fact, we can eliminate manual work with AI Marketer by using automated ways to collect data and using artificial intelligence to lower the manual workload of the marketer.')

st.text('')
st.text('')

st.text('')
st.write('If you love the project like I do ... ')
components.html("""
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="catyung" data-color="#5F7FFF" data-emoji="🍕"  data-font="Poppins" data-text="Buy me a pizza" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
""")

col1, col2, col3 ,col4= st.columns(4)

with col1:
    st.title('🏇')
    st.subheader("Competitor Analysis")
    
    st.caption("Xray your competitor and their performance by user feedback")

with col2:
    st.title('💰')
    st.subheader("Cart Analysis")
    
    st.caption("Find out the correlation of different products to set product combination")

with col3:
    st.title('👨‍👩‍👦‍👦')
    st.subheader("Customer Segmentation")
    
    st.caption("Segment your customers and target on the prospect")

with col4:
    st.title('👑')
    st.subheader('RFM Model')
    st.caption('Identify customers who are most engaged with your products or services')



st.text('')
st.text('')

col1, col2, col3 ,col4= st.columns(4)

with col1:
    st.title("👥")
    st.subheader("Review Analysis")

    st.caption("Understand your customer by their reviews")

with col2:
    st.title('⌨')
    st.subheader("Google AdWord Generator")
    
    st.caption('Create a list of keywords for Google AdWords')

with col3:
    st.title("💯")
    st.subheader("Trend Forecast")
    
    st.caption('Predict a future trend accurately based on the previous data you have')

with col4:
    st.title('🤑')
    st.subheader("Price Analysis")
    
    st.caption('Help you clearly understand what the right price point is for your products')

    