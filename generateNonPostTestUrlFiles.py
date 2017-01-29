from replaceKey import * 
from functions.keygen_functions import *
from functions.getOauthKey import *
from functions.keygen_helper import *
import xml.dom.minidom as XDM
from functions.UrlUtils import isUrlRequest
import xml.etree.ElementTree as etree

def getXMLResultOutput(urlToBeRequested):
	r = requests.get(urlToBeRequested,verify=False)
	contents = r.text.encode('utf-8')
	if len(contents) != 0:
		return XDM.parseString(contents).toprettyxml(indent="   ").encode('utf-8')
	return contents

def writeRequestAndResult(results, urlToBeRequested):
	results.write('-------------------------- Making requests ... --------------------------\n')
	results.write(urlToBeRequested)
	results.write('\n--------------------------- Key Before MD5 Encrpytion -----------------------------')
	keyBeforeMD5 = getBeforeMD5(urlToBeRequested)
	results.write('\n' + str(keyBeforeMD5) + '\n')
	results.write('---------------------------------------------------------------------------')
	xmlstr = getXMLResultOutput(urlToBeRequested)
	results.write('\n' + xmlstr + '\n')
	results.write('-------------------------- Finished making requests ------------------------')

def generateXMLOutputsBasedOnUrlFiles( testUrlAddressFileName , inputFileName):
	queryTypeFileName = inputFileName.split('/')[2].split('.')[0]
	XMLOutputResultsFileName = 'outputs/results_'+ testUrlAddressFileName.split('/')[1].split('.')[0]+'_'+ queryTypeFileName +'.txt' 
	
	results = open(XMLOutputResultsFileName, 'w') 
	results.write('Starting...... ')

	with open(testUrlAddressFileName) as f:
		for line in f:
			if isUrlRequest(line):
				print('--------------------------------------------')
				print('Making requests ... ' + line )
				urlToBeRequested = line.strip()
				writeRequestAndResult(results, urlToBeRequested)
				print('Finished ........... ')
				print('--------------------------------------------')
			else:
				results.write(line + '\n')

	print('--------------------------------------------------------------------')
	print('\n------------------ files were saved into -------------------------')
	print('------------------' + XMLOutputResultsFileName +'-------------------')
	print('--------------------------------------------------------------------\n\n\n\n')
	results.close()
	return XMLOutputResultsFileName

def elements_equal(e1, e2):
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

def elements_equal_without_text(e1, e2):

    if e1.tag != e2.tag: 
    	return False
    # if e1.text != e2.text: return False
    if e1.tail != e2.tail: 
    	return False
    if e1.attrib != e2.attrib: 
    	return False
    if len(e1) != len(e2): 
    	return False
    return all(elements_equal_without_text(c1, c2) for c1, c2 in zip(e1, e2))



    

def compareTwoXMLResultsFromDifferentMachines(machine01_outputFileName, machine02_outputFileName):

	resultFromMachine01 = []
	resultFromMachine02 = []

	XMLOutputResultsFileName = 'outputs/difference_results.txt' 

	results = open(XMLOutputResultsFileName, 'w') 

	msg = '\n\n\nStarting compare differences between \n(1) ' + machine01_outputFileName + ' and \n(2) ' + machine02_outputFileName + '\n\n\n\n\n'
	results.write(msg)

	with open(machine01_outputFileName) as f:
		for line in f:
			if isUrlRequest(line):
				urlToBeRequested = line.strip()
				xmlResult = getXMLResultOutput(urlToBeRequested)
				etreeXML = etree.XML(xmlResult)
				resultFromMachine01.append(etreeXML)

	with open(machine02_outputFileName) as f:
		for line in f:
			if isUrlRequest(line):
				urlToBeRequested = line.strip()
				xmlResult = getXMLResultOutput(urlToBeRequested)
				etreeXML = etree.XML(xmlResult)
				resultFromMachine02.append(etreeXML)

	# print('resultFromMachine01',resultFromMachine01)
	# print('resultFromMachine02',resultFromMachine02)

	resultLengthMachine01 = len(resultFromMachine01)
	resultLengthMachine02 = len(resultFromMachine02)

	print(resultLengthMachine01)
	print(resultLengthMachine02)

	numElementsAndValueMatchingResults = 0
	numElementsMatchingResults = 0
	numUnmatchingResults = 0

	if resultLengthMachine01 != resultLengthMachine02:
		print 'The two two machine had different Number of responses. Terminating program'
		exit()

	else:
		differences = []

		for i in range(0, resultLengthMachine01):
			res1 = resultFromMachine01[i]
			res2 = resultFromMachine02[i]

			if elements_equal(res1, res2) :
				numElementsAndValueMatchingResults += 1
			elif elements_equal_without_text(res1,res2): 
				numElementsMatchingResults += 1
			else:
				res1 = etree.tostring(res1)
				res2 = etree.tostring(res2)

				difference = str(machine01_outputFileName) + ': ' + str(res1) + '\n'
				difference += str(machine02_outputFileName) + ': ' + str(res2)
				differences.append(difference)

				numUnmatchingResults += 1
				
		print('numElementsAndValueMatchingResults',numElementsAndValueMatchingResults)
		print('numElementsMatchingResults',numElementsMatchingResults)
		print('numUnmatchingResults',numUnmatchingResults)

		results.write('\n\n\nNumber of Exactly Matching Results: ' + str(numElementsAndValueMatchingResults) + '\n')
		results.write('\n\n\nNumber of Element Only Matching Results: ' + str(numElementsMatchingResults) + '\n')
		results.write('\n\n\nNumber of Unmatching Result: ' + str(numUnmatchingResults) + '\n')

		results.write('\n\n\Details of Unmatching results: ' + str(numUnmatchingResults) + '\n')
		differencesLength = len(differences)

		if differencesLength is 0:
			results.write('There was no different between etrees in terms of tag, tail, attrib. For details, read python etree docs.')
		else:
			for i in range(0, differencesLength):
				results.write('\n' + differences[i] + '\n')

		return XMLOutputResultsFileName

