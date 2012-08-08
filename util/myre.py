'''
File: myre.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 3/24/11
Functionality: Contains commonly used regular expression utilities
Contents:
    INTRE, NUMRE - regular expression pattern recognizing an int
    FLOATSTR - rege ex string representing a float
    CONTROL_CHARS_RE - reg ex string recognizing any control character XML is
                       found not to like in my work
    getFirstNum - function that returns the first int from a string
History:
    4/7/11 - added CONTROL_CHARS_RE
    9/13/11 - added UNICODE_CONTROL_CHARS
'''
import re

INTRE = NUMRE = re.compile('\d+')               # reg ex pattern for an int
FLOATSTR = '-?(?:(?:\d+\.?\d*)|(?:\d*\.\d+))'   # reg ex string for a float

# regex pattern recognizing chars xml does not like
CONTROL_CHARS_RE = re.compile('\x01|(&#((1[29])|(20?)|(31));)')

# regex pattern recognizing first 32 ascii characters that are control chars
# except for tab (9) and newline (10) because many strings don't have problems
# with those
UNICODE_CONTROL_CHARS = re.compile('[\x00-\x08\x0b-\x1f]')

def getFirstNum(s):
    '''
    Function: getFirstNum
    Input: s - a string
    Output: answer - a string representing the first int in s, '' if none.
    Functionality: Finds and returns the first integer portion of a string
    '''
    match =  NUMRE.search(s)        # search string for an integer

    if match:                       # if an int found
        answer = match.group()      # set it (as string) to output
    else:                           # otherwise
        anwer = ''                  # set output to empty string

    return answer                   # return output
