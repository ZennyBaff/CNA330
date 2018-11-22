#Runs a script that provides importing the sheet "Figure2.3" into a variable, takes the sheet "Figure2.2" and lists out specific columns and makes a bar graph, and creates a table for this information (but exporting this information is under construction).
#ijhardgrave@student.rtc.edu
#Ian Hardgrave CNA 330 Fall 2018

#https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.plot.bar.html
#https://pandas.pydata.org/pandas-docs/stable/10min.html#viewing-data
#https://stackoverflow.com/questions/28774960/how-to-get-read-excel-data-into-an-array-with-python
#https://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats/34658667
#https://www.youtube.com/watch?v=xtgEh48ipAs
#https://pythonspot.com/matplotlib-bar-chart/
#https://www.youtube.com/watch?v=LaCjP0uQxzc

import os
import csv
import shutil
import xlrd
import xlwt
import requests
import mysql.connector
import matplotlib.pyplot as plt; plt.rcdefaults()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Download_File():
    #Downloads the XLS spreadsheet from AWS.
    url = 'https://s3.amazonaws.com/happiness-report/2018/WHR2018Chapter2OnlineData.xls'
    r = requests.get(url, allow_redirects=True)
    open('WHR2018Chapter2OnlineData.xls', 'wb').write(r.content)


def Connect_to_sql():
    # connects to the PHPMyAdmin database.
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cna330',
                                    buffered = True)
    return conn

def Create_Table(conn):
    #Creates a table for the sheet "Figure2.3".
    cursor= conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS world_happiness_report (Country TEXT, Changes_in_happiness_scores TEXT, Whisker_high TEXT, Whisker_low TEXT);")

def Import_Figure23():
    #Reads Columns A-D on the "Figure2.3" tab of "WHR2018Chapter2OnlineData.xls", and imports the data into a "Page_3" variable. This can also be exported into a excel spreadsheet to demonstrate the import worked.

    Page_3 =(pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.3', index_col=None,  na_values=['NA'], usecols= "A,B,C,D"))
    Page_3.to_excel('Imported.xls', sheet_name='Sheet1')
    print("Proof of Import from Figure2.3:")
    print(Page_3)
    Import_Other = Page_3
    return Import_Other


#UDNER CONSTRUCTION
#def Import_CA():
#    Page_CA = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.3', index_col=None, na_values=['NA'], usecols="A"))
#    CA = Page_CA
#    return CA
#def Import_CB():
#    Page_CB = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.3', index_col=None, na_values=['NA'],usecols="B"))
#    CB = Page_CB
#    return CB
#def Import_CC():
#    Page_CC = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.3', index_col=None, na_values=['NA'],usecols="C"))
#    CC = Page_CC
#   return CC
#def Import_CD():
#    Page_CD = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.3', index_col=None, na_values=['NA'],usecols="D"))
#    CD = Page_CD
#    return CD




def List_Bar_Creation():
    #Creating the lists that are read off of the Excel spreadsheet.
    Page_2_A = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.2', index_col=None,  na_values=['NA'], usecols= "A"))
    Page_2_B = (pd.read_excel('WHR2018Chapter2OnlineData.xls', 'Figure2.2', index_col=None, converters={'Happiness':float}, na_values=['NA'], usecols= "B"))
    Page_2_A_List = list(Page_2_A['Country'])
    Page_2_B_List = list(Page_2_B['Happiness score'])
    Page_2_B_List_Float = [float(i) for i in Page_2_B_List]
    Passed_List = Page_2_A_List

    #Creating the Bar Graph from the lists.
    y_pos = np.arange(len(Page_2_A_List))
    plt.bar(y_pos, Page_2_B_List_Float, align='center', alpha=0.5)
    plt.xticks(y_pos,Page_2_A_List)
    plt.ylabel('Happiness')
    plt.xlabel('Countries')
    plt.title("World Happiness Report")
    plt.show()


    return Passed_List

#UNDER CONSTRUCTION
#def Export_to_SQL(conn,Import_Other,CA,CB,CC,CD):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
#    List_A = Import_Other
#    ca = CA
#    cb = CB
#    cc = CC
#   cd = CD
#   cursor = conn.cursor()
#   try:
#        for page in List_A:
#            Country = page
#            cursor.execute("SELECT Country FROM world_happiness_report WHERE Country = '" + Country + "';")
#            Test_List = cursor.rowcount
#            if Test_List != 1:
#                Country = ca
#                Changes_in_happiness_scores = cb
#                Whisker_high = cc
#                Whisker_low = cd
#                cursor.execute(
#                    "INSERT INTO world_happiness_report(Country, Changes_in_happiness_scores, Whisker_high, Whisker_low) VALUES('" + Country + "' ,'" + Changes_in_happiness_scores + "' ,'" + Whisker_high + "' ,'" + Whisker_low + "');")
 #           else:
#                continue

 #   except:
 #       pass
 #   return


def main():
    #Main controller
    Download_File()
    conn = Connect_to_sql()
    Create_Table(conn)
    Import_Figure23()
    List_Bar_Creation()
    #CA = Import_CA()
    #CB = Import_CB()
    #CC = Import_CC()
    #CD = Import_CD()
    #Export_to_SQL(conn,Import_Other,CA,CB,CC,CD)
    conn.commit()
    conn.close()

#First Priority
if __name__ == '__main__':
    main()








#with open('WHR2018Chapter2OnlineData.xls','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
#    dr = csv.DictReader(fin) # comma is default delimiter
#    to_db = [(i['Country'], i['Changes_in_happiness_scores'], i['Whisker_high'], i['Whisker_low']) for i in dr]

#c.executemany('''INSERT INTO location (Country, Changes_in_happiness_scores, Whisker_high, Whisker_low) VALUES (%s, %s, %s, %s);''', to_db)









#bunch of crap
#__________________________________________________________
#df = pd.DataFrame.append({'Country':[Page_2_A_List], 'Happiness score':[test]})
#complete = df.plot.bar(x='Country',y='Happiness',rot=0)
#print(getdata)
