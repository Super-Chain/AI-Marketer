'''
Input:
A dataframe with content, ratings, company
A list of attributes eg. customer service, delivery, price

Output:
A dataframe with different scores of attributes
'''

import pandas as pd
from word_forms.word_forms import get_word_forms
import streamlit as st
from io import StringIO
import plotly.express as px
import requests
from bs4 import BeautifulSoup

def synonyms(term):
    '''
    Return the synonym of the term
    param: term(str): the term you would like to find
    return: (list): a list of synonyms
    '''
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] 



st.text('')
st.title('🏇Competitor Analysis')
st.text('')
st.markdown(':white_check_mark:Xray your competitor and their performance by user feedback')
st.write('Suggested Data : Competitor Name , Competitor Reviews, Rating(1-5)')

if st.button('Get Demo Data') :
    dataset = pd.read_csv('./dataset/reviews.csv',encoding= 'unicode_escape')
    st.write(dataset.head(10))

    # check user input
    try:
        # user-identified attributes
        #attributes = [i.strip() for i in input_sum.split(',')]
        attributes = ['service', 'shipping', 'price', 'easiness', 'variety', 'quality']

        # read data
        df = dataset.dropna(subset=['content', 'ratings'])
        df = df[['content', 'ratings', 'company']]

    except Exception as e:
        #If error
        st.write(repr(e))
        st.error('Error format. Try again!')
    with st.spinner('Training model...'):

        ### Pre-process data
        # split the customer review to a list of strings, seperated by full stops
        contents = [a for b in [i.split('.') for i in list(df.content)] for a in b]
        # store all similar words into all_words eg. all_words = [[a1, a2, a3...], [b1, b2, b3...]]
        all_words = []

        for att in attributes:

            ### Synonym Approach
            words = synonyms(att)
            # spaces are added in front and at back to prevent subword occurrence
            words = [' '+w[0] for w in words][:5]
            # add the original attribute
            words.append(' '+att+' ')
            all_words.append(words)

        #st.write("ANALZING DATA")

        ### count the no. of customer reviews
        all_stats = []
        for words in all_words: # loop through the nested list containing all the similar words
            # find all relevant reviews if any one of the words appear in the reivew
            all_companies = df[df['content'].str.contains('|'.join(words))]
            company_stats = pd.DataFrame()
            for company in set(all_companies['company']): # loop through companies

                # check if have reivews
                if len(all_companies[all_companies['company'] == company]) == 0:
                    st.error(f"{company} - {words[-1][1:-1]}: This attribute has no related reviews. Try again!")

                # filter out the company and count their rating occurrences
                stat = pd.Series(all_companies[all_companies['company'] == company]['ratings'].value_counts()).sort_index()
                print(stat)
                try:
                    # 1,2 stars as negative
                    negative = stat.loc[:2].sum()
                except: # if no negative
                    negative = 0
                try:
                    # 3, 4 stars as neutral
                    neutral = stat.loc[3:4].sum()
                except:
                    neutral = 0
                try:
                    # 5 stars as postive
                    positive = stat.loc[5].sum()
                except:
                    positive = 0
                stat = pd.Series({'negative': negative, 'neutral': neutral, 'positive': positive})
                # store as percentage
                company_stats[company] = stat / stat.sum()
            # store the series in the all_stats list
            all_stats.append(company_stats)
        # concat all series into a dataframe
        companies_stats = pd.concat(all_stats, keys=[i[-1][1:-1] for i in all_words])

        # calculate the score by using the percentage distribution and store in a dataframe (positive - negative)
        scores = pd.DataFrame()
        for att in attributes: # loop through attributes
            att_df = companies_stats.loc[att].T
            company_dict = {} # add company score to the dictionary
            for company in companies_stats.columns: # for all companies
                row = att_df.loc[company]
                att_score = row['positive'] - row['negative']
                company_dict[company] = att_score
            # add the company scores of a attribute to the dataframe
            scores[att] = pd.Series(company_dict)

        # standardize the scores for each attribute
        for col in scores.columns:
            scores[col] = (scores[col] - scores[col].mean())/scores[col].std() 
        
        # store to session state variable so everytime when loop the result is stored

        scores['company'] = list(scores.index)
        st.session_state['scores'] = scores
        st.session_state['columns'] = tuple(list(scores.columns)[:-1])
        
    if 'scores' in st.session_state:
        ### output
        st.title('Coordinates of the positioning map')
        st.dataframe(st.session_state['scores'].iloc[:,:-1])
        ## user choose x and y axis
        col_x, col_y = st.columns(2)
        with col_x:
            x_axis = st.selectbox("Choose x-axis", st.session_state['columns'])
        with col_y:
            y_axis = st.selectbox("Choose y-axis", st.session_state['columns'])            
        try:        
            # scattered plot
            st.title('Positioning Map')
            fig = px.scatter(st.session_state['scores'], x=x_axis, y=y_axis,width=800,height=800, text='company', size_max=60)
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=False)

        except:
            pass
    

