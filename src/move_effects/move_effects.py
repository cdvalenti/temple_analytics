####################################################################################
#Temple University Analytics Competition Source Code
#Also submitted to Dr. Joseph Picone for ECE 3822
#
#Authors:
# Christian D. Valenti
# Alexander Arocho
# Chiehjeng Chen
#
#Description of script:
#   1. Read supplied csv file from merck (merck_data.csv)
#   2. Reorganizes the data by zipcode, counts number of employees in each zip and in each organization
#   3. For every zipcode, find the drive duration in minutes to Whithouse Station, Kenilworth, and West Point zipcodes
#   4. For every zipcode, find the change in drive duration for move to Kenilworth and West Point, from Whitehouse Station
#   5. Write results to a new csv file (merck_output.csv)
#
###################################################################################

#import the googlemaps and csv libraries to be used in this project
import googlemaps
import csv
import time

#define a file names
file_name ='../../data/merck_data.csv'
output_file = '../../data/move_effects/merck_output.csv'

#zip codes for move locations
Whitehouse_Station_NJ = '08889'
Kenilworth_NJ = '07033'
West_Point_PA = '19486'

#google maps api key
api_key = 'AIzaSyBkfNH9_w6wPbWrzmSnxxVXvOvzuVj0b7s'

def organize_data(file_name):
  
  #create empty list to be appended in this function
  zipcode_info = [['Zip Code', 'Number of Employees', 'Number in Org A', 'Number in Org B', 
  'Number in Org C', 'Number in Org D', 'Number in Org E', 'Number in Org F', 'Number in Org G', 
  'Number in Org H', 'Number in Org I', 'Number in Org J', 'Number in Org K', 'Number in Org L', 
  'Driving Minutes to White House Station, NJ', 'Driving Minutes to Kenilworth, NJ', 'Driving Minutes to West Point, PA',
  'Change in Duration for Kenilworth Move', 'Change in Duration for West Point Move']]
  
  #open csv file
  f = open(file_name)
  merck_data = csv.reader(f)
  
  count = 0
  #for every row in the data provided, take the zip code and
  #if not already added to the list, add it
  for row in merck_data:
    if (row[1] not in zipcode_info) and (count is not 0):
      zipcode_info.append(row[1])
      #use to add single quote before number
      #zipcode_info.append("'" + row[1])
    count = count + 1
  f.close()
  
  #take the newly created list and transform each element from a string to a list containing that string
  for index in range(len(zipcode_info)):
    if index is not 0:
      zipcode_info[index] = [zipcode_info[index]]
  
  #for every zip code recorded the list, go into the data provided to count how many times this is repeated
  #add this number to the end of each zipcode's list
  for index in range(len(zipcode_info)):
    if index is not 0:
      zip_count = 0
      f = open(file_name)
      merck_data = csv.reader(f)
      for row in merck_data:
        if zipcode_info[index][0] in row:
          zip_count = zip_count + 1
      f.close()
      zipcode_info[index].append(zip_count)
  
  #list of organizations for org parsing
  organizations = ['Org A', 'Org B', 'Org C', 'Org D', 'Org E', 
  'Org F', 'Org G', 'Org H', 'Org I', 'Org J', 'Org K', 'Org L']
  
  #for every zipcode, count how many are in each organization append to end of each list
  for org in organizations:
    for index in range(len(zipcode_info)):
      if index is not 0:
        org_count = 0
        f = open(file_name)
        merck_data = csv.reader(f)
        for row in merck_data:
          if (zipcode_info[index][0] == row[1]) and (row[2] == org):
            org_count = org_count + 1
        f.close()
        zipcode_info[index].append(org_count)
  
  #return the list created in this function
  return zipcode_info

def calculate_distances(zip_info):
  
  #open a google maps client
  gmaps = googlemaps.GoogleMaps(api_key)
  
  #for every zip code find length of drive to Whitehouse Station, NJ in minutes
  for index in range(len(zip_info)):
    if index is not 0:
      start =  zip_info[index][0]
      end = Whitehouse_Station_NJ
      directions = gmaps.directions(start, end)
      time =  directions['Directions']['Duration']['seconds']
      minutes_to_work = time/60.0
      zip_info[index].append(minutes_to_work)

  #for every zip code find length of drive to Kenilworth, NJ in minutes
  for index in range(len(zip_info)):
    if index is not 0:
      start =  zip_info[index][0]
      end = Kenilworth_NJ
      directions = gmaps.directions(start, end)
      time =  directions['Directions']['Duration']['seconds']
      minutes_to_work = time/60.0
      zip_info[index].append(minutes_to_work)
  
  #for every zip code find length of drive to KWest Point, PA in minutes
  for index in range(len(zip_info)):
    if index is not 0:
      start =  zip_info[index][0]
      end = West_Point_PA
      directions = gmaps.directions(start, end)
      time =  directions['Directions']['Duration']['seconds']
      minutes_to_work = time/60.0
      zip_info[index].append(minutes_to_work)
  
  return zip_info

def calculate_change(zip_info):
  
  #for every zipcode
  for index in range(len(zip_info)):
    if index is not 0:
      
      #subtract Kenilworth Duration from Whitehouse Station
      change = float(zip_info[index][15]) - float(zip_info[index][14])
      #append to list
      zip_info[index].append(change)
      
      #subtract Kenilworth Duration from Whitehouse Station
      change = float(zip_info[index][16]) - float(zip_info[index][14])
      #append to list
      zip_info[index].append(change)

  return zip_info
  
def main():
  
  start_time = time.time()
  
  #Go through merck's data file and organize zip data
  zip_info = organize_data(file_name)
  
  #Use zips to calculate distances
  zip_info = calculate_distances(zip_info)
  
  #use drive durations to find change in drive durations
  zip_info = calculate_change(zip_info)
  
  #write zip_info to an output csv file
  with open(output_file, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(zip_info)
  
  #print duration of script out of curiousity
  end_time = time.time()
  total_time = end_time - start_time()
  minutes = total_time/60.0
  print "It took %.2f minutes to complete the script" % minutes

if __name__ == '__main__':
  main()
