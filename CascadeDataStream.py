#!/usr/bin/env python3

import csv
import sys
from multiprocessing import Pool
import time
import numpy
import collections
import math

# Record Start time and date to monitor the total run time of script
start = time.time()
start_time = time.strftime("%H:%M:%S")
start_date = time.strftime("%d/%m/%Y")

# ================================================================================================================== #
#                               This Section is to Define the Functions for the Script                               #
# ================================================================================================================== #

#######################################################################################################################
"""                                                                                                                   #
A proof-of-concept implementation of algorithms and formulas described in [1].                                        #
[1] https://arxiv.org/abs/1403.6348                                                                                   #
Blaz Sovdat (blaz.sovdat@gmail.com)                                                                                   #
"""  #


def log2(p):  #
    return math.log(p, 2) if p > 0 else 0  #
    #


CountChange = collections.namedtuple('CountChange', ('label', 'change'))  #


#

class EntropyHolder:
    def __init__(self, labels=[]):
        self.counts_ = collections.defaultdict(int)

        self.entropy_ = 0
        self.sum_ = 0

    def __len__(self):
        return len(self.counts_)

    def update(self, count_changes):
        r = sum([change for _, change in count_changes])

        residual = self._compute_residual(count_changes)

        self.entropy_ = self.sum_ * (self.entropy_ - log2(self.sum_ / (self.sum_ + r))) / (self.sum_ + r) - residual

        self._update_counts(count_changes)

        return self.entropy_

    def _compute_residual(self, count_changes):
        r = sum([change for _, change in count_changes])
        residual = 0

        for label, change in count_changes:
            p_new = (self.counts_[label] + change) / (self.sum_ + r)
            p_old = self.counts_[label] / (self.sum_ + r)

            residual += p_new * log2(p_new) - p_old * log2(p_old)

        return residual

    def _update_counts(self, count_changes):
        for label, change in count_changes:
            self.sum_ += change
            self.counts_[label] += change

    def entropy(self):
        return self.entropy_

    def count(self, label):
        return self.counts_[self.label2index[label]]

    def total_counts(self):
        return self.sum_


def naive_entropy(counts):  # Calculate entropy the classical way                                                     #
    s = sum(counts)  #
    return sum([-(r / s) * log2(r / s) for r in counts])  #


#######################################################################################################################

