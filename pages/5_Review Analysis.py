'''
Created by : 
Motaz Saidani (Github : Motaz-Saidani)
'''
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import country_converter as coco
from bertopic import BERTopic
from transformers import AutoModelForSequenceClassification
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

def BERTopicModeling(text, n_topics=50, top_n_words=10):
  MODEL = 'cardiffnlp/twitter-roberta-base-sentiment' # this transformer was trained on over 58 million tweets
                                              # This might be the best transformer for our case because
                                              # it can capture the same informal style of writing in reviews

  embedding_model = AutoModelForSequenceClassification.from_pretrained(MODEL)
  umap_model = UMAP(n_neighbors=15,
            n_components=5,
            metric='cosine',
            low_memory=True)
  topic_model = BERTopic(language="english",
                embedding_model=embedding_model,
                umap_model=umap_model,
                calculate_probabilities=False,
                top_n_words=top_n_words,           # number of words to be extracted per topic
                n_gram_range=(1, 2),               # number of words in topic representation
                min_topic_size=5,                  # reviews with less than 5 words will be ignored
                nr_topics=n_topics,                # merging components into 50 topics total
                verbose=True)
  topics, _ = topic_model.fit_transform(text)
  return topic_model, topics 


st.text('')
st.title('👥Review Analysis')
st.text('')
st.markdown(':white_check_mark:Understand your customer by their reviews')
st.write('Suggested Data : Reviews , Rating (1-5) , Date of reviews')

if st.button('Get Demo Data'):
  df = pd.read_csv('./dataset/MyproteinTrustpilot.csv')
  st.dataframe(df.head(10))
  date = 'date'
  review = 'review'
  rating = 'rating'
        # Labeling the dataset
  def LabelFunc(rating):
    if rating >= 4:
      return 'Positive'
    elif rating <= 2:
      return 'Negative'
    else:
      return 'Neutral'
  df['label'] = df[rating].apply(LabelFunc)
  st.session_state['timestamps_pos'] = df[df['label']=='Positive']['date'].reset_index(drop=True)
  st.session_state['timestamps_neut'] = df[df['label']=='Neutral']['date'].reset_index(drop=True)
  st.session_state['timestamps_neg'] = df[df['label']=='Negative']['date'].reset_index(drop=True)

  print('rows size :', df.shape[0],'\ncolumns size :', df.shape[1])
  df[:3]
  #Install NLTK packages
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  nltk.download('omw-1.4')
  # ## Topic Modeling with BERTopic
  # ### Preprocessing
  stop_words = set(stopwords.words('english'))
  lemmatizer = WordNetLemmatizer()
  print('downloaded all NLTK models')
  def TextPreprocessor(text):
    clean_text = text
    #clean_text = re.sub('[^a-zA-Z]', ' ', clean_text)                          # removing numbers & punctuation
    #clean_text = str(clean_text).lower()                                       # all characters to lowercase
    clean_text = word_tokenize(clean_text)                                     # tokenizing the text
    clean_text = [word for word in clean_text if word not in stop_words]       # removing stopwords
    #clean_text = [PorterStemmer().stem(i) for i in clean_text]                 # stemming
    clean_text = [lemmatizer.lemmatize(word=w, pos='v') for w in clean_text]   # Lemmatizing
    #clean_text = [i for i in clean_text if len(i) > 2]                         # removing words with less than 3 letters
    clean_text = ' '.join(clean_text)                                          # joining the tokens back to a sequence
    return clean_text

  df['clean_review'] = df[review].apply(TextPreprocessor); df['clean_review']

  print('cleaned review')

# dividing the reviews to three categories (Positive/Neutral/Negative)
  st.session_state['positive_reviews'] = df[df['label']=='Positive']['clean_review'].reset_index(drop=True)
  st.session_state['neutral_reviews'] = df[df['label']=='Neutral']['clean_review'].reset_index(drop=True)
  st.session_state['negative_reviews'] = df[df['label']=='Negative']['clean_review'].reset_index(drop=True)

