import json
import fcntl
import os
from apis_call import *
from threading import Thread
import time
from termcolor import colored
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)


class AutomateGame:

    def __init__(self, total_amount, session_id, member_id, bet_amount):
        self.TOTAL_AMOUNT = total_amount
        self.SESSION_ID = session_id
        self.MEMBER_ID = member_id
        self.AB_VERSION = "R1.0.0.1"
        self.CCS_ID = "2000"
        self.STAMP_ID = 1
        
        self.DRAW_NO = ""
        self.DRAW_CARD = ""
        self.BET_PLACED_DRAW_ID = ""
        self.BET_PLACED_DRAW_CARD = ""
        self.is_pattern_found_r = False
        self.is_pattern_found_b = False
        self.is_bet_placed_r = False
        self.is_bet_placed_b = False
        self.game_bet_ammount = bet_amount
        self.game_win_ammount = bet_amount*1.95
        self.win_amount = 0

        # This function should return (remaining_time, draw_id)
        self.REM_TIME, self.DRAWID = getAndharBaharLastStatus(
            f"{self.MEMBER_ID},{self.SESSION_ID},{self.AB_VERSION}"
        )

        if not self.DRAWID:
            raise ValueError("Invalid Draw ID!")

        # Start timer in a separate thread
        timer_thread = Thread(target=self.start_timer, args=(self.REM_TIME,))
        timer_thread.daemon = True
        timer_thread.start()
        

    def check_pattern(self):

        # if draw no is r then check if bet placed already, if yes then take amount else 

        if self.DRAW_NO == "R":
            if self.is_bet_placed_r and self.DRAW_NO == "R":
                self.take_bet()
                # self.place_bet()
            
            elif self.DRAW_NO == "R":
                self.place_bet("R")

            if self.is_bet_placed_b:
                self.is_bet_placed_b = False

        elif self.DRAW_NO == "B":
            if self.is_bet_placed_b and self.DRAW_NO == "B":
                self.take_bet()
                # self.place_bet()
            
            elif self.DRAW_NO == "B":
                self.place_bet("B")

            if self.is_bet_placed_r:
                self.is_bet_placed_r = False
            


    def place_bet(self, bet_on):
        temp_amount = self.TOTAL_AMOUNT - self.game_bet_ammount
        # For B pattern

        if bet_on == "B":
            res = placeABBet(f"{self.SESSION_ID},{self.DRAWID},{self.STAMP_ID},{self.CCS_ID},{self.MEMBER_ID},{temp_amount:.2f},0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{self.game_bet_ammount},0,0,0")
        else:
            res = placeABBet(f"{self.SESSION_ID},{self.DRAWID},{self.STAMP_ID},{self.CCS_ID},{self.MEMBER_ID},{temp_amount:.2f},0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{self.game_bet_ammount},0,0,0,0")

        
        if res == "OK":
            self.TOTAL_AMOUNT -= self.game_bet_ammount
            self.BET_PLACED_DRAW_ID = self.DRAWID
            self.STAMP_ID += 1
            file_path = "/home/ubuntu/my-api/data.json"

            if bet_on == "B":
                self.is_bet_placed_b = True
            else:
                self.is_bet_placed_r = True

            with open(file_path, "r+") as f:
                # Acquire an exclusive lock — this will block until it's available
                fcntl.flock(f, fcntl.LOCK_EX)

                data = json.load(f)

                # Modify the data
                data[self.MEMBER_ID] = self.TOTAL_AMOUNT

                # Rewind and truncate before writing new data
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)

                # Release the lock (automatically released when file is closed)
                fcntl.flock(f, fcntl.LOCK_UN)

            logging.info(f"BET PLACED SUCCESSFULLY  ---- AMOUNT - {self.TOTAL_AMOUNT}")
        else:
            if bet_on == "B":
                self.is_bet_placed_b = True
            else:
                self.is_bet_placed_r = True


    def take_bet(self):
        self.win_amount += self.game_win_ammount
        temp_amount = self.TOTAL_AMOUNT + self.win_amount
        input_str = f"{self.SESSION_ID},{self.BET_PLACED_DRAW_ID},{self.STAMP_ID},{self.CCS_ID},{self.MEMBER_ID},{self.TOTAL_AMOUNT:.2f},3,1,{self.DRAW_CARD},{self.win_amount:.2f},0,0,0,{self.win_amount:.2f},0"
        logging.info(f"Take bet input: {input_str}")
        res = takeABBet(input_str)
        logging.info(f"Response text is from the take amount api : {res}")
        if res == "OK":
            self.TOTAL_AMOUNT = temp_amount
            self.win_amount = 0
            self.STAMP_ID += 1
            self.is_bet_placed = False
            logging.info(f"Successfully Received the Winning Amount {self.TOTAL_AMOUNT}")

    
    def get_new_draw_no(self):

        logging.info("Getting Draw Card")
        draw_no, rem_time, draw_id, draw_card = getAndharBaharDrawnoResult(f"{self.DRAWID}")

        logging.info(f"Draw info: {draw_no}, {draw_id}, {rem_time}, {draw_card}")
    
        if not draw_id or not draw_no:
            logging.error("Failed to get new draw ID or draw No")
            return

        self.REM_TIME = rem_time
        self.DRAWID = draw_id
        self.DRAW_NO = draw_no
        self.DRAW_CARD = draw_card
        
        # Start timer again with updated rem_time
        Thread(target=self.start_timer, args=(self.REM_TIME,), daemon=True).start()

        Thread(target=self.check_pattern, daemon=True).start()



    def start_timer(self, rem_time):
        time.sleep(rem_time)
        self.get_new_draw_no()



if __name__ == "__main__":
    
    MEMBER_ID = os.environ.get("MEMBER_ID")
    LOGIN_ID  = os.environ.get("LOGIN_ID")
    BET_AMOUNT = os.environ.get("BET_AMOUNT")

    # ---- Validate and type-cast ----
    if not MEMBER_ID or not LOGIN_ID:
        raise ValueError("MEMBER_ID and LOGIN_ID must be set in environment.")

    try:
        BET_AMOUNT = float(BET_AMOUNT)
    except (TypeError, ValueError):
        raise ValueError("BET_AMOUNT must be a number in environment.")


    # ---- Login and start ----
    SESSION_ID, TOTAL_AMOUNT = login(LOGIN_ID)
    if not SESSION_ID or not TOTAL_AMOUNT:
        raise ValueError("Login failed: invalid session id or amount.")

    AutomateGame(TOTAL_AMOUNT, SESSION_ID, MEMBER_ID, BET_AMOUNT)

    while True:
        time.sleep(1)


