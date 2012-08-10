'''
Author: Scott Halgrim
Date: 7/27/12
Functionality: "Onetime" code used to determine the median and IQR
               number of reports per patient in the training, test,
               and all sets.
'''
import std_import as si
import re
from org.ghri.shalgrim.onetime.num_rpts_ptnts_w_reports import PNUM

# get module logger
logger = si.logging.getLogger('org.ghri.shalgrim.onetime.median_iqr_rpts_per_ptnt')

def getRptNamesByPID(adir, pidfn):

    # initialize dict to have every pid with empty list
    rptNamesByPID = {line.strip():[] for line in si.myos.readlines(pidfn)}
    fns = si.myos.listdir(adir)             # get all filenames

    for fn in fns:                          # for each filename
        pid = PNUM.search(fn).group()       # get patient ID

        # note that a defaultdict is not appropriate here because the directory
        # has more patients than are in our filtered (primary > 1/1/95) cohorts
        # and so I want to distinguish between those not in our cohort (exclude)
        # and those in our cohort with zero reports (empty list)
        try:
            rptNamesByPID[pid].append(fn)   # add filename to list for that pid
        except KeyError:
            pass                            # if that ptnt not in list skip

    return rptNamesByPID

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

    # TODO: modularize for test and all
    trnRptsByPtnt = getRptNamesByPID(trndir, trnFilterFn)
    trnRptsByPtntSorted = sorted(trnRptsByPtnt.items(), key=lambda k, v: len(v))

    # get median index
    medind = len(trnRprtsByPtntSorted)/2

    # get median
    if len(trnRptsByPtntSorted)%2 == 0:
        trnmed = (len(trnRptsByPtntSorted[medind][1]) + len(trnRptsByPtntSorted[medind-1][1]))/2.0
    else:
        trnmed = len(trnRptsByPtntSorted[medind][1])

    # get median index
    medind = len(trnRprtsByPtntSorted)/2

    # get median
    if len(testRptsByPtntSorted)%2 == 0:
        testmed = (len(testRptsByPtntSorted[medind][1]) + len(testRptsByPtntSorted[medind-1][1]))/2.0
    else:
        trnmed = len(testRptsByPtntSorted[medind][1])

    q1ind = int(len(trnRptsByPtntSorted)*0.25) + 1
    q3ind = int(len(trnRptsByPtntSorted*0.75))

    q1 = len(trnRptsByPtntSorted[q1ind][1])
    q3 = len(trnRptsByPtntSorted[q3ind][1])

    #trnSetIds = getPtntIdSet(trnFilterFn)
    #testSetIds = getPtntIdSet(testFilterFn)

    #outlines = []
    #outlines.append('numTrnRpts: %d'%(getNumReports(trndir, trnSetIds)))
    #outlines.append('numTestRpts: %d'%(getNumReports(testdir, testSetIds)))
    #outlines.append('numTrnPtntsWithRpt: %d'%(getNumPtnts(trndir, trnSetIds)))
    #outlines.append('numTestPtntsWithRpt: %d'%(getNumPtnts(testdir, testSetIds)))

    #si.myos.writelines(outlines, outfn)