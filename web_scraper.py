"""
Web scraper for r6tracker
Functions:
    - get_webpage_data: function to get the webpage data
    - extract_data: function to get relevant data and place it in a dictionary
    - create_table: function to create sql database structure
"""


import requests
import urllib.request
import datetime
from bs4 import BeautifulSoup
import sqlite3






def get_webpage_data(url):
    """
    Function to get data from a webpage and returns a soup object containing the html data.
    
    Input:
        - url: string with the full webpage address
        
    Output:
        - soup: structured text of the webpage
    """    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
    

def extract_data(soup,output_dictionary):
    """
    Function to get the relevant data and return them in a dictionary.
    
    Inputs:
        - soup: object with webpage data
        - output_dictionary: dictionary with name, platform and date to be filled with relevant data
    
    Output:
        - output_dictionary: dictionary filled with data
    """    
    
    unstructured_data = soup.find_all("div", class_="trn-defstat__value")
    original_length = len(output_dictionary)
    for i in range(len(unstructured_data)):
        try:
            output_dictionary[(unstructured_data[i+original_length]['data-stat'])] = unstructured_data[i+original_length].string[1:-1].replace(',','')
        except:
            print(str([i]) + ' could not be printed')
    
    return output_dictionary


def create_table(input_dictionary,dictionary_name):
    """
    Function to create sqlite database.
    
    Inputs:
        - input_dictionary: dictionary containing the data written to the sql database.
                            The keys become the names of the table columns in the table.
        - dictinary_name: string with the name of the dicionary for the sql table.
        
    Output: string with the sql command to create a new table in the database.
    
    
    """
    
    list_keys = list(input_dictionary.keys())
    list_values = list(input_dictionary.values())
    sql_input = "CREATE TABLE IF NOT EXISTS %s (" % (dictionary_name)
    
    for i in range(0,len(input_dictionary)):
        current_key = list_keys[i]
        try:
            current_value = float(list_values[i])
            print(list_values[i])
            print(current_value)
            sql_input = sql_input + current_key + (' REAL, ')
        except:
            sql_input = sql_input + current_key  + (' TEXT, ')
            
    sql_input = sql_input[:-2] + ')'
        
    return sql_input
    
    
def dynamic_data_entry(input_dictionary,dictionary_name):
    """
    Function to add data to database.
    """
    
    list_keys = list(input_dictionary.keys())
    list_values = list(input_dictionary.values())
    sql_input = "INSERT INTO %s (" % (dictionary_name)

    
    
    
#    sql_input = "INSERT INTO %s ( %s ) VALUES ( %s ) ;" % (dictionary_name,columns_keys,columns_values)
    c.execute(sql_input)
    c.commit()
    return sql_input




# get the date when the data is collected from the webpage
current_date = datetime.datetime.now()
current_date = current_date.strftime('%Y-%m-%d')

url = 'https://r6.tracker.network/profile/pc/mazamii' 
url_pieces = url.split('/')
soup = get_webpage_data(url)

dictionary_with_data = {'Name': url_pieces[-1], 'Platform': url_pieces[-2], 'Date': current_date}
dictionary_with_data = extract_data(soup,dictionary_with_data)





conn = sqlite3.connect('Rainbow_Six_Siege_Stats_Database.db')
c = conn.cursor()
taq = create_table(dictionary_with_data,'Rainbow_Six_Siege_Stats_Database')
#temp = dynamic_data_entry(dictionary_with_data,'Rainbow_Six_Siege_Stats_Database')
c.close()






























