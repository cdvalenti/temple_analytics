#!/usr/bin/python

import math
import csv
j=0
k=0
g=0
people = [0]*11
col = []
test = []
totpeople = 0
#----------------------------------------------------------------------------------
#Calculate Distance Change times Number of people in each org.
#----------------------------------------------------------------------------------
with open('../data/move_effects/merck_output.csv','rb') as csvfile:
    data = csv.reader(csvfile)
    #In each row of the data file, calculate the "distance change" against the number of people in each org.
    for row in data:
	#This if statement skips the first row of the csv file, the header.
	if (k > 0) and (k < 506):
	    #test[] makes a clear test list for each new row of multiplied values
	    test=[]
	    #There are 11 organizations. at index 3-13. This for loop iterates thru them and multiplyes them against the distance change, at index 17.
	    for i in range(11):
       	        test.append(int(row[i+2]) * float(row[17]))
		people[i] = int(row[i+2]) + people[i]
		totpeople = int(row[i+2]) + totpeople
	        g = 1
	    if g == 1:
	        col.append(test)
	k=k+1
#----------------------------------------------------------------------------------
#Calculate Total change in distance for every one in each org.
#----------------------------------------------------------------------------------
Total= []
for i in range(11):
    add = 0
    for j in range(len(col)):
	add = float(col[j][i]) + add
    Total.append(add)
print Total

#----------------------------------------------------------------------------------
#Check that the total people in each org adds up to total people in all
#----------------------------------------------------------------------------------
G=0
for i in range(len(people)):
    G = people[i] +G

#----------------------------------------------------------------------------------
#Printing the results.
#----------------------------------------------------------------------------------
orgs = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','H']
print "The total number of employees is %s." % (totpeople)
for i in range(len(orgs)):
	print "The total number of employees in Org %s is equal to %s. Their combined driving time change is %s." % (orgs[i], people[i], Total[i])




















