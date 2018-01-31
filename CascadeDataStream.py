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


# ================================================================================================================== #
#                               This Section is to Define the Functions for the Script                               #
# ================================================================================================================== #


# ============================================================================ #
#           A Function to find the entropy of a list of identifiers            #
# ============================================================================ #
# ---------------------------- Start of Function ---------------------------- #
def entropy(dictionary_of_identifiers):
    probabilities_dict = {x: int(dictionary_of_identifiers[x]) / sum(dictionary_of_identifiers.values()) for x in
                          dictionary_of_identifiers}
    probabilities = numpy.array(list(probabilities_dict.values()))
    return - probabilities.dot(numpy.log2(probabilities))


# ---------------------------- End of Function ---------------------------- #


# ============================================================================ #
#   A Function to Create the nodes, links, and roots from the given csv file   #
# ============================================================================ #
# ---------------------------- Start of Function ---------------------------- #
def DataProcessor(input_file):
    InFileName = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open('output_files/' + InFileName + '-nodes.csv', 'w') as nodes_csv, \
            open('output_files/' + InFileName + '-links.csv', 'w') as links_csv, \
            open('output_files/' + InFileName + '-roots.csv', 'w') as roots_csv:
        node_writer = csv.writer(nodes_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        links_writer = csv.writer(links_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        roots_writer = csv.writer(roots_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        with open(InFile) as f:
            line = f.readline()  # Read one line at a time and process it
            diversity = -1  # Defining the value of diversity to start with. -1 is to make the first occurrence zero
            div = 0  # diversity (div) used for if statement so that 'diversity' value does not change again and again
            # all_identifiers = []
            while line:  # This while loop is to read one line at a time until the lines are finished
                temp_list = [item.strip(',\n') for item in line.split(';')]  # Split the line to a list at semicolon
                line = f.readline()
                if temp_list[2] != "":  # Check if there are identifiers, append it to nodes
                    # Updated list converts the identifiers to a list, sorts them, & converts them back to a string
                    updated_temp_list = [temp_list[0], temp_list[1],
                                         ','.join(map(str, sorted((temp_list[2]).split(","))))]

                    """ The below loop converts the 3rd item of temp_list, i.e. the identifiers string to a list, loops
                     through all the identifiers and checks if the identifier is present in the links_dictionary. If yes
                      then it updates the ID with the current identifier, if not, it adds the identifier to the dict.
                      In the second case it also adds the identifier with its ID to the roots.csv file. Apart from that
                       it also adds the identifiers to 'all_identifiers' dictionary with their count as the keys. If an
                       identifier is already in the dictionary, its key is incremented by 1. """
                    for identifier in updated_temp_list[2].split(','):  # Go through the identifiers in current line
                        if identifier not in links_dict:  # If identifier not already present in links dict., add it
                            links_dict[identifier] = updated_temp_list[0]
                            all_identifiers[identifier] = 1
                            roots_writer.writerow([updated_temp_list[0], identifier])  # Write roots to the csv file
                        else:  # If identifier already present in links dictionary
                            links_writer.writerow([links_dict[identifier], updated_temp_list[0], identifier])
                            links_dict[identifier] = updated_temp_list[0]  # Update identifier's ID in links_dict
                            all_identifiers[identifier] = 1  # Increment the keys for repeating identifiers

                    entropy_value = '{:.3f}'.format(entropy(all_identifiers))  # Calculate the entropy to 3 decimal pts

                    if updated_temp_list[2] not in identifiers_watched:
                        diversity += 1  # Upon seeing a new identifier set, increment diversity by 1
                        identifiers_watched[updated_temp_list[2]] = 0  # Add identifier set to dict with 0 specificity
                        div = diversity
                    else:  # If identifier in dictionary
                        identifiers_watched[updated_temp_list[2]] += 1  # Increment its value (specificity) by 1
                        div = 0  # diversity zero due to a duplicate identifier set
                    nodes_list = [updated_temp_list[0], updated_temp_list[1], updated_temp_list[2],
                                  identifiers_watched[updated_temp_list[2]], div, entropy_value]
                    node_writer.writerow(nodes_list)  # Write the row to nodes csv file

# ---------------------------- End of Function ---------------------------- #


# ================================================================================================================== #
#                               This Section is to Define the Functions for the Script                               #
# ================================================================================================================== #

# links_dictionary is a dictionary to keep the identifiers and the ID of their last occurrence
links_dict = {}

# identifiers_watched is a dictionary with watched identifiers with their specificity values as keys
identifiers_watched = {}

# all_identifiers is a dictionary for storing the identifiers and their counts, i.e. times it occurs
all_identifiers = {}

# ================================================================================================================== #
#                                        Main Part of the Program Starts Here                                        #
# ================================================================================================================== #

# Defining a variable to store the input file
InFile = "examples/prep-e2g-smallest.csv"
# InFile = sys.argv[1]

FileName = InFile.split('\\').pop().split('/').pop().rsplit('.', 1)[0]


# =========================================================================== #
#  Creation of nodes, links, and roots by calling the function defined above  #
# =========================================================================== #
# Below call is for single processor
# DataProcessor(InFile)

# Comment above function call and uncomment below if you want to use parallel processing
pool = Pool(processes=4)
pool.apply_async(DataProcessor(InFile))

# print('############################################################################################################')

# Record Finish time and date to monitor the total run time of script
finish_time = time.strftime("%H:%M:%S")
finish_date = time.strftime("%d/%m/%Y")
time_file = sys.stdout

# ====================================================================================================== #
# Write the start and finish times and elapsed time to the file "Script-Report.csv"                      #
sys.stdout = open('output_files/' + FileName + '-Script-Report.csv', 'w')                                #
print('The script started running at ', start_time, 'on', start_date)                                    #
print('The script finished processing at', finish_time, 'on', finish_date)                               #
print('Memory information printed below:')                                                               #
print('The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB')                        #
print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched)) / 1000000, 'MB')      #
print('Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.')                    #
sys.stdout.close()                                                                                       #
sys.stdout = time_file                                                                                   #
# ====================================================================================================== #

print("All Done BOSS!!!")
print('Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.')
print('The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB')
print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched)) / 1000000, 'MB')

# --------------------------------------------------- #
#  A Script by Muhammad Ali Hashmi (31-January-2018)  #
# --------------------------------------------------- #