def compareTwoMachines(machine01, machine02):
	if not machine01 in getDomainList() or not machine02 in getDomainList():
		print('Machine you have specified is not appropirate. We will not generate or run any endpoints.')
		exit()

	machine01_outputFileName = generateEndpoints(machine01,'inputs/DivideAndConquer/api_get_requests.txt')
	machine02_outputFileName = generateEndpoints(machine02,'inputs/DivideAndConquer/api_get_requests.txt')
	testResultFileName = compareTwoXMLResultsFromDifferentMachines(machine01_outputFileName, machine02_outputFileName)
	print('Files were saved into ', testResultFileName)

def runGetRequests(machine):
	if not (machine in getDomainList()):
		print('Machine you have specified is not appropirate. We will not generate or run any endpoints.')
		exit()

	# run All non-post request queries except Form Complete
	inputFileName = 'inputs/DivideAndConquer/api_get_requests.txt'
	p01_outputFileName = generateEndpoints(machine,inputFileName)
	generateXMLOutputsBasedOnUrlFiles(p01_outputFileName,inputFileName)

def runOauthRequests(machine):
	
	checkWhetherMachineIsCorrect(machine)

	# only check server status for all oauth web app
	inputFileName = 'inputs/DivideAndConquer/oauth_requests.txt'
	p01_outputFileName = 'inputs/DivideAndConquer/oauth_requests_server_status.txt'

	queryTypeFileName = inputFileName.split('/')[2].split('.')[0]
	oauthOutputFileName = 'outputs/results_' + queryTypeFileName +'.txt'

	if machine == 'production01':
		generateXMLOutputsBasedOnUrlFiles(p01_outputFileName,inputFileName)

	print('oauthOutputFileName',oauthOutputFileName)
	print('Writing to ......' ,oauthOutputFileName)
	results = open(oauthOutputFileName, 'a') 

	# # # ----------------------------------------
	# # #  Get oauth Token TO PARTNERAPI SERVER:
	# # # ----------------------------------------
	zoomTestQAEnhancedOauthToken = getOauthToken(machine, 'ZoomTestQAEnhanced')
	print('\nget oauthToken using PartnerAPIApp',zoomTestQAEnhancedOauthToken)
	results.write('\n\n\n\nTEST OAUTH GENERATE: ' + machine + '\nget oauthToken using PartnerAPIapp: ' + zoomTestQAEnhancedOauthToken)
	print('\n\n\n')

	# # # ----------------------------------------
	# # #  Token validate DIRECTLY TO OAUTH SERVER:
	# # # ----------------------------------------
	# tokenValidate = validateDirectlyFromOauthapp(machine)
	# print('tokenValidate directly from oauth',tokenValidate)
	# print('\n\n\n')

	# # # ----------------------------------------
	# # #  Get oauth Token DIRECTLY TO OAUTH SERVER:
	# # # ----------------------------------------
	getToken = getDirectlyFromOauthappOauthToken(machine)
	print('get oauthToken using OauthWebapp',getToken)
	results.write('\nget oauthToken using OauthWebapp: ' + getToken)
	results.write('\n\n---------------------------------------------------------------------\n\n\n')

	print('\n\n\n')

	print('--------------------------------------------------------------------')
	print('\n------------------ files were saved into -------------------------')
	print('------------------' + oauthOutputFileName +'-------------------')
	print('--------------------------------------------------------------------\n\n\n\n')
	# results.close()

# run form complete output xmls
def runOverallFormComplete(machine):
	machine = machine + 'fc'

	if not (machine in getDomainList()):
		print('Machine you have specified is not appropirate. We will not generate or run any endpoints.')
		exit()

	formCompleteTestUrlFileName = 'inputs/DivideAndConquer/fc_get_requests.txt'
	p01_fc_outputFileName = generateEndpoints(machine,formCompleteTestUrlFileName)
	generateXMLOutputsBasedOnUrlFiles(p01_fc_outputFileName,formCompleteTestUrlFileName)

# run whole script
# machine = 'production01'

# runGetRequests(machine)
# runOverallFormComplete(machine)





