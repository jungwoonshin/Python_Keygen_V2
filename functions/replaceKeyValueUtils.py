from keygen_functions import *
from getOauthKey import *
import hashlib
from datetime import datetime, timedelta
import sys
# from UrlUtils import isUrlRequest, getMachineAppropirateTestsUrls
from UrlUtils import *
from keygen_helper import getMD5Key

sys.path.append('../outputs')


def getOutputXmlFileName(machine):

	oAuthIsValidUntil = datetime.now() + timedelta(hours=6)
	oAuthIsValidUntil = oAuthIsValidUntil.strftime("%Y-%m-%d-%H:%M")

	Md5keyIsValidUntil= datetime.now() + timedelta(days=1)
	Md5keyIsValidUntil = Md5keyIsValidUntil.strftime("%Y-%m-%d")

	outputFileNameYesValidationTime =  'outputs/' + machine +'_oauth_'+ str(oAuthIsValidUntil) +'_md5_'+Md5keyIsValidUntil +'.txt'
	outputFileNameNoValidatation = 'outputs/' + machine + '.txt'

	return outputFileNameNoValidatation

def getKeyValue(machineAppropirateUrlAddress,oauthTokenList):

	queryStr = machineAppropirateUrlAddress.split('?')[1]
	queryType = getQueryType(machineAppropirateUrlAddress)
	pc = getPc(machineAppropirateUrlAddress)
	pcVal = pc.split('=')[1]
	# pcVal = pcVal.lower()

	# this is oauth
	if '/v3' in machineAppropirateUrlAddress or '/v4' in machineAppropirateUrlAddress or '/v2' in machineAppropirateUrlAddress:
		key = oauthTokenList[pcVal]
	else:
		key = getMD5Key(queryStr, queryType, pcVal)

	return key

def getOldKeyIndexes(machineAppropirateUrlAddress):
	oldKeyValStartIndex = machineAppropirateUrlAddress.find('key=') + 5
	oldKeyVal = machineAppropirateUrlAddress[oldKeyValStartIndex:].split('&')[0]
	oldKeyValEndIndex = machineAppropirateUrlAddress.find(oldKeyVal) + len(oldKeyVal)
	return (oldKeyValStartIndex, oldKeyValEndIndex)

def getUnproccessedLineOrUrlAddressWithFreshKey(machine, line, oauthTokenList):
	
	if isUrlRequest(line):
		machineAppropirateUrlAddress = getMachineAppropirateTestsUrls(line, machine)
		
		if containsKeyParamter(machineAppropirateUrlAddress):
			freshKeyValue = getKeyValue(machineAppropirateUrlAddress,oauthTokenList)
			(oldKeyValStartIndex, oldKeyValEndIndex) = getOldKeyIndexes(machineAppropirateUrlAddress)
			urlAddressWithFreshKey = machineAppropirateUrlAddress[:oldKeyValStartIndex-1] + freshKeyValue +machineAppropirateUrlAddress[oldKeyValEndIndex:]
			machineAppropirateUrlAddress = urlAddressWithFreshKey

		return machineAppropirateUrlAddress

	else:
		return line

def writeResultsFile(machine, inputEndpointFile):

	oauthTokenList = {'ZoomTestQA': getOauthToken(machine,'ZoomTestQA'), 'ZoomTestQAEnhanced': getOauthToken(machine,'ZoomTestQAEnhanced'),\
				'ZoomTestQAPackageFullContact': getOauthToken(machine,'ZoomTestQAPackageFullContact'),\
				 'ZoomTestQAPackagePreviewWithName': getOauthToken(machine,'ZoomTestQAPackagePreviewWithName'),\
				'ZoomTestQAPackagePreview': getOauthToken(machine,'ZoomTestQAPackagePreview')}

	outputXmlFileName = str(getOutputXmlFileName(machine))
	outputXmlFile = open(outputXmlFileName,'w')

	outputXmlFile.write('Current Time: ' + str(datetime.now()))
	outputXmlFile.write('\n\noauthTokenList generated was...... ' + str(oauthTokenList) +'\n\n\n\n\n')

	print('==========================Start  writing============================')

	with open(inputEndpointFile) as f:
		for line in f:
			lineToBeWritten = getUnproccessedLineOrUrlAddressWithFreshKey(machine, line, oauthTokenList)
			outputXmlFile.write(lineToBeWritten +'\n')

	print('==========================complete writing============================')
	print('\n------------------ files were saved into -------------------')
	print('------------------' + outputXmlFileName +'------------------')

	outputXmlFile.close()

	return outputXmlFileName
















