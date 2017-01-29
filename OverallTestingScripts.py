from generatePostTestUrlFiles import *
from generateNonPostTestUrlFiles import * 

'''choose which machines you want to run'''
# machine = 'local'
machine = 'production01'
# machine = 'staging01'
# machine = 'production02'
# machine = 'production03'

# ****** NOTE:please make sure to comment form complete tests for PRODUCTION04
# machine = 'production04'

''' ----------------  GET REQUESTS ----------------
	# to generate only the endpoints url'''
generateEndpoints(machine,'inputs/DivideAndConquer/api_get_requests.txt')

'''(1) generate & RUN non-fc get requests'''
# runGetRequests(machine)

'''(2) generate & RUN fc get requests'''
# runOverallFormComplete(machine)
 
''' ----------------  POST REQUESTS ----------------
	generate & run all post requests'''
# runPostFormCompleteOverallTest(machine)

''' ----------------  OAUTH WEB APP TEST ----------------
	generate & run all requests'''
# oauthMachineList = ['production01','production02','production03']
# for machineToTest in oauthMachineList:
# 	runOauthRequests(machineToTest)

''' ----------------  Request Access Token Only ------------'''
# machine = 'staging01'
# pc = 'zoomtestqa'
# oauthVal = getOauthToken(machine,pc)
# print(oauthVal)

''' ----------------  Test two machines ------------'''
# machine1 = 'production01'
# machine2 = 'staging02'
# compareTwoMachines(machine1, machine2)



