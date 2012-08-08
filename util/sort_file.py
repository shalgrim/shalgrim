'''
Date: 6/27/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality: Sometimes you just gotta sort a file
Arguments: Input filename, Output filename
'''

from std_import import *

if __name__ == '__main__':
    try:
        infn = sys.argv[1]      # get file to be sorted
        outfn = sys.argv[2]     # get file to write sorted version to
    except IndexError:          # if not enough args print usage msg
        print >> sys.stderr, 'Usage: python sort_file.py infilename outfilename'
        sys.exit()

    lines = [line.strip() for line in myos.readlines(infn)] # read in file
    lines.sort()                                            # sort lines
    myos.writelines(lines, outfn)                           # write output file

    
