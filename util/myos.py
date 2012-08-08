'''
File: myos.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 8/31/10
Functionality: Encapsulates frequently used os-related functionality
Contents:
    getColsFromFile - Gets column lists out of some kind of char-separated txt
                      file
    mkdir_p - function that emulates Unix's mkdir -p functionality
    remSuffixes - function that removes the suffixes from a filename so that
                  a file's parallel files can be found in other directories
    locateFile - function that finds a file of a particular name in a list of
                 directories
    writeTokenizedLines - function that writes tokenized lines to output file
    write - function that Writes text to a file taking advantage of openw
History:
    9/28/10 - added read and writelines
    9/29/10 - added openw
            - modified writelines to use openw
    10/8/10 - added close
            - modified openw to return stdout if no filename given
    10/13/10 - added getColsFromFile
    10/19/10 - added printiter
    10/25/10 - modified getColsFromFile so that it could handle some (or all)
               lines not having enough columns
    12/14/10 - added write
'''
import os, errno, sys, logging

def getColsFromFile(fn, *args, **kwargs):
    '''
    Function: getColsFromFile
    Input:
        fn - a filename
        args - a tuple of column indexes we want to extract
        kwargs - dict of keyword args.  We only look for colsep, the column
                 separator in the column now. It's assumed to be '\t'
    Output: answer - a list of lists where the inner lists' values are the
                     values of the columns requested in args
    Functionality: Gets column lists out of some kind of char-separated txt file
    History:
        10/13/10 - created
        10/25/10 - Modified so that it could handle some (or all) lines not
                   having enough columns
    '''

    try: colsep = kwargs['colsep']  # get column separator
    except KeyError: colsep='\t'    # if not there, default to \t

    # read in the file's lines and separate into columns
    lines = [line.split(colsep) for line in readlines(fn)]
    
    answer = []         # initialize output
    
    for colnum in args: # for each desired column number

        try:
            # put that column's values in a list and append to output
            answer.append([line[colnum].strip() for line in lines])

        # but if at least one line does not have the right number of columns
        # 10/25 update: put line above in try and added this except block
        except IndexError:

            # log a warning message
            logging.warning('At least one line in %s too short for index %d'%(fn, colnum))
            column = []             # then initialize the column

            for line in lines:      # and for each line

                # add that line's colnumth element to the column
                try: column.append(line[colnum].strip())

                # and if it's not there, add None
                except IndexError: column.append(None)
                
            answer.append(column)   # then append column to output

    return answer                   # return output

def remSuffixes(basename):
    '''
    Function: remSuffixes
    Input: basename - a filename, base name (no path) only
    Output: answer - basename with all of its suffixes (designated by dots)
                     removed
    Functionality: removes the suffixes from a filename so that a file's
                   parallel files can be found in other directories
    '''
    answer = basename       # initialize output to input

    while '.' in answer:    # while there is still a .suffix in name
        answer = os.path.splitext(answer)[0]   # remove last suffix

    return answer           # return suffixless filename
        

def mkdir_p(path):
    '''
    Function: mkdir_p
    Input:
        path - the path of the dir to be created
    Output: none
    Functionality: Emulates mkdir -p functionality in unix which doesn't care
                   if a dir already exists and creates parent dirs if needed
    Author: TZ[omega]TZIOY
    Reference: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    History:
        7/15/11 - added WindowsError exception checking for
                  trunk\DelineNotes.bat and added the logging of exc.errno
    '''
    try:
        os.makedirs(path)   # just make all dirs in path
    except OSError, exc:    # unless you get an error... # Python >2.5
        if exc.errno == errno.EEXIST:   # and that errors no is the path exists
            pass                        # that you can ignore

        # if the problem is that path == ''
        elif exc.errno == errno.ENOENT and not path:
            pass                        # then ignore that too
        else:                           # otherwise

            # write errno to stderr
            print >> sys.stderr, 'exc.errno: %d'%(exc.errno)
            logging.error('exc.errno: %d'%(exc.errno))  # log the errno
            raise                           # and re-raise error

    return

