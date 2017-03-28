#!/usr/bin/python
########################################################################
# Helper Functions
########################################################################
import csv

# Hash to Text Converter..


def save_data_to_csv_file(csv_file_name, data, keys, separator, sub_separator, replace_bad='#'):
    '''Convert 2 level Hash to Text & putting in to consideration they provided keys'''

    with open(csv_file_name, 'wb') as csvfile:

        writer = csv.writer(csvfile, delimiter=separator)

        # Write Header
        writer.writerow(keys)

        # Iterate Over the Data
        for cn in data:
            # initialize new row
            row = []

            ######
            for key in keys:
                # Get Key & Valye Value...
                value = data[cn].get(key, '')

                # Convert List to Str
                if type(value) == list:
                    value = sub_separator.join(value)

                # Remove Bad characters (separator)
                value = str(value).replace(separator, replace_bad)

                # append value to row
                row.append(value)

            # Save row
            writer.writerow(row)
