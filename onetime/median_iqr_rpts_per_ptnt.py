'''
Author: Scott Halgrim
Date: 7/27/12
Functionality: "Onetime" code used to determine the median and IQR
               number of reports per patient in the training, test,
               and all sets.
               Does it with and without zero-report patients.  Gives
               both sets of numbers.
'''
import std_import as si
import re, copy
from org.ghri.shalgrim.onetime.num_rpts_ptnts_w_reports import PNUM

# get module logger
logger = si.logging.getLogger('org.ghri.shalgrim.onetime.median_iqr_rpts_per_ptnt')

def getRptNamesByPID(adir, pidfn, includeZeroRptPtnts=True):
    '''
    Given a directory of pathology reports named in such a way that the filename
    encodes the patient id according to the PNUM regex, a filename of a file 
    containing a list of patients in the cohort, this function returns a dict
    of patient IDs (as a string of an int) with the filenames belonging to that
    patient.
    If includeZeroRptPtnts is True, then all patients in that file are returned.
    Those with no reports have an empty list as their value.
    If includeZeroRptPtnts is False, then only those patients in the file and
    who have reprots are returned.
    '''

    # initialize dict to have every pid with empty list
    rptNamesByPID = {line.strip():[] for line in si.myos.readlines(pidfn)}
    fns = si.os.listdir(adir)             # get all filenames

    for fn in fns:                          # for each filename
        pid = PNUM.search(fn).group()       # get patient ID

        try:
            rptNamesByPID[pid].append(fn)   # add filename to list for that pid
        except KeyError:                    
            pass                            # if that ptnt not in list skip

    # filter out patients with zero reports if appropriate
    if not includeZeroRptPtnts:
        rptNamesByPid = {k:v for k, v in rptNamesByPid.items() if len(v) > 0}

    return rptNamesByPID

def getQuartileVals(rptsByPtnt):
    '''
    From a dict whose keys are ptnt IDs and whose values are lists of the reports
    for that patient, calculates the median, and IQR q3 and q1 vals for the number
    of reports for the set.
    '''

    # turn dict into list sorted by length of number of reports
    rptsByPtntSorted = sorted(rptsByPtnt.items(), key=lambda (k, v): len(v))

    # get median index
    medind = len(rptsByPtntSorted)/2

    # get median
    if len(rptsByPtntSorted)%2 == 0:
        med = (len(rptsByPtntSorted[medind][1]) + len(rptsByPtntSorted[medind-1][1]))/2.0
    else:
        med = len(rptsByPtntSorted[medind][1])


    #get quartile indexes
    # TODO: These wouldn't have made a difference for this data
    #       but I should change the calcs to match with page 34 in my stats book
    q1ind = int(len(rptsByPtntSorted)*0.25) + 1
    q3ind = int(len(rptsByPtntSorted)*0.75)

    # geat quartile values
    q1 = len(rptsByPtntSorted[q1ind][1])
    q3 = len(rptsByPtntSorted[q3ind][1])

    return (q1, med, q3)



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


    trnRptsByPtnt = getRptNamesByPID(trndir, trnFilterFn)
    testRptsByPtnt = getRptNamesByPID(testdir, testFilterFn)

    # make all dict.  could make into util function
    # first verify there's no overlap in patients
    assert len(set(trnRptsByPtnt.keys()).intersection(set(testRptsByPtnt.keys()))) == 0

    allRptsByPtnt = copy.copy(trnRptsByPtnt)        # then initialize by copying train

    for k, v in testRptsByPtnt.items():             # then add those from test
        allRptsByPtnt[k] = v

    # get q1, med, and q3 for train, test, and all sets
    trnq1, trnmed, trnq3 = getQuartileVals(trnRptsByPtnt)
    testq1, testmed, testq3 = getQuartileVals(testRptsByPtnt)
    allq1, allmed, allq3 = getQuartileVals(allRptsByPtnt)

    # create output for the numbers when 0-rpt ptnts included
    outlines = ['WITH ZERO REPORT PATIENTS']
    outlines.append('TRAIN q1: %.1f, median: %.1f, q3: %.1f'%(trnq1, trnmed, trnq3))
    outlines.append('TEST q1: %.1f, median: %.1f, q3: %.1f'%(testq1, testmed, testq3))
    outlines.append('ALL q1: %.1f, median: %.1f, q3: %.1f'%(allq1, allmed, allq3))

    # run it again but remove zero-report patients
    trnq1, trnmed, trnq3 = getQuartileVals({k:v for k, v in trnRptsByPtnt.items() if len(v) > 0})
    testq1, testmed, testq3 = getQuartileVals({k:v for k, v in testRptsByPtnt.items() if len(v) > 0})
    allq1, allmed, allq3 = getQuartileVals({k:v for k, v in allRptsByPtnt.items() if len(v) > 0})

    # create output for when 0-rpt ptnts excluded
    outlines.append('WITHOUT ZERO REPORT PATIENTS')
    outlines.append('TRAIN q1: %.1f, median: %.1f, q3: %.1f'%(trnq1, trnmed, trnq3))
    outlines.append('TEST q1: %.1f, median: %.1f, q3: %.1f'%(testq1, testmed, testq3))
    outlines.append('ALL q1: %.1f, median: %.1f, q3: %.1f'%(allq1, allmed, allq3))

    si.myos.writelines(outlines, outfn)