"""Module for saving data to a csv file."""
import csv


def file_saver(output_path='simulation_data.csv', data_head=[], data_list=[]):
    """
    Save simulation data to a csv file for a given parameters.

    Input Arguments:
        - output_path: The name of the file
        - data_head: The header of the file, ex: ['Energy(eV)', 'Volume']
        - data_list: The data of each header, ex: [[1,2,..,3,4], [1,2,..,4,3]]
    """
    with open(output_path, 'w', newline='') as csvfile:
        # seperates each element in the row with a comma
        csv_write = csv.writer(csvfile, delimiter=',')
        csv_write.writerow(data_head)

        for n in range(0, len(data_list[0])):
            # Takes the n:th number of element in each list in data_list
            row = [data_list[i][n] for i in range(0, len(data_list))]
            # writes the 'row' as the n:th row in the file
            csv_write.writerow(row)
