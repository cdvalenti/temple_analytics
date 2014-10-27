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
# Simple script to get duration of a drive, one drive at a time
# Script contains error handling for start and end points that do not work in google maps
#   1. Asks user for start and end point
#   2. Calculates duration, prints out
#   3. Asks user if it wants to do another request
#
####################################################################################


import googlemaps
import pygame

#set up google maps
api_key = 'AIzaSyBkfNH9_w6wPbWrzmSnxxVXvOvzuVj0b7s'
gmaps = googlemaps.GoogleMaps(api_key)

#sounds to be used for notifications
ding = '../../sounds/ding.wav'
horn = '../../sounds/bike_horn.wav'
pygame.mixer.init()

#function to play a sound
def play_sound(wav_file):
  
  pygame.mixer.music.load(wav_file)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
    continue

#search function
def search():
  
  print "Search Google Maps for Drive Duration"
  
  error_count = 0
  error_limit = 2
  
  while(1):
    
    #get start and end locations
    print ""
    start = str(raw_input("Start Location:  "))
    end = str(raw_input("End Location:    "))
    
    #use googlemaps to search, print duration, play sound, clear error count
    try:
      directions = gmaps.directions(start, end)
      minutes =  directions['Directions']['Duration']['seconds'] / 60.0
            
      print "\nDuration of drive from %s to %s:\n%.2f minutes\n" %(start,end,minutes)
      play_sound(ding)
            
      error_count = 0
    
    #error exception, print message, play sound, increase error count, quit if 3 in a row
    except:
      
      print "Error calculating duration from %s to %s, please try again\n" %(start,end)
      play_sound(horn)
      
      error_count = error_count + 1
      if error_count > error_limit:
        print "Too many continuous errors, quiting script...\n"
        quit()
    
    #ask if user wants to search again
    again = raw_input("Search again? (Y or N) >>  ")
    if again not in ['Y', 'y', 'Yes', 'yes', 'YES']:
      print "\nQuiting Script..."
      quit()

def main():
  search()

if __name__ == '__main__':
  main()
