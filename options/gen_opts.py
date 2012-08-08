'''
File: gen_opts.py
Author: Scott Halgrim, shalgrim@gmail.com
Date: 10/8/10
Functionality: Extends OptionParser with  commonly used functionality like
               output and logging info and allows for a minimum number of args
               to be established at creation
Contents:
    GenArgParser - class that extends ArgumentParser with  commonly used
                   functionality like output and logging info. Differs from
                   GenOptionParser in that this class's superclass hasn't been
                   deprecated and it handles required arguments on its own so I
                   took that part out
    GenOptionParser - a class that extends OptionParser with  commonly used
                      functionality like output and logging info and allows for
                      a minimum number of arguments to be established at creation
    ConfigFileParser - subclass of GenOptionParser that does not parse a config
                       file but rather adds an option for a configuration file.
NOTE: The optparse module used here is deprecated and newer code should use
      argparse
History:
    10/25/10 - added GenArgParser
    1/12/11 - added workingdir option to GenArgParser
    4/13/11 - added ConfigFileParser
'''
import optparse, sys, logging, argparse

class GenArgParser(argparse.ArgumentParser):
    '''
    Class: GenArgParser
    Superclass: argparse.ArgumentParser
    Members: none that aren't inherited
    Functionality: Extends ArgumentParser with  commonly used functionality like
                   output and logging info. Differs from GenOptionParser in that
                   this class's superclass hasn't been deprecated and it handles
                   required arguments on its own so I took that part out
    History:
        1/12/11 - added workingdir option
    '''
    def __init__(self, **kwargs):
        '''
        Method: __init__
        Input:
            self - this GenArgParser
            kwargs - dict of additional keyword arguments
        Output: self - a new GenArgParser
        Functionality: constructor
        History:
            1/12/11 - added workingdir option initialization
        '''

        # call superclass constructor
        argparse.ArgumentParser.__init__(self, **kwargs)

        # add o option for output filename.  If not given output wil be written
        # to stdout if myos.openw is used
        self.add_argument('-o', '--outfn', action='store', type=str,
                                      help='output filename [default: stdout]')

        # add l option for log filename
        self.add_argument('-l', '--logfile', action='store', type=str,
                                                        default=r'C:\tmp\pylog')

        # add w option for working directory, added 1/12/11
        self.add_argument('-w', '--workingdir', action='store', type=str,
                                                    default=r'C:\tmp\pywork')

        # add m for logging mode.  E.g., a for append or w for write
        self.add_argument('-m', '--logmode', action='store', type=str,
                                                                    default='a')

        # add v option for logging level
        self.add_argument('-v', '--loglevel', action='store', type=int,
                                                        default=logging.WARNING)

        return
    
class GenOptionParser(optparse.OptionParser):
    '''
    Class: GenOptionParser
    Superclass: optparse.OptionParser
    Members:
        numRequiredArgs - the number of required arguments. If the parser sees
                          less than this number it will print a usage message
                          and exit
    Functionality: Extends OptionParser with  commonly used functionality like
                   output and logging info and allows for a minimum number of
                   arguments to be established at creation
    '''

    def __init__(self, numReqArgs=0, **kwargs):
        '''
        Method: __init__
        Input:
            self - this GenOptionParser
            numReqArgs - number of required arguments
            kwargs - dict of additional keyword arguments
        Output: self - a new GenOptionParser
        Functionality: constructor
        '''

        # call superclass constructor
        optparse.OptionParser.__init__(self, **kwargs)

        self.numRequiredArgs = numReqArgs   # set numRequiredArgs member

        # add o option for output filename.  If not given output wil be written
        # to stdout if myos.openw is used
        self.add_option('-o', '--outfn', action='store', type='string',
                                    help='output filename [default: stdout]')

        # add l option for log filename
        self.add_option('-l', '--logfile', action='store', type='string',
                                                        default=r'C:\tmp\pylog')

        # add m for logging mode.  E.g., a for append or w for write
        self.add_option('-m', '--logmode', action='store', type='string',
                                                                    default='a')

        # add v option for logging level
        self.add_option('-v', '--loglevel', action='store', type='int',
                                                        default=logging.WARNING)
        
        return
        
    def parse_args(self):
        '''
        Method: parse_args
        Input: self - this GenOptionParser
        Output:
            options - an object containing options user entered
            args - non-option arguments from user
        Functionality: parses command line options and arguments and verified
                       a minimum number of arguments were provided
        '''

        # call superclass parse_args
        options, args = optparse.OptionParser.parse_args(self)
        
        if len(args) != self.numRequiredArgs:   # if not enough args provided
            self.print_usage()                  # print usage message
            sys.exit()                          # exit

        return options, args                    # return output

class ConfigFileParser(GenArgParser):
    '''
    Class: ConfigFileParser
    Superclass: GenArgParser
    Members: none that aren't inherited
    Functionality: Extends GenArgParser by adding the -c configfile option.
    Note: Does not, as the name suggests, parse a config file.  It's just the
          GenArgParser with the --configfile option added.  I didn't just add
          that to GenArgParser because I'd used the -c option in at least
          patient_date_from_doc_clasifs.py previously
    History:
        4/13/11 - Created
    '''
    def __init__(self, usage='%(prog)s configfile [options]', **kwargs):
        '''
        Method: __init__
        Input:
            self - this GenArgParser
            kwargs - dict of additional keyword arguments
        Output: self - a new GenArgParser
        Functionality: constructor
        '''

        # call superclass constructor
        GenArgParser.__init__(self, usage=usage, **kwargs)

        # add c argument for config file
        self.add_argument('configfn', help='config filename')

        return
    
    def getlist(self, listsect, listlen):
        answer = [self.get(listsect, str(i)) for i in range(listlen)]
        
        return answer