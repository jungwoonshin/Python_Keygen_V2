from UrlUtils import getDomainList

import urllib2
import urllib
import requests
import json

import jwt
from datetime import datetime, date, time, timedelta
import uuid

def getPassword(pc):
	pc = pc.lower()
	passDict = {'zoomtestqa':'123456','zoomtestqaenhanced':'123456'}
	if pc in passDict:
		password = passDict[pc]
	else:
		password = 'testing123'


	# print('password',password)
	return password

def getZitokenDirectly(pc):
	zipayload = {
		'ziPartnerCode':pc
	}
	password = getPassword(pc)

	utc0 = datetime(1970,1,1)
	issueTime = datetime.utcnow()
	iat = issueTime - utc0
	iat = int(iat.total_seconds())
	exp = issueTime - utc0
	exp = exp + timedelta(minutes=60)
	exp = int(exp.total_seconds())

	# # print(exp.seconds)
	payload = {
		'iss':'zoominfo',\
		'iat': iat,\
		'jti': str(uuid.uuid4()),\
		'ziPayLoad':zipayload,\
		'exp': exp
	}
	encoded = jwt.encode(payload, password, algorithm='HS256')
	return encoded

# this by default goes into staging machine to generate oauth token
def getOauthToken():
	return getOauthToken('staging')

# get zitoken from partnerapi keygenerator app
def getZitoken(pc):

	req = urllib2.Request('http://localhost:8080/partnerapikey/zoom/zitoken?pc=' + pc)
	the_page = urllib2.urlopen(req).read()

	zitokenParamStartKey = '<ziToken>'
	zitokenParamEndKey = '</ziToken>'
	zitokenStartIndex = the_page.find(zitokenParamStartKey) + len(zitokenParamStartKey)
	zitokenEndIndex = the_page.find(zitokenParamEndKey)

	zitokenVal = the_page[zitokenStartIndex:zitokenEndIndex]
	# print('zitokenVal',zitokenVal)
	return zitokenVal

def getOauthValIndexes(result):
	oauthTokenParamStartIndex = '<token>'
	oauthTokenParamEndIndex ='</token>'
	oauthTokenStartIndex = result.find(oauthTokenParamStartIndex) + len(oauthTokenParamStartIndex)
	oauthTokenEndIndex = result.find(oauthTokenParamEndIndex)

	if (oauthTokenStartIndex is -1 or oauthTokenEndIndex is -1):
		return (0, len(result)) 

	return (oauthTokenStartIndex, oauthTokenEndIndex)

def getOauthToken(machine, pc):
	data = """<?xml version="1.0" encoding="utf-8"?>
	<TokenPostInput xmlns="http://partnerapi.zoominfo.com/partnerapistatic/xsd/V1/TokenPostInput.xsd">
	<pc>""" + pc + """</pc>
	<ziToken>"""
	data += getZitokenDirectly(pc)
	data += """</ziToken></TokenPostInput>"""

	domainList = getDomainList()
	domainName = domainList[machine]
	oauthTokenServerUrl = "https://" + domainName + "8443/partnerapi/v2/token"
	print('oauthTokenServerUrl',oauthTokenServerUrl)
	r = requests.post(oauthTokenServerUrl, data=data, headers = {'Content-Type': 'application/xml','Accept':'application/xml'}, verify=False)
	result = r.text

	(oauthTokenStartIndex, oauthTokenEndIndex) = getOauthValIndexes(result)
	oauthVal = result[oauthTokenStartIndex:oauthTokenEndIndex]

	return str(oauthVal)

def validateDirectlyFromOauthapp(machine):
	
	oauthToken = getOauthToken(machine,'ZoomTestQA')
	# oauthToken = getDirectlyFromOauthappOauthToken(machine)
	# print('oauthToken',oauthToken)
	machine = 'oauth_' + machine
	domainList = getDomainList()
	machine = domainList[machine]
	url = 'https://' + machine + '8443/oauth2/validate?'
	# url = 'https://oa.staging.zoominfo.com/oauth2/validate?'

	print('url',url)
	r = requests.get(url, headers = {'Authorization':'Bearer '+ oauthToken,'Content-Type': 'application/x-www-form-urlencoded','Accept':'application/json'}, verify=False)
	result = r.text
	return str(result)
	# print(result)

def validateDirectlyFromOauthappWithOauth(machine, oauthVal):
	
	oauthToken = oauthVal

	machine = 'oauth_' + machine
	domainList = getDomainList()
	machine = domainList[machine]
	url = 'https://' + machine + '8443/oauth2/validate?'
	# url = "https://oa.staging.zoominfo.com/oauth2/validate?"

	# url = 'https://localhost:8443/oauth2/validate?'

	print('url',url)
	r = requests.get(url, headers = {'Authorization':'Bearer '+ oauthToken,'Content-Type': 'application/x-www-form-urlencoded','Accept':'application/json'}, verify=False)
	result = r.text
	print(str(result))

def getDirectlyFromOauthappOauthToken(machine):
	data = """applicationId=7692&applicationSecret=zoominfoPartnerapiApp&clientId=ZoomTestQA&ziToken=""" + getZitokenDirectly('ZoomTestQA')
	# data = """applicationId=7692&applicationSecret=zoominfoPartnerapiApp&clientId=ZoomTestQA"""
	machine = 'oauth_' + machine
	domainList = getDomainList()
	machine = domainList[machine]
	url2 = "https://" + machine + "8443/oauth2/token"
	# url2 = "https://oa.staging.zoominfo.com/oauth2/token"
	# url2 = "https://localhost:8443/oauth2/token"

	print('url2',url2)
	r = requests.post(url2, data=data, headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept':'application/json'}, verify=False)
	# print(r.text)
	result = json.loads(r.text)['oauthToken']   
	print('oauthVal',result)
	return str(result)

def getDirectlyFromOauthappOauthTokenWithPc(machine,pc):
	data = 'applicationId=7692&applicationSecret=zoominfoPartnerapiApp&clientId='
	data += pc
	data += '&ziToken=' 
	data += getZitokenDirectly(pc)

	machine = 'oauth_' + machine
	domainList = getDomainList()
	machine = domainList[machine]
	url2 = "https://" + machine + "8443/oauth2/token"

	print('url2',url2)

	r = requests.post(url2, data=data, headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept':'application/json'}, verify=False)
	# print(r.text)
	result = json.loads(r.text)['oauthToken']   
	# print('oauthVal',result)
	return str(result)

# print(getDirectlyFromOauthappOauthTokenWithPc('staging01','apiQaAuto'))

# some extra examples
# localhost:8080/oauth2/purge/partners?pc=ZoomTestQAEnhanced&appId=7692&appSt=zoominfoPartnerapiApp

# getDirectlyFromOauthappOauthToken('local')
# print(getOauthToken('staging01','zoomtestqa'))
# print(getOauthToken('local','zoomtestqa'))

# 1464134827
# 1464131227

# validateDirectlyFromOauthapp('staging01')

# validateDirectlyFromOauthapp('local', getDirectlyFromOauthappOauthToken('local'))
# getDirectlyFromOauthappOauthToken('local')

# validateDirectlyFromOauthappWithOauth('local', '39ff0b70-7eb4-481d-8606-6a2394e868be')

# machine = 'local'
# machine ='production01'


# oauthVal = getDirectlyFromOauthappOauthToken(machine)

# print('oauthVal',oauthVal)
# validateDirectlyFromOauthappWithOauth(machine, oauthVal)

# print(validateDirectlyFromOauthapp(machine))

# print(getOauthToken('production01','zoomtestqa'))
