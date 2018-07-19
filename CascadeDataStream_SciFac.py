#!/usr/bin/env python2.7

import csv
import sys
import multiprocessing
import time
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


class EntropyHolder:  #
    def __init__(self, labels=[]):  #
        self.counts_ = collections.defaultdict(int)  #

        self.entropy_ = 0.0  #
        self.sum_ = 0.0  #

    def __len__(self):  #
        return len(self.counts_)  #

    def update(self, count_changes):  #
        r = sum([change for _, change in count_changes])  #

        residual = self._compute_residual(count_changes)  #

        self.entropy_ = self.sum_ * (self.entropy_ - log2(self.sum_ / (self.sum_ + r))) / (self.sum_ + r) - residual  #

        self._update_counts(count_changes)  #

        return self.entropy_  #

    def _compute_residual(self, count_changes):  #
        r = sum([change for _, change in count_changes])  #
        residual = 0.0  #

        for label, change in count_changes:  #
            p_new = (self.counts_[label] + change) / (self.sum_ + r)  #
            p_old = self.counts_[label] / (self.sum_ + r)  #
            #
            residual += p_new * log2(p_new) - p_old * log2(p_old)  #
            #
        return residual  #

    def _update_counts(self, count_changes):  #
        for label, change in count_changes:  #
            self.sum_ += change  #
            self.counts_[label] += change  #

    def entropy(self):  #
        return self.entropy_  #

    def count(self, label):  #
        return self.counts_[self.label2index[label]]  #

    def total_counts(self):  #
        return self.sum_  #


def naive_entropy(counts):  # Calculate entropy the classical way                                                     #
    s = sum(counts)  #
    return sum([-(r / s) * log2(r / s) for r in counts])  #
    #
    #


#######################################################################################################################


