# icecast2soundexchange
A Python script to convert icecast access.log logfiles to what SoundExchange needs

This is based on what is described at:
https://digitalservices.npr.org/post/soundexchange-streaming-file-format-standard-announced

It assumes that the icecast fields are in this order:

c-ip null null [datetime] c-uri-request c-status c-bytes c-referer c-User-Agent seconds

Such as:

1.2.3.4 - - [05/Apr/2021:07:28:01 -0700] "GET /128 HTTP/1.1" 200 57635827 "-" "Lavf/58.29.100" 3600

The mapping looks like this for the Soundexchange required columns:
* "IP address" (#.#.#.#; Do NOT include port numbers (127.0.0.1:3600))
  icecast: c-ip
* "Date" listener tuned in (YYYY-MM-DD)
  icecast: date (but must be converted to UTC)
* "Time" listener tuned in (HH:MM:SS; 24-hour military time; UTC time zone)
  icecast: time (but must be converted to UTC)
* "Stream" ID (No spaces)
  Station Call Letters
* "Duration" of listening (Seconds)
  icecast: seconds
* HTTP "Status" Code
  icecast: c-status
* "Referrer"/Client Player  
  icecast: c-User-Agent
  
You will need to update the timezone and the station call letters in the script.  The output is tab delimited format that SoundExchange requires.

Typically you would run it as:

ice2se.py access.log > soundexchange.log

You will need to install the pytz module.  This is typically done by running "pip install pytz".  pytz does the conversion from localtime to UTC that SoundExchange needs.

This should run on Unix variants and Mac from a terminal window.  If you are using Windows, follow these instructions... https://edu.google.com/openonline/course-builder/docs/1.10/set-up-course-builder/check-for-python.html#windows

