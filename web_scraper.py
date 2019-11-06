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
    """    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
    

def extract_data(soup,output_dictionary):
    """
    Function to get the relevant data and return them in a dictionary.
    """    
    
    unstructured_data = soup.find_all("div", class_="trn-defstat__value")
    for i in range(len(unstructured_data)):
        try:
            output_dictionary[(unstructured_data[i+len(output_dictionary)]['data-stat'])] = unstructured_data[i].string[1:-1].replace(',','')
        except:
            print(str([i]) + ' could not be printed')
    
    return output_dictionary


def create_table(input_dictionary,dictionary_name):
    """
    Function to create sqlite database.
    """
    
    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in input_dictionary.keys())
    sql_input = "CREATE TABLE IF NOT EXISTS %s ( %s ) ;" % (dictionary_name, columns)
    c.execute(sql_input)
    return sql_input
#    return sql_input
    
    
def dynamic_data_entry(input_dictionary,dictionary_name):
    """
    Function to add data to database.
    """
    
    
    c.execute("INSERT INTO %s ( %s ) ",(dictionary_name,a,b,d))
    conn.commit()


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



















