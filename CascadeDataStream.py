#!/usr/bin/env python3

import csv
import sys
from multiprocessing import Pool
import time
start = time.time()
start_time = time.strftime("%H:%M:%S")
start_date = time.strftime("%d/%m/%Y")

# Defining a variable to store the input file
InFile = "examples/prep-e2g-smallest.csv"
#InFile = sys.argv[1]

# links_dictionary is a dictionary to keep the identifiers and the ID of their last occurrence
links_dict = {}

# =========================================================================== #
#          Creation of nodes by calling the function defined above            #
# =========================================================================== #
def DataProcessor(input_file):
    InFileName = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open('output_files/'+InFileName+'-nodes.csv', 'w') as nodes_csv, open('output_files/'+InFileName+'-links.csv', 'w') as links_csv, open('output_files/'+InFileName+'-roots.csv', 'w') as roots_csv:
        node_writer = csv.writer(nodes_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        links_writer = csv.writer(links_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        roots_writer = csv.writer(roots_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        with open(InFile) as f:
            line = f.readline() # Read one line at a time and process it
            while line: # This while loop is to read one line at a time until the lines are finished
                temp_list = [item.strip(',\n') for item in line.split(';')] # Split the line to a list at semicolon
                line = f.readline()
                if temp_list[2] != "":  # Check if there are identifiers, append it to nodes
                    node_writer.writerow(temp_list) # Write the row to nodes csv file
                    for identifier in temp_list[2].split(','): # Go through the identifiers in current line
                        if identifier not in links_dict: # If identifier not already present in links dictionary, add it
                            links_dict[identifier] = temp_list[0]
                            roots_writer.writerow([temp_list[0], identifier]) # Write the roots to the csv file for roots
                        else: # If identifier already present in links dictionary
                            links_writer.writerow([links_dict[identifier], temp_list[0], identifier]) # Write links to csv file
                            links_dict[identifier] = temp_list[0] # If identifier already present, update its ID in links_dict

# =========================================================================== #
#  Creation of nodes, links, and roots by calling the function defined above  #
# =========================================================================== #
# Below call is for single processor
DataProcessor(InFile)

# Comment above function call and uncomment below if you want to use parallel processing
#pool = Pool(processes=16)
#pool.apply_async(DataProcessor(InFile))


#print('############################################################################################################')

finish_time = time.strftime("%H:%M:%S")
finish_date = time.strftime("%d/%m/%Y")
time_file = sys.stdout

# Write the start and finish times and elapsed time to the file "Script-Report.csv"
sys.stdout = open('Script-Report.csv', 'w')
print('The script started running at ', start_time, 'on', start_date)
print('The script finished processing at', finish_time, 'on', finish_date)
print('Total processing time was', "{0:.2f}".format(time.time()-start), 'seconds.')
sys.stdout.close()
sys.stdout = time_file

#print("All Done BOSS!!!")
#print('Total processing time was', "{0:.2f}".format(time.time()-start), 'seconds.')


#---------------------------------------------------#
# A Script by Muhammad Ali Hashmi (18-January-2018  #
#---------------------------------------------------#

