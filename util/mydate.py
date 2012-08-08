'''
File: mydate.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 10/18/10
Functionality: wrappers for classes in datetime module
Contents:
    MyDatetime - wrapper class for datetime.datetime that makes formatting calls
                 easier and also handles strings that are not dates
History:
    8/18/11: udpated MyDatetime.__sub__ to include warnings if you try to
             subtract a nondate
    10/10/11: added calcAge function
'''

import datetime, logging

DEFAULT_FORMAT='%m/%d/%Y'   # default date format
DEFAULT_DATE='01/01/1900'   # default date

def calcAge(bday, eventday):
    '''
    Function: calcAge
    Input:
        bday - birthday as datetime.date or datetime.datetime
        eventday - day of event we are calc'ing age for as datetime.date or
                   datetime.datetime
    Output: answer - int of age at eventday
    Functionality: Calculates age
    '''
    raw = eventday.year - bday.year     # subtract years to get raw age
    adjust = 0                          # initialize adjustment to 0

    if eventday.month < bday.month:     # if bday month is later than event mnth
        adjust = -1                     # adjust age by 1
    elif eventday.month == bday.month:  # or if in same month bug
        if eventday.day < bday.day:     # bday day is later than event day
            adjust = -1                 # adjust by 1

    answer = raw + adjust               # incorporate adjustment to output
    
    return answer                       # return output

class MyDatetime:
    '''
    Class: MyDatetime
    Members:
        dt - the wrapped datetime
        nondate - boolean indicating whether this represents a non-date
        repr - string representation of date or non-date at creation
    Functionality: Wraps python datetime class to format nicely using str()
                   operator and to handle strings that are not dates in case
                   they need to coexist with dates eg when a system-assigned
                   recurrence date can also be undefined if the patient did not
                   have a recurrence.
    History:
        8/18/11: udpated __sub__ to include warnings if you try to subtract a
                  nondate
    '''

    def __init__(self, datestr=DEFAULT_DATE, fmat=DEFAULT_FORMAT):
        '''
        Method: __init__
        Input:
            self - this MyDatetime
            datestr - string representing a date
            fmat - date format of datestr
        Output: self - a new MyDatetime
        Functionality: constructor
        '''
        try:
            # try converting datestr to a datetime using fmat format
            self.dt = datetime.datetime.strptime(datestr, fmat)
            self.nondate = False    # if it works, set nondate to False
        except ValueError, ve:      # if date doesn't convert

            # log a warning message
            logging.warning('%s. Storing %s as string not datetime'%
                                                                (ve, datestr))
            # set the dt member to the default date
            self.dt=datetime.datetime.strptime(DEFAULT_DATE, DEFAULT_FORMAT)
            self.nondate = True     # indicate we are not really storing a date

        self.repr = datestr     # store input string as representation
        self.format = fmat      # store input fmat string as format member

        return

    def __str__(self):
        '''
        Method: __str__
        Input: self - this MyDatetime
        Output: self formatted according to fmat
        Functionality: Overrides str() operator to call toString method passing
                       format member
        '''
        return self.toString(self.format)

    def toString(self, fmat):
        '''
        Method: toString
        Input:
            self - this MyDate
            fmat - date formatting string
        Output: answer - self formatted according to fmat
        Functionality: Formats this date to a string using fmat format string
        History:
            12/14/10 - Modified to handle non-date strings
        '''
        # if not really a date, just set output to string representation
        if self.nondate: answer = self.repr

        # otherwise convert to string according to input format string
        else: answer = self.dt.strftime(fmat)
            
        return answer       # return output

    def isDate(self):
        '''
        Method: isDate
        Input: self - this Mydatetime
        Output: answer - True if self represents a datetime, False otherwise
        Functionality: accessor
        '''
        if self.nondate: answer = False     # if not date, set output to False
        else: answer = True                 # else set output to True

        return answer                       # return output

    def __sub__(self, other):
        '''
        Method: __sub__
        Input: self, other - Mydatetimes
        Output: The timedelta between the datetime wrapped by self and that
                wrapped by other
        Functionality: Overrides - operator
        History:
            8/18/11: udpated to include warnings if you try to subtract a
                     nondate
        '''
        # if this is not a date, log warning
        if self.nondate: logging.warning('subtracting from nondate')

        # if other is not a date, log warning
        if other.nondate: logging.warning('subtracting nondate')

        return self.dt - other.dt   # return difference of date members
