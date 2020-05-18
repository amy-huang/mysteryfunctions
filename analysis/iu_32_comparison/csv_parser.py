import csv
import sys
from datetime import *
from action_classes import *
from statistics import *

from Levenshtein import distance, editops
from distance import jaccard
from stringdist import rdlevenshtein, levenshtein

from sklearn.cluster import KMeans
import numpy as np

if len(sys.argv) < 3:
    print("Usage: python3 csv_parser.py <csv0> <fcns>")
    exit(1)

#################################################################
# Making the character mappings for input similarity comparison

# Values seen in inputs, outputs, actual outputs
seenNums = {}
# Mapping seen value to unicode chara
charaMappings = {}
# For where to start mappings
UNICODE_START = 0

def getVals(fcn, isIn, inOrOut):
    valType = None
    if isIn == True:
        valType = in_out_types[fcn][0]
    else: 
        valType = in_out_types[fcn][1]

    # Get vals based on arg count
    if num_inputs[fcn] > 1:
        args = inOrOut.split()
        if isIn == True and len(args) != num_inputs[fcn]:
            # print("error, num args does not match args found")
            # print(fcn)
            # print(args)
            # for 2 inp fcns
            args = inOrOut.split(",")

        vals = []
        for a in args:
            vals += valType.getNums(a)
        return vals

    elif num_inputs[fcn] == 1:
        return valType.getNums(inOrOut)

    else:
        print("error, > 1 args for fcn")

def recordSeenVals(someVals):
    for val in someVals:
        seenNums[val] = True

# Sort seen nums and assign them to characters
def makeCharaMappings():
    sortedKeys = sorted(seenNums.keys())
    # print("num unique charas", len(sortedKeys))
    # print(sortedKeys)
    for i in range(len(sortedKeys)):
        charaMappings[sortedKeys[i]] = chr(i + UNICODE_START)

def inducedDiff(first, second: EvalInput):
    # firstNum = int(first.input)
    # secondNum = int(second.input)
    # return abs(firstNum - secondNum)
    return rdlevenshtein(first.input, second.input)

def inducedEditOps(first, second: EvalInput):
    return editops(first.input, second.input)

def inputEditOps(fcn:str, first, second: EvalInput):
    if fcn == "Induced":
        return inducedEditOps(first, second)

    inType = in_out_types[fcn][0]
    firstCharas = inType.toCharas(first.input)
    secondCharas = inType.toCharas(second.input)
    return editops(firstCharas, secondCharas)

def opsToNum(ops):
    if len(ops) == 0:
        return 0

    num = ""
    for op in ops:
        if op[0] == "insert":
            num += "1"
        if op[0] == "delete":
            num += "2"
        if op[0] == "replace":
            num += "3"
        num += str(op[1])
        num += str(op[2])
    return int(num)

def inputDifference(fcn:str, first, second: EvalInput):
    if fcn == "Induced":
        return inducedDiff(first, second)

    inType = in_out_types[fcn][0]
    firstCharas = inType.toCharas(first.input)
    secondCharas = inType.toCharas(second.input)
    return rdlevenshtein(firstCharas, secondCharas)

class Bool:
	@staticmethod
	def getNums(val):
		if val == "true":
			return "1"
		return ["0"]

	@staticmethod
	def toCharas(val):
		return charaMappings[val]

class Int:
	@staticmethod
	def getNums(val):
		return [val]

	@staticmethod
	def toCharas(val):
		# return str(val)
		return charaMappings[val]

class ListInt:
	@staticmethod
	def getNums(val):
		nums = val.split()
		return nums

	@staticmethod
	def toCharas(val):
		charas = ""
		nums = val.split()
		for n in nums:
			# charas += chr(int(n))
			charas += charaMappings[n]
		return charas

class Float:
	@staticmethod
	def getNums(val):
		return [val]

	@staticmethod
	def toCharas(val):
		# return str(val)
		return charaMappings[val]

# Function input and output types
in_out_types = {
    "Average": [ListInt, Float],
    "Median": [ListInt, Float],
    "SumParityInt": [ListInt, Int],
    "SumParityBool": [ListInt, Bool],
    "Induced": [Int, Int],
    "EvenlyDividesIntoFirst": [ListInt, Bool],
    "SecondIntoFirstDivisible": [ListInt, Bool],
    "FirstIntoSecondDivisible": [ListInt, Bool],
    "SumBetween": [ListInt, Int],
}

