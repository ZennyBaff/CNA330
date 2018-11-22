#Encryption experiments
#ijhardgrave@student.rtc.edu
#Ian Hardgrave CNA330 Fall 2018

import mysql.connector

def main():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1',
                                   database='cna330',
                                   buffered=True)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pikachu (id INT PRIMARY KEY AUTO_INCREMENT, 
        username TEXT, password TEXT, credit_card TEXT, ssn TEXT);''')

    cursor.execute('''INSERT INTO pikachu (username, password, credit_card, ssn) VALUES ('ian', SHA2('coolguy', 256), '321321-321321', '333-33-333');''')
    cursor.execute('''SELECT SHA2 ('abc', 224)''')
    result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close


if __name__ == "__main__":
    main()