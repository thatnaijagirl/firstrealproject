#!/usr/bin/env python
# coding: utf-8

# ### Question 1A

# #### Total count of casual users and the Total count of registered users in each holiday of 2012.

# In[9]:


import pandas as pd
import sqlite3

#I have already uploaded my sql database unto jupyter notebook, so I'll just connect to it using the conn syntax

conn = sqlite3.connect('Sharing_Bike.db')


# In[10]:


#the 'pd.read_sql_query' is used here to query the database and generate a desired output for df_totalcount

df_totalcount = pd.read_sql_query(
    ''' SELECT A.dteday as date, sum(casual) as total_casual, 
    sum(registered) as total_registered 
    FROM bike as A 
    JOIN Calendar as B on A.dteday = B.dteday 
    WHERE holiday is 1 
    GROUP by A.dteday;''', conn)


# In[11]:


df_totalcount


# #### Question 1B: Average Count of Users per Hour

# In[12]:


df_perhour = pd.read_sql_query(
    '''SELECT hr as hour, 
    CAST(avg(casual) as INT) as avg_casual, 
    CAST(avg(registered) as INT) as avg_registered 
    FROM bike 
    GROUP by hr;''', conn)

#I used the CAST function to get rid of the decimals from the AVG function


# In[6]:


df_perhour


# #### Question 1C: Top 20 dates of the highest total counts of casual users 

# In[13]:


df_topdates = pd.read_sql_query(
    '''SELECT dteday as top_dates, 
    sum(casual) as total_casual 
    FROM bike
    GROUP by dteday 
    ORDER by total_casual DESC
    LIMIT 20;
    ''', conn)


# In[14]:


df_topdates


# ### QUESTION 2

# #### Question 2A: Sales Price prediction & Reasonable Choices from Dataset

# In[15]:


#we're importing the stats function to help explore the data

import numpy as np
import statsmodels.formula.api as smf
from itertools import combinations


# In[16]:


df_realstate = pd.read_csv('Realstate.csv') 
df_realstate.head(5)


# #### LIST ALL COMBINATIONS

# In[21]:


variables = ['Size','Beds','Baths','Num_Garage','Year','Highway','Aircondition','SwimmingPool']
all_combinations = []
for d in range (1, len(variables), +1):
    dr = combinations(variables, d)
    for r in dr:
        all_combinations.append(list(r))
print(all_combinations)


# In[23]:


print('The total amount of reasonable choices =',len(all_combinations))


# ### Question 2B
# 

# We need to convert the categorical values into numerical values before answering this question

# Categorical Variables = ('Highway','Aircondition','Swimmingpool')
# As we do not want to create new varibles, we would have to use the 'replace' function in pandas to assign numerical variables 
# to the categorical variables.
# We will do this by converting the boolean values 'yes' and 'no' into 1 & 0

# In[28]:


df_realstate= pd.read_csv('Realstate.csv')
df_realstate.Highway.replace(('yes','no'), (1,0), inplace=True)
df_realstate.Aircondition.replace(('yes','no'), (1,0), inplace=True)
df_realstate.SwimmingPool.replace(('yes','no'), (1,0), inplace=True)

df_realstate


# ### To do the combinations
# Linear regression is an interpretation of the correlation between the dependent and independent variable.

# In[29]:


df_realstate.corr()


# According to the table in out[29]; the Highway has the worst correlation of all the independent variables

# #### calculate the R-squared for all the variables

# In[36]:


import numpy as np
import statsmodels.api as sm
for k in all_combinations:
    if len(k)==1:
       for c in k:
           y = df_realstate['SalePrice']
           x = df_realstate[c]
           x = sm.add_constant(x)
           c_model = sm.OLS(y,x).fit()
       print('The R-squared of ', c, 'is',c_model.rsquared)


# In terms of predicting the SalePrice, "Size" has the highest R-squared value and may be said to have the greatest impact on SalePrice

# In[ ]:




