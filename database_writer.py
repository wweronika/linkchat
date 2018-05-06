import sys
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

arguments = sys.argv[1:]

for argument in arguments:
    file = open(argument, "r")
    file_content = file.read()
    for command in file_content.split(';'):
    	cursor.execute(command)

connection.commit()
connection.close()