# ============================================================================ #
#           A Function to find the entropy of a list of identifiers            #
# ============================================================================ #
# ---------------------------- Start of Function ---------------------------- #
def myentropy(dictionary_of_identifiers):
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
    infilename = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open('output_files/' + infilename + '-nodes.csv', 'w') as nodes_csv, \
            open('output_files/' + infilename + '-links.csv', 'w') as links_csv, \
            open('output_files/' + infilename + '-roots.csv', 'w') as roots_csv:
        node_writer = csv.writer(nodes_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        links_writer = csv.writer(links_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        roots_writer = csv.writer(roots_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)

        with open(InFile) as f:
            line = f.readline()  # Read one line at a time and process it
            diversity = -1  # Defining the value of diversity to start with. -1 is to make the first occurrence zero
            #div = 0  # diversity (div) used for if statement so that 'diversity' value does not change again and again

            while line:  # This while loop is to read one line at a time until the lines are finished
                current_line = [item.strip(',\n') for item in line.split(';')]  # Split the line to a list at semicolon
                line = f.readline()
                if current_line[2] != "":  # Check if there are identifiers, process it then. Discard otherwise
                    # Updated list converts the identifiers to a list, sorts them, & converts them back to a string
                    current_line_sorted = [current_line[0], current_line[1],
                                           ','.join(map(str, sorted((current_line[2]).split(","))))]

                    """ The below loop converts the 3rd item of temp_list, i.e. the identifiers string to a list, loops
                     through all the identifiers and checks if the identifier is present in the links_dictionary. If yes
                      then it updates the ID with the current identifier, if not, it adds the identifier to the dict.
                      In the second case it also adds the identifier with its ID to the roots.csv file. Apart from that
                       it also adds the identifiers to 'all_identifiers' dictionary with their count as the keys. If an
                       identifier is already in the dictionary, its key is incremented by 1. """
                    for identifier in current_line_sorted[2].split(','):  # Go through the identifiers in current line
                        entropy.update([CountChange(identifier, 1)])
                        # freq[identifier] += 1
                        if identifier not in links_dict:  # If identifier not already present in links dict., add it
                            links_dict[identifier] = current_line_sorted[0]
                            # all_identifiers[identifier] = 1  ### Delete if not necessary
                            roots_writer.writerow([current_line_sorted[0], identifier])  # Write roots to the csv file
                        else:  # If identifier already present in links dictionary
                            links_writer.writerow([links_dict[identifier], current_line_sorted[0], identifier])
                            links_dict[identifier] = current_line_sorted[0]  # Update identifier's ID in links_dict
                            # all_identifiers[identifier] += 1  # Increment the keys for repeating identifiers. ### Delete if not necessary

                            # identifier_count_changes = [CountChange(key, val) for key, val in all_identifiers.items()]  # #####
                    # entropy.update(identifier_count_changes)  # #####
                    # all_updated_entropies.append('{:.3f}'.format(entropy.entropy()))  # #####

                    # Entropy is also called Shannon index (H'). Pielou (J) = H'/ln(S). S is total species (unique)
                    # entropy_value = '{:.3f}'.format(naive_entropy(all_identifiers.values()))  # Calculate the entropy to 3 decimal pts
                    # all_entropies.append(entropy_value)  # #####
                    pielou = '{:.3f}'.format(float(entropy.entropy()) / numpy.log(len(links_dict)))

                    if current_line_sorted[2] not in identifiers_watched:
                        diversity += 1  # Upon seeing a new identifier set, increment diversity by 1
                        identifiers_watched[current_line_sorted[2]] = 0  # Add identifier set to dict with 0 specificity
                        div = diversity  # div value updated so that 'diversity' value does not change again and again
                    else:  # If identifier already in identifiers_watched dictionary
                        identifiers_watched[current_line_sorted[2]] += 1  # Increment its value (specificity) by 1
                        div = 0  # diversity zero due to a duplicate identifier set
                    nodes_list = [current_line_sorted[0], current_line_sorted[1], current_line_sorted[2],
                                  identifiers_watched[current_line_sorted[2]], div, '{:.3f}'.format(entropy.entropy()),
                                  pielou]
                    print('Nodes List: ', nodes_list)
                    node_writer.writerow(nodes_list)  # Write the row to nodes csv file


# ---------------------------- End of Function ---------------------------- #


# ================================================================================================================== #
#                               This Section is to Define the Functions for the Script                               #
# ================================================================================================================== #
# The class to hold the entropy
entropy = EntropyHolder()
# freq = collections.defaultdict(int)

# links_dictionary is a dictionary to keep the identifiers and the ID of their last occurrence
links_dict = {}

# identifiers_watched is a dictionary with watched identifiers with their specificity values as keys
identifiers_watched = {}

# all_identifiers is a dictionary for storing the identifiers and their counts, i.e. times it occurs
# all_identifiers = {}

# all_entropies = []
# all_updated_entropies = []

# ================================================================================================================== #
#                                        Main Part of the Program Starts Here                                        #
# ================================================================================================================== #

# Defining a variable to store the input file
InFile = "examples/foobar.csv"
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
sys.stdout = open('output_files/' + FileName + '-Script-Report.csv', 'w')  #
print('The script started running at ', start_time, 'on', start_date)  #
print('The script finished processing at', finish_time, 'on', finish_date)  #
print('Memory information printed below:')  #
print('The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB')  #
print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched)) / 1000000, 'MB')  #
print('Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.')  #
sys.stdout.close()  #
sys.stdout = time_file  #
# ====================================================================================================== #

# print("All Incremental Entropies: ", all_updated_entropies)
# print("All Naive Entropies:       ", all_entropies)
# print('All Identifiers: ', len(all_identifiers))
# print('Links Dictionary: ', len(links_dict))

print("All Done BOSS!!!")
print('Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.')
print('The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB')
print('The size of identifiers_watched is: ', (sys.getsizeof(identifiers_watched)) / 1000000, 'MB')

# --------------------------------------------------- #
#  A Script by Muhammad Ali Hashmi (31-January-2018)  #
# --------------------------------------------------- #
