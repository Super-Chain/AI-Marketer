import streamlit as st
import streamlit.components.v1 as components


st.text('')

st.title('What is Module ?')
st.subheader('Module offers you the freedom to link different modules together (Just like LEGOs)')
st.write('By the time that you are doing differnet customized marketing tasks, you might found that you need to customized the data flow or analytics steps, this is where module can be used !')
st.write('Handling your marketing task based on what you need and simplify your workload now')

st.text('')
st.text('')
st.write('If you love the project like I do ... ')
components.html("""
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="catyung" data-color="#5F7FFF" data-emoji="🍕"  data-font="Poppins" data-text="Buy me a pizza" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
""")


col1, col2, col3 ,col4= st.columns(4)

with col1:
    st.title('📈')
    st.subheader("Regression")
    st.caption("Regression is a technique used to find relationships between variables in data. It can be used to predict future values of one variable based on the values of another variable.")

with col2:
    st.title('🎏')
    st.subheader("Classification")
    st.caption("Classification is the task of identifying which category a given observation belongs to. In other words, it is the task of distinguishing between different groups, it is useful to handle task for marketing like event prediction.")

with col3:
    st.title("📋")
    st.subheader('Text Summarizer')
    st.caption('Text Summarizer is a machine learning algorithm that extracts the most important points from a text document. Text Summarizer can be used to summarize long documents quickly and easily.')

with col4:
    st.title("🌗")
    st.subheader("Clustering")
    st.caption("Clustering is a technique used in machine learning to group data points into clusters. Clustering can be used to find patterns in data, and to predict future events.")

st.text('')
st.text('')

col1, col2, col3 ,col4= st.columns(4)

with col1:
    st.title('🔥')
    st.subheader("Sentiment Analysis")
    st.caption('Sentiment analysis is a technique used in machine learning to analyze the tone of text data. Sentiment analysis can be used to understand customer sentiment towards the product, campaign or brand.')

with col2:
    st.title("📖")
    st.subheader("Translation")
    st.caption('Translate the text data into your prefered language')

with col3:
    st.subheader("")   

with col4:
    st.subheader("")        

#        with col3:
#            st.title('💹')
#           st.subheader("Time Series")
#            st.caption("A time series is a series of data points, each of which is associated with a time stamp. Time series data can be used to predict future events. Time series data is often used in marketing to predict customer behavior, product demand, and other trends.")
