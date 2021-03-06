import pandas as pd
from w3lib.html import remove_tags
import datetime as dt
import numpy as np
import re

"""
General Functions
"""

def copy_df(dataframe):
   return dataframe.copy()

def replacenan(dataframe):
    dataframe.replace('nan', np.nan, inplace=True)
    return dataframe
    
def dropNullJobs(dataframe):
    """
    Drop null values that make an online job vacancy unusable for analysis.
    The subset to drop is: ['post_date', 'job_title', 'job_description']
    """
    dataframe.dropna(subset=['post_date', 'job_title', 'job_description'], inplace=True)
    return dataframe

# remove duplicates
def removeDupes(dataframe, subset=['job_title', 'job_description', 'company', 'job_location', 'post_date']):
    dataframe = dataframe.sort_values(by='post_date').drop_duplicates(subset=subset, keep='last')
    return dataframe

def listToRows(dataframe, column):
    return dataframe.explode(column)

def removeTags(dataframe, column_list):
    for i in column_list:
        dataframe[i] = dataframe[i].apply(remove_tags)
    return dataframe

# Description
def clean_text(text):
    to_replace = ['\r', '\n', '•']
    replace = [' ', ' ', '\n']

    for idx, val in enumerate(to_replace):
        text = text.replace(val, replace[idx])
    text = text.strip()
    return text

def cleanDescription(dataframe, column_list):
    for i in column_list:
        dataframe[i] = dataframe[i].apply(lambda x: clean_text(x))
    return dataframe

def invertDate(x):
    if type(x) == float:
        return np.nan
    date = x.split('-')
    return date[2].strip()+'-'+date[1].strip()+'-'+date[0].strip()

def pipeInvertDate(dataframe, function=invertDate):
    dataframe['post_date'] = dataframe['post_date'].apply(lambda x: function(x))
    return dataframe


"""
Date Related Functions
"""
def postDatePreprocess(dataframe, sep=" "):
    dataframe['post_date'] = dataframe['post_date'].apply(lambda x: x.split(sep)[0]) 
    return dataframe

def postDateFillNa(dataframe):
    dataframe['post_date'] = dataframe['post_date'].ffill(limit=1).bfill()
    return dataframe

# convert portuguese months to numbers
def longToShortDate(x, sep):
    months = ['janeiro', 'fevereiro','março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    months_dic = {value:idx+1 for idx, value in enumerate(months)}
    date = [i.strip() for i in x.split(sep)]
    return f'{date[0]}/{months_dic[date[1]]}/{date[2]}'

# convert to datetime object
def convertToDatetime(dataframe, function, sep=' '):
    # Remove comma from date
    dataframe['post_date'] = dataframe['post_date'].apply(lambda x: str(x).lower().replace(',',''))
    dataframe['post_date'] = dataframe['post_date'].apply(lambda x: dt.datetime.strptime(function(x, sep), "%d/%m/%Y"))
    return dataframe

# Convert Scrape date to datetime
def toDatetime(dataFrame, columns_list, dayfirst=False):
    for i in columns_list:
        dataFrame[i] = pd.to_datetime(dataFrame[i], dayfirst=dayfirst)
    return dataFrame
    
def notDateToNan(x):
    if re.findall('(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](19|20)\d\d', str(x)) != []:
        return x
    else:
        return np.nan

def applyFuncToColumn(dataframe, function=notDateToNan, columns_list=['post_date']):
    for i in columns_list:
        dataframe[i] = dataframe[i].apply(lambda x: function(x))
    return dataframe


"""
OTHER FUNCTIONS
"""
def totalJobsByYearMonth(dataframe):
    dataframe['post_year'] = dataframe['post_date'].dt.year
    dataframe['post_month'] = dataframe['post_date'].dt.month
    return pd.DataFrame(dataframe.groupby(['post_year', 'post_month'])['job_title'].count()).sort_values(by=['post_year', 'post_month'], ascending=False)


def cleanCompany(dataframe):
    def capitalize(x):
        try:
            return x.capitalize()
        except AttributeError:
            return ''
    dataframe['company'] = dataframe['company'].apply(lambda x: capitalize(x))
    return dataframe