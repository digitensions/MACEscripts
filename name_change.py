# Written by Joanna White and James Wingate
# Code that searches within named columns in an excel (xlsx or csv) file, then changes existing filename from Column 2 to Column 1.

import os
import xlrd
import pandas

def main():
    # Variable that reads excel file (this can be changed to csv) from the path name
    xlsx = pandas.read_excel("/Volumes/Path_to_file/name.xlsx")
    # Focuses variable to Columns listed
    xlsx = xlsx[['Column Title 1', 'Column Title 2']]
    
    # Variable to define path to directory contain files for renaming (mov in this case)
    vidpath = '/Users/path_to_directory/Rename Videos'
    # For loop using os.listdir, to loop through each file in the directory vidpath
    for file in os.listdir(vidpath):
        # Only select the files that end with .mov
        if (file.endswith(".mov")):
            # Variable newname uses pandas .loc (locate) to find a row which matches file, and .iloc[0] (integer locate) removes the column titles and only returns the name value from the row, [0].replace get's the first value and replaces all : with .
            newname = xlsx.loc[xlsx.loc[:, 'Column Title 2'] == file].iloc[0][0].replace(':', '.')
            # Uses os.rename to changes the vidpath/file to vidpath/newname and adds a .mov to the end
            os.rename(vidpath + '/' + file, vidpath + '/' + newname + '.mov')

if __name__ == "__main__":
    main()
