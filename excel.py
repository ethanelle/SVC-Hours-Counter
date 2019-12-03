import pandas as pd
import numpy as np
import re

REGEX = re.compile('[^@]+@[^@]+\.[^@]+')
TIME_REGEX = re.compile('\d+hr\s30')

class Person:
    name = ""
    email = ""
    hours = 0

people = []

df = pd.read_csv('spreadsheet.csv')

for index, row in df.iterrows():
    if type(row['Date of Event']) == str:
        if TIME_REGEX.match(row['Date of Event']):
            n = float(re.compile('\d+').match(row['Date of Event']).group()) + 0.5
            df.at[index, 'Date of Event'] = n
            # print(n)

for index, row in df.iterrows():
    if type(row['Name of Event Coordinator']) == str:
        if REGEX.match(row['Name of Event Coordinator']):
            found = False
            for person in people:
                if person.email == row['Name of Event Coordinator']:
                    time = str(row['Date of Event'])
                    if len(time) <= 0:
                        time = 0
                    person.hours += float(time)
                    found = True
                    break
            if found == False:
                p = Person()
                p.name = row['Name of Event']
                p.email = row['Name of Event Coordinator']
                time = str(row['Date of Event'])
                if len(time) <= 0:
                    time = 0
                p.hours = float(time)
                people.append(p)

pruned = []
for person in people:
    if person.hours > 0:
        pruned.append(person)

people = sorted(pruned, key=lambda x: x.hours, reverse=True)

f = open('result.txt', 'w')

f.write("--- Over 10: ---\n")

for person in people:
    if person.hours >= 10:
        s = person.name + "\t" + person.email + "\t" + str(person.hours) + "\n"
        f.write(s)

f.write("\n\n--- Over 7.5: ---\n")
for person in people:
    if person.hours >= 7.5 and person.hours < 10:
        s = person.name + "\t" + person.email + "\t" + str(person.hours) + "\n"
        f.write(s)

f.write("\n\n--- Everyone: ---\n")


for person in people:
    s = person.name + " " + str(person.hours) + "\n\n"
    f.write(s)

f.close()