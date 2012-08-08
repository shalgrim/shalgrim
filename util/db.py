'''
File: db.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 9/29/10
Functionality: Encapsulates frequently used database-related functionality
Contents:
    - selColumn - function that selects a column from a table given as little as
                  a datasource
    - selColumnCursor - function that selects a column from a table given a
                        cursor
    - connectToNlpdev - function that creates and returns a connection to NLPdev
                        on ghriNLP
    - selColumns - function that queries cols from tbl using cnctn.
    - connectToNewClarity - function that creates a connection to a Clarity
                            reporting database.
    - connectToClarity - different name for connectToNewClarity
    - connectToNoNo - function that creates a connection to the ChsDwNoContact
                      database on the ctrhs-sql2k server
    - countRows - (unimplemented/untested) function that executes a select
                  count(*) query on a supplied table
History:
    12/30/10 - added connectToNlpdev and selColumns
    7/11/11 - added connectToNewClarity
    7/20/11 - added connectToNoNo
    7/27/11 - added countRows
    9/27/11 - added dbDateToDatetime
'''

from std_import import *
from adodbapi import connect    # see 9/29/10 log for how to install adodbapi
from pyodbc import connect as pyoconnect    # installed pydobc 7/13/11
import datetime

def selColumn(table, column, cursor=None, cnctn=None, datasrc=None):
    '''
    Function: selColumn
    Input:
        table - table from which to select
        column - column to select
        cusror - database cursor
        cntn - database connection
        datsrc - data source name (e.g., odbc connection name)
    Output: valuelist - a list of values of column in table
    Functionality: Selects a column from a table given a cursor or, barring
                   that, a connection or, barring that, a data source.
    '''
    # if the user provided a cursor, we'll want to use that, but if not
    if not cursor:

        # if the user provided a connection, we'll want to use that, but if not
        if not cnctn:

            # get the connection using the datasource name
            cnctn = connect('Data Source=%s;Trusted_Connection=true;'%(datasrc))
            
        cursor = cnctn.cursor()     # get cursor from connection

    # select column from table
    valuelist = selColumnCursor(cursor, table, column)

    return valuelist            # return output

def selColumns(cnctn, tbl, cols):
    '''
    Function: selColumns
    Input:
        cnctn - database connection
        tbl - table to select from
        cols - list of columns to select
    Output: rows - the rowset returned by the query
    Functionality: Queries cols from tbl using cnctn.
    History:
        12/30/10 - created
    '''
    colstring = ','.join(cols)  # convert list of columns to string for all cols
    crsr = cnctn.cursor()       # get cursor from connection
    crsr.execute('SELECT %s FROM %s'%(colstring, tbl))      # execute query
    rows = crsr.fetchall()                          # get all rows from query

    return rows                                     # return output

def selColumnCursor(crsr, tbl, clm):
    '''
    Function: selColumnCursor
    Input:
        crsr - database cursor
        tbl - table to select from
        clm - column to select
    Output: valuelist - a list of the values in tbl.clm
    Functionality: Queries clm from table using crsr.
    '''
    crsr.execute('SELECT %s FROM %s'%(clm, tbl))    # execute query
    rows = crsr.fetchall()                          # get all rows from query
    valuelist = [row[0] for row in rows]   # convert to list of values in column

    return valuelist                    # return output

def connectToNlpdev(api='adodbapi'):
    '''
    Function: connectToNlpdev
    Input:
        api - which odbc api to use. originally we only used adodbapi but had
              problems with that on VMs so added pyodbc, which seems to work
              better but I didn't want to chance breaking all the old stuff
    Output: cnctn - connection to NLPdev database on ghriNLP server
    Functionality: Creates a connection to NLPdev on ghriNLP
    History:
        12/30/10 - created
        7/13/11 - added api input and modified to use pyodbc as well
        7/27/11 - added warning logging message for using adodbapi from some
                  machines at GHRI
    '''

    if api == 'adodbapi':
        logging.warning('Using adodbapi to connect to Nlpdev may not work ' + \
                        'on some machines, including GHRI VMs')
        # make connection with adodbapi
        cnctn = connect('Data Source=ghriNLP;Initial Catalog=NLPdev;' + \
                        'Trusted_Connection=true;')
    elif api == 'pyodbc':
        # make connection with pyodbc
        cnctn = pyoconnect('DSN=ghriNLP;DATABASE=NLPdev;')
    else:
        logging.warning('Unrecognized api, using pyodbc')

        # make connection with pyodbc
        cnctn = pyoconnect('DSN=ghriNLP;DATABASE=NLPdev;')

    return cnctn            # return output

