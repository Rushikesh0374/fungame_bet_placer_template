
import utils

def getAndharBaharLastStatusRequestBody(input_str):
    encrypted_data = utils.encrypt(str(input_str))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IGetAndharBaharLastStatus xmlns="http://tempuri.org/"><abindata>{encrypted_data}</abindata></IGetAndharBaharLastStatus></s:Body></s:Envelope>
"""
    return request_body


def getAndharBaharDrawNoRequestBody(value):
    encrypted_drawId = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IGetAnharBaharDrawno xmlns="http://tempuri.org/"><abdrawno>{encrypted_drawId}</abdrawno></IGetAnharBaharDrawno></s:Body></s:Envelope>
"""

    return request_body


def getLoginRequestBody(encrypted_mem_id):
    request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IGetLogin xmlns="http://tempuri.org/"><mem_id>{encrypted_mem_id}</mem_id></IGetLogin></s:Body></s:Envelope>"""
    # request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IGetLogin xmlns="http://tempuri.org/"><mem_id>8FcgToAzq/XxB3M92whpMFI8wnMx7JEXCvpCViSUGFLpavBpXFzPQus/TP8C0oPtu5izZ4z5W8B3ErEbgTWPkAzN0SreRnqToJuyRvoh+HU=</mem_id></IGetLogin></s:Body></s:Envelope>"""
    return request_body


def getAndharBaharBetRequestBody(value):
    encrypted_bet_str = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IAndharBaharBetDataProcess xmlns="http://tempuri.org/"><abbetstr>{encrypted_bet_str}</abbetstr></IAndharBaharBetDataProcess></s:Body></s:Envelope>
"""
    
    return request_body


def getAndharBaharTakeBetRequestBody(value):
    encrypted_take_str = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><IAndharBaharTakeDataProcess xmlns="http://tempuri.org/"><takestr>{encrypted_take_str}</takestr></IAndharBaharTakeDataProcess></s:Body></s:Envelope>

"""
    
    return request_body
