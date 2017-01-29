
def getDomainList():
	domainList = {'local':'localhost:','staging01':'lxsjbsapi01.xoominfo.com:','staging02':'lxsjbsapi02.xoominfo.com:','staging03':'lxsjbsapi03.xoominfo.com:',\
					'production01':'lxpjbsapi01.xoominfo.com:','production02':'lxpjbsapi02.xoominfo.com:','production03':'lxpjbsapi03.xoominfo.com:','production04':'lxpjbsapi04.xoominfo.com:',\
					'oauth_local':'lxsjbsoa01.xoominfo.com:','oauth_staging01':'lxsjbsoa01.xoominfo.com:','oauth_staging02':'lxsjbsoa02.xoominfo.com:','oauth_staging03':'lxsjbsoa03.xoominfo.com:',\
					'oauth_production01':'lxpjbsoa01.xoominfo.com:','oauth_production02':'lxpjbsoa02.xoominfo.com:','oauth_production03':'lxpjbsoa03.xoominfo.com:',\
					'staging01fc':'lxsjbsfc01.xoominfo.com:','staging02fc':'lxsjbsfc02.xoominfo.com:','staging03fc':'lxsjbsfc03.xoominfo.com:',\
									'production01fc':'lxtjbsapi01.xoominfo.com:','production02fc':'lxtjbsapi02.xoominfo.com:','production03fc':'lxtjbsapi03.xoominfo.com:'}
	return domainList

def listIntoLowerCase(totalList):	
	for i in totalList.keys():
		toBeLowercased = totalList[i]
		for j in range(0,len(toBeLowercased)):
			toBeLowercased[j] = toBeLowercased[j].lower()


def getTotalList():
	
	personSearchFieldsUsedForKey = ['firstname','middleinitial','lastname',
	'persontitle','titleseniority','titleclassification','companyid',
	'companyname','companydesc','industryclassificaton','industryKeywords','state','metroregion','country',
	'zipcode','radiusmiles','location','locationsearchtype','revenueclassificationmin','revenueclassificationmax','EmployeeSizeClassificationMin','EmployeeSizeClassificationMax',
	'IsPublic','CompanyRanking','school','degree','gender','companyDomainName','titleCertification','companyPastOrPresent',
	'ValidDateMonthDist','ValidDateMonthDist','ContactRequirements','EmailAddress','personids']

	personDetailFieldsUsedForKey = ['PersonID','EmailAddress']

	companySearchFieldsUsedForKey = ['companyName','companyDesc','IndustryClassification','industryKeywords',
	'RevenueClassificationMin','RevenueClassificationMax','EmployeeSizeClassificationMin','EmployeeSizeClassificationMax',
	'IsPublic','CompanyRanking','State','MetroRegion','Country','ZipCode','RadiusMiles','location','companyids']

	companyDetailFieldsUsedForKey = ['companyID','companydomain']

	companyMatchFieldsUsedForKey =[ 'companyId','name','domain','ticker']
	personMatchFieldsUsedForKey =  ['personId','fullname','firstname','lastname','emailAddress','companyid','companyname','jobtitle','phone','state','zipcode','country']

	# if you uncomment this you have to 'usage_query':usageQueryFieldsUsedForKey' put inside totalList
	# usageQueryFieldsUsedForKey = ['pc','serssiontoken','id']

	creditDecCompanyFieldsUsedForKey = ['exportname','key']

	totalList = {'person_search':personSearchFieldsUsedForKey,'people_search':personSearchFieldsUsedForKey,'person_detail':personDetailFieldsUsedForKey,'person_match':personMatchFieldsUsedForKey
	,'company_search':companySearchFieldsUsedForKey,'company_detail':companyDetailFieldsUsedForKey,'match_person':personMatchFieldsUsedForKey,'company_match':companyMatchFieldsUsedForKey
	,'match_company':companyMatchFieldsUsedForKey,'dec_company':creditDecCompanyFieldsUsedForKey}
	
	listIntoLowerCase(totalList)

	return totalList