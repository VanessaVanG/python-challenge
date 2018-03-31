'''Vanessa Van Gilder
PyPoll'''

#import libraries
import csv
import os

#store file name in variable
file_name = 'election_data_2.csv'

#store the results file name in variable
results_file = 'Election_Results.txt'

#path to collect the data
csvpath = os.path.join('Resources', file_name)

#read in the file
with open(csvpath, newline='') as csvfile:

    #split at the commas
    csvreader = csv.reader(csvfile, delimiter=',')

    #skip the headers
    next(csvreader, None)

    #initialize variables
    votes = 0
    candidates = set()
    cand_vote = 0
    cand_stats = []
    
    '''Find total number of votes cast and each candidate'''
    #loop through each row
    for row in csvreader:
        
        #increment votes
        votes += 1

        #find the unique candidates by adding to a set
        candidates.add(row[2])


    '''Find total # of votes for each candidate and percentage of votes'''
    #make a dictionary with each candidate as a key and an empty list of values
    vote_dict = dict.fromkeys(candidates, [])
    
    #loop through the candidates set
    for candidate in candidates:
        #start at the beginning of the file again
        csvfile.seek(0)
        
        #loop through the csv file
        for row in csvreader:

            #if the candidate's name is in the vote column
            if candidate == row[2]:
                #add 1 to their vote count
                cand_vote += 1

            #get the percentage
            perc = (cand_vote / votes) * 100
            #round to one decimal place 
            perc = round(perc, 1)

            #add the percentage & vote count to the value's list in the dictionary
            vote_dict[candidate] = [perc, cand_vote]

        #reset cand_vote
        cand_vote = 0

    '''Find the winner, accounting for ties'''
    #assign the values(candidate votes) of the vote_dict to a variable
    v = vote_dict.values()
    #get the maximum vote count
    maxVal = max(v)
    #make a list for the winner(s)
    winner = []

    #loop through the dictionary's candidates(keys) 
    for key in vote_dict.keys():

        #if the candidate has same # of votes as the max votes,
        if vote_dict[key] == maxVal:
            #add the candidate's name to the winner's list
            winner.append(key)
        
    '''Print everything out and export to a text file'''
    #make a variable storing the dividing line
    lines = '-' * 30
         
    #print,export top part
    top = """
Election Results
{}
Total Votes: {}
{}""".format(lines, votes, lines)
    print(top)
    print(top, file=open(results_file, "a"))
    
    #loop through the vote_dict   
    for k, v in vote_dict.items():
        #add candidate name (key) to cand_stats
        cand_stats.append(k)
        
        #loop through the values
        for i in v:
            #add the values to cand_stats
            cand_stats.append(i)
        
        #store middle part in variable and print, export
        middle = "{}: {}% ({})".format(cand_stats[0],cand_stats[1],cand_stats[2])
        print(middle)
        print(middle, file=open(results_file, "a"))
        cand_stats = []

    #print bottom part
    print(lines)
    print(lines, file=open(results_file, "a"))
    print("Winner:", *winner, sep=' ')
    print("Winner:", *winner, sep=' ', file=open(results_file, "a"))
    print(lines)
    print(lines, file=open(results_file, "a"))

    #close the file
    csvfile.close()   