else:
####################################################################################################################

    with st.form("Input your data: "):
        
        #Example Input
        sum_example = 'price, delivery, service, variety'
        #User Input
        input_sum =st.text_input("Use the example below or input the aspects in English (Better to use the words appear in the reviews)", value=sum_example)
        #Map the columns 
        contents_example = 'content'
        content = st.text_input('Please input the column name of Review',contents_example)

        ratings_example ='ratings'
        ratings = st.text_input('Please input the column name of Rating',ratings_example)

        company_example ='company'
        company = st.text_input('Please input the column name of Company',company_example)

        # User upload file
        uploaded_file_competitor = st.file_uploader("Choose a file (Header should include title, content and ratings)")

        if uploaded_file_competitor is not None:
            # To read file as bytes:
            bytes_data = uploaded_file_competitor.getvalue()
            #st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file_competitor.getvalue().decode("utf-8"))
            #st.write(stringio)

            # To read file as string:
            string_data = stringio.read()

            # Can be used wherever a "file-like" object is accepted:
            dataset = pd.read_csv(uploaded_file_competitor,encoding= 'unicode_escape')
            st.write(dataset.head(10))
        
        # When clicked analyze button
        submitted = st.form_submit_button("Analyze")


        
        if submitted:
        #Change Button Color by Markdown
            st.markdown(f""" <style>.css-1cpxqw2 {{backgound-color: rgb(78, 116, 255); !important}}</style> """, unsafe_allow_html=True)
            # check user input
            try :
                # user-identified attributes
                attributes = [i.strip() for i in input_sum.split(',')]
                #attributes = ['service', 'shipping', 'price', 'easiness', 'variety', 'quality']

                # read data
                df = dataset.dropna(subset=[content, ratings])
                df = df[[content, ratings, company]]
                df = df.rename(columns={content:"content",ratings:"ratings",company:"company"})
                print(df)

            except Exception as e:
                #If error
                st.write(repr(e))
                st.error('Error format. Try again!')
            with st.spinner('Training model...'):

                ### Pre-process data
                # split the customer review to a list of strings, seperated by full stops
                contents = [a for b in [i.split('.') for i in list(df.content)] for a in b]

                #st.write("TRAINING MODEL")

                ### train Top2Vec model 
                model = Top2Vec(documents=contents, speed='learn', embedding_model='doc2vec')
                # word similarity threshold
                threshold = 0.5
                # store all similar words into all_words eg. all_words = [[a1, a2, a3...], [b1, b2, b3...]]
                all_words = []

                #st.write("FINISHED TRAINING MODEL")

                ### check if all input attributes have been trained by the model
                for ind, att in enumerate(attributes):
                    try:
                        model.similar_words(keywords=[att], keywords_neg=[], num_words=1)
                    # if not trained
                    except ValueError as e:
                        st.write(att, 'has not been trained')      
                        # find other word forms of this word
                        forms = get_word_forms(att)
                        forms = list(set([i for j in list(forms.values()) for i in j]) - {att})
                        for form in forms:
                            st.write("Trying " + form)
                            try:
                                # and try these words
                                model.similar_words(keywords=[form], keywords_neg=[], num_words=1)
                                # if trained, change to this word
                                attributes[ind] = form
                                st.write(f"{att} has not been trained. It has been changed to {form}")
                                break
                            except ValueError as e:
                                pass
                            # when all fail
                            st.error(f"{att} has not been trained. No similar words have been found. Try to change your input!")


                #st.write("FINDING SIMILAR KEYWORDS")

                for att in attributes:
                    words, word_scores = model.similar_words(keywords=[att], keywords_neg=[], num_words=20)
                    # spaces are added in front and at back to prevent subword occurrence
                    words = [' '+w[0]+' ' for w in list(zip(words, word_scores)) if w[1] > threshold]
                    # add the original attribute
                    words.append(' '+att+' ')
                    all_words.append(words)

                #st.write("ANALZING DATA")

                ### count the no. of customer reviews
                all_stats = []
                for words in all_words: # loop through the nested list containing all the similar words
                    # find all relevant reviews if any one of the words appear in the reivew
                    all_companies = df[df['content'].str.contains('|'.join(words))]
                    company_stats = pd.DataFrame()
                    for company in set(all_companies['company']): # loop through companies

                        # check if have reivews
                        if len(all_companies[all_companies['company'] == company]) == 0:
                            st.error(f"{company} - {words[-1][1:-1]}: This attribute has no related reviews. Try again!")

                        # filter out the company and count their rating occurrences
                        stat = pd.Series(all_companies[all_companies['company'] == company]['ratings'].value_counts()).sort_index()
                        # 1,2 stars as negative
                        negative = stat.loc[:2].sum()
                        # 3, 4 stars as neutral
                        neutral = stat.loc[3:4].sum()
                        # 5 stars as postive
                        positive = stat.loc[5].sum()
                        stat = pd.Series({'negative': negative, 'neutral': neutral, 'positive': positive})
                        # store as percentage
                        company_stats[company] = stat / stat.sum()
                    # store the series in the all_stats list
                    all_stats.append(company_stats)
                # concat all series into a dataframe
                companies_stats = pd.concat(all_stats, keys=[i[-1][1:-1] for i in all_words])

                # calculate the score by using the percentage distribution and store in a dataframe (positive - negative)
                scores = pd.DataFrame()
                for att in attributes: # loop through attributes
                    att_df = companies_stats.loc[att].T
                    company_dict = {} # add company score to the dictionary
                    for company in companies_stats.columns: # for all companies
                        row = att_df.loc[company]
                        att_score = row['positive'] - row['negative']
                        company_dict[company] = att_score
                    # add the company scores of a attribute to the dataframe
                    scores[att] = pd.Series(company_dict)

                # standardize the scores for each attribute
                for col in scores.columns:
                    scores[col] = (scores[col] - scores[col].mean())/scores[col].std() 
                
                # store to session state variable so everytime when loop the result is stored

                scores[company] = list(scores.index)
                st.session_state['scores'] = scores
                st.session_state['columns'] = tuple(list(scores.columns)[:-1])
                
    if 'scores' in st.session_state:
        ### output
        st.title('Coordinates of the positioning map')
        st.dataframe(st.session_state['scores'].iloc[:,:-1])
        ## user choose x and y axis
        col_x, col_y = st.columns(2)
        with col_x:
            x_axis = st.selectbox("Choose x-axis", st.session_state['columns'])
        with col_y:
            y_axis = st.selectbox("Choose y-axis", st.session_state['columns'])            
        try:        
            # scattered plot
            st.title('Positioning Map')
            fig = px.scatter(st.session_state['scores'], x=x_axis, y=y_axis,width=800,height=800, text='company', size_max=60)
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=False)
#                @st.cache
#                def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
#                     return df.to_csv().encode('utf-8')

#                csv = convert_df(st.session_state['scores'])

#                st.download_button(
#                     label="Download data as CSV",
#                     data=csv,
#                     file_name='competitor.csv',
#                     mime='text/csv',
#                 )
        except:
            pass
        
