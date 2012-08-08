'''
File: mystring.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 10/18/10
Functionality: Extends str so that join can handle sequences containing non-
               strings
Contents:
    MyStr - class that extends str so that join can handle sequences containing
            non-strings
'''

class MyStr(str):
    '''
    Class: MyStr
    Members: none
    Functionality: Extends str so that join can handle sequences containing
                   non-strings
    '''
    
    def join(self, seq):
        '''
        Method: join
        Input:
            self - this MyStr
            seq - a sequence
        Output: a string where the members of seq are converted to seq and then
                joined by self
        Functionality: Overrides str.join to explicitly convert each member of
                       seq before attempting to join
        '''

        # convert each item in seq to a string and join with self and return
        return str.join(self, [str(v) for v in seq])