def connectToNoNo(api='pyodbc'):
    '''
    Date: 7/20/11
    Input:
        api - which odbc api to use. we never used adodbapi with this database,
              which is why the default here is pyodbc
    Output: cnctn - connection to the ChsDwNoContact database on the ctrhs-sql2k
                    server, not to be confused with the ctrhs-sql2k\sql2k server
    Functionality: Creates a connection to the ChsDwNoContact database on the
                   ctrhs-sql2k server (not to be confused with the
                   ctrhs-sql2k\sql2k server), which is where the Nono and
                   Nochartreview lists are stored in sql.
    '''
    if api == 'pyodbc':
        # make connection with pyodbc
        try:
            # TODO: modularize this stuff
            cnctn = pyoconnect('DSN=CTRHS-SQL2K;DATABASE=ChsDwNoContact;')
        except Exception as myerr:
            logging.error('myerr: %s'%(str(myerr)))
            raise
    elif api == 'adodbapi':
        # make connection with adodbapi. untested
        logging.warning('Connecting to nono with adodbapi untested.')
        try:
            cnctn = connect('Data Source=CTRHS-SQL2K;' + \
                            'Initial Catalog=ChsDwNoContact;')
        except Exception as myerr:
            if not myerr:
                logging.error('myerr is None')
            logging.error('myerr: %s'%(str(myerr)))
            raise
    else:
        logging.warning('Unrecognized api, using pyodbc')

        # make connection with pyodbc
        cnctn = pyoconnect('DSN=CTRHS-SQL2K;DATABASE=ChsDwNoContact;')

    return cnctn            # return output


def connectToNewClarity(api='pyodbc'):
    '''
    Function: connectToNewClarity
    Input:
        api - which odbc api to use. we never used adodbapi with this database,
              which is why the default here is pyodbc
    Output: cnctn - connection to the new Clarity database.
    Functionality: Creates a connection to the new Clarity reporting database
                   where "new" means after the changes rolled out in November,
                   2010
    History:
        7/11/11 - Created
        7/13/11 - Removed whichdb input and decided to make two mtehods,
                  renaming this from connectToClarity and I will create
                  connectToOldClarity, too
    '''
    logging.debug('entering connectToNewClarity with api %s'%(api))

    if api == 'pyodbc':
        # make connection with pyodbc
        logging.debug('pre pyoconnect')
        try:
            cnctn = pyoconnect('DSN=epclarity_rpt;DATABASE=Clarity;')
        except Exception as myerr:
            logging.error('myerr: %s'%(str(myerr)))
            raise
        logging.debug('post pyoconnect')
    elif api == 'adodbapi':
        # make connection with adodbapi. I don't think i've every been able
        # to connect to New Clarity with this api, or maybe it's just on the
        # VM I've had trouble...
        logging.warning('Connecting to Clarity with adodbapi untested.')
        try:
            cnctn = connect('Data Source=epclarity_rpt;' + \
                            'Initial Catalog=Clarity;')
        except Exception as myerr:
            if not myerr:
                logging.error('myerr is None')
            logging.error('myerr: %s'%(str(myerr)))
            raise
        logging.debug('post connect with adodbapi')
    else:
        logging.warning('Unrecognized api, using pyodbc')

        # make connection with pyodbc
        cnctn = pyoconnect('DSN=epclarity_rpt;DATABASE=Clarity;')

                    # not sure why, but this part doesn't work with this driver
                    #'Trusted_Connection=true;')

    return cnctn            # return output

def countRows(table, conn=None):
    '''
    Function: countRows
    Input:
        table - table name
        conn - database connection, defaults to Nlpdev if not given
    Output: answer - the number of rows in table in conn
    Functionality: Counts the number of rows in table using conn
    Note: This is unused, and therefore untested, as of 7/27/11
    History:
        7/27/11 - created
    '''
    # until this is implemented, log warning message that it's unused/untested
    logging.warning('Using countRows, an untested function')
    
    if not conn:                            # if no connection provided
        conn = connectToNlpdev('pyodbc')    # connect to Nlpdev using pyodbc
        
    cursor = conn.cursor()                              # get db cursor
    cursor.execute('SELECT COUNT(*) FROM %s'%(table))   # query select count(*)
    answer = cursor.fetchall()[0][0]                    # get count from cursor

    return answer                                       # return output

# I created and used connectToNewClarity when I thought there was still an old
# clarity that could be used. But there's only one, so we'll just use the same
# function to be both connectToClarity and connectToNewClarity for now
connectToClarity = connectToNewClarity

def dbDateToDatetime(dbdate, fmat='%Y-%m-%d'):
    '''
    Function: dbDateToDatetime
    Input:
        dbdate - the string from a date column in a database
        fmat - format of string to convert if it's not NULL.  Defaults to
                the 'yyyy-mm-dd' format common to sql server
    Output: answer - None if dbdate is NULL, otherwise it converts the
                     'yyyy-mm-dd' format into a datetime object
    Functionality: Converts a database date column to a datetime object.
    History: Created 9/27/11 for trying to figure out combos for the clinical
             BrCaRec algorithm
    '''
    if dbdate == 'NULL':        # if the column said 'NULL'
        answer = None           # set output to None
    else:                       # otherwise

        # split on whitespace to get rid of trailing potential time format
        # (e.g., '00:00:00.000') and then convert the rest according to fmat
        # and set to output
        answer = datetime.datetime.strptime(dbdate.split()[0], fmat)

    return answer               # return output
