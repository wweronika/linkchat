import sys
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

arguments = sys.argv[1:]

for argument in arguments:
    file = open(argument, "r")
    cursor.execute(file.read())

connection.commit()
connection.close()