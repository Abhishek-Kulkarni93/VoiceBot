import bs4
import requests
import mysql.connector
import os
from mysql.connector.constants import ClientFlag
# mysql-connector>=8.0.22
# beautifulsoup4>= 4.9.3


#get the HTMl of a webpage
url = 'https://www.inf.ovgu.de/inf/en/pamt-p-4702.html'
page = requests.get(url)
with open('fin_exam_office_webpage.html','w') as f:
    f.write(page.text)

config = {'user': 'root',
          'password': 'voiceBot',
          'host': '34.123.44.0',
          'database': 'fin_examination_office'}

# 'client_flags': [ClientFlag.SSL],
# 'ssl_ca': 'ssl_cert/server-ca.pem',
# 'ssl_cert': 'ssl_cert/client-cert.pem',
# 'ssl_key': 'ssl_cert/client-key.pem'

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

cursor.execute('truncate table fin_exam_office')
print('Table fin_exam_office has been truncated !')
print('-------------------------------------------')

# # print(cursor.execute('use fin_examination_office'))
#
# # cursor.execute('create table fin_exam_office(question varchar(50), answer varchar(500))')
# # connection.commit()
#
# cursor.execute("insert into fin_exam_office values('aa','11')")
#
# connection.commit()
#
#
# cursor.execute('SELECT * FROM fin_exam_office;')
# result = cursor.fetchall()
# print(result)
# connection.close()

# question 1 : office hours
def get_office_hours():
    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')
    # print(len(a.find_all('p')))
    for i in a.find_all('p'):
        if str(i.string).startswith('Monday'):
            print(i.getText())
            sql_statement = "insert into fin_exam_office values ('monday_office_hours', '{}')".format(str(i.getText()))
            cursor.execute(sql_statement)
            connection.commit()
        if str(i.string).startswith('Tuesday'):
            print(i.getText())
            sql_statement = "insert into fin_exam_office values ('tuesday_office_hours', '{}')".format(str(i.getText()))
            cursor.execute(sql_statement)
            connection.commit()
        if str(i.string).startswith('Wednesday'):
            print(i.getText())
            sql_statement = "insert into fin_exam_office values ('wednesday_office_hours', '{}')".format(
                str(i.getText()))
            cursor.execute(sql_statement)
            connection.commit()
    page.close()


get_office_hours()


# question 2: personal consultation
def personal_consultation():
    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')
    for i in a.find_all('p'):
        if str(i.getText()).startswith('Personal consultation'):
            print(i.getText())
            sql_statement = "insert into fin_exam_office values ('personal_consultation', '{}')".format(
                str(i.getText()))
            # print(sql_statement)
            cursor.execute(sql_statement)
            connection.commit()

    page.close()


personal_consultation()


# question 3,4,5
# FIN exam office location , email ID, telephone, fax number

def fin_exam_office_contact():
    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')

    a = a.find_all('div', attrs={'class': 'secondary_content_news_box'})

    for i in range(len(a)):

        # prints the address
        if a[i].find('div', attrs={'class': 'adressfeld'}):
            print('Address of examination office is: ' + a[i].find('div', attrs={'class': 'adressfeld'}).text.strip())
            address = 'Address of examination office is: ' + a[i].find('div',
                                                                       attrs={'class': 'adressfeld'}).text.strip()
            sql_statement = "insert into fin_exam_office values ('office_address', '{}')".format(address)
            # print(sql_statement)
            cursor.execute(sql_statement)
            connection.commit()

        # prints email ID
        if a[i].find('p', attrs={'class': 'box_mailadresse'}):
            print(
                'Email ID of examination office is ' + a[i].find('p', attrs={'class': 'box_mailadresse'}).text.strip())
            email = 'Email ID of examination office is ' + a[i].find('p',
                                                                     attrs={'class': 'box_mailadresse'}).text.strip()
            sql_statement = "insert into fin_exam_office values ('office_email', '{}')".format(email)
            # print(sql_statement)
            cursor.execute(sql_statement)
            connection.commit()

        numbers = a[i].find_all('p')
        for i in numbers:

            # prints tel number
            if i.getText().startswith('Tel'):
                print('Telephone number is ' + i.getText().strip('Tel. : '))
                tel = 'Telephone number is ' + i.getText().strip('Tel. : ')
                sql_statement = "insert into fin_exam_office values ('office_tel_no', '{}')".format(tel)
                # print(sql_statement)
                cursor.execute(sql_statement)
                connection.commit()

            # prints fax number
            if i.getText().startswith('Fax'):
                print('Fax number is ' + i.getText().strip('Fax: '))
                fax = 'Fax number is ' + i.getText().strip('Fax: ')
                sql_statement = "insert into fin_exam_office values ('office_fax_no', '{}')".format(fax)
                # print(sql_statement)
                cursor.execute(sql_statement)
                connection.commit()

    page.close()


fin_exam_office_contact()

print('---------------------------------------------------------')
print('Here is the latest data added in the table . Please check!')
print('---------------------------------------------------------')

cursor.execute('select * from fin_exam_office')
result = cursor.fetchall()
print(result)
connection.close()
