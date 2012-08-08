'''
File: eval_file_opts.py
Author: Scott Halgrim, shalgrim@gmail.com
Date: 10/7/10
Functionality: Extends GenOptionParser with a DEFAULT_USAGE message and a
               default number of required arguments (2) useful for evaluation
Contents:
    EvalOptionParser - class that extends GenOptionParser with a DEFAULT_USAGE
                       message and a default number of required arguments (2)
                       useful for evaluation
NOTE: This class currently does not do much since its only extensions are a
       default usage message and minimum number of required arguments, both of
       which are easily established with a call to the superclass constructor
NOTE: The optparse module used here is deprecated and newer code should use
      argparse
'''
import optparse, sys
from org.ghri.shalgrim.options.gen_opts import GenOptionParser

class EvalOptionParser(GenOptionParser):
    '''
    Class: GenOptionParser
    Superclass: optparse.OptionParser
    Members:
        DEFAULT_USAGE - a default usage message in case one is not sent in
        numRequiredArgs - the number of required arguments. If the parser sees
                          less than this number it will print a usage message
                          and exit
    Functionality: Extends GenOptionParser with a DEFAULT_USAGE message and a
                   default number of required arguments (2) useful for
                   evaluation
    '''
    # DEFAULT_USAGE message for an evaluation process parser
    DEFAULT_USAGE = '%prog goldfilename sysfilename [options]'

    def __init__(self, numReqArgs=2, **kwargs):
        '''
        Method: __init__
        Input:
            self - this EvalOptionParser
            kwargs - dict of additional keyword arguments
        Output: self - a new EvalOptionParser
        Functionality: constructor
        '''
        
        if 'usage' not in kwargs:                 # if usage message not sent in
            kwargs['usage'] = self.DEFAULT_USAGE  # set to default

        # call superclass constructor
        GenOptionParser.__init__(self, numReqArgs=numReqArgs, **kwargs)

        return
