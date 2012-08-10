'''
Author: Scott Halgrim
Date: 7/27/12
Functionality: "Onetime" code used to determine the number of reports
               in the training and test sets and the number of patients
               with reports in each set.
'''
import std_import as si
import re

PNUM = re.compile(r'\d+')
EMPTY_SET = set()

# get module logger
logger = si.logging.getLogger('org.ghri.shalgrim.onetime.num_rpts_ptnts_w_reports')

def getNumReports(d, filterSet=EMPTY_SET):
    fns = si.os.listdir(d)

    if filterSet:
        reports = [fn for fn in fns if PNUM.search(fn).group() in filterSet]
    else:
        reports = fns

    return len(reports)

def getNumPtnts(d, filterSet=EMPTY_SET):
    fns = si.os.listdir(d)
    ptntset = set([PNUM.search(fn).group() for fn in fns])

    if filterSet:
        ptntset.intersection_update(filterSet)

    return len(ptntset)

def getPtntIdSet(fn):
    if fn:
        filterLines = si.myos.readlines(fn)
        idset = set([pid.strip() for pid in filterLines])
    else:
        idset = EMPTY_SET

    return idset

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
    cp = si.ConfigParser.SafeConfigParser(allow_no_value = True)    # create config file parser
    cp.read(options.configfn)               # read in config file

    trndir = cp.get('Main', 'TrainSetDir')
    testdir = cp.get('Main', 'TestSetDir')
    trnFilterFn = cp.get('Main', 'TrainPIDsFile')
    testFilterFn = cp.get('Main', 'TestPIDsFile')
    outfn = options.outfn       # get name of output file

    trnSetIds = getPtntIdSet(trnFilterFn)
    testSetIds = getPtntIdSet(testFilterFn)

    outlines = []
    outlines.append('numTrnRpts: %d'%(getNumReports(trndir, trnSetIds)))
    outlines.append('numTestRpts: %d'%(getNumReports(testdir, testSetIds)))
    outlines.append('numTrnPtntsWithRpt: %d'%(getNumPtnts(trndir, trnSetIds)))
    outlines.append('numTestPtntsWithRpt: %d'%(getNumPtnts(testdir, testSetIds)))

    si.myos.writelines(outlines, outfn)