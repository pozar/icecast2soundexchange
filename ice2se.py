#!/usr/bin/python3

import datetime
import pytz
import sys
import socket
import shlex

callsign = 'KXXX'
# Change the following to your local timezone
localtz = 'America/Los_Angeles'
# 
# Icecast logs look like:
# Fields: c-ip null null [datetime] c-uri-request c-status c-bytes c-referer c-User-Agent seconds
# Example:
# 1.2.3.4 - - [05/Apr/2021:07:28:01 -0700] "GET /128 HTTP/1.1" 200 57635827 "-" "Lavf/58.29.100" 3600
# 0       1 2 3                     4      5                   6   7        8   9                10
# Soundexchange Required Columns:
# * "IP address" (#.#.#.#; Do NOT include port numbers (127.0.0.1:3600))
#   Icecast: c-ip
# * "Date" listener tuned in (YYYY-MM-DD)
#   Icecast: date (but must be converted to UTC)
# * "Time" listener tuned in (HH:MM:SS; 24-hour military time; UTC time zone)
#   Icecast: time (but must be converted to UTC)
# * "Stream" ID (No spaces)
#   Station Call Letters
# * "Duration" of listening (Seconds)
#   Icecast: seconds
# * HTTP "Status" Code
#   Icecast: c-status
# * "Referrer"/Client Player  
#   Icecast: c-User-Agent

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

total = len(sys.argv)
if total < 2:
    print("I need a file name on the command line")
    quit()

print("IP Address\tDate\tTime\tStream\tDuration\tStatus\tReferrer")
with open(sys.argv[1], "r") as infile:
    for line in infile:
        li=line.strip()
        if not li.startswith("#"):
            try:
                foo = shlex.split(li)
            except:
                pass
            ipaddr = foo[0]
            try:
                # Check for a valid IP address
                socket.inet_aton(ipaddr)
                logdatetime = foo[3][1:]
                status = foo[6]
                referrer = foo[8]
                sduration = foo[10]
                # Create datetime object
                try: 
                    d = datetime.datetime.strptime(logdatetime, "%d/%b/%Y:%H:%M:%S")
                except:
                    eprint("ERROR:" + line, end='')
                    continue
                # Set the time zone 
                try: 
                    d = pytz.timezone(localtz).localize(d)
                except:
                    eprint("ERROR:" + line, end='')
                    continue
                # Transform the time to UTC
                d = d.astimezone(pytz.utc)
                try: 
                    duration = int(sduration)
                except:
                    eprint("ERROR:" + line, end='')
                    continue
                if duration > 1:
                    print(ipaddr + '\t' + d.strftime("%Y-%m-%d\t%H:%M:%S") + '\t' + callsign + '\t' + sduration + '\t' + status + '\t' + referrer)

            except socket.error:
                # No IP address on this line.  Skip it.
                pass