def locateFile(dirs, basename):
    '''
    Function: locateFile
    Input:
        dirs - a list of directories
        basename - the base filename of a file
    Output: answer - the first directory in dirs that contains basename
    Functionality: Finds a file of a particular name in a list of directories
    '''
    for d in dirs:                              # for each dir in dirs
        fullname = os.path.join(d, basename)    # create potential abs filename

        if os.access(fullname, os.F_OK):        # if that file exists
            answer = d                          # set output to this dir
            break                               # and exit loop
        
    else:                                       # if file never found
        # raise exception
        raise Exception(basename + ' does not exist in ' + str(dirs))
     
    return answer                               # return output


def writeTokenizedLines(tlines, outfn):
    '''
    Function: writeTokenizedLines
    Input:
        tlines - a list of lists.  The outer list is lines and the inner list is
                 space-separated tokens
        outfn - output filename
    Output: none
    Functionality: writes tokenized lines to output file
    '''

    outfile = open(outfn, 'wb')         # open output file for write

    for line in tlines:                 # for each tokenized line
        outline = ' '.join(line) + '\n' # separate with space and add newline
        outfile.write(outline)          # write line to file

    outfile.close()                     # close output file

    return

def readlines(filename):
    '''
    Function: readlines
    Input: filename - absolute path of a file
    Output: lines - list of lines in the file
    Functionality: Reads in a file into a list of lines
    '''
    filedescriptor = open(filename)     # open file
    lines = filedescriptor.readlines()  # read in lines
    filedescriptor.close()              # close file

    return lines                        # return output

def read(filename):
    '''
    Function: read
    Input: filename - absolute path of a file
    Output: text - text of file
    Functionality: Reads in a file in one line
    History:
        9/28/10 - created
    '''
    filedescriptor = open(filename)     # open file
    text = filedescriptor.read()        # read in file
    filedescriptor.close()              # close file

    return text                         # return output

def writelines(lines, filename):
    '''
    Function: writelines
    Input:
        lines - a list of strings to be written to filenaem
        filename - absolute path of a file
    Output: None
    Functionality: Writes a list of strings to a file, one per line
    History:
        9/28/10 - created
        9/29/10 - modified to use openw below instead of open
        12/30/10 - modified to use close below instead of method on file object
    '''
    filedescriptor = openw(filename)    # open file, creating path if necessary

    for line in lines:                      # for each line in input
        filedescriptor.write(line + '\n')   # write out to its line

    close(filedescriptor)                   # close file

    return

def write(txt, filename):
    '''
    Function: write
    Input:
        txt - text to be written to filenaem
        filename - absolute path of a file
    Output: None
    Functionality: Writes text to a file, taking advantage of openw here
    History:
        12/14/10 - created
        12/30/10 - modified to use close below instead of method on file object
    '''    
    filedescriptor = openw(filename)    # open file for write
    filedescriptor.write(txt)           # write text
    close(filedescriptor)               # close file

    return

def openw(filename=''):
    '''
    Function: openw
    Input: filename - the filename to open for write
    Output: descriptor - the file descriptor of the file opened for write
    Functionality: Opens a file for writing, creating the path provided for it
                   if necessary. If no arg given, returns sys.stdout
    History:
        9/29/10 - created
        10/8/10 - modified to allow to return sys.stdout if no file sent in
    '''
    if filename:        # if filename given

        # create path to filename if necessary
        mkdir_p(os.path.dirname(filename))
        descriptor = open(filename, 'w')    # open file for write
    else:                                   # if no file given
        descriptor = sys.stdout             # set output to sys.stdout
    
    return descriptor                   # return output

def close(fd):
    '''
    Function: close
    Input: fd - a file descriptor
    Output: none
    Functionality: Closes the file descriptor, but doesn't if it can't be
                   closed.  E.g., if it is stdout
    History:
        10/8/10 - created
    '''
    try: fd.close()                 # try closing descriptor
    except AttributeError: pass     # ignore if it can't be closed

    return

def printiter(iterator, filename=''):
    '''
    Function: printiter
    Input:
        iterator - an iterator
        filename - file to write iterator to
    Output: none
    Functionality: Writes each element of iterator as a line to filename.  If
                   no filename given, writes to stdout.
    History:
        10/19/10 - created
    '''
    fd = openw(filename)    # open output file for write

    for i in iterator:      # for each element in iterator
        print >> fd, i      # write it to file

    close(fd)               # close file

    return
