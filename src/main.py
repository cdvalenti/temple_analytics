#Temple University Analytics Competition Source Code
#
#Authors:
#Christian D. Valenti
#Alexander Arocho
#Chiehjeng Chen
#
#

import googlemaps

White_zip = '08889'
Ken_zip = '07033'
WP_zip = '19486'

gmaps = googlemaps.GoogleMaps('awesome_team')

start=  '19026'
end = 'Orlando, FL'
directions = gmaps.directions(start, end)
time =  directions['Directions']['Duration']['seconds']
minutes = time/60.

print 'Duration: ' + str(minutes) + ' minutes or ' + str(minutes/60.) + ' hours'
