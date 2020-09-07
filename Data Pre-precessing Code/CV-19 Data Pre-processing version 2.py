#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


# In[49]:


cd ~/Desktop/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports


# In[50]:


import glob
#grap all the csv file names
# The * is not a regex, it just means "match anything"
# This matches 01-22-2020.csv, 01-23-2020.csv, etc.
list_of_dfs = []
for filename in glob.glob("*.csv"):
        list_of_dfs.append(pd.read_csv(filename))


# In[51]:


#process column names, standardise 
n=len(list_of_dfs)
column_names = set()
for i in range(n):
    for col in list_of_dfs[i].columns:
        if col not in column_names:
            column_names.add(col)
column_names

update_column_names = {'Country/Region':'Country_Region','Last Update':'Last_Update','Lat':'Latitude','Long_':'Longitude','Province/State':'Province_State'}
for i in range(n):
     list_of_dfs[i].rename(columns=update_column_names, inplace=True)


# In[54]:


#adjust columns orders and create new columns ready to stack/combine files
for i in range(n):
    for col in column_names:
        if col not in list_of_dfs[i]:
            list_of_dfs[i][col]=np.nan
column_name_ordered = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Latitude','Longitude','Confirmed','Deaths','Recovered','Active','Combined_Key','Incidence_Rate','Case-Fatality_Ratio']
for i in range(n):
    list_of_dfs[i]=list_of_dfs[i][column_name_ordered]
combined_df = pd.concat(list_of_dfs)
combined_df.head()


# In[55]:


#I realized inconsistency of country names: eg China and Mianland China, UK and United Kingdom.
#Adjust inconsistency in naming
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Mainland China','China')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('UK','United Kingdom')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Bahamas, The','Bahamas')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Gambia, The','Gambia')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Gambia, The','Gambia')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Guinea-Bissau, The','Guinea')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Iran (Islamic Republic of)','Iran')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of Ireland','Ireland')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of Ireland','Ireland')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of Korea','Korea')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of Moldova','Moldova')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of Korea','Korea')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Republic of the Congo','Congo')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Taipei and environs','Taiwan*')
combined_df['Country_Region'] = combined_df['Country_Region'].replace('Taiwan','Taiwan*')
combined_df['Province_State'] = combined_df['Province_State'].replace('Unknown',np.nan)
combined_df.head()


# In[64]:


#Obtain Combined_Key, This code takes 5mins to run
#==============================================================================================================================#
#combined_df['Combined_Key'] = combined_df[['Admin2','Province_State','Country_Region']].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)


# In[65]:


combined_df.head()


# In[66]:


#Select only Useful clolumns
combined_df=combined_df[['Combined_Key','Last_Update','Confirmed','Deaths','Recovered','Active','Incidence_Rate','Case-Fatality_Ratio']]
combined_df.head()


# In[72]:


#Making sure all rows in Combined_Key are filled.
combined_df[pd.isnull(combined_df['Combined_Key'])]


# In[73]:


#Change date formate
combined_df['Last_Update'] = pd.to_datetime(combined_df['Last_Update']).dt.date
combined_df.head()


# In[78]:


#Fill na in confirmed, deaths,recovered and active columns and then set to int
combined_df[['Confirmed','Deaths','Recovered','Active']]=combined_df[['Confirmed','Deaths','Recovered','Active']].fillna(0)
combined_df[['Confirmed','Deaths','Recovered','Active']]=combined_df[['Confirmed','Deaths','Recovered','Active']].astype('int32')
combined_df.head()


# In[79]:


#sort the data before remove duplicate rows
combined_df = combined_df.sort_values(['Combined_Key','Last_Update'])
#remove duplicate rows
combined_dictinct_df = combined_df.drop_duplicates(subset=['Combined_Key','Last_Update','Confirmed','Deaths'],keep="last")
combined_dictinct_df.head()


# In[81]:


#Create a copy of combined_distinct_df to distinct.csv file
combined_dictinct_df.to_csv('~/Desktop/COVID-19-master/distinct.csv')


# In[ ]:




