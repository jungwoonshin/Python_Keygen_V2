"""

Author: John Shin
Last Update 05.13.2016

This script generates a file that contains endpoint with up-to-date key (both md5 and oauth) 
It assumes that url address that you want to have updated key value to start with http or https with no spaces in front.
It will only replace the key value for the line that starts with http or https.

If the key value included in the url of input text file is MD5, then it will generate md5 key appropirate for the url requests.
If the key value is OauthToken, then it will replace it to fresh oauthToken value.
After replacing the key values, this script will simpy save them in to outputs folder.
The file name is "machine" + input file name you have used in running this script.

------------------------
Some example usages are

generateEnpointsAndOauthKey('local','/Users/jungwoonshin/javaide/scripts/zoom/Python_Keygen/inputs/yingchao/New OAuth Endpoint.txt')
generateEnpointsAndOauthKey('local','/Users/jungwoonshin/javaide/scripts/zoom/Python_Keygen/inputs/DivideAndConquer/AllAuthWithoutRequests.txt')
generateEnpointsAndOauthKey('staging01','/Users/jungwoonshin/javaide/scripts/zoom/Python_Keygen/inputs/yingchao/New OAuth Endpoint.txt')

"""

from functions.replaceKeyValueUtils import writeResultsFile
from functions.keygen_helper import checkWhetherMachineIsCorrect

# machine parameter is either 'staging01'/'staging02'/'staging03' or 'production01'/'production02'/'production03'
def generateEndpoints(machine, inputFileName):
	checkWhetherMachineIsCorrect(machine)
	outputXmlFileName = writeResultsFile(machine,inputFileName)
	return outputXmlFileName












