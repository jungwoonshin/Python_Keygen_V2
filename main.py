
import argparse
from generatePostTestUrlFiles import *
from generateNonPostTestUrlFiles import * 

def getArguments():

	parser = argparse.ArgumentParser(description='This is a script that can test Partner API urls endpoints. \n\n \
		To use this script, you need to specify two things. \n\n \
		1. Machine \n\
		2. Request Type. \n\
		For example, you can type the following command: python main.py --m \'production01\' --t \'apigetrequests\'\n\
		For more information, type python main.py --help.')

	parser.add_argument('--m', metavar='machine', type=str, 
		help='Choose a machine that will be tested. \n \
		Examples) local, staging01, staging02, staging03, production01, production02, production03, production04.\n \
	** NOTE: Only get requests are available on production04 machine.')

	parser.add_argument('--m2', metavar='machine2', type=str, 
		help='Choose a machine2 that will be compared with machine. \n \
		Examples) local, staging01, staging02, staging03, production01, production02, production03, production04.\n \
	** NOTE: Only get requests are available on production04 machine.')

	parser.add_argument('--t', metavar='testType', type=str, 
		help='Options: 1. apiGetRequests\n 2. fcGetRequests\n 3. allPostRequests\n 4. oauthRequests (All values are case-insensitive)\n 5. compareTwoMachines \n')

	args = parser.parse_args()
	machine = args.m
	machine2 = args.m2
	testType = args.t
	machine = machine.lower()
	machine2 = machine2.lower()
	testType = testType.lower()

	return (machine, machine2, testType)

def validateInput(machine, machine2, testType):

	machineList = ['local', 'staging01', 'staging02', 'staging03', 'production01', 'production02', 'production03', 'production04']
	testTypeList = ['apigetrequests','fcgetrequests','allpostrequests','oauthrequests','comparetwomachines']

	if not (machine in machineList) :
		print('Please input correct Machine.')
		exit()

	if not (machine2 in machineList) :
		print('Please input correct Machine.')
		exit()

	if not (testType in testTypeList):
		print('Please input correct testType.')
		exit()

def runAppropirateTest(testType, machine, machine2):

	print '========================================================\n\n\n\n'

	if testType == 'apigetrequests':
		print 'NOW STARTING TO RUN API GET REQUESTS'
		print '\n\n\n========================================================\n\n\n\n'
		runGetRequests(machine)
	
	elif testType == 'fcgetrequests':
		print 'NOW STARTING TO RUN FC GET REQUESTS'
		print '\n\n\n========================================================\n\n\n\n'
		runOverallFormComplete(machine)
	
	elif testType == 'allpostrequests':
		print 'NOW STARTING TO RUN FC POST REQUESTS\n\n'
		print 'Please make sure you \n'
		print '(1) run this script locally'
		print '(2) delploy partnerapikey.war'
		print '\n\n\n========================================================\n\n\n\n'
		runPostFormCompleteOverallTest(machine)
	
	elif testType == 'oauthrequests':
		print 'NOW STARTING TO RUN OAUTH REQUESTS'
		print '\n\n\n========================================================\n\n\n\n'
		runOauthRequests(machine)

	elif testType == 'comparetwomachines':
		print 'NOW STARTING TO RUN Compare Two machines'
		print 'Please make sure you \n'
		print 'Specified both --m and --m2 which are machines to be tested'
		print '\n\n\n========================================================\n\n\n\n'
		compareTwoMachines(machine, machine2)


(machine, machine2, testType) = getArguments()
validateInput(machine, machine2, testType)
runAppropirateTest(testType, machine, machine2)