#Select sentiment 
  if 'negative_reviews' in st.session_state:
    #  print('pass')
    option_sentiment = 'Negative'

    negative_reviews = st.session_state['negative_reviews']

    # ### Topic Modeling
    # POSITIVE
    #def option_sentiment_pos(option_sentiment):
    if option_sentiment == 'Negative':
      with st.spinner('Training model...'):    
        neg_bertopic = BERTopicModeling(negative_reviews)
        neg_topic_model = neg_bertopic[0]
        neg_topics = neg_bertopic[1]
        frequency = neg_topic_model.get_topic_info(); frequency
        neg_topic_model.get_topic(0)
        #timestamps_pos = df[df['positive_reviews']['date']].reset_index(drop=True)
        topic_model_overtime_neg = neg_topic_model.topics_over_time(docs=negative_reviews, 
                                                            topics=neg_topics, 
                                                            timestamps=st.session_state['timestamps_neg'], 
                                                            global_tuning=True, 
                                                            evolution_tuning=True, 
                                                            nr_bins=50)

        topics_overtime_neg = neg_topic_model.visualize_topics_over_time(topic_model_overtime_neg, 
                                                            top_n_topics=10)
                                                          
    
        #Output for POS:
        st.title('Topic Vs Time')
        st.write(topics_overtime_neg)
        topics_distance_map_neg = neg_topic_model.visualize_topics(); topics_distance_map_neg
        st.title('Topic Distance Map')
        st.write(topics_distance_map_neg)
        topics_bar_neg = neg_topic_model.visualize_barchart(top_n_topics=20); topics_bar_neg
        st.title('Different Topics')
        st.write(topics_bar_neg)


