import csv
import sys


def FileConverter(input_file):
    infilename = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    with open(infilename + '-specificity.txt', 'w') as specificity_csv, \
            open(infilename + '-diversity.txt', 'w') as diversity_csv, \
            open(infilename + '-entropy.txt', 'w') as entropy_csv, \
            open(infilename + '-pielou.txt', 'w') as pielou_csv, \
            open(infilename + '-all_prop.txt', 'w') as all_prop_csv:
        specificity_writer = csv.writer(specificity_csv, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC,
                                        skipinitialspace=True)
        diversity_writer = csv.writer(diversity_csv, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC,
                                      skipinitialspace=True)
        entropy_writer = csv.writer(entropy_csv, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        pielou_writer = csv.writer(pielou_csv, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        all_prop_writer = csv.writer(all_prop_csv, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)

        with open(input_file) as f:
            line = f.readline()  # Read one line at a time and process it

            while line:  # This while loop is to read one line at a time until the lines are finished
                current_line = [item.strip('",\n\r') for item in line.split(';')]  # Split the line to list at semicolon
                line = f.readline()
                date_stamp = current_line[1][:-9]  # Save Date only
                time_stamp = current_line[1][11:]  # Save the time only
                timestamp = ' '.join([date_stamp, time_stamp])  # Join date and time without 'T' in between them
                specificity = [str(timestamp), int(current_line[3])]  # [-1] is to remove the last Z from time
                diversity = [str(timestamp), int(current_line[4])]
                entropy = [str(timestamp), float(current_line[5])]
                pielou = [str(timestamp), current_line[6]]
                all_properties = [str(timestamp), int(current_line[3]), int(current_line[4]), float(current_line[5]),
                                  float(current_line[6])]
                specificity_writer.writerow(specificity)
                diversity_writer.writerow(diversity)
                entropy_writer.writerow(entropy)
                pielou_writer.writerow(pielou)
                all_prop_writer.writerow(all_properties)



# InFile = 'test.csv'
InFile = sys.argv[1]

FileConverter(InFile)
