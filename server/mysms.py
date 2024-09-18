import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import string 
import random 
## ==== 설치해주세요 ====
## pip install coolsms_python_sdk

## @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP

class MySms:
    def mysendsms(self, tosms):
    
    # set api key, api secret
        api_key = "api_key"
        api_secret = "api_secret"
        
        _LENGTH = 8 # 8자리 
        # 숫자 + 대소문자 + 특수문자 
        string_pool =  string.digits #  + string.ascii_letters+ string.punctuation 
        # 랜덤한 문자열 생성 
        result = "" 
        for i in range(_LENGTH) : 
            result += random.choice(string_pool) # 랜덤한 문자열 하나 선택 
        print(result)
        
        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = tosms # Recipients Number '01000000000,01000000001'
        params['from'] = 'phone number' # Sender number
        params['text'] = "WAFLEX 인증문자입니다. 회원가입을 위한 인증번호는 " +result+" 입니다." # Message
        
        cool = Message(api_key, api_secret)
        
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])
            
            if "error_list" in response:
                print("Error List : %s" % response['error_list'])
        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
        
        return result
        sys.exit()


