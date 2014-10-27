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
# Calculates and records the average change in drive duration for each organization for the move to:
#   >> Kenilworth, NJ
#
# Uses already organized data in merck_output.csv 
#
####################################################################################

#import csv for readng and writing csv files
import csv

#use organized merck data for reading data, write results to output
input_file = '../../data/merck_output.csv'
output_file = '../../data/org_data/org_data.csv'

def main():
  
  #define headers for output csv
  org_csv = [['Organization','Number of Employees in Organization', 'Total Change in Drive Duration for Organization', 'Average Change in Drive Duration for Organization']]
  orgs = ['','','Org A','Org B','Org C','Org D','Org E','Org F','Org G','Org H','Org I','Org J','Org K','Org L']
  
  #for every possible org (columns 2 -14 in merck data)
  for org in range(2,14):
    
    #create empty list that will temporarily hold each row in the final table
    org_list = list()
    
    #open organized merck data csv file
    f = open(input_file)
    merck_data = csv.reader(f)
    
    #inti employees in each org and change for org
    emp_in_org = 0
    total_change = 0
    
    #for every zip in the merck data
    count = 0
    for row in merck_data:
      
      #dont want to read header
      if (count is not 0):
        
        #accumulate employees in each org
        num_in_org = float(row[org])
        emp_in_org = emp_in_org + num_in_org
        
        #multiply change in dur for kenilworth move by employees in the org
        change = float(row[-2]) * num_in_org
        #accumulate total change
        total_change = total_change + change
        
      count = count + 1
    
    f.close()
    
    #calculate average change for that org
    avg_change = total_change / emp_in_org
    #create a row with data recorded
    org_list = [orgs[org], emp_in_org, total_change, avg_change]
    #add row to future csv file
    org_csv.append(org_list)
  
  #once complete for all orgs, save csv file  
  with open(output_file, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(org_csv)

if __name__ == '__main__':
  main()
