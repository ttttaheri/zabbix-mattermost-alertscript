#!/usr/bin/python
#coding: utf8

import json
import os
import sys
import requests

# Mattermost incoming web-hook URL and user name
URL = "<incoming webbook uri>" # example: httpsL//mattermost.example.com/hooks/ere5h9gfbbbk8gdxsei1tt8ewewechjsd
USERNAME = "zabbix"
ICON = "<icon_url>"
LEVELS = ["Warning", "Average","High", "Disaster"]

def send_to_mattermost(webhook, channel, message, username="zabbix", color="#FF2A00", icon="", highlight=False):
	# Build our JSON payload and send it as a POST request to the Mattermost incoming web-hook URL
	payload = {"icon_url": icon, "attachments": [{"color": color, "text": message}], "channel": channel, "username": username, "icon_emoji": ""}
	if highlight:
		payload["message"] = ":warning: Cc <!here>"
	requests.post(webhook, data={"payload": json.dumps(payload)})

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print("Usage: python "+sys.argv[0]+" <CHANNEL> <SUBJECT> <MESSAGE>")
		sys.exit(1)

	## Values received by this script:
	# To = sys.argv[1] (Mattermost channel or user to send the message to, specified in the Zabbix web interface; "@username" or "#channel")
	# Subject = sys.argv[2] (usually containing either "Problem" or "Resolved")
	# Message = sys.argv[3] (whatever message the Zabbix action sends)

	# Get the Mattermost channel or user (sys.argv[1]) and Zabbix subject (sys.argv[2])
	channel = sys.argv[1]
	subject = sys.argv[2]
        if "Resolved" in subject:
            subject=subject.replace("Resolved",":white_check_mark:")
        elif "Problem" in subject:
            subject=subject.replace("Problem",":warning:")
	
	color = "#00FF13" if "Resolved" in subject else "#FF2A00"

	# The message that we want to send to Mattermost  is the "subject" value (sys.argv[2] / $subject - that we got earlier)
	#  followed by the message that Zabbix actually sent us (sys.argv[3])
	message = "### "+subject + "\n\n"+sys.argv[3]

	# Let's highlight every connected people if the level is serious
	highlight = False
	for level in LEVELS:
		if level in message:
			highlight = True
			break

	# Send notification
	send_to_mattermost(URL, channel, message, username=USERNAME, color=color, icon=ICON, highlight=highlight)
