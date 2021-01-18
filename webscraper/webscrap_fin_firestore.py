import bs4
import requests
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("digengproject01-firebase-adminsdk-ci8o7-aedd3f645c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
doc = db.collection('dept').document('fin')

# to insert data as a key value
# doc.set({'question2': 'answer2'}, merge=True)

page = open('fin_exam_office_webpage.html', 'r')


# question 1 : office hours
def get_office_hours():
    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')
    # print(len(a.find_all('p')))
    for i in a.find_all('p'):
        if str(i.string).startswith('Monday'):
            print(i.getText())
            doc.set({'Monday': str(i.string)}, merge=True)
        if str(i.string).startswith('Tuesday'):
            print(i.getText())
            doc.set({'Tuesday': str(i.string)}, merge=True)
        if str(i.string).startswith('Wednesday'):
            print(i.getText())
            doc.set({'Wednesday': str(i.string)}, merge=True)
    page.close()


get_office_hours()


# question 2: personal consultation
def personal_consultation():

    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')
    for i in a.find_all('p'):
        if str(i.getText()).startswith('Personal consultation'):
            print(i.getText())
            doc.set({'Personal consultation': str(i.getText())}, merge=True)
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
            address = a[i].find('div', attrs={'class': 'adressfeld'}).text.strip()
            doc.set({'Address': address}, merge=True)

        # prints email ID
        if a[i].find('p', attrs={'class': 'box_mailadresse'}):
            print('Email ID of examination office is ' + a[i].find('p', attrs={'class': 'box_mailadresse'}).text.strip())
            email = a[i].find('p', attrs={'class': 'box_mailadresse'}).text.strip()
            doc.set({'Email ID': email}, merge=True)

        numbers = a[i].find_all('p')
        for i in numbers:

            # prints tel number
            if i.getText().startswith('Tel'):
                print('Telephone number is ' + i.getText().strip('Tel. : '))
                tel = i.getText().strip('Tel. : ')
                doc.set({'Tel No': tel}, merge=True)

            # prints fax number
            if i.getText().startswith('Fax'):
                print('Fax number is ' + i.getText().strip('Fax: '))
                fax = i.getText().strip('Fax: ')
                doc.set({'Fax No': fax}, merge=True)
    page.close()


fin_exam_office_contact()
