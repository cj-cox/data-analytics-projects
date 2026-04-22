#!/usr/bin/env python
# coding: utf-8

# # **EDA** Superstore Sales Dataset 
# 
# ## Workflow
# 1. Load dataset into Python using Jupyter Notebook
#     - Allows interactive programming, seeing the results of input commands immediately
# 2. Perform data cleaning and exploration
# 3. Create a few simple visualizations for initial analysis prior to loading into Tableau for full analysis

# In[1]:


# Loading necessary libraries for cleaning and analysis

import numpy as np  # Fundamental for numerical operations
import pandas as pd  # Essential for manipulating and analyzing large dataframes
import matplotlib.pyplot as plt  # Allows creation of data visualizations in Python
import seaborn as sns  # Allows creation of data visualizations in Python as well, usually requiring less code


df = pd.read_csv("datasets/train.csv", index_col=[0])  # Laoding dataset from the downloaded csv file

print(df.head())  # Taking advantage of Jupyter Notebooks REPL(Read Evalute Print Loop) functionality for an overview of the data


# ## Observations
# 1. What information is included in this dataset?
#     - Unique identifiers for orders placed by each customer
#     - Columns for both the date of the order and the date the order was shipped
#     - How the order was shipped
#     - Unique identifier for each customer
#     - Each customer's name
#     - Column representing various customer types
#     - Geographic information for each order
#     - Regional information for each order
#     - Unique identifiers for each product ordered
#     - Data for the name of the ordered product, what type of product it is, and what department of the store it belongs to
#     - Total amount paid for the ordered product
# 3. What information needs to be checked for formatting errors or other concerns?
#     - The **Order Date** and **Ship Date** columns are not formatted for the US
#       * These columns currently display the date with the day first, followed by the month, then by the year
#         * This will pose a problem when attempting to perform analysis, the dates will need to be converted to month/day/year instead
# 
# ## Checking for missing values and datatype issues 
# Calling for a ```DataFrame``` of all columns, showing their name, count of non-missing values, and datatype.

# In[2]:


print(df.info())  # Lists how the information in each column is currently formatted


# ## Obersvations
# - Both **Order Date** and **Ship Date** are not currently formatted as dates, as previously assumed
# - There are 11 rows of orders that do not include the postal code. This is found by observing the Non-Null Count. Since the postal code is not needed for sales analysis these NaN values will be ignored for now and removed later in my workflow 
# 
# ## Change date format
# Converting **Order Date** to format that will be recognized as date and time when performing analysis
# - I am not converting the **Ship Date** column, as this data is not necessary for performing my sales analysis and will be removed from the dataset prior to export

# In[3]:


df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)  # Tells Python data in this column should be recognized as a date and time value formatted with the day preceeding the month

print(df.dtypes)  # Verifying command was successful


# ## Identifying unnecessary columns
# 1. **Customer Name** is not needed for sales analysis and also poses a potential PII concern and will therefore be removed
# 2. I have previously determined the **Postal Code** column will be removed
# 3. I have already determined **Postal Code** and **Ship Date** will be removed
# 4. **Ship Mode** will also not be necessary for sales analysis and will therefore be removed
# 
# ## Removing unnecessary columns
# Executing command to remove all columns I have determined to be unecessary or potentially harmful to analysis

# In[4]:


df.drop(['Customer Name', 'Postal Code', 'Ship Date', 'Ship Mode'], axis=1, inplace=True)  # Removing the listed columns from the dataset

print(df.head())  # Verifying command was successful


# ## Checking for and removing duplicates
# The following commands first check for the total number of duplicate rows. The second command will remove those duplicates

# In[5]:


print(df.duplicated().sum())  # Finds rows where each column contains a duplicate entry of another column


# In[6]:


df.drop_duplicates(keep='first', inplace=True)  # Removes all duplicate rows, leaving the first occurance of the row


# ## Verifying no negative **Sales** values
# This step will identify if any orders may have been returns.

# In[7]:


print((df['Sales'] < 0).sum())  # Locates any values within the Sales column that are less than 0 and returns the total found


# ## Removing any potential leading/trailing whitespace from ```str``` values
# Utilizing regular expressions to remove any unseen spaces preceeding or following any text within the dataframe. These unseen spaces can negatively impact analysis if not found and removed.

# In[8]:


df = df.replace(r'^ +| +$', r'', regex=True)  # Replaces any empty space preceding or trailing text with nothing, thus removing the empty spaces


# ## Quick exploration
# Now that the data has been cleaned I will quickly explore and visualize what the data is telling us, prior to completing full analysis in Tableau.

# In[9]:


print(df.describe())  # Quick statistical summary of the data


# In[10]:


print(df['Region'].value_counts())  # Quick summary of sales by region


# In[11]:


print(df['Category'].value_counts())  # Quick summary of sales by category


# In[12]:


print(df['Segment'].value_counts())  # Quick summary of sales by customer segment


# ## Observations
# - Sales have generally increased over time
#   * 2015 has the lowest sales and 2018 has the highest sales
# - The West region has the highest volume of orders
# - Office Supplies has the hightest volume of orders
# - Consumers have placed the most orders
# 
# ## Quick visualizations
# Creating some quick visualizations to further display my findings.
# 
# ## Sales Over Time
# Line graph to further show an increase in sales as time has passed.

# In[13]:


df_monthly = df.resample('MS', on='Order Date').sum()  # Aggregates sales by month for easier readability

sns.lineplot(x=df_monthly.index, y='Sales', data=df_monthly)
plt.title('Sales Over Time')
plt.show()


# ## Orders by Region
# Bar graph to further show the region with the highest number of orders.

# In[14]:


sns.countplot(x='Region', data=df)
plt.title('Orders by Region')
plt.xlabel('Region')
plt.ylabel('Number of Orders')
plt.show()


# ## Orders by Category
# Bar graph to further show the category with the highest number of orders.

# In[15]:


sns.countplot(x='Category', data=df)
plt.title('Orders by Category')
plt.xlabel('Category')
plt.ylabel('Number of Orders')
plt.show()


# ## Orders by Segment
# Bar graph to further show the segment with the highest number of orders.

# In[16]:


sns.countplot(x='Segment', data=df)
plt.title('Orders by Segment')
plt.xlabel('Segment')
plt.ylabel('Number of Orders')
plt.show()


# ## Exporting clean data to new *csv*

# In[17]:


# Saving cleaned data to a new csv file for further analysis in Tableau

try:
    df.to_csv('datasets/train_cleaned.csv')
except FileNotFoundError:
    print("The path does not exist.")
except PermissionError:
    print("Permission denied for the file.")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    print("File saved successfully.")

