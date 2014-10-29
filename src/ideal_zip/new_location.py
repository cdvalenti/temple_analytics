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
#
# Note:
# Because of request limits set by google, this script must be ran repeatedly over several days
# Zipcodes previously ran are handled by the code to ensure doubling up does not occur
#
# find_zips():
#   1. Find likely drivers by looking at original drive duration
#   2. Find possible ideal zipcodes by looking at original drive duration
#   3. If an output file already exists, add the previous data to the ideal zips list
#   4. Send zip lists back to main
#
# get_avg_time():
#   1. For every ideal zip, fetch duration of every likely driving zip
#   2. Multiply duration by commuters in driving zip, accumulate 
#   3. Get average by dividing sum by total commuters
#   4. Record results in a csv
#   Notes: 
#     Function has error handling if call to googlemaps fails
#     Zips of failed request, name of error, and commuters in request are recorded to a csv
#     If too many failures in a row, request limits have likely been met, script will save what it has and quit
#
# main():
#   Runs the two functions above
#
####################################################################################

#import the googlemaps and csv libraries to be used in this project
import googlemaps
import csv
import time
import pygame
import sys

#define files and api key
input_file = '../../data/move_effects/merck_output.csv'
output_file = '../../data/ideal_zip/best_zip.csv'
error_file = '../../data/ideal_zip/error_zips.csv'
#api_key = 'AIzaSyBkfNH9_w6wPbWrzmSnxxVXvOvzuVj0b7s'
api_key = 'AIzaSyC3vUwqxmcQxBvc5sMd91cRjXYE2iNHcyY'

#sounds to be used for notifications
ding = '../../sounds/ding.wav'
horn = '../../sounds/bike_horn.wav'
pygame.mixer.init()

def find_zips():
  
  #list to hold zipcodes within a certain distance from the original location
  local_zips = list()
  #list to hold drivers with less than a 3 hour commute
  possible_drivers = list()
  
  #open merck_data csv file with all duration and change info
  f = open(input_file)
  merck_data = csv.reader(f)
  
  #set limits for defining drivers and local zips
  driver_limit = 60.0
  local_limit = 60.0
  
  #go through  all zipcodes in merck data, create lists for possible ideal zips, and possible drivers
  count = 0  
  for row in merck_data:
    if count is not 0:
      #create list of drivers using duration of original location < limit
      if float(row[14]) < driver_limit:
        possible_drivers.append([row[0],row[1]])
      #create list of local zips using duration of original location < limit
      if float(row[14]) < local_limit:
        local_zips.append([row[0]])
        
    count = count + 1
  
  f.close()
  
  #if previous zipcode data exists, go through it and enter it into possible ideal locations list
  try:
    print "opening previous results.."
    #open output file from previous run
    f = open(output_file, "r")
    prev_data = csv.reader(f)
    
    completed_zips = list()
    
    #if there is usable data for a zip, record it in a list
    for row in prev_data:
      if len(row) > 1:
        if row[1] == '':
          break
        elif float(row[1]) > 0.0:
          completed_zips.append(row)
    
    print "previous results recorded..."
    
    #enter previous data into local zips list
    for index in range(len(local_zips)):
      for zips in completed_zips:
        if local_zips[index][0] in zips:
          local_zips[index] = zips
    
    print "previous data entered into list..."
  
  #if no output file, exists continue with script 
  except:
    pass
  
  #send lists to main
  return possible_drivers, local_zips
  
def get_avg_time(employee_zips, local_zips):
  
  #open a google maps cient
  gmaps = googlemaps.GoogleMaps(api_key)
  
  #if error file already exists, load it into error list
  try:
    print "uploading previous error list"
    f = open(error_file, "r")
    prev_errors = csv.reader(f)
    error_zips = list()
    for row in prev_errors:
      error_zips.append(row)
  except:
    #create header for error list
    error_zips = [['Start Zip', 'End Zip','Employees','Error Message','Duration']]
  
  #initialize count and define continuous error limit
  error_count = 0
  error_limit = 10
  
  #Go through every possible ideal zip
  for zipcode in local_zips:
    
    #if data isnt already there
    if len(zipcode) < 2:
      
      print ""
      print "Driving Durations if location was moved to " + zipcode[0]
      
      #initialize time and commuters for possible ideal zip
      total_time = 0
      commuters = 0
      
      #for every likely driver zipcode
      for index in range(len(employee_zips)):
        
        #start zip is the zip of driver, end zip is the possible ideal zip
        start = employee_zips[index][0]
        end = zipcode[0]
        
        #if they are not the same zip
        if start is not end:
          
          #try to use googlemaps
          try:
            #get driving duration in minutes
            directions = gmaps.directions(start, end)
            minutes =  directions['Directions']['Duration']['seconds'] / 60.0
            print str(employee_zips[index][1]) + " would commute %.2f minutes" %minutes
            
            #multiple duration by number of employees in starting zip
            minutes = minutes * float(employee_zips[index][1])
            #accumulate time
            total_time = total_time + minutes
            #accumulate commuters
            commuters = commuters + float(employee_zips[index][1])
            #reset error counter bc of success
            error_count = 0
          #if googlemaps fails, handle error  
          except:
            #record error name
            error = sys.exc_info()[0]
            #record commuters in zip
            commuters_in_zip = float(employee_zips[index][1])
            #add zips, commuters, and error to error list
            error_zips.append([start,end,commuters_in_zip,error])
            print "Error calculating duration from %s to %s, added to error list" %(start,end)
            
            #play audible horn to signify error
            pygame.mixer.music.load(horn)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
              continue
            
            #increase error counter
            error_count = error_count + 1
            
            #if too many errors in a row, save files and quit script
            if error_count > error_limit:
              print "Too many continuous errors, saving files and quiting script..."
              
              #save files
              with open(output_file, "wb") as f:
                writer = csv.writer(f)
                writer.writerows(local_zips)
              
              with open(error_file, "wb") as f:
                writer = csv.writer(f)
                writer.writerows(error_zips)
              
              #quit function
              return
        
        #if start zip is the same as end zip, do nothing to time, but add commuters
        elif start is end:
          commuters = commuters + float(employee_zips[index][1])
        
        #sleep half sec to ensure script does not violate google limits      
        time.sleep(0.5)
      
      #once done with all possible drivers, calculate average time for ending zip, add time and commuters to that zips list  
      avg_time = total_time / commuters
      zipcode.append(avg_time)
      zipcode.append(commuters)
      
      print "Average time for %s is %.2f minutes\n" %(zipcode[0], avg_time)
      
      #save output and error files
      with open(output_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(local_zips)
      
      with open(error_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(error_zips)
      
      #play audible ding to signify success
      pygame.mixer.music.load(ding)
      pygame.mixer.music.play()
      while pygame.mixer.music.get_busy() == True:
        continue

  return

def main():
  
  #record start time to later calculate time of script
  start_time = time.time()
  
  #find drivers and possible ideal zipcodes
  possible_drivers, local_zips = find_zips()
  
  #print quantity of each
  print "Number of possible drivers: " + str(len(possible_drivers))
  print "Number of possible ideal locations: " + str(len(local_zips))
  
  #find the average commute time for each possible ideal zip, also saves any errors recieved
  get_avg_time(possible_drivers, local_zips)
  
  #print duration of script out of curiousity
  end_time = time.time()
  total_time = end_time - start_time
  minutes = total_time/60.0
  print "It took %.2f minutes to complete the script" % minutes

if __name__ == '__main__':
  main()
