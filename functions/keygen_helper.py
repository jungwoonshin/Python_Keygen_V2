
# python keygenerator.py --p 123456 --u SF_PremiumQA --qt person_search --qs "emailAddress=adam.alami@zoominfo.com&firstName=adam&lastName=alami"

from keygen_functions import *
from getOauthKey import *
from QueryTypeAndDomainListConfig import *
from UrlUtils import *

import hashlib
from datetime import datetime, timedelta
import sys
sys.path.append('../outputs')

def getParametersDict(password, queryString,queryType):
	parameters = queryString.split('&')
	parametersDict = []
	for i in range(0,len(parameters)):
		fieldAndValue = parameters[i].split('=')
		parametersDict.append((fieldAndValue[0].lower(),fieldAndValue[1]))
	return parametersDict

def getKeyAfterMD5Key(queryString, queryType):
	FinalKeyBeforeMD5 = getKeyBeforeMD5(queryString, queryType)
	FinalKeyAfterMD5 = getMD5(FinalKeyBeforeMD5)
	return FinalKeyAfterMD5

def	getBeforeMD5(line):

	if 'key=' in line:
		pc = getPc(line)
		queryStr = line.split('?')[1]
		query_type = getQueryType(line)
		key = getMD5Key(queryStr,query_type,pc)
		KeyParamStartingindex = line.find('key=') + 5
		
		if '&' in line:
			queryStrStartingWithKey = line[KeyParamStartingindex:]
			keyVal = queryStrStartingWithKey.split('&')[0]
			
			# this is oauth
			if '-' in keyVal:
				return 'This is oauth so there is no key value before encryption'

			keyValStartIndex = line.find(keyVal)
			keyValEndIndex = line.find(keyVal) + len(keyVal)
			pcVal = pc.split('=')[1].lower()

			password = getPassword(pcVal)
			return getKeyBeforeMD5(queryStr, query_type, password)

	# there is no key.		
	return line


def	getBeforeMD5fromUrlAddress(line):
	queryStr = line.split('?')[1]
	queryType = getQueryType(line)
	key = getMD5Key(queryStr,queryType)
	KeyParamStartingindex = line.find('key=') + 5
	queryStrStartingWithKey = line[KeyParamStartingindex:]
	keyVal = queryStrStartingWithKey.split('&')[0]
	# this is oauth
	if '-' in keyVal:
		return 'This is oauth so there is no key value before encryption'
	keyValStartIndex = line.find(keyVal)
	keyValEndIndex = line.find(keyVal) + len(keyVal)
	return getKeyBeforeMD5(queryStr, query_type)

def getKeyBeforeMD5(queryString, queryType, password):
	# print('queryType',queryType)
	# this is a special case for usage query
	if (queryType == 'usage_query'):
		return getOnlyPasswordAndDateWithMD5(password)
	# if(queryType is 'authn_pro')
	if (queryType == 'authn_pro'):
		return getSpecialCaseWithMD5('aptetestPass')
	if (queryType == 'dec_company'):
		# print('sadasdu219302390129301293090')
		return getSpecialCaseWithMD5('teoN1,123456')

	parametersDict = getParametersDict(password, queryString,queryType)
	totalList = getTotalList()
	query_type = totalList[queryType]
	FinalKeyBeforeMD5 = addPasswordAndDate('',query_type,parametersDict,password)
	return FinalKeyBeforeMD5

def getPassword(pc):
	if '=' in pc:
		pc = pc.split('=')[1]
	pc = pc.lower()
	# print('pc',pc)

	passwordDict = {'zoomtestqa':'123456','zoomtestqaenhanced':'123456','default':'testing123'}
	if pc in passwordDict:
		password = passwordDict[pc]
	else:
		password = passwordDict['default']
	return password

def getMD5Key(queryString, queryType, pcVal):
	password = getPassword(pcVal)
	# print('pcVal',pcVal)
	# print('password',password)
	FinalKeyBeforeMD5 = getKeyBeforeMD5(queryString, queryType, password)
	FinalKeyAfterMD5 = getMD5(FinalKeyBeforeMD5)
	# print('FinalKeyBeforeMD5',FinalKeyBeforeMD5)
	# print('FinalKeyAfterMD5',FinalKeyAfterMD5)
	return FinalKeyAfterMD5

def checkWhetherMachineIsCorrect(machine):
	if not (machine in getDomainList()):
		print('Machine you have specified is not appropirate. We will not generate or run any endpoints.')
		exit()


# print(getMD5(getSpecialCaseWithMD5('abLd1,123456')))

# print(getMD5(getSpecialCaseWithMD5('teoN1,123456')))