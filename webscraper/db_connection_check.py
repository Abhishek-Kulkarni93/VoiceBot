import mysql.connector
from mysql.connector.constants import ClientFlag

config = {'user': 'root',
          'password': 'voiceBot',
          'host': '34.123.44.0',
          'database': 'fin_examination_office',
          'client_flags': [ClientFlag.SSL],
          'ssl_ca': 'ssl_cert/server-ca.pem',
          'ssl_cert': 'ssl_cert/client-cert.pem',
          'ssl_key': 'ssl_cert/client-key.pem'}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

'''
To insert a record in table:
sql_statement = "insert into fin_exam_office values ('office_email', '{}')".format(email)
cursor.execute(sql_statement)
connection.commit()
'''


cursor.execute('select * from fin_exam_office')
print(cursor.fetchall())
connection.close()