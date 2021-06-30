import json, urllib.request
from datetime import datetime
import tzlocal
import re
import smtplib, ssl
import time
sender_email = ""
recipient_email = ""
smtp_password = ''
smtp_server = ""
port = 
json_url = ""
local_timezone = tzlocal.get_localzone() # get pytz timezone
var = 1

while var == 1 : 
    
    response = urllib.request.urlopen(json_url)
    data = json.loads(response.read())
    unix_timestamp = int(data["now"])
    
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    formattedtime = local_time.strftime("%m-%d-%Y %H:%M:%S %p")
   
    aircraftdata = data["aircraft"]

    match = re.search(r'(N12345|N12456)', str(aircraftdata))

    if match:
        message = """From: Server <{sender_email}>
    To: Recipient <{recipient_email}>

    Found {matched} in current search at {localtime}
    """.format(sender_email=sender_email, recipient_email=recipient_email, matched=match.group(), localtime=formattedtime)
        print("match found")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, smtp_password)
            print("logged in")
            print(message)
            server.sendmail(sender_email, recipient_email, message)
            print("mail sent")
            server.quit()
            print("server quit")
    
    time.sleep(600)