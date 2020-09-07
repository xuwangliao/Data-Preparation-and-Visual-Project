#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


# In[11]:


#Make Sure Within the directory, only conain files that required update
cd ~/Desktop/COVID-19-master/archived_data/archived_daily_case_updates


# In[12]:


import glob
#grap all the csv file names
# The * is not a regex, it just means "match anything"
# This matches 01-22-2020.csv, 01-23-2020.csv, etc.
list_of_dfs = []
for filename in glob.glob("*.csv"):
        list_of_dfs.append(pd.read_csv(filename))


# In[17]:


list_of_dfs[0].head()


# In[21]:


#process column names, standardise 
n=len(list_of_dfs)
column_names = set()
for i in range(n):
    for col in list_of_dfs[i].columns:
        if col not in column_names:
            column_names.add(col)
column_names


# In[27]:


#Only certain columns are required from the files
column_names_needed = ['Province_State','Country_Region','Last_Update','Confirmed','Deaths','Recovered']


# In[28]:


update_column_names = {'Country/Region':'Country_Region','Last Update':'Last_Update','Lat':'Latitude','Long_':'Longitude','Province/State':'Province_State'}
for i in range(n):
     list_of_dfs[i].rename(columns=update_column_names, inplace=True)


# In[29]:


#adjust columns orders and create new columns ready to combine
for i in range(n):
    for col in column_names:
        if col not in list_of_dfs[i]:
            list_of_dfs[i][col]=np.nan
column_name_ordered = column_names_needed
for i in range(n):
    list_of_dfs[i]=list_of_dfs[i][column_name_ordered]
combined_df = pd.concat(list_of_dfs)
combined_df.head()


# In[ ]:


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


# In[36]:


#save combined_df DataFrame to additional_data.csv
combined_df.to_csv('~/Desktop/COVID-19-master/additional_data.csv')


# In[40]:


cd ~/Desktop/COVID-19-master


# In[44]:


modified_add_data = pd.read_csv('additional_data.csv')
modified_add_data.head()


# In[ ]:




