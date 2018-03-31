'''Vanessa Van Gilder
PyBank'''

#import libraries
import os
import csv
import statistics

#store file name in variable
file_name = 'budget_data_1.csv'

#path to collect the data
csvpath = os.path.join('Resources', file_name)

#read in the file
with open(csvpath, newline='') as csvfile:

    #split at the commas
    csvreader = csv.reader(csvfile, delimiter=',')

    #skip the headers
    next(csvreader, None)

    '''Find total number of months, total revenue, greatest increase and decrease in revenue'''
    #initialize variables
    revenue = 0
    greatest_inc = 0
    greatest_dec = 0
    changes = []
    rev_list = []

    #loop through each row
    for row in csvreader:
        #add each month's revenue
        revenue += int(row[1])

        #find the greatest increase in revenue
        if int(row[1]) > greatest_inc:
            greatest_inc = int(row[1])
            #grab the date as well
            greatest_inc_date = row[0]

        #find the greatest decrease in revenue
        if int(row[1]) < greatest_dec:
            greatest_dec = int(row[1])
            #grab the date as well
            greatest_dec_date = row[0]
        
        #put all the revenue in the rev_list
        rev_list.append(int(row[1]))

        #months is the number of rows
        months = len(rev_list)


    '''Find the average change in revenue between months'''
    #loop through the rev_list  using a range
    for i in range(1, len(rev_list)):
        #add the difference between each month to the changes list
        changes.append(rev_list[i] - rev_list[i-1])
    
    #find the average
    avg_rev_change = round(statistics.mean(changes), 2)
   
    '''Print everything out and export to a text file'''
    #save output to a variable
    output = """
Financial Analysis
--------------------------------
Total Months: {}
Total Revenue: {}
Average Revenue Change: ${}
Greatest Increase in Revenue: {} (${})
Greatest Decrease in Revenue: {} (${})
""".format(months, revenue, avg_rev_change, greatest_inc_date, greatest_inc, greatest_dec_date, greatest_dec)
    
    #print to terminal
    print(output)

    #export to text file named Financial_Analysis, append
    print(output, file=open("Financial_Analysis.txt", "a"))

    #close the file
    csvfile.close()
