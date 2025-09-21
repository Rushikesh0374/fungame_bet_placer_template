import os
import requests
import re
import json
import time
import utils
import random
from request_body_templete import *
import mail
import logging
from send_notification import send_broadcast_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("apis_call.log"),
        logging.StreamHandler()
    ]
)

session = requests.Session()

def retry_with_backoff(func, *args, max_retries=5, fixed_interval=1, **kwargs):
    """
    Execute a function with retry logic and fixed interval
    
    Args:
        func: The function to execute
        max_retries: Maximum number of retries
        fixed_interval: Fixed time interval between retries in seconds
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the function or None if all retries failed
    """
    retries = 0
    
    while retries <= max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retries += 1
            if retries > max_retries:
                send_broadcast_message(topic="all_users",title="Server Alert",body="Code has crashed, please check the server!")

                logging.error(f"Maximum retries ({max_retries}) exceeded. Last error: {str(e)}")
               	os._exit(1)
            
            # logging.info(f"Retry {retries}/{max_retries} after error: {str(e)}. Waiting {fixed_interval}s")
            time.sleep(fixed_interval)


def _login_request(encrypted_mem_id):
    """Internal function to make login request"""
    url = "https://sev02.gigp.vip/GAAndroidSer/AndWsService.svc"

    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev02.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IGetLogin"
    }

    body = getLoginRequestBody(encrypted_mem_id)

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()

    print(response.text)    
    match = re.search(r'OK,([\d.]+),([\d.]+)', response.text)
    logging.info(f"Login response: {match.group(2)}, {float(match.group(2))}")
    if match:
        session_id = int(match.group(1))
        amount = float(match.group(2))
        logging.info(f"amount: {amount}")
        return session_id, amount
    else:
        logging.error(f"Login response format unexpected: {response.text}")
        raise ValueError("Unexpected login response format")

def login(encrypted_mem_id):
    """Perform login and return session ID with retry mechanism"""
    try:
        return retry_with_backoff(_login_request, encrypted_mem_id, max_retries=3, fixed_interval=1)
    except Exception as e:
        logging.error(f"Login failed after retries: {str(e)}")
        return None, None

def _getAndharBaharLastStatus_request(input_str):
    """Internal function to make Andhar Bahar last status request"""
    url = "https://sev04.gigp.vip/GAAndroidSer/AndWsService.svc"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev04.gigp.vip",
        "SOAPAction": '"http://tempuri.org/IAndWsService/IGetAndharBaharLastStatus"'
    }
    body = getAndharBaharLastStatusRequestBody(input_str)

    response = session.post(url, headers=headers, data=body)
    response.raise_for_status()

    match = re.search(r"<IGetAndharBaharLastStatusResult>(.*?)</IGetAndharBaharLastStatusResult>", response.text)
    if match:
        encrypted_result = match.group(1)
        decrypted_result = utils.decrypt(encrypted_result)

        # Example decrypted_result: "Some:Prefix:123456,20"
        parts = decrypted_result.split(":")
        if len(parts) >= 3:
            draw_info = parts[2].split(",")
            drawId = int(draw_info[0])
            timerVal = int(draw_info[1])
            return timerVal + 1, drawId
        else:
            logging.error(f"Decrypted format invalid: {decrypted_result}")
            raise ValueError("Invalid decrypted format")
    else:
        logging.error(f"Unexpected response format: {response.text}")
        raise ValueError("Unexpected response format")

def getAndharBaharLastStatus(input_str):
    """Get Andhar Bahar last status with retry mechanism"""
    try:
        return retry_with_backoff(_getAndharBaharLastStatus_request, input_str, max_retries=4, fixed_interval=1)
    except Exception as e:
        logging.error(f"Get Andhar Bahar last status failed after retries: {str(e)}")
        return None, None
    
def _getAndharBaharDrawnoResult_request(input_str):
    """Internal function to make Andhar Bahar draw number request"""
    url = "https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev06.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IGetAnharBaharDrawno"
    }

    body = getAndharBaharDrawNoRequestBody(input_str)
    
    response = session.post(url, headers=headers, data=body)
    response.raise_for_status()
    # print(response.text)

    match = re.search(r"<IGetAnharBaharDrawnoResult>(.*?)</IGetAnharBaharDrawnoResult>", response.text)
    if match:
        parts = match.group(1).split(',')

        if len(parts) != 5:
            raise ValueError("Response parts count not 5, got: " + str(len(parts)))

        win_card = parts[0]
        logging.info(f"draw_card: {win_card}")
        if win_card[0] == "0" or win_card[0] == "1":
            draw_val = "R"
        else:
            draw_val = "B"

        rem_time = int(parts[-2])
        draw_id = int(parts[-1])

        return draw_val, rem_time, draw_id, win_card
    
    else:
        logging.error(f"Unexpected response format: {response.text}")
        raise ValueError("Unexpected response format")

def getAndharBaharDrawnoResult(input_str):
    """Get Andhar Bahar draw number result with retry mechanism"""
    try:
        # Using more retries (10) with fixed 1 second interval
        return retry_with_backoff(_getAndharBaharDrawnoResult_request, input_str, 
                                  max_retries=10, fixed_interval=1)
    except Exception as e:
        logging.error(f"Get Andhar Bahar draw number result failed after retries: {str(e)}")
        return None, None, None, None

def _placeABBet_request(input_str):
    """Internal function to place Andhar Bahar bet"""
    url = "https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev06.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IAndharBaharBetDataProcess"
    }

    body = getAndharBaharBetRequestBody(input_str)

    response = session.post(url, headers=headers, data=body)
    response.raise_for_status()
    # print(response.text)

    if re.search(r'\bOK\b', response.text):
        logging.info("Successfully Bet Placed!")
        return "OK"
    else:
        logging.error("Error while Placing bet..")
        raise ValueError(f"Placing bet failed: {response.text}")

def placeABBet(input_str):
    """Place Andhar Bahar bet with retry mechanism"""
    try:
        # Fixed 1 second interval between retries for placing bets
        result = retry_with_backoff(_placeABBet_request, input_str, 
                                   max_retries=3, fixed_interval=1)
        return result if result else "ERROR"
    except Exception as error:
        logging.error(f"Error while placing bet after retries: {error}")
        return "ERROR"

def _takeABBet_request(input_str):
    """Internal function to take Andhar Bahar bet"""
    # Using the correct URL and host from the template
    url = "https://sev06.gigp.vip/GAAndroidSer/AndWsService.svc"

    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev06.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IAndharBaharTakeDataProcess"
    }

    body = getAndharBaharTakeBetRequestBody(input_str)

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    # print(response.text)  # Uncommented to see response for debugging

    if re.search(r'\bOK\b', response.text):
        return "OK"
    else:
        logging.error("Error while taking amount..")
        raise ValueError(f"Taking bet failed: {response.text}")

def takeABBet(input_str):
    """Take Andhar Bahar bet with retry mechanism"""
    try:
        result = retry_with_backoff(_takeABBet_request, input_str, 
                                   max_retries=3, fixed_interval=1)
        return result if result else "ERROR"
    except Exception as error:
        logging.error(f"Error while taking bet amount after retries: {error}")
        return "ERROR"

# 524216789,6655010,3,2000,GK00555068,759.00,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0
