import sys
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

command = ''

while True:
    command = str(input())

    if command == 'exit':
        exit(0)

    result = cursor.execute(command)
    for row in result:
        print(row)

connection.close()