else:
  uploaded_file = st.file_uploader("Choose a file")
  # Importing data (Data used is the one from TrustPilot)
  if uploaded_file is not None:
      # To read file as bytes:
      bytes_data = uploaded_file.getvalue()
      #st.write(bytes_data)
      # Can be used wherever a "file-like" object is accepted:
      df = pd.read_csv(uploaded_file)
      #df = pd.read_csv('https://raw.githubusercontent.com/Super-Chain/NLP-MiniProject/main/MyproteinTrustpilot.csv?token=GHSAT0AAAAAABODR2K337F4SXFRETVPHA4AYQ67QRA')
      st.dataframe(df.head(10))          # removing null values & duplicates
      example_date = 'date'
      example_review = 'review'
      example_rating = 'rating'
      date = st.text_input('Input the column name of date',example_date)
      review = st.text_input('Input the column name of review',example_review)
      rating = st.text_input('Input the column name of rating',example_rating)
      
      if st.button('Match Data') :
        df = df.dropna().drop_duplicates()
        # converting 'date' to time object
        df['date'] = pd.to_datetime(df[date])

        # displaying results
        #print('\n', df['country'].value_counts(),'\n')
        #df['country'].value_counts()[:5].plot(kind='bar')
        # Retaining only UK observations
        ###########Country########
        with st.spinner('Training...'):
          #df = df[df['country']==country].reset_index(drop=True)

          # Labeling the dataset
          def LabelFunc(rating):
            if rating >= 4:
              return 'Positive'
            elif rating <= 2:
              return 'Negative'
            else:
              return 'Neutral'
          df['label'] = df[rating].apply(LabelFunc)
          st.session_state['timestamps_pos'] = df[df['label']=='Positive']['date'].reset_index(drop=True)
          st.session_state['timestamps_neut'] = df[df['label']=='Neutral']['date'].reset_index(drop=True)
          st.session_state['timestamps_neg'] = df[df['label']=='Negative']['date'].reset_index(drop=True)

          print('rows size :', df.shape[0],'\ncolumns size :', df.shape[1])
          df[:3]
          #Install NLTK packages
          nltk.download('punkt')
          nltk.download('stopwords')
          nltk.download('wordnet')
          nltk.download('omw-1.4')
          # ## Topic Modeling with BERTopic
          # ### Preprocessing
          stop_words = set(stopwords.words('english'))
          lemmatizer = WordNetLemmatizer()
          print('downloaded all NLTK models')
          def TextPreprocessor(text):
            clean_text = text
            #clean_text = re.sub('[^a-zA-Z]', ' ', clean_text)                          # removing numbers & punctuation
            #clean_text = str(clean_text).lower()                                       # all characters to lowercase
            clean_text = word_tokenize(clean_text)                                     # tokenizing the text
            clean_text = [word for word in clean_text if word not in stop_words]       # removing stopwords
            #clean_text = [PorterStemmer().stem(i) for i in clean_text]                 # stemming
            clean_text = [lemmatizer.lemmatize(word=w, pos='v') for w in clean_text]   # Lemmatizing
            #clean_text = [i for i in clean_text if len(i) > 2]                         # removing words with less than 3 letters
            clean_text = ' '.join(clean_text)                                          # joining the tokens back to a sequence
            return clean_text

          df['clean_review'] = df[review].apply(TextPreprocessor); df['clean_review']

          print('cleaned review')

        # dividing the reviews to three categories (Positive/Neutral/Negative)
          st.session_state['positive_reviews'] = df[df['label']=='Positive']['clean_review'].reset_index(drop=True)
          st.session_state['neutral_reviews'] = df[df['label']=='Neutral']['clean_review'].reset_index(drop=True)
          st.session_state['negative_reviews'] = df[df['label']=='Negative']['clean_review'].reset_index(drop=True)

    #Select sentiment 
      if 'negative_reviews' in st.session_state:
        #  print('pass')
        option_sentiment = st.selectbox('Select based on sentiment',('Positive','Neutral','Negative'))
        if st.button('Apply'):
          positive_reviews = st.session_state['positive_reviews']
          neutral_reviews = st.session_state['neutral_reviews']
          negative_reviews = st.session_state['negative_reviews']
          # ### Topic Modeling
          # POSITIVE
          #def option_sentiment_pos(option_sentiment):
          if option_sentiment == 'Positive':
            with st.spinner('Training model...'):    
              pos_bertopic = BERTopicModeling(positive_reviews)
              pos_topic_model = pos_bertopic[0]
              pos_topics = pos_bertopic[1]
              frequency = pos_topic_model.get_topic_info(); frequency
              pos_topic_model.get_topic(0)
              #timestamps_pos = df[df['positive_reviews']['date']].reset_index(drop=True)
              topic_model_overtime_pos = pos_topic_model.topics_over_time(docs=positive_reviews, 
                                                                  topics=pos_topics, 
                                                                  timestamps=st.session_state['timestamps_pos'], 
                                                                  global_tuning=True, 
                                                                  evolution_tuning=True, 
                                                                  nr_bins=50)

              topics_overtime_pos = pos_topic_model.visualize_topics_over_time(topic_model_overtime_pos, 
                                                                  top_n_topics=10)
                                                                
          
              #Output for POS:
              p_title('Topic Vs Time')
              st.write(topics_overtime_pos)
              topics_distance_map_pos = pos_topic_model.visualize_topics(); topics_distance_map_pos
              p_title('Topic Distance Map')
              st.write(topics_distance_map_pos)
              topics_bar_pos = pos_topic_model.visualize_barchart(top_n_topics=20); topics_bar_pos
              p_title('Different Topics')
              st.write(topics_bar_pos)

            #def option_sentiment_neut(option_sentiment):
          if option_sentiment == 'Neutral' :
            print("Netural")
            with st.spinner('Training...'):
              # NEUTRAL
              neut_bertopic = BERTopicModeling(neutral_reviews)
              neut_topic_model = neut_bertopic[0]
              neut_topics = neut_bertopic[1]

              frequency = neut_topic_model.get_topic_info(); frequency
              # -1 refers to outliers

              neut_topic_model.get_topic(0)
              ##########Output of NEUT#######
                      # Output Topics over time
              #timestamps_neut = df[df['label']=='Neutral']['date'].reset_index(drop=True)
              topic_model_overtime_neut = neut_topic_model.topics_over_time(docs=neutral_reviews,
                                                                  topics=neut_topics,
                                                                  timestamps=st.session_state['timestamps_neut'], 
                                                                  global_tuning=True, 
                                                                  evolution_tuning=True, 
                                                                  nr_bins=50)

              topics_overtime_neut = neut_topic_model.visualize_topics_over_time(topic_model_overtime_neut, 
                                                                  top_n_topics=10)
              st.title('Topic Vs Time')
              st.write(topics_overtime_neut)
              topics_distance_map_neut = neut_topic_model.visualize_topics(); topics_distance_map_neut
              st.title('Topic Distance Map')
              st.write(topics_distance_map_neut)
              topics_bar_neut = neut_topic_model.visualize_barchart(top_n_topics=20); topics_bar_neut
              st.title('Different Topics')
              st.write(topics_bar_neut)

          if option_sentiment == 'Negative' :
            print("Negative")
            with st.spinner('Training') :
    # NEGATIVE
              neg_bertopic = BERTopicModeling(negative_reviews)
              neg_topic_model = neg_bertopic[0]
              neg_topics = neg_bertopic[1]
              frequency = neg_topic_model.get_topic_info(); frequency
      # -1 refers to outliers
              neg_topic_model.get_topic(1)
              #Output Topics over time
              #timestamps_neg = df[df['label']=='Negative']['date'].reset_index(drop=True)
              topic_model_overtime_neg = neg_topic_model.topics_over_time(docs=negative_reviews, 
                                                              topics=neg_topics, 
                                                              timestamps=st.session_state['timestamps_neg'], 
                                                              global_tuning=True, 
                                                              evolution_tuning=True, 
                                                              nr_bins=50)

              topics_overtime_neg = neg_topic_model.visualize_topics_over_time(topic_model_overtime_neg, 
                                                              top_n_topics=10)

      # Clicking on the topic in the legend will remove it from the graph
      # Clicking on it again will add it back
              st.write(topics_overtime_neg)
              topics_distance_map_neg = neg_topic_model.visualize_topics(); topics_distance_map_neg
              st.write(topics_distance_map_neg)
              topics_bar_neg = neg_topic_model.visualize_barchart(top_n_topics=20); topics_bar_neg
              st.write(topics_bar_neg)