# Number of inputs per function
num_inputs = {
    "Average": 1,
    "Median": 1,
    "SumParityInt": 1,
    "SumParityBool": 1,
    "Induced": 1,
    "EvenlyDividesIntoFirst": 2,
    "FirstIntoSecondDivisible": 2,
    "SecondIntoFirstDivisible": 2,
    "SumBetween": 2,
}

# Just the names
FCN_NAMES = ["Average", "Median", "SumParityBool", "SumParityInt", "SumBetween", "Induced"]

#################################################################

if __name__ == "__main__":
    # Do initial recording of each subject's traces
    idsToSubs = {}
    with open(sys.argv[1], newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        header = next(rows) # header

        # Current subject we're recording actions for
        subject = None

        for row in rows:
            # See if we need to start a new Subject
            ID = row[0]
            if subject == None:
                subject = Subject(ID)
                idsToSubs[ID] = subject
            elif ID != subject.ID:
                subject = Subject(ID)
                idsToSubs[ID] = subject

            fcnName = row[1]
            key = row[2]
            time = row[4]
            actType = row[3]
            action = None

            inType = in_out_types[fcnName]
            outType = in_out_types[fcnName]

            # Record specific action taken
            if (actType == "eval_input"):
                action = EvalInput(key, time)
                inp = row[5]
                out = row[6]
                action.setInputOutput(inp, out)

                recordSeenVals(getVals(fcnName, True, inp))
                recordSeenVals(getVals(fcnName, False, out))

                subject.addEvalInput(fcnName, action)

            elif (actType == "quiz_answer"):
                action = QuizQ(key, time)
                quizQ = row[7]
                inp = row[5]
                out = row[6]
                realOut = row[8]
                result = row[9]

                display = "✗"
                if (result == "true"):
                    display = "✓"

                action.setQ(quizQ, inp, out, realOut, display)

                recordSeenVals(getVals(fcnName, True, inp))
                recordSeenVals(getVals(fcnName, False, out))
                recordSeenVals(getVals(fcnName, False, realOut))

                subject.addQuizQ(fcnName, action)

            elif (actType == "final_answer"):
                action = FinalAnswer(key, time)
                guess = row[10]
                action.setGuess(guess)
                subject.addFinalAnswer(fcnName, action)
            # else:
            #     print("WARNING: unknown action type")

    # Make character mappings using the characters observed
    makeCharaMappings()

    # Distributions to look at
    COR = "COR"
    MCOR = "MCOR"
    SCOR = "SCOR"
    XCOR = "XCOR"

    # Get fine grained tags 
    for whichFile in ["32", "IU"]:
        for fcn in FCN_NAMES:
            with open("answer_labels/{} fine grained labels - {}.csv".format(whichFile, fcn), newline='') as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                header = next(rows) # header

                for row in rows:
                    ID = row[0]
                    answer = row[1]
                    tags = []
                    for i in range(2, len(row)):
                        enteredTags = row[i].split()
                        for tag in enteredTags:
                            if tag != '':
                                tags.append(tag)

                    if ID not in idsToSubs:
                        # print("WARNING: this ID has no subject", ID)
                        continue
                    if idsToSubs[ID] == None:
                        # print("WARNING: this ID has None subject", ID)
                        continue
                    if idsToSubs[ID].didFcn(fcn):
                        idsToSubs[ID].addAnswerTags(fcn, tags)

    # Map fcn to correctness to tag frequencies. uh oh this calls for another class!!!
    # Then we can look at each fcn's things
    tagsByRating = TagsByFcn()

    # fcn to list of diff IDs
    diffsIDs = {} 
    # fcn to list of diff lists
    diffsLists = {}

    allIDs = []
    allLists = []

    # ID and fcn to ops vector
    numOps = {}
    # ID to num op trace
    editOps = {}
    # ID to average len of same op sequence size 2 and up
    stretchLens = {}
    # from this, get line graph, avg/med, frequency

    # ops frequency, list ops to num
    opsFreq = {}

    # Open a csv for each corr rating, then go through subs and write Ls to csv
    for fcn in sys.argv[2:]:
        print(fcn)
        distros = DistributionKeeper()
        with open("COR_Ls.csv", "w") as COR_CSV:
            with open("MCOR_Ls.csv", "w") as MCOR_CSV:
                with open("SCOR_Ls.csv", "w") as SCOR_CSV:
                    with open("XCOR_Ls.csv", "w") as XCOR_CSV:
                        csv_dict = {}
                        csv_dict["COR"] = COR_CSV
                        csv_dict["MCOR"] = MCOR_CSV
                        csv_dict["SCOR"] = SCOR_CSV
                        csv_dict["XCOR"] = XCOR_CSV

                        for ID in idsToSubs.keys():
                            # Get correctness tag for answer
                            rating = None
                            tags = idsToSubs[ID].getAnswerTags(fcn)
                            if tags != None:
                                if "COR" in tags:
                                    rating = "COR"
                                elif "MCOR" in tags:
                                    rating = "MCOR"
                                elif "SCOR" in tags:
                                    rating = "SCOR"
                                elif "XCOR" in tags:
                                    rating = "XCOR"
                                else:
                                    # print("ID {} fcn {} has no rating".format(ID, fcn))
                                    continue

                                tagsByRating.addTags(fcn, tags)

                                # Consec input diffs to csv
                                evals = idsToSubs[ID].functionAttempts[fcn].allEvals()
                                distros.addNumEvals(rating, len(evals))

                                csvfile = csv_dict[rating]
                                # stretchLens = "{},".format(ID)
                                maxDiff = 0
                                diffsArray = []
                                ID_FCN = "{}_{}".format(ID, fcn)
                                numOps[ID_FCN] = []

                                currOps = ""
                                currLen = 0
                                editOps[ID_FCN] = []

                                for i in range(1, len(evals)):
                                    # edit ops
                                    ops = inputEditOps(fcn, evals[i-1], evals[i])
                                    # editOps[idfcn].append(opsToNum(ops)) # encoding actual ops
                                    numOps[ID_FCN].append(len(ops))
                                    
                                    # Look at average length of same op sequences
                                    currOpsList = []
                                    for op in ops:
                                        currOpsList.append(op[0])
                                    nextOps = " ".join(sorted(currOpsList))

                                    if nextOps not in opsFreq:
                                        opsFreq[nextOps] = 0
                                    opsFreq[nextOps] += 1

                                    # Next group of operations is the same as current streak
                                    if nextOps == currOps:
                                        currLen += 1
                                    else:
                                        # If no change in input, count as part of streak, keep currOps same
                                        if len(nextOps) == 0:
                                            currLen += 1
                                        else:
                                            # Change in ops means streak just ended
                                            if len(currOps) > 0:
                                                if not ID_FCN in stretchLens:
                                                    stretchLens[ID_FCN] = []
                                                stretchLens[ID_FCN].append(currLen)
                                                editOps[ID_FCN].append(currOps)
                                                # print("{} change in op {} to {}".format(ID_FCN, currOps, nextOps))

                                            # Start new streak
                                            currOps = nextOps
                                            currLen = 1

                                    # Edit distance for writing to csv
                                    # diff = inputDifference(fcn, evals[i-1], evals[i])
                                    # diffsArray.append(diff)
                                    # line += "{},".format(diff) # raw diff

                                    # if diff > maxDiff:
                                    #     maxDiff = diff

                                # If a stretch went all the way to the end, make sure to record if max
                                if len(currOps) > 0:
                                    if not ID_FCN in stretchLens:
                                        stretchLens[ID_FCN] = []
                                    stretchLens[ID_FCN].append(currLen)
                                    editOps[ID_FCN].append(currOps)
                                    # print("{} end trace w streak {}".format(ID_FCN, currOps))

                                # Writing edit distance to csv
                                # line += "\n"
                                # csvfile.write(line)
                                distros.addMaxDiff(rating, maxDiff)

                                # Add to list of all diff traces for this fcn
                                allIDs.append("{}_{}".format(ID, fcn))
                                allLists.append(diffsArray)
                                
                                sub = idsToSubs[ID]
                                acts, EIs, QAs = sub.allFcnActions(fcn)
                                distros.addQuizAttempts(rating, len(QAs.keys()))
                                distros.addEIsBwQAs(rating, sub.ID, sub.getEvalLens(fcn))
        # Per function printouts
        # print(distros.EIsBwQAs())
        # print(distros.highestDiffs())
        # print(distros.numEvals())
        # print(distros.firstStretchStats())

        # Print edit ops
        # for ID in editOps:
        #     line = "{}, ".format(ID)
        #     for ops in editOps[ID]:
        #         line += "{}, ".format(ops)
        #     print(line)

    # # Consecutive input difference clustering
    # maxConsecLen = 0
    # for t in allLists:
    #     if len(t) > maxConsecLen:
    #         maxConsecLen = len(t)
    # # Fill with 0s
    # filled = []
    # for trace in allLists:
    #     newTrace = []
    #     for val in trace:
    #         newTrace.append(val)
    #     while len(newTrace) < maxConsecLen:
    #         newTrace.append(0)
    #     filled.append(newTrace)

    # Across all printouts
    # print("Ratings across all fcns done")
    # for ID in idsToSubs:
    #     sub = idsToSubs[ID]
    #     line = "{}, ".format(ID)
    #     # for rating in sub.answerTagsByOrder():
    #     #     line += "{}, ".format(rating)
    #     totalScore = sum(sub.answerTagsByOrder())
    #     print(line)

    # Stretch len stats
    with open("sameOps.csv", "w") as SAMEOPS:
        with open("sameOpStats.csv", "w") as SAMEOPSTATS:
            for ID_FCN in stretchLens:
                ID = ID_FCN.split("_")[0]
                FCN = ID_FCN.split("_")[1]

                lentrace = ""
                score = idsToSubs[ID].ratingsByFcn()[FCN]
                avg = 0
                median = 0
                if len(stretchLens[ID_FCN]) > 0:
                    avg = sum(stretchLens[ID_FCN]) / len(stretchLens[ID_FCN])
                    median = sorted(stretchLens[ID_FCN])[floor(len(stretchLens[ID_FCN]) / 2)]

                    lentrace += "{}, {}, {}, {}, ".format(len(editOps[ID_FCN]), FCN, score, ID)

                    # Trace of stretch lengths
                    lenDistro = {}
                    for sl in stretchLens[ID_FCN]:
                        if sl not in lenDistro:
                            lenDistro[sl] = 0
                        lenDistro[sl] += 1
                        lentrace += "{}, ".format(sl)

                    # Terminal printout of same ops stretch length distros
                    # termPrint = "{}, ".format(ID_FCN)
                    # for sl in range(sorted(lenDistro.keys())[-1] + 1):
                    #     if sl not in lenDistro:
                    #         termPrint += "0, "
                    #     else:
                    #         termPrint += "{}, ".format(lenDistro[sl])

                    alleditOps = "{}, {}, {}, {}, ".format(len(editOps[ID_FCN]), FCN, score, ID)
                    lastOps = ""
                    for ops in editOps[ID_FCN]:
                        if ops == lastOps:
                            print("ERROR {} same consecutive ops not caught {}".format(ID_FCN, ops))
                        lastOps = ops
                        alleditOps += "{}, ".format(ops)
                    alleditOps += "\n"
                    SAMEOPS.write(alleditOps)

                # # Add actual trace of ops
                # for op in editOps[ID]:
                #     line += "{}, ".format(op)
                lentrace += "\n"
                SAMEOPSTATS.write(lentrace)

    # # Most common ops between consecutive input evals
    # for ops in sorted(opsFreq.keys()):
    #     print("{}, {}".format(ops, opsFreq[ops]))

    # # Consecutive edit ops vector clustering
    # maxConsecLen = 0
    # allLists = []
    # for user in numOps:
    #     trace = numOps[user]
    #     if len(trace) > maxConsecLen:
    #         maxConsecLen = len(trace)
    #     allLists.append(numOps[user])
        
    # # Fill with 0s
    # filled = []
    # for l in allLists:
    #     newTrace = []
    #     for num in l:
    #         newTrace.append(num)
    #     while len(newTrace) < maxConsecLen:
    #         newTrace.append(0)
    #     filled.append(newTrace)

    # toCluster = np.array(filled)
    # print("WSS vals for {}".format("".join(sys.argv[2:])))
    # # Try a bunch of values for k, and record WSS for each to choose a final result
    # for k in range(1, 11):
    #     kmeans = KMeans(n_clusters = k).fit(toCluster)
    #     centroids = kmeans.cluster_centers_
    #     pred_clusters = kmeans.predict(toCluster)
    #     curr_sse = 0

    #     # Write result to CSV
    #     clusterIdxs = {}
    #     for i in range(len(kmeans.labels_)):
    #         if kmeans.labels_[i] not in clusterIdxs:
    #             clusterIdxs[kmeans.labels_[i]] = []
    #         clusterIdxs[kmeans.labels_[i]].append(i)

    #     csv_name = "{}_k{}.csv".format("".join(sys.argv[2:]), k)
    #     with open(csv_name, "w") as CSVFILE:
    #         for label in sorted(clusterIdxs.keys()):
    #             CSVFILE.write("Cluster {},\n".format(label))
    #             for idx in clusterIdxs[label]:
    #                 ID = allIDs[idx]
    #                 line = "{}, ".format(ID)
    #                 trace = allLists[idx]
    #                 for val in trace:
    #                     line += "{}, ".format(val)
    #                 line += "\n"
    #                 CSVFILE.write(line)
        
    #     # calculate square of Euclidean distance of each point from its cluster center and add to current WSS
    #     for i in range(len(toCluster)):
    #         curr_center = centroids[pred_clusters[i]]
    #         curr_sse += (toCluster[i, 0] - curr_center[0]) ** 2 + (toCluster[i, 1] - curr_center[1]) ** 2
        
    #     print("{}, {},".format(k, curr_sse))

    # print(tagsByRating)

    # print("Function distros")
    # posToFcnTotals = {}
    # for pos in range(5):
    #     posToFcnTotals[pos] = {}
    #     for fcn in FCN_NAMES:
    #         posToFcnTotals[pos][fcn] = 0
    # for ID in idsToSubs:
    #     sub = idsToSubs[ID]
    #     distro = sub.getFcnDistro()
    #     for pos in range(len(distro)):
    #         if pos in posToFcnTotals:
    #             fcn = distro[pos]
    #             if fcn in posToFcnTotals[pos]:
    #                 posToFcnTotals[pos][fcn] = posToFcnTotals[pos][fcn] + 1
    # for pos in range(5):
    #     line = "{}, ".format(pos)
    #     for fcn in FCN_NAMES:
    #         line += "{}, ".format(posToFcnTotals[pos][fcn])
    #     print(line)

    # with open("all_Ls.csv", "x") as csvfile:
    #     # Map each fcn to map of eval inputs length to list of traces from subjects
    #     # fcnToTraces = {} 
    #     for sub in idsToSubs.keys():
    #         idsToFcnTraces[sub.ID] = {}

    #         # print("{}\n\n".format(sub))
    #         # TODO: now look at input similarity and also proportions of sections by
    #         # looping over the subjects - for each subject and fcn, what is 
    #         # consec similarity look like - graphs?
    #         for fcn in sub.functionAttempts:
    #             evals = sub.functionAttempts[fcn].allEvals()

    #             # highestDiff = 0
    #             # highestDiffIdx = 0
    #             # for i in range(1, len(evals)):
    #             #     diff = inputDifference(fcn, evals[i-1], evals[i])
    #             #     if diff > highestDiff:
    #             #         highestDiff = diff
    #             #         highestDiffIdx = i-1
    #             # quizzesAttempted = 0
    #             # for idx in sub.functionAttempts[fcn].quizAttemptIndices():
    #             #     if highestDiffIdx > idx:
    #             #         quizzesAttempted += 1
    #             # csvfile.write(fcn + ", " + str(quizzesAttempted) + ",\n")

    #             # if fcn not in fcnToTraces:
    #             #     fcnToTraces[fcn] = {}
    #             # if len(evals) not in fcnToTraces[fcn]:
    #             #     fcnToTraces[fcn][len(evals)] = []
    #             # fcnToTraces[fcn][len(evals)].append(evals)

    #             idsToFcnTraces[sub.ID][fcn] = evals




