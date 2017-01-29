
# python keygenerator.py --p 123456 --u SF_PremiumQA --qt person_search --qs "emailAddress=adam.alami@zoominfo.com&firstName=adam&lastName=alami"
import sys
sys.path.append('./functions')
import argparse
from keygen_functions import *
from keygen_helper import getMD5Key
from UrlUtils import getPc, getQueryType
# from Users.jungwoonshin.javaide.scripts.zoom.Python_Keygen.functions.keygen_helper import *

# password = '123456'
# password = 'test123'
# queryType = 'person_search'
# queryType = 'company_search'
# queryString = 'lastName=chou&state=Massachusetts&pc=ZoomTestQA&outputType=xml&outputFieldOptions=localaddress,companyaddress,jobfunction,managementlevel,companyLogo&rpp=10'

# queryString = 'country=Country.Sweden&pc=ZoomTestQADefinedUniverse&outputType=xml&key=428f3fcfe269f28ff2a4ebdba482be87&outputFieldOptions=companyPhone,companyfax,companyLogo'
# queryString = 'RPP=20&Page=1&pc=zoomtestqa&firstName=Val&lastName=Mattal&companyPastOrPresent=1&key=74eb4d6b8c46a66ed3f596761c88b1e1'
# queryString = 'firstname=yonatan&lastname=stern&pc=ZoomTestQA&outputType=xml&outputfieldoptions=education,webreference,pastemployment&key=4e5c82700adb43be40e01bf61d6b7c3e'
# queryString = 'http://localhost:8080/partnerapi/person/match?personid=27704460&pc=ZoomTestQA&outputType=xml&outputfieldoptions=education,webreference,pastemployment&key=b47298430c9235bc8f8f2b393fa1068a'
# queryString = 'http://localhost:8080/partnerapi/person/detail?personid=27704460&pc=ZoomTestQA&outputType=xml&outputfieldoptions=education,webreference,pastemployment&key=b47298430c9235bc8f8f2b393fa1068a'

# http://api.staging.zoominfo.com/partnerapi/company/detail?CompanyID=1&pc=pc&key=834b897fb0c4c727e7cd27de7ca1864b

# queryString = 'http://localhost:8080/partnerapi/person/detail?personid=27704460&pc=ZoomTestQA&outputType=xml&outputfieldoptions=localaddress,jobfunction,managementlevel&key=158e91475b1e3190be0c439792aa5c79'
# queryString = 'http://lxpjbsapi01.xoominfo.com:8080/partnerapi/person/match?firstName=Robert&lastName=Zimmer&companyName=Global Alliance Management LLC&pc=ZoomTestQA&outputType=xml&key=f01a5eca152cfca37750f1e706d06d9a&echoInput=true&outputFieldOptions=companyEmployeeCount,companyRevenueNumeric,jobfunction,managementlevel&numMatches=10'

# queryString ='http://localhost:8080/partnerapi/person/search?fullname=john%20shin&firstname=john&state=ma&pc=ZoomTestQA&key=995010b6d5b13a82bf35189dc91932d3'






# queryString = 'https://localhost:8443/partnerapi/person/detail?personId=-1937616756&pc=ZoomTestQA&outputType=xml&key=f83fa9b9ac11a2d604995e66fccc4c9f&outputFieldOptions= jobfunction,managementlevel,localAddress,companyLogo,companyTopLevelIndustry'
# queryString = 'https://localhost:8443/partnerapi/person/match?pc=zoomtestqa&firstName=Rick&lastName=Jones&companyName=Bannockburn%20Securities%20LLC&echoInput=true&key=fbd5c40c80dfc76217e8511a217496d7'
# queryString ='http://partnerapi.zoominfo.com/partnerapi/company/detail?companyID=70175813&pc=zoomtestqa&outputType=xml&key=6faf3947868bbbf6640997d214ab927d'

# queryString = 'http://lxsjbsapi01:8080/partnerapi/company/match?pc=apiQaAuto&numMatches=10&echoInput=TRUE&companyId=344589814&phone1=781-693-7500&street1=307+Waverley+Oaks+Rd.&city1=Waltham&state1=Massachusetts&zip1=2452&country1=USA+-+All&key=0b171ee43c41cd94d9b9dfba9673a5ca'



queryString = 'https://localhost:8443/partnerapi/person/search?pc=ZoomTestQA&key=f83fa9b9ac11a2d604995e66fccc4c9f&firstName=john&outputfieldoptions=companyemployeecount,companyaddress,companylogo,jobfunction,companyrevnuerange,companyrevenuenumeric,companyemployeerange,personids,companytype,companyrevenue&rpp=3'
queryType = getQueryType(queryString)

if('?' in queryString):
	queryString = queryString.split('?')[1]

pc = getPc(queryString)
print('------pc',pc)
# queryString ='personid=-1696958686&pc=ZoomTestQA&outputType=xml'

FinalKeyAfterMD5 = getMD5Key(queryString, queryType, pc)
print('------API KEY(after MD5)------')
print('FinalKEyAfterMD5: ',FinalKeyAfterMD5)
print('------------------------------\n')

fullAddress = getFullUrlAddress(queryString, queryType,FinalKeyAfterMD5)

print('------Full Address------')
print(fullAddress)
print('------------------------------\n')
# print('hashlibMD5',hashlibMD5)






