import datetime
import hashlib

def getPassword(pc):
	if '=' in pc:
		pc = pc.split('=')[1]
	pc = pc.lower()

	passwordDict = {'zoomtestqa':'123456','zoomtestqaenhanced':'123456','default':'testing123'}
	if pc in passwordDict:
		password = passwordDict[pc]
	else:
		password = passwordDict['default']
	return password

def getFullUrlAddress(queryString, queryType,FinalKeyAfterMD5):

	addressFront = 'http://localhost:8080/partnerapi/'
	getUrlAddressByQueryType = {'person_search':'person/search?','company_search':'company/search?','company_mach':'company/match?',
									'person_match':'person/match?','person_detail':'person/detail?','company_detail':'company/detail?','authn_pro':'zoom/authn/pro?',
									'credits_decrement':'zoom/credits/dec/person?','credits_decrement':'zoom/credits/dec/company?',
									'formcomplete':'labs/formcomplete?'}

	params = queryString.split('&')
	queryStringWithoutKey = None
	
	for p in params:
		if p.find('key=') is not -1:
			keyStartIndex = queryString.find('key=')
			keyEndIndex = keyStartIndex + len(p)

			# print 'queryString', queryString
			# print 'queryString[:keyStartIndex-1]',queryString[:keyStartIndex-1]
			# print 'queryString[keyEndIndex+1:]', queryString[keyEndIndex+1:]
			queryStringWithoutKey = queryString[:keyStartIndex-1] + queryString[keyEndIndex+1:]
			break

	if queryStringWithoutKey is None:
		queryStringWithoutKey = queryString

	queryStringWithUpToDateKey = queryStringWithoutKey +'&key=' + FinalKeyAfterMD5
	fullAddress = addressFront + getUrlAddressByQueryType[queryType] + queryStringWithUpToDateKey
	return fullAddress

def getMD5(beforemd5):
	m = hashlib.md5()
	m.update(beforemd5.encode('utf-8'))
	return m.hexdigest()

# def computeMD5hash(string):
#     m = hashlib.md5()
#     m.update(string.encode('utf-8'))
#     return m.hexdigest()

def listIntoLowerCase(totalList):	
	for i in totalList.keys():
		toBeLowercased = totalList[i]
		for j in range(0,len(toBeLowercased)):
			toBeLowercased[j] = toBeLowercased[j].lower()

def addPasswordAndDate(FinalKeyBeforeMD5,query_type,parametersDict,password):
	# print('query_type',query_type)
	for j in range(0,len(query_type)):
		for i in range(0,len(parametersDict)):
			if(query_type[j] == parametersDict[i][0]):
				# print('parametersDict[i][1][:2]',parametersDict[i][1][:2])
				FinalKeyBeforeMD5 = FinalKeyBeforeMD5 + parametersDict[i][1][:2]
				parametersDict.remove(parametersDict[i])
				break

	forPrintBeforeMD5 = FinalKeyBeforeMD5 + '  ' + str(password)

	FinalKeyBeforeMD5 = FinalKeyBeforeMD5 + str(password)
	dateTimeNow = datetime.datetime.now()

	year = str(dateTimeNow.year)
	month = str(dateTimeNow.month)
	date = str(dateTimeNow.day)
	forPrintBeforeMD5 = forPrintBeforeMD5 + '  ' + date +  month + year
	FinalKeyBeforeMD5 = FinalKeyBeforeMD5 + date + month + year
	
	return FinalKeyBeforeMD5

def getOnlyPasswordAndDateWithMD5(password):
	FinalKeyBeforeMD5 = str(password)
	dateTimeNow = datetime.datetime.now()

	year = str(dateTimeNow.year)
	month = str(dateTimeNow.month)
	date = str(dateTimeNow.day)
	FinalKeyBeforeMD5 = FinalKeyBeforeMD5 + date + month + year
	return FinalKeyBeforeMD5

def getSpecialCaseWithMD5(priorValsBeforeDate):
	dateTimeNow = datetime.datetime.now()

	year = str(dateTimeNow.year)
	month = str(dateTimeNow.month)
	date = str(dateTimeNow.day)

	FinalKeyBeforeMD5 = priorValsBeforeDate + date +month +year
	return FinalKeyBeforeMD5
















