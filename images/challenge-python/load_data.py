#!/usr/bin/env python
import csv
import pymysql.cursors

# Usar pymysql para fazer as operações de inserção no banco de dados

connection = pymysql.connect(host='localhost',
                             user='codetest',
                             password='swordfish',
                             database='codetest',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


sql_insert_country = "INSERT INTO Country (name) VALUES (%s)"
sql_insert_county = "INSERT INTO County (name,country_id_fk) VALUES (%s,%s)"
sql_insert_city = "INSERT INTO City (name,county_id_fk) VALUES (%s,%s)"
sql_insert_person = "INSERT INTO Person (given_name,family_name,date_of_birth,place_of_birth,id_city_fk) VALUES (%s,%s,%s,%s,%s)"
sql_query_find_country = "SELECT id FROM Country WHERE name=%s"
sql_query_find_county = "SELECT id FROM County WHERE name=%s"
sql_query_find_city = "SELECT id FROM City WHERE name=%s"


cursor = connection.cursor()
duplicates_destroyer = set()

# Loading the countries' data
with open('../../data/places.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[2] != "country" and row[2] not in duplicates_destroyer:
            cursor.execute(sql_insert_country,(row[2]))
            duplicates_destroyer.add(row[2])

# Loading the counties' data
with open('../../data/places.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[1] != "county" and row[1] not in duplicates_destroyer:
            cursor.execute(sql_query_find_country,(row[2]))
            id_country = cursor.fetchone()
            cursor.execute(sql_insert_county,(row[1],id_country["id"]))
            duplicates_destroyer.add(row[1])

# Loading the cities' data
with open('../../data/places.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[0] != "city" and row[0] not in duplicates_destroyer:
            cursor.execute(sql_query_find_county,(row[1]))
            id_county = cursor.fetchone()
            cursor.execute(sql_insert_city,(row[0],id_county["id"]))
            duplicates_destroyer.add(row[1])            

# Loading the peoples' data
with open('../../data/people.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader: 
        person_identity = f"{row[0]}-{row[1]}-{row[2]}"
        if row[2] != "date_of_birth" and person_identity not in duplicates_destroyer:
            cursor.execute(sql_query_find_city,(row[3]))
            id_city = cursor.fetchone()
            if id_city is not None:
                cursor.execute(sql_insert_person,(row[0],row[1],row[2],row[3],id_city["id"]))
                duplicates_destroyer.add(person_identity)
            else:
                cursor.execute(sql_insert_person,(row[0],row[1],row[2],row[3],None))
                duplicates_destroyer.add(person_identity)

# Close Cursor
cursor.close()
# Commit changes
connection.commit()
# Close connection
connection.close()