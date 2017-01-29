
def getDomainList():
	domainList = {'local':'localhost:','localfc':'localhost:','staging01':'lxsjbsapi01.xoominfo.com:','staging02':'lxsjbsapi02.xoominfo.com:','staging03':'lxsjbsapi03.xoominfo.com:',\
					'production01':'lxpjbsapi01.xoominfo.com:','production02':'lxpjbsapi02.xoominfo.com:','production03':'lxpjbsapi03.xoominfo.com:','production04':'lxpjbsapi04.xoominfo.com:',\
					'oauth_local':'lxsjbsoa01.xoominfo.com:','oauth_staging01':'lxsjbsoa01.xoominfo.com:','oauth_staging02':'lxsjbsoa02.xoominfo.com:','oauth_staging03':'lxsjbsoa03.xoominfo.com:',\
					'oauth_production01':'lxpjbsoa01.xoominfo.com:','oauth_production02':'lxpjbsoa02.xoominfo.com:','oauth_production03':'lxpjbsoa03.xoominfo.com:',\
					'staging01fc':'lxsjbsfc01.xoominfo.com:','staging02fc':'lxsjbsfc02.xoominfo.com:','staging03fc':'lxsjbsfc03.xoominfo.com:',\
									'production01fc':'lxpjbsfc01.xoominfo.com:','production02fc':'lxpjbsfc02.xoominfo.com:','production03fc':'lxpjbsfc03.xoominfo.com:'}
	return domainList		

def addPortToDomainAddress(machineAppropirateDomainAddress, line):
 	if 'https' in line or 'http' in line:
		domainAddressWithPort = machineAppropirateDomainAddress + '8443'
	return domainAddressWithPort


def getPc(line):
	startIndex = line.find('pc=')
	endIndex = len(line) + line[startIndex:].find('&')
	pcVal = line[startIndex:endIndex].split('&')[0]
	# print('pcVal',pcVal)
	return pcVal

def getQueryTypeValByUsingParmeterValue(line):
	startIndex = line.find('query_type')
	endIndex = line.find('&')
	queryTypeVal = line[startIndex : endIndex].split('=')[1]
	queryTypeVal = queryTypeVal.split('_')[0] + '_' +queryTypeVal.split('_')[1]
	return queryTypeVal

def getQueryTypeValFromSlashRemovedLine(line):
	toRemoveStartIndex = line.find('externalurl')
	toRemoveEndIndex = line[toRemoveStartIndex:].find('&')

	# externalurl is the last paramter. So just remove external url paramater key and value
	if toRemoveEndIndex is -1:
		line = line[:toRemoveStartIndex-1]
	else:
		line = line[:toRemoveStartIndex-1] + line[toRemoveEndIndex+1:]
		# print('TESTING SPECIAL CASE +__ASDA_SDA_SDA_ line',line)
	queryTypeVal= getQueryType(line)
	return queryTypeVal

def getQueryType(line):
	# print('getQueryType',line)
	numberOfElements = len(line.split('/'))
	queryTypeVal = None

	if 'query_type' in line:
		queryTypeVal = getQueryTypeValByUsingParmeterValue(line)

	# if there is externalurl paramter inside request, using / to break down the values rule breaks. So we make a special case.
	elif 'externalurl' in line.lower():
		queryTypeVal = getQueryTypeValFromSlashRemovedLine(line)

	elif numberOfElements is 6 or numberOfElements is 7 or numberOfElements is 8:
		queryTypeVal = line.split('/')[numberOfElements-2] + '_' + line.split('/')[numberOfElements-1].split('?')[0]
			
	elif queryTypeVal == None:
		print(' ********** WARNING THIS PARAMATER IS NOT BE SUPPORED BY THE KEYGENERATOR ')
		queryTypeVal = 'default'

	return queryTypeVal

def	getMachineAppropirateTestsUrls(line, machine):
	# this is load balancer test
	if 'partnerapi.zoominfo.com' in line:
		return line

	httpOrhttpsWithDoubleDash = line.split('//')[0] +'//'
	domainAddress = line.split('//')[1].split('/')[1:]
	domainAddressStartIndex = line.find(domainAddress[0]) 

	domainList = getDomainList()
	machineAppropirateDomainAddress = domainList[machine]

	dominAddressWithPort = addPortToDomainAddress(machineAppropirateDomainAddress, line)
	
	testUrl = httpOrhttpsWithDoubleDash + dominAddressWithPort + '/' +  line[domainAddressStartIndex:]

	return testUrl

def	isUrlRequest(line):
	firstForLetters = line[:4]
	if firstForLetters in 'http' or firstForLetters in 'https':
		return True
	return False

def	containsKeyParamter(machineAppropirateUrlAddress):
	if 'key=' in machineAppropirateUrlAddress:
		return True
	return False
