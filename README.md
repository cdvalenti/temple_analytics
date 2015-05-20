## Temple University Analystics Challenge
##### Authors: Alexander Arocho, Chiehjeng Chen, Christian D. Valenti

#### UPDATE!!!!
Out of 130 entries, we were chosen as 1 of the 20 finalists. All of the finalists performed a 5 minute presentation to a panel of executives from companies such as QVC, Merck, and NBCUniversal. 
The panel of executives decided our graphic and presentation deserved SECOND PLACE!!

To see the graphic we presented at the competetion click here: http://ibit.temple.edu/analytics/files/2014/11/ChenFull.png

------

**ABOUT:** This repository contains the code and data files used to complete the 2nd Annual Temple Analytics Challenge outlined (http://ibit.temple.edu/analytics/).

Our group has specifically decided to take on the Merck Challenge: Understanding a Corporate Move's Impact (http://ibit.temple.edu/analytics/impact-of-a-corporate-move/).

For any questions, feel free to contact Christian Valenti at christian.valenti@temple.edu

------
####


#### Effects of Move on Driving Duration
**Method:** Python script (src/move_effects/move_effects.py) to determine the change in drive duration for every zip code possessed by an employee. The script reorganizes the data given by Merck to be ordered by zipcode. Each zip code has the following attributes:
* Number of Employees
* Number of Employees in Organization (A - L)
* Driving Minutes to Whitehouse Station, NJ (zipcode: 08889)
* Driving Minutes to Kenilworth, NJ (zipcode: 07033)
* Driving Minutes to West Point, PA (zipcode: 19486)
* Change in minutes for move to Kenilworth, NJ
* Change in minutes for move to West Point, PA
To obtain driving minutes, the googlemaps (https://pypi.python.org/pypi/googlemaps/) python library was utilized. This data is then saved to a .csv (data/move_effects/merck_output.csv).

**Open Heat Map** (openheatmap.com) was used to display the useable information from above into maps.
The output file above (data/move_effects/merck_output.csv) was manually reorganized in excel to a format that could be understood by the openheatmap website.
Four (4) sets of maps were created:
* Change in duration per zip code (Kenilworth, NJ)
* Change in duration per zip code (West Point, PA)
* Weighted (by number of employees) change in duration per zip code (Kenilworth, NJ)
* Weighted (by number of employees) change in duration per zip code (West Point, PA)

Map Links:
* Per Zip Code (Kenilworth, NJ): http://www.openheatmap.com/view.html?map=ConcubinarianIntercommunionXenic
* Per Zip Code (West Point, PA): http://www.openheatmap.com/view.html?map=SubcaudateCystogenousPygmyism
* Weighted by Zip Code Population (Kenilworth, NJ): http://www.openheatmap.com/view.html?map=XviiControversalLallations
* Weighted by Zip Code Population (West Point, PA): http://www.openheatmap.com/view.html?map=FregataCumbernauldsDiluent

Major cities were added to the maps in an image editor to help the viewer.

#### Organizational Impact of a Move
Using the output file from  before (data/move_effects/merck_output.csv), the organizational data was manipulated in python (src/org_data/org_data_kenilworth.py and src/org_data/org_data/westpoint.py) to show the effects that each move had specifically on organizations. This data was then organized into tables in excel and presented.

#### Finding an Ideal Location
The difficult task of finding an ideal location for a Corporate move included many steps. 
The first task was to find the zip codes local to most of the employees. To determine this, we decided the drive duration to the original location (Whithouse Station) had to be within one hour.
Secondly, we had to determine which employees actually drove to work. Since many of the employee zipcodes were very far from the original location, it was fair to assume many worked remotely or from home. We decided that if the drive duration for the original location was an hour or less, they most likely drove to work.
With two sets of zipcodes, we then had to calculate the drive time from every possible driving zipcode to every possible ideal location zipcode (nearly 85,000 googlemaps requests). This was acheived once again utilizing the googlemaps library in a python script (src/ideal_zip/new_location.py). With such a large number of requests, an official Google API key had to be obtained to increase request limits. Even then, exception handling had to be incorporated to cath request failures due to timeouts and limits exceeded. Once a limit is exceeded, we had to wait 24 hours to re start the code. We didn't want to restart the process, so the code saves the data from the previous run, uploads it into a list, and starts where it left off. This prevented needed the code to finsih completely in one run.
**RESULTS** : http://www.openheatmap.com/view.html?map=EmpowermentsSphygmophonesOxydasic

------

###Results
Out of 130 entries, our team won second place. The final graphic can be found at
http://ibit.temple.edu/analytics/files/2014/11/ChenFull.png
