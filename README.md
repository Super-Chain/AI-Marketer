<img src="https://www.ai-marketer.tech/wp-content/uploads/2022/03/1-removebg-preview-e1648533328450.png">

## What is AI Marketer ?
AI Marketer is an AI-enabled marketing analytics tool that uses only a few clicks to generate insightful data.
Its for online marketer to analyze marketing data by AI & ML algorithms without a single-line of code.

By using our preset marketing task, you can get answer from unstructured data in numbers, text, tables, and charts.

## Website :
www.ai-marketer.tech 

## Update: 
Updated the pages structure of Streamlit App, based on that all the functions are being moved to /pages folder, if you are not able to replicate the pages function, please update your streamlit version

## How to start the streamlit server ?
```
streamlit run Home.py
```

## Why we create AI Marketer ?
To help marketer with no statistic / data analytics background to analyze data and handling routine marketing task in just a few clicks

## Tutorial :
https://youtube.com/channel/UCvmEPC9fUfY8L2-v9IV1i4w

## Features :

Two Parts – Tasks / Module

**Task**:
</br>→ Combine different modules to analysis and generate different graphs
</br> Example: RFM model = Classification + Regression
</br>Analyse CSV file and show the data into bar chart by analysed segment groups 


**Module**:
</br>→ independent function and method
</br>

| Tasks | Input | Result |
| :-------------: | :-------------: | ------------- |
| Price Analysis  | Product name and ```Country Code``` (Alpha-2)  | list and line chart show all the shops with name and price |
| Trend Forecast  | Product name and *```Country Code``` (Alpha-2)  | Show the prediction of the upcoming month and seasonality <br/> <br/>Line chart and list will be shown |
| RFM model  | Upload a CSV file  | Show the table after system made RFM ```Segment tags``` for each customer <br/>  <br/>Bar chart show the distribution of the RFM tags |
| Competitor Analysis  | Upload a CSV file  | Show the list of different shops with score in different aspects <br/>  <br/>Positioning Map: Select two aspects and located based on the relationship|
| Customer Segmentation  | Upload a CSV file  | Cluster to show to distribution of the customers <br/> <br/>Elbow graph show the value of k <br/> <br/>List and bar chart to show the performance of different customer groups <br/> <br/>Bottom Section: All the statistics are shown by different customer groups |
| Review Analysis  | Upload a CSV file  | Filter the keywords that the customer mentioned <br/> <br/>Line chart shows the trend of the topics over time <br/> <br/>Topic Distance Map: show the similarity of different words|
| Google adWord Generator  | Type keywords combination  | A list of showing all the words combination with ```Match_type``` |
| Cart Analysis  | Upload a CSV file  | A list of showing the relationship of different products <br/> <br/>(high probability → closer relationship) |

*Optional, Default: the whole world

>For your reference:
<br/>``` Country Code ```: https://www.iban.com/country-codes
<br/>``` Match_type ```: https://support.google.com/google-ads/answer/7478529?hl=en
<br/>``` Segment tags``` (analysed by the system):
<br/>Champions > Loyal Accounts > Potential Loyalist > New Active Account > Low Spenders > At Risk > Need Attention > About to Sleep > Lost

## Road Map 

### Integration with 3rd parties datasource by API

Our product focuses on analysing the data which users need to upload. At this moment, we are required to upload a CSV file. In order to increase the usage and convenience, we propose to integrate with 3rd parties data source , e.g : Google Sheet , Zapier for better user experience.

### Intended Outcome:
Users can get seamless integration with their datasource, instead of using manual input by uploading a local CSV file.

### Suggested Integration : 
Google Sheet , 2. Zapier , 3. Database 


## What packages do we use ?
AI Marketer is a non-profit open-source project, we build AI Marketer with a lot of help from other open source packages :

### Front end :
Streamlit (https://streamlit.io/)

### Machine Learning & AI packages :
PyCaret (https://pycaret.org/)

Transformers (https://huggingface.co/docs/transformers/index)

Bertopic (https://maartengr.github.io/BERTopic/index.html)

Prophet (https://facebook.github.io/prophet/)

SpaCy (https://spacy.io/)

Top2Vec (https://github.com/ddangelov/Top2Vec)


### Others :
Google Trans (https://github.com/ssut/py-googletrans)

Plotly (https://plotly.com/)

## Creator & Contributor 
Super Chain (Github : Super-Chain)

LAU, Ching Ming, Samuel (Github : samuellau0802)

Motaz Saidani (Github : Motaz-Saidani)

Cat YUNG (Github : catyung)

We welcome your contribution anytime

## Collabration & Contact 
Please feel free to contact us at : 
support@ai-marketer.tech

## Version 
Beta 
