from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

api_key = 'NCS5805501D62D8B'
api_secret = 'A86DF83FB2F77AC52F0322A8B1B294A1'

params = dict()
params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
params['to'] = '01029953874' # Recipients Number '01000000000,01000000001'
params['from'] = '01029953874' # Sender number
params['text'] = 'Test Message' # Message

cool = Message(api_key, api_secret)
try:
    response = cool.send(params)
    print(response)
    print("Success Count : %s" % response['success_count'])
    print("Error Count : %s" % response['error_count'])
    print("Group ID : %s" % response['group_id'])

    if "error_list" in response:
        print("Error List : %s" % response['error_list'])

except CoolsmsException as e:
    print("Error Code : %s" % e.code)
    print("Error Message : %s" % e.msg)