import streamlit as st
import requests
import time
import json
import pandas as pd
from pycaret.arules import *
from io import StringIO
from pycaret.datasets import get_data

st.text('')
st.title('💰Cart Analysis')
st.text('')
st.markdown(':white_check_mark:Find out the correlation of different products to set product combination')
st.text('Suggested Data : Invoice No (Unique Identifier of each order ) , Product Name (Product Description)')
if st.button("Get Demo Data") :
    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv('./dataset/rfm.csv')
    #check the input of data
    st.dataframe(data.head(10))
    with st.spinner('Training Model'):
        s = setup(data=data,transaction_id = 'InvoiceNo',item_id = 'Description', ignore_items = 'POSTAGE')
        try:
            model = create_model()
            if not model.empty:
                model['antecedents'] = [' + '.join(list(i)) for i in list(model['antecedents'])]
                model['consequents'] = [' + '.join(list(i)) for i in list(model['consequents'])]
            else:
                st.write("No relationship could be found in the cart")
            model = model[['antecedents', 'consequents', 'lift']]
            model = model.sort_values(by='lift', ascending=False)
            
        # if user input cannot be found in the data
        except KeyError as e:
            print(repr(e))
            st.error("Wrong user input! Could not find in the data")

    # output
    try:
        #st.write('[Lift ratio example: If 50% of people who buy A, B will buy C, and in general 25% of people will buy C, the lift ratio will be 50%/25% = 2.\n The larger the ratio, the relationship of A, B leading to C is more significant.]')
        model = model.rename(columns={"antecedents":"Cart set (When customer bought...)","consequents":"Predicted Set (they will also buy...)","lift":"When customer buying the Cart set, the possibility of buying the Predicted set is increased ..."})
        st.title('Result')
        st.dataframe(model,width=2000)

    except:
        pass


else:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #st.write(bytes_data)

        # To convert to a string based IO:
        #stringio = StringIO(uploaded_fil.getvalue().decode("utf-8"))
        #st.write(stringio)

        # To read file as string:
        #string_data = stringio.read()

        # Can be used wherever a "file-like" object is accepted:
        data = pd.read_csv(uploaded_file)


        #check the input of data
        st.dataframe(data.head(10))
        #Let user input the name of transaction_id & Description

        example_InvoiceNo = 'InvoiceNo'
        example_Description = 'Description'
        example_ignore_items = 'POSTAGE'
        InvoiceNo = st.text_input('Input the Invoice ID', example_InvoiceNo)
        Description = st.text_input('Input the items ID',example_Description)
        ignore_items = st.text_input('Input the ignore items (Seperated by comma) (Optional)',example_ignore_items)
        ignore_items = [i.strip() for i in ignore_items.split(',')]
        ignore_items  = [i for i in ignore_items if i != '']

        
        if st.button('Submit') :
            with st.spinner('Training Model'):
                s = setup(data=data,transaction_id = InvoiceNo,item_id = Description, ignore_items = ignore_items)
                try:
                    model = create_model()
                    if not model.empty:
                        model['antecedents'] = [' + '.join(list(i)) for i in list(model['antecedents'])]
                        model['consequents'] = [' + '.join(list(i)) for i in list(model['consequents'])]
                    else:
                        st.write("No relationship could be found in the cart")
                    model = model[['antecedents', 'consequents', 'lift']]
                    model = model.sort_values(by='lift', ascending=False)
                    
                # if user input cannot be found in the data
                except KeyError as e:
                    print(repr(e))
                    st.error("Wrong user input! Could not find in the data")

            # output
            try:
                #st.write('[Lift ratio example: If 50% of people who buy A, B will buy C, and in general 25% of people will buy C, the lift ratio will be 50%/25% = 2.\n The larger the ratio, the relationship of A, B leading to C is more significant.]')
                model = model.rename(columns={"antecedents":"Cart set (When customer bought...)","consequents":"Predicted Set (they will also buy...)","lift":"When customer buying the Cart set, the possibility of buying the Predicted set is increased ..."})
                st.title('Result')
                st.dataframe(model)

                @st.cache
                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')

                csv = convert_df(model)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='cart.csv',
                    mime='text/csv',
                )

            except:
                pass

