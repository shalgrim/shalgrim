'''
Author: Scott Halgrim
Date: 7/27/12
Functionality: "Throwaway" code used to calculate the mean and std deviation of
               the follow-up period for our training and test sets.
'''
import std_import as si
from org.ghri.util.util import mymath # TODO: fix that double util thing

# get module logger
logger = si.logging.getLogger('org.ghri.shalgrim.onetime.brcarec_mean_sd_chain0435')

if __name__ == '__main__':                  # if run as main, not if imported
    
    # usage string to give if user asks for help or gets command line wrong
    usageStr = '%(prog)s configfile [options]'
    parser = si.opts.ConfigFileParser(usage=usageStr)  # create cmd line parser
    options = parser.parse_args()                   # parse command line

    # start logging at root according to command line
    si.mylogger.config(logfn=options.logfile, logmode=options.logmode, \
                                                    loglevel=options.loglevel)

    logger.setLevel(options.loglevel)   # set module logging level to input

    # TODO: subclass this so i can set defaults and let the get function
    #       have some error checking, etc.
    cp = si.ConfigParser.SafeConfigParser()    # create config file parser
    cp.read(options.configfn)               # read in config file

    # get name of tab-separated file that contains all of the BNs and INs in the
    # first column
    infn = cp.get('Main', 'InputFile')
    outfn = options.outfn       # get name of output file

    lines = si.myos.readlines(infn)[1:]         # slice off header row
    trainvals = [int(line.split()[0]) for line in lines if line.split()[1] == 'Train']
    testvals = [int(line.split()[0]) for line in lines if line.split()[1] == 'Test']
    
    outlines = []

    # do the divs by 365.25 to get years out of days
    outlines.append('Train mean: %02f'%(mymath.mean(trainvals)/365.25))
    outlines.append('Train SSD: %02f'%(mymath.ssd(trainvals)/365.25))
    outlines.append('Test mean: %02f'%(mymath.mean(testvals)/365.25))
    outlines.append('Test SSD: %02f'%(mymath.ssd(testvals)/365.25))
    outlines.append('All mean: %02f'%(mymath.mean(trainvals + testvals)/365.25))
    outlines.append('All SSD: %02f'%(mymath.ssd(trainvals + testvals)/365.25))
    si.myos.writelines(outlines, outfn)