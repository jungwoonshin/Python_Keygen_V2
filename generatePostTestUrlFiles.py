from functions.getOauthKey import *
from functions.keygen_functions import *
import xml.etree.ElementTree as ET
import xml.dom.minidom as XDM


def sendRequest(url,data):
	data=data.strip()

	r = requests.post(url, data=data, headers = {'Content-Type': 'application/xml','Accept':'application/xml'}, verify=False)
	response = r.text.encode('utf-8')

	print('\n\n*********************** Making requests ...' + url + ' ***********************\n\n\n' )
	print(response)
	print('***********************Finished making requests ... ***********************'+'\n\n\n')

	return response

def sendRequest(results,url,data):

	# input print & write
	prettyDataXML = XDM.parseString(data).toprettyxml(indent="   ")
	print("input",prettyDataXML )
	results.write("input\n")
	results.write(prettyDataXML)
	# end of input print & write

	data=data.strip()

	r = requests.post(url, data=data, headers = {'Content-Type': 'application/xml','Accept':'application/xml'}, verify=False)
	response = r.text.encode('utf-8')
	print('\n\n*********************** Making requests ...' + url + ' ***********************' )
	results.write('\n\n*********************** Making requests ...' + url + ' ***********************\n' )
	print('response',response)
	xmlstr = XDM.parseString(response).toprettyxml(indent="   ")
	print('\n' + xmlstr + '\n' )
	results.write(xmlstr)

	return response 

def getKeyValueForPersonMatcherPostRequest(results):
	url = 'http://localhost:8080/partnerapikey/match/person'
	data = """<?xml version="1.0" encoding="utf-8"?>
	<matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>   
	<pc>ZoomTestQA</pc>
	<key>3387b304b21785e760c29e0594a1d58b</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results, url,data)
	print(' *************** WARNING: if you have an connection refused error message, \
		please delpoy partnerapikeygenerator.war file.')
	print('response',response)
	root = ET.fromstring(response)
	keyVal = root[1].find('personMatchKeyResult').find('Key').text
	return keyVal

def getKeyValueForCompanyMatcherPostRequest(results):
	url = 'http://localhost:8080/partnerapikey/match/company'
	data = """<?xml version="1.0" encoding="utf-8"?>
	<matchCompanyPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchCompanyPostInput.xsd">
	<matchInput> 
	<pc>ZoomTestQA</pc>
	<key>641450f5a6ce958abd16d72ba01335ac</key>
	<numMatches>2</numMatches>
	<echoInput>false</echoInput>
	</matchInput> 
	<matchCompanyInput>
	<uniqueInputId>111AA</uniqueInputId>
	<companyId>25248427</companyId>
	<name>The Mitre Corporation</name>
	<matchCompanyContactInput>
	<street>202 Burlington Road</street>
	<city>Bedford</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<state>Massachusetts</state>
	<zip>01730</zip> 
	</matchCompanyContactInput>
	</matchCompanyInput>
	<matchCompanyInput>
	<uniqueInputId>222BB</uniqueInputId>
	<domain>www.google.com</domain>
	<ticker>GOOG</ticker>
	<matchCompanyContactInput>
	<city>Boston</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<city>California</city>
	</matchCompanyContactInput>
	</matchCompanyInput>
	</matchCompanyPostInput>"""
	response =  sendRequest(results, url,data)
	root = ET.fromstring(response)
	keyVal = root[1].find('companyMatchKeyResult').find('Key').text
	return keyVal

def getPersonMatchResponse(results,machineNumber, key):
	url = 'http://'+machineNumber+'8080/partnerapi/person/match'
	data = """<?xml version="1.0" encoding="utf-8"?>
	<matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>
	<pc>ZoomTestQA</pc>
	<key>""" + key + """</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getCompanyMatchResponse(results,machineNumber, key):
	url = 'http://'+machineNumber+'8080/partnerapi/company/match'

	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchCompanyPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchCompanyPostInput.xsd">
	<matchInput> 
	<pc>ZoomTestQA</pc>
	<key>"""+key+"""</key>
	<numMatches>2</numMatches>
	<echoInput>false</echoInput>
	</matchInput> 
	<matchCompanyInput>
	<uniqueInputId>111AA</uniqueInputId>
	<companyId>25248427</companyId>
	<name>The Mitre Corporation</name>
	<matchCompanyContactInput>
	<street>202 Burlington Road</street>
	<city>Bedford</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<state>Massachusetts</state>
	<zip>01730</zip> 
	</matchCompanyContactInput>
	</matchCompanyInput>
	<matchCompanyInput>
	<uniqueInputId>222BB</uniqueInputId>
	<domain>www.google.com</domain>
	<ticker>GOOG</ticker>
	<matchCompanyContactInput>
	<city>Boston</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<city>California</city>
	</matchCompanyContactInput>
	</matchCompanyInput>
	</matchCompanyPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getEnhancedPersonMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v2/person/match'
	data = """<?xml version="1.0" encoding="utf-8"?>
	<matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>   
	<pc>ZoomTestQAEnhanced</pc>
	<key>"""+key+"""</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getEnhancedPersonMatchExist(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v2/person/match/exist'
	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>   
	<pc>ZoomTestQAEnhanced</pc>
	<key>"""+key+"""</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV3CompanyMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v3/company/match'
	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchCompanyPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchCompanyPostInput.xsd">
	<matchInput> 
	<pc>ZoomTestQA</pc>
	<key>"""+key +"""</key>
	<numMatches>2</numMatches>
	<echoInput>false</echoInput>
	</matchInput> 
	<matchCompanyInput>
	<uniqueInputId>111AA</uniqueInputId>
	<companyId>25248427</companyId>
	<name>The Mitre Corporation</name>
	<matchCompanyContactInput>
	<street>202 Burlington Road</street>
	<city>Bedford</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<state>Massachusetts</state>
	<zip>01730</zip> 
	</matchCompanyContactInput>
	</matchCompanyInput>
	<matchCompanyInput>
	<uniqueInputId>222BB</uniqueInputId>
	<domain>www.google.com</domain>
	<ticker>GOOG</ticker>
	<matchCompanyContactInput>
	<city>Boston</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<city>California</city>
	</matchCompanyContactInput>
	</matchCompanyInput>
	</matchCompanyPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV4CompanyMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v4/company/match'
	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchCompanyPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchCompanyPostInput.xsd">
	<matchInput> 
	<pc>ZoomTestQA</pc>
	<key>"""+key +"""</key>
	<numMatches>2</numMatches>
	<echoInput>false</echoInput>
	</matchInput> 
	<matchCompanyInput>
	<uniqueInputId>111AA</uniqueInputId>
	<companyId>25248427</companyId>
	<name>The Mitre Corporation</name>
	<matchCompanyContactInput>
	<street>202 Burlington Road</street>
	<city>Bedford</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<state>Massachusetts</state>
	<zip>01730</zip> 
	</matchCompanyContactInput>
	</matchCompanyInput>
	<matchCompanyInput>
	<uniqueInputId>222BB</uniqueInputId>
	<domain>www.google.com</domain>
	<ticker>GOOG</ticker>
	<matchCompanyContactInput>
	<city>Boston</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<city>California</city>
	</matchCompanyContactInput>
	</matchCompanyInput>
	</matchCompanyPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV4CompanyMatchWithFacetsOptions(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v4/company/match'
	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchCompanyPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchCompanyPostInput.xsd">
	<matchInput> 
	<pc>ZoomTestQA</pc>
	<key>"""+key +"""</key>
	<numMatches>2</numMatches>
	<echoInput>false</echoInput>
	<facetOptions>All</facetOptions>
	</matchInput> 
	<matchCompanyInput>
	<uniqueInputId>111AA</uniqueInputId>
	<companyId>25248427</companyId>
	<name>The Mitre Corporation</name>
	<matchCompanyContactInput>
	<street>202 Burlington Road</street>
	<city>Bedford</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<state>Massachusetts</state>
	<zip>01730</zip> 
	</matchCompanyContactInput>
	</matchCompanyInput>
	<matchCompanyInput>
	<uniqueInputId>222BB</uniqueInputId>
	<domain>www.google.com</domain>
	<ticker>GOOG</ticker>
	<matchCompanyContactInput>
	<city>Boston</city>
	</matchCompanyContactInput>
	<matchCompanyContactInput>
	<city>California</city>
	</matchCompanyContactInput>
	</matchCompanyInput>
	</matchCompanyPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV3PersonMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v3/person/match'
	data ="""<?xml version="1.0" encoding="utf-8"?><matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>
	<pc>ZoomTestQA</pc>
	<key>""" + key + """</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV4PersonMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v4/person/match'
	data ="""<?xml version="1.0" encoding="utf-8"?><matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>
	<pc>ZoomTestQA</pc>
	<key>""" + key + """</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Nick</firstName>
	<lastName>Norman</lastName>
	<emailAddress>nnorman@halogensoftware.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response

def getV3EnhancedPersonMatch(results,machineNumber, key):
	url = 'https://'+machineNumber+'8443/partnerapi/v3/enhanced/person/match'
	data ="""<?xml version="1.0" encoding="utf-8"?>
	<matchPersonPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/MatchPersonPostInput.xsd">
	<matchInput>   
	<pc>ZoomTestQAEnhanced</pc>
	<key>""" + key + """</key>
	<numMatches>2</numMatches>
	<echoInput>true</echoInput>
	</matchInput>
	<matchPersonInput>
	<uniqueInputId>1A</uniqueInputId>
	<firstName>Adam</firstName>
	<lastName>Alami</lastName>
	<emailAddress>adam.alami@zoominfo.com</emailAddress>
	</matchPersonInput>
	<matchPersonInput>
	<firstName>Heather</firstName>
	<lastName>Reisman</lastName>
	</matchPersonInput>
	<matchPersonInput>
	<personId>265274387</personId>
	</matchPersonInput>
	</matchPersonPostInput>"""
	response =  sendRequest(results,url,data)
	return response




def runPostFormCompleteOverallTest(machine):

	XMLOutputResultsFileName = 'outputs/results_post_'+machine+'.txt'

	oauthKey = getOauthToken(machine,'ZoomTestQA')
	oauthKeyZoomTestQAEnhanced = getOauthToken(machine,'ZoomTestQAEnhanced')


	domainList = {'local':'localhost:','staging01':'lxsjbsapi01.xoominfo.com:','staging02':'lxsjbsapi02.xoominfo.com:','staging03':'lxsjbsapi03.xoominfo.com:',\
				'production01':'lxpjbsapi01.xoominfo.com:','production02':'lxpjbsapi02.xoominfo.com:','production03':'lxpjbsapi03.xoominfo.com:','production04':'lxpjbsapi04.xoominfo.com:',\
				# 'staging01fc':'lxtjbsapi01.xoominfo.com:','staging02fc':'lxsjbsapi02.xoominfo.com:','staging03fc':'lxsjbsapi03.xoominfo.com:',\
								'production01fc':'lxtjbsapi01.xoominfo.com:','production02fc':'lxtjbsapi02.xoominfo.com:','production03fc':'lxtjbsapi03.xoominfo.com:'}

	machine = domainList[machine]

	results = open(XMLOutputResultsFileName, 'w') 
	results.write('Starting...... \n\n\\nn')
	personMatchKey = getKeyValueForPersonMatcherPostRequest(results)
	companyMatchKey = getKeyValueForCompanyMatcherPostRequest(results)

	results.write('-------------------------------------------Writing person Match Key ... -------------------------------------------\n' )
	results.write(personMatchKey)
	results.write('\n-------------------------------------------Finished making requests ... -------------------------------------------'+'\n\n\n')
	
	results.write('-------------------------------------------Writing company Match Key ... -------------------------------------------\n' )
	results.write(companyMatchKey)
	results.write('\n-------------------------------------------Finished making requests ... -------------------------------------------'+'\n\n\n')

	getPersonMatchResponse(results,machine,personMatchKey)


	print( '********* results: ',results)
	print( '********* machine: ',machine)
	print( '********* companyMatchKey: ',companyMatchKey)

	getCompanyMatchResponse(results,machine,companyMatchKey)

	print('oauthKey',oauthKey)

	results.write('\n\n\n\n\n-------------------------------------------Writing oauth Key ... -------------------------------------------\n' )
	results.write(oauthKey+'\n\n\n')
	results.write('\n-------------------------------------------Finished making requests ... -------------------------------------------'+'\n\n\n')

	getEnhancedPersonMatchExist(results,machine,oauthKeyZoomTestQAEnhanced)
	getEnhancedPersonMatch(results,machine,oauthKeyZoomTestQAEnhanced)

	getV3CompanyMatch(results,machine,oauthKey)
	getV3PersonMatch(results,machine,oauthKey)
	getV4PersonMatch(results,machine,oauthKey)
	getV4CompanyMatch(results, machine, oauthKey)
	getV4CompanyMatchWithFacetsOptions(results, machine, oauthKey)
	getV3EnhancedPersonMatch(results,machine, oauthKeyZoomTestQAEnhanced)

	print('--------------------------------------------------------------------')
	print('\n------------------ files were saved into -------------------------')
	print('------------------' + XMLOutputResultsFileName +'-------------------')
	print('--------------------------------------------------------------------\n\n\n\n')

# specify which machine to test
# runOverallTest('staging01')
# runOverallTest('local')
# runOverallTest('production01')

