'''
File: sel_column.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 9/29/10
Functionality: Gets values of one column from a table and writes each to a line
               in a file
Contents:
    - __main__ code that gets the values of a column from a database and writes
      each to a line in a file
'''
import sys
from org.ghri.shalgrim.util import db, myos

if __name__ == '__main__':      # if run as main
    try:
        # get name of odbc connection (technically data source)
        odbc = sys.argv[1]
        table = sys.argv[2]     # get name of table to select from
        column = sys.argv[3]    # get name of column to select
        outfn = sys.argv[4]     # get name of output file
    except IndexError:              # if not enough args given

        # print usage error message
        print >> sys.stderr, '%'% \
              ('Error. Usage: python sel_column.py odbc table column outfile')
        sys.exit()              # and exit

    # get list of rows of that clm
    values = db.selColumn(table, column, datasrc=odbc)
    myos.writelines(values, outfn)              # write each val to output file
