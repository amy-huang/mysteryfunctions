import csv
import sys
from Levenshtein import *
from datetime import *
from mf_classes import *

if len(sys.argv) != 2:
	print("Usage: python3 csv_parser.py <csv name>")
	exit(1)
CSV = sys.argv[1]

TEST_ID = "eadelacr"
UNICODE_START = 257
NUM_CHARS_MAX = 300 # exact num is 239

"""
Map ids to each row list
configure weighted DL using each input
each fcn type
"""
idsToRows = {}
seenNums = {}
inputs = {}
charaMappings = {}

# empty list is empty string,
# which DL can use
def numsToCharas(nums):
	result = ""
	for num in nums.split():
		result += charaMappings[num]
	return result

def recordSeenVals(inp, out, realOut):
	for num in inp.split():
			seenNums[num] = True

	for num in out.split():
		seenNums[num] = True

	for num in realOut.split():
		seenNums[num] = True

def makeCharaMappings():
	sortedKeys = sorted(seenNums.keys())
	for i in range(len(sortedKeys)):
		charaMappings[sortedKeys[i]] = chr(i + UNICODE_START)


#########################################################################

# Sequential input similarity analysis
subjects = {} # ID to Subject
inputs_per_fcn = {}
# fcn -> ID -> list of inputs eval'd before 1st quiz attempt

with open(CSV, newline='') as csvfile:
	rows = csv.reader(csvfile, delimiter=',')
	header = next(rows) # header

	subject = None

	for row in rows:
		ID = row[0]
		if subject == None:
			subject = Subject(ID)
		elif ID != subject.ID:
			subjects[subject.ID] = subject
			subject = Subject(ID)

		fcn = row[1]
		if fcn not in subject.actions:
			subject.actions[fcn] = []

		key = row[2]
		time = row[4]
		actType = row[3]
		action = None

		if (actType == "eval_input"):
			action = EvalInput(key, time)
			inp = row[5]
			out = row[6]
			action.setInputOutput(inp, out)

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
			#print(action)

		elif (actType == "final_answer"):
			action = FinalAnswer(key, time)
			guess = row[10]
			action.setGuess(guess)
		else:
			print("unknown action type")

		subject.addAction(fcn, action)

# For each person's function session, look at 
# differences between eval input until next subject

for ID in subjects:
	#print(subjects[s])
	for fcn in subjects[ID].actions:
		lastIn = None
		for act in subjects[ID].actions[fcn]:
			if type(act) == EvalInput:
				inCharas = numsToCharas(act.input)
				# compare with the last input eval'd, if existent
				if lastIn == None:
					lastIn = inCharas
					continue
				# convert this input to string, and take distance
				d = distance(lastIn, inCharas)
				print(d)
				print()
			elif type(act) == QuizQ or type(act) == FinalAnswer:
				# go to next fcn session
				break
			else:
				print("unknown action type")

# makeCharaMappings()

# for p in idsToRows:
# 	inp = idsToRows[p][5]
# 	# print(idsToRows)
# 	print("======")
# 	# print(inp)
# 	asChara = numsToCharas(inp)
# 	print(asChara)
	# for c in asChara:
	# 	print("'" + str(ord(c)) + "'")

