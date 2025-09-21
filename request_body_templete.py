import utils

def getAndharBaharLastStatusRequestBody(input_str):
    encrypted_data = utils.encrypt(str(input_str))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing"
            xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetAndharBaharLastStatus</a:Action>
    <a:MessageID>urn:uuid:442076cc-9425-4fa3-a99b-02df327ee10a</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev04.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IGetAndharBaharLastStatus xmlns="http://tempuri.org/">
      <abindata>{encrypted_data}</abindata>
    </IGetAndharBaharLastStatus>
  </s:Body>
</s:Envelope>"""
    return request_body


def getAndharBaharDrawNoRequestBody(value):
    encrypted_drawId = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetAnharBaharDrawno</a:Action>
    <a:MessageID>urn:uuid:fa73f144-39c5-4f10-85e0-fc11ddf15083</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IGetAnharBaharDrawno xmlns="http://tempuri.org/">
      <abdrawno>{encrypted_drawId}</abdrawno>
    </IGetAnharBaharDrawno>
  </s:Body>
</s:Envelope>"""

    return request_body


def getLoginRequestBody(encrypted_mem_id):
    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
        <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetLogin</a:Action>
        <a:MessageID>urn:uuid:14adbfa6-966e-4288-8631-dd5849b0800a</a:MessageID>
        <a:ReplyTo>
            <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
        </a:ReplyTo>
        <a:To s:mustUnderstand="1">https://sev02.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
    </s:Header>
    <s:Body>
        <IGetLogin xmlns="http://tempuri.org/">
            <mem_id>{encrypted_mem_id}</mem_id>
        </IGetLogin>
    </s:Body>
</s:Envelope>"""
    return request_body


def getAndharBaharBetRequestBody(value):
    encrypted_bet_str = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IAndharBaharBetDataProcess</a:Action>
    <a:MessageID>urn:uuid:09bd47b2-8824-427d-8c48-f886d8c9ec5e</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IAndharBaharBetDataProcess xmlns="http://tempuri.org/">
      <abbetstr>{encrypted_bet_str}</abbetstr>
    </IAndharBaharBetDataProcess>
  </s:Body>
</s:Envelope>"""
    
    return request_body


def getAndharBaharTakeBetRequestBody(value):
    encrypted_take_str = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IAndharBaharTakeDataProcess</a:Action>
    <a:MessageID>urn:uuid:a75c3892-2beb-4c67-a584-d2014c2e0c72</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IAndharBaharTakeDataProcess xmlns="http://tempuri.org/">
      <takestr>{encrypted_take_str}</takestr>
    </IAndharBaharTakeDataProcess>
  </s:Body>
</s:Envelope>"""
    
    return request_body

