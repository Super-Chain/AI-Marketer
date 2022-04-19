import streamlit as st

#########
#SIDEBAR
########



def sidebar() :
    st.sidebar.header('</>AI Marketer - Marketing Analytics by AI :crystal_ball:')
    nav = st.sidebar.radio('',['🏠Homepage','===Task===','🏇Competitor Analysis','💰Cart Analysis','👨‍👩‍👦‍👦Customer Segmentation','👑RFM Model','👥Review Analysis','⌨Google AdWord Generator','💯Trend Forecast', '🤑Price Analysis','===Module===','📈Regression','🎏Classification','🌗Clustering','🔥Sentiment Analysis', '📖Translation' ,'📋Text Summarizer'])
    return nav