# ============================================================================ #
#   A Function to Create the nodes, links, and roots from the given csv file   #
# ============================================================================ #
# ---------------------------- Start of Function ---------------------------- #
def DataProcessor(input_file):
    infilename = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open(infilename + '-nodes.csv', 'w') as nodes_csv, \
            open(infilename + '-links.csv', 'w') as links_csv, \
            open(infilename + '-roots.csv', 'w') as roots_csv:
        node_writer = csv.writer(nodes_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        links_writer = csv.writer(links_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        roots_writer = csv.writer(roots_csv, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)

        with open(InFile) as f:
            line = f.readline()  # Read one line at a time and process it
            diversity = 0  # Defining the value of diversity to start with. -1 is to make the first occurrence zero
            pielou = 0
            '''Changed diversity value to 0 to start diversity at 1 instead of 0'''

            while line:  # This while loop is to read one line at a time until the lines are finished
                current_line = [item.strip(',\n\r') for item in line.split(';')]  # Split the line to list at semicolon
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
                        if identifier not in links_dict:  # If identifier not already present in links dict., add it
                            links_dict[identifier] = current_line_sorted[0]
                            # Keep Modularity as previously calculated  #!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!
                            # Keep Diameter as previously calculated    #!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!
                            roots_writer.writerow([current_line_sorted[0], identifier])  # Write roots to the csv file
                        else:  # If identifier already present in links dictionary
                            links_writer.writerow([links_dict[identifier], current_line_sorted[0], identifier])
                            links_dict[identifier] = current_line_sorted[0]  # Update identifier's ID in links_dict

                    # Entropy is also called Shannon index (H'). Pielou (J) = H'/ln(S). S is total species (unique)
                    pielou = '{:.3f}'.format(float(entropy.entropy()) / log2(len(links_dict)))

                    """ Below for loop is for taking care of specificity and diversity. It adds all the identifiers from
                    current line (as a string) to the identifiers_watched dictionary with default specificity 0. In next
                    line, if the identifiers string is already present in the identifiers_watched dictionary, its value
                    (specificity) is incremented by 1. When a new identifier string is observed, its diversity is also
                    incremented by 1."""
                    if current_line_sorted[2] not in identifiers_seen:
                        diversity += 1  # Upon seeing a new identifier set, increment diversity by 1
                        # Add identifier set to dict with 0 specificity and the current value of diversity
                        identifiers_seen[current_line_sorted[2]] = [0, diversity]
                        div = diversity  # div value used so that 'diversity' value does not change again and again
                    else:  # If identifier already in identifiers_watched dictionary
                        identifiers_seen[current_line_sorted[2]][0] += 1  # Increment its value (specificity) by 1
                        div = identifiers_seen[current_line_sorted[2]][1]  # Pick diversity from identifiers_watched

                    """ The order of the nodes_list is as follows:
                    Node ID; TimeStamp; Identifiers; Specificity; Diversity; Entropy; Pielou"""
                    nodes_list = [current_line_sorted[0], current_line_sorted[1], current_line_sorted[2],
                                  identifiers_seen[current_line_sorted[2]][0], div, '{:.3f}'.format(entropy.entropy()),
                                  pielou]
                    node_writer.writerow(nodes_list)  # Write the row to nodes csv file
                else:  # This statement is to take care of the nodes without identifiers.
                    no_identifier_line_sorted = [current_line[0], current_line[1]]
                    empty_ident_diversity = 0
                    empty_ident_specificity = 0
                    """ The order of the nodes_list is as follows:
                                        Node ID; TimeStamp; Specificity; Diversity; Entropy; Pielou"""
                    no_identifier_node_list = [no_identifier_line_sorted[0], no_identifier_line_sorted[1],
                                               empty_ident_specificity, empty_ident_diversity,
                                               '{:.3f}'.format(entropy.entropy()),pielou]
                    node_writer.writerow(no_identifier_node_list)  # Write the row to nodes csv file


# ---------------------------- End of Function ---------------------------- #


# ================================================================================================================== #
#                      This Section is to Define the Dictionaries and Variables for the Script                       #
# ================================================================================================================== #
entropy = EntropyHolder()  # The class to hold the current entropy

links_dict = {}  # links_dictionary is a dictionary to keep the identifiers and the ID of their last occurrence

# identifiers_seen is a dictionary having already seen identifiers with their [specificity, diversity] values as keys
identifiers_seen = {}

# ================================================================================================================== #
#                                        Main Part of the Program Starts Here                                        #
# ================================================================================================================== #

# Defining a variable to store the input file
# InFile = "examples/foobar.csv"
# InFile = "examples/prep-e2g-smallest.csv"
InFile = sys.argv[1]

FileName = InFile.split('\\').pop().split('/').pop().rsplit('.', 1)[0]  # Store the name of the input file

# =========================================================================== #
#  Creation of nodes, links, and roots by calling the function defined above  #
# =========================================================================== #
# Below call is for single processor
# DataProcessor(InFile)

# Comment above function call and uncomment below if you want to use parallel processing
cpu_count = multiprocessing.cpu_count()  # Check the number of physical processors available
pool = multiprocessing.Pool(processes=cpu_count)  # Use all the available processors
pool.apply_async(DataProcessor(InFile))

# print('############################################################################################################')

# Record Finish time and date to monitor the total run time of script
finish_time = time.strftime("%H:%M:%S")
finish_date = time.strftime("%d/%m/%Y")
time_file = sys.stdout

# ====================================================================================================== #
# Write the start and finish times and elapsed time to the file "Script-Report.csv"                      #
sys.stdout = open(FileName + '-Script-Report.csv', 'w')                                #
print 'The script started running at ', start_time, 'on', start_date                                     #
print 'The script finished processing at', finish_time, 'on', finish_date                                #
print 'The script used', cpu_count, 'CPU processors.'                                                   #
print 'Memory information printed below:'                                                                #
print 'The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB'                         #
print 'The size of identifiers_watched is: ', (sys.getsizeof(identifiers_seen)) / 1000000, 'MB'       #
print 'Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.'                     #
sys.stdout.close()                                                                                       #
sys.stdout = time_file                                                                                   #
# ====================================================================================================== #

# print "All Done BOSS!!!"
# print 'Total processing time was', "{0:.2f}".format(time.time() - start), 'seconds.'
# print 'The script used', cpu_count, 'CPU processors.'
# print 'The size of links_dict is: ', (sys.getsizeof(links_dict)) / 1000000, 'MB'
# print 'The size of identifiers_watched is: ', (sys.getsizeof(identifiers_seen)) / 1000000, 'MB'

# --------------------------------------------------- #
#  A Script by Muhammad Ali Hashmi (09-February-2018) #
# --------------------------------------------------- #
