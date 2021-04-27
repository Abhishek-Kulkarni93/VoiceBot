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
            time = i.getText().partition(':')[2].strip()
            print('Monday Working hours : ' + i.getText().partition(':')[2])
            doc.set({'Monday': time}, merge=True)
        if str(i.string).startswith('Tuesday'):
            time = i.getText().partition(':')[2].strip()
            print('Tuesday Working hours : ' + i.getText().partition(':')[2])
            doc.set({'Tuesday': time}, merge=True)
        if str(i.string).startswith('Wednesday'):
            time = i.getText().partition(':')[2].strip()
            print('Wednesday Working hours : ' + i.getText().partition(':')[2])
            doc.set({'Wednesday': time}, merge=True)
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

# que 7 ,8 - examination plans


def direct_links():
    page = open('fin_exam_office_webpage.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')

    primary_links = a.find_all('div', attrs={'id': 'primaer_nav_direktlinks_liste'})
    # print(primary_links)

    for i in range(len(primary_links)):
        links = primary_links[i].find('ul', attrs={'class': 'level1'}).find_all('li')

        for j in links:
            if str(j).__contains__('The Faculty'):
                print('The Faculty ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'Faculty': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)
            if str(j).__contains__('Research'):
                print('Research ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'Research': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)
            if str(j).__contains__('International'):
                print('International ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'International': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)

    secondary_links = a.find_all('div', attrs={'id': 'sekundaer_nav_links'})

    # print(a)

    for i in range(len(secondary_links)):
        # print(a[i].find('ul', attrs={'class':'nav_links_5','id':'sekundaer_nav_links_min'}))

        links = secondary_links[i].find('ul', attrs={'class': 'nav_links_5', 'id': 'sekundaer_nav_links_min'}).find_all('li')

        for j in links:
            if str(j).__contains__('About the Examination Office'):
                print('About the Examination Office ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'About the Examination Office': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)
            if str(j).__contains__('Study Regulations'):
                print('Study Regulations ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'Study Regulations': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)
            if str(j).__contains__('Examination Board'):
                print('Examination Board ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'Examination Board': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)
            if str(j).__contains__('Examination Plans'):
                print('Examination Plans ' + 'https://www.inf.ovgu.de/' + j.a['href'])
                doc.set({'Examination Plans': 'https://www.inf.ovgu.de/' + j.a['href']}, merge=True)

    #addind deadlines link
    doc.set({'Deadlines':'https://www.inf.ovgu.de/inf/en/Study/Being+a+student/Examination+Office/Examination+Plans/Deadlines.html'},merge=True)

    page.close()

direct_links()


def individual_forms():
    page = open('forms_fin.html', 'r')
    a = bs4.BeautifulSoup(page, features='lxml')

    all_links = a.find_all('div', attrs={'class': 'egotec-page_frame'})

    for sections in range(4):
        links = all_links[sections].find_all('a')
        for j in links:
            if str(j.getText()) != 'Titel':
                form_name = j.getText()
                form_link = 'https://www.inf.ovgu.de/' + j['href']
                print(form_name)
                print(form_link)
                doc.set({form_name:form_link}, merge=True)

# individual_forms()
