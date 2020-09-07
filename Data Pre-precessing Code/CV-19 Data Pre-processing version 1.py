#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


# In[3]:


cd ~/Desktop/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports


# In[113]:


import glob
#grap all the csv file names
# The * is not a regex, it just means "match anything"
# This matches 01-22-2020.csv, 01-23-2020.csv, etc.
list_of_dfs = []
for filename in glob.glob("*.csv"):
        list_of_dfs.append(pd.read_csv(filename))


# In[114]:


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


# In[115]:


#adjust columns orders and create new columns ready to combine
for i in range(n):
    for col in column_names:
        if col not in list_of_dfs[i]:
            list_of_dfs[i][col]=np.nan
column_name_ordered = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Latitude','Longitude','Confirmed','Deaths','Recovered','Active','Combined_Key','Incidence_Rate','Case-Fatality_Ratio']
for i in range(n):
    list_of_dfs[i]=list_of_dfs[i][column_name_ordered]
combined_df = pd.concat(list_of_dfs)
combined_df.head()


# In[116]:


#Identify Country_Region and Province_State which do not contain lattitute information and safe it as
#location_distinct_df.csv file.
combined_df[pd.isnull(combined_df['Latitude'])][["Admin2","Province_State","Country_Region"]]
location_df = combined_df[pd.isnull(combined_df['Latitude'])][["Admin2","Province_State","Country_Region"]]
location_distinct_df = location_df.drop_duplicates()


# In[118]:


#After adding the missing lattitute and Longitude information,bring it into Python and ready to update
#missing latitude and longitude columns in combined_df DataFrame.
location_update_df = pd.read_csv('C:/Users/alexl/Desktop/COVID-19-master/location.csv')


# In[120]:


location_update_df.head()


# In[121]:


#Replace Province_State column "Unknown" with "NAN" 
combined_df['Province_State'] = combined_df['Province_State'].replace('Unknown',np.nan)
# Update Missing latitude and longitude columns
for i in range(len(location_update_df)):
    latitude,longitude = location_update_df.iloc[i,3],location_update_df.iloc[i,4]
    filt = (combined_df['Province_State']==location_update_df.iloc[i,1] if pd.notnull(location_update_df.iloc[i,1]) else True) & (combined_df['Country_Region']==location_update_df.iloc[i,2]) & (combined_df['Admin2']==location_update_df.iloc[i,0] if pd.notnull(location_update_df.iloc[i,0]) else True)
    combined_df.loc[filt,'Latitude'],combined_df.loc[filt,'Longitude'] = latitude,longitude
combined_df.head()


# In[128]:


#Change date formate
combined_df['Last_Update'] = pd.to_datetime(combined_df['Last_Update']).dt.date
combined_df.head()


# In[132]:


#Fill na in confirmed, deaths,recovered and active columns and then set to int
combined_df[['Confirmed','Deaths','Recovered','Active']]=combined_df[['Confirmed','Deaths','Recovered','Active']].fillna(0)
combined_df[['Confirmed','Deaths','Recovered','Active']]=combined_df[['Confirmed','Deaths','Recovered','Active']].astype('int32')


# In[133]:


combined_df.head()


# In[134]:


#sort the data before remove duplicate rows
combined_df = combined_df.sort_values(['Country_Region','Province_State','Admin2','Last_Update'])
#remove duplicate rows
combined_df_test = combined_df.drop_duplicates(subset=['Country_Region','Last_Update','Confirmed','Deaths','Admin2','Province_State'],keep="last")


# In[136]:


combined_df_test.head()


# In[137]:


combined_df_test.to_csv('cleaned2.csv')


# In[ ]:


#=============================================================================================================================#
#Update missing Incidence_Rate and Case-Fatility_Ratio

