#!/usr/bin/env python3

import csv
import sys
from multiprocessing import Pool
import time
import numpy

# Record Start time and date to monitor the total run time of script
start = time.time()
start_time = time.strftime("%H:%M:%S")
start_date = time.strftime("%d/%m/%Y")

# ============================================================================ #
#           A Function to find the entropy of a list of identifiers            #
# ============================================================================ #
def entropy(list_of_identifiers):
    probabilities_dict = {x:list_of_identifiers.count(x)/len(list_of_identifiers) for x in list_of_identifiers}
    probabilities = numpy.array(list(probabilities_dict.values()))

    return - probabilities.dot(numpy.log2(probabilities))

# ============================================================================ #
#   A Function to Create the nodes, links, and roots from the given csv file   #
# ============================================================================ #
def DataProcessor(input_file):
    InFileName = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open(InFileName+'-nodes.csv', 'w') as nodes_csv, open(InFileName+'-links.csv', 'w') as links_csv, open(InFileName+'-roots.csv', 'w') as roots_csv:
        node_writer = csv.writer(nodes_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        links_writer = csv.writer(links_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        roots_writer = csv.writer(roots_csv, quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        with open(InFile) as f:
            line = f.readline() # Read one line at a time and process it
            diversity = -1 # Defining the value of diversity to start with. -1 is to make the first occurrence zero
            div = 0 # diversity (div) used for if statement so that 'diversity' value does not change again and again
            #all_identifiers = []
            while line: # This while loop is to read one line at a time until the lines are finished
                temp_list = [item.strip(',\n') for item in line.split(';')] # Split the line to a list at semicolon
                line = f.readline()
                if temp_list[2] != "":  # Check if there are identifiers, append it to nodes
                    # The updated list below converts the identifiers to a list, sorts them, and converts them back to a string
                    updated_temp_list = [temp_list[0], temp_list[1], ','.join(map(str, sorted((temp_list[2]).split(","))))]
                    for items in updated_temp_list[2].split(","): # This loop is to create a list of all identifiers for entropy calculation
                        all_identifiers.append(items)
                    entropy_value = '{:.3f}'.format(entropy(all_identifiers)) # Calculate the entropy and restrict decimal to 3 points
                    print(all_identifiers)
                    if updated_temp_list[2] not in identifiers_watched:
                        diversity += 1 # Upon seeing a new identifier set, increment diversity by 1
                        identifiers_watched[updated_temp_list[2]] = 0 # Add the new identifier set to dictionary with zero specificity
                        div = diversity
                    else:
                        identifiers_watched[updated_temp_list[2]] += 1  # If identifier in dictionary, increment its value (specificity) by 1
                        div = 0 # diversity zero due to a duplicate identifier set
                    nodes_list = [updated_temp_list[0], updated_temp_list[1], updated_temp_list[2], identifiers_watched[updated_temp_list[2]], div, entropy_value]
                    node_writer.writerow(nodes_list) # Write the row to nodes csv file
                    for identifier in updated_temp_list[2].split(','): # Go through the identifiers in current line
                        if identifier not in links_dict: # If identifier not already present in links dictionary, add it
                            links_dict[identifier] = updated_temp_list[0]
                            roots_writer.writerow([updated_temp_list[0], identifier]) # Write the roots to the csv file for roots
                        else: # If identifier already present in links dictionary
                            links_writer.writerow([links_dict[identifier], updated_temp_list[0], identifier]) # Write links to csv file
                            links_dict[identifier] = updated_temp_list[0] # If identifier already present, update its ID in links_dict

# ------------------------------------------------------------------------------------ #
# Defining a variable to store the input file
#InFile = "examples/prep-e2g-smallest.csv"
InFile = sys.argv[1]

FileName = InFile.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

# links_dictionary is a dictionary to keep the identifiers and the ID of their last occurrence
links_dict = {}

# identifiers_watched is a dictionary with watched identifiers with their specifity values as keys
identifiers_watched = {}

all_identifiers = []
# =========================================================================== #
#  Creation of nodes, links, and roots by calling the function defined above  #
# =========================================================================== #
# Below call is for single processor
#DataProcessor(InFile)

# Comment above function call and uncomment below if you want to use parallel processing
pool = Pool(processes=16)
pool.apply_async(DataProcessor(InFile))


#print('############################################################################################################')

finish_time = time.strftime("%H:%M:%S")
finish_date = time.strftime("%d/%m/%Y")
time_file = sys.stdout

# Write the start and finish times and elapsed time to the file "Script-Report.csv"
sys.stdout = open(FileName+'-Script-Report.csv', 'w')
print('The script started running at ', start_time, 'on', start_date)
print('The script finished processing at', finish_time, 'on', finish_date)
print('Memory information printed below:')
print('The size of links_dict is: ', (sys.getsizeof(links_dict))/1000000, 'MB')
print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched))/1000000, 'MB')
print('Total processing time was', "{0:.2f}".format(time.time()-start), 'seconds.')
sys.stdout.close()
sys.stdout = time_file

#print("All Done BOSS!!!")
#print('Total processing time was', "{0:.2f}".format(time.time()-start), 'seconds.')
#print('The size of links_dict is: ', (sys.getsizeof(links_dict))/1000000, 'MB')
#print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched))/1000000, 'MB')


#---------------------------------------------------#
# A Script by Muhammad Ali Hashmi (29-January-2018  #
#---------------------------------------------------#


