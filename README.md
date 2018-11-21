Zabbix Mattermost AlertScript
========================


About
-----
This script is a fork of [muokata/zabbix-mattermost-alertscript](https://github.com/muokata/zabbix-mattermost-alertscript). It has been rewritten in Python in order to manage rich messages (having newline and more) correctly JSON encoded. 

Please refer to the original repo for version supports and thanks. 


Installation
------------

### The script itself

This [`mattermost.py` script](https://raw.githubusercontent.com/jirouette/zabbix-mattermost-alertscript/master/mattermost.py) needs to be placed in the `AlertScriptsPath` directory that is specified within the Zabbix servers' configuration file (`zabbix_server.conf`) and must be executable by the user running the zabbix_server binary (usually "zabbix") on the Zabbix server before restarting the Zabbix server software:

	[root@zabbix ~]# grep AlertScriptsPath /etc/zabbix/zabbix_server.conf
	### Option: AlertScriptsPath
	AlertScriptsPath=/usr/lib/zabbix/alertscripts

	[root@zabbix ~]# ls -lh /usr/lib/zabbix/alertscripts/mattermost.py
	-rwxr-xr-x 1 root root 1.9K Nov 21 18:31 /usr/lib/zabbix/alertscripts/mattermost.py

Configuration
-------------

### mattermost web-hook

An incoming web-hook integration must be created within your Mattermost account which can be done at https://<your mattermost uri>/chattr/integrations/incoming_webhooks:


the incoming web-hook URL would be something like:

	https://<your mattermost uri>/hooks/ere5h9gfbbbk8gdxsdsduwuicsd

Make sure that you specify your correct Mattermost incoming web-hook URL and feel free to edit the sender user name at the top of the script:

	# Mattermost incoming web-hook URL and user name
	URL = "https://<your mattermost uri>/hooks/ere5h9gfbbbk8gdxsdsduwuicsd"
	USERNAME = "zabbix"


### Within the Zabbix web interface

When logged in to the Zabbix servers web interface with super-administrator privileges, navigate to the "Administration" tab, access the "Media Types" sub-tab, and click the "Create media type" button.

You need to create a media type as follows:

* **Name**: Mattermost
* **Type**: Script
* **Script name**: mattermost.py

...and ensure that it is enabled before clicking "Save".

However, on Zabbix 3.x and greater, media types are configured slightly differently and you must explicity define the parameters sent to the `mattermost.py` script. On Zabbix 3.x, three script parameters should be added as follows:

* `{ALERT.SENDTO}`
* `{ALERT.SUBJECT}`
* `{ALERT.MESSAGE}`

Then, create a "Mattermost" user on the "Users" sub-tab of the "Administration" tab within the Zabbix servers web interface and specify this users "Media" as the "Mattermost" media type that was just created with the Mattermost.com channel ("#alerts" in the example) or user name (such as "@ericoc") that you want messages to go to in the "Send to" field as seen below:

Additionally, you can have multiple different Zabbix users each with "Mattermost" media types that notify unique Mattermost users or channels upon different triggered Zabbix actions.


Testing
-------
Assuming that you have set a valid Mattermost web-hook URL within your "mattermost.py" file, you can execute the script manually (as opposed to via Zabbix) on a terminal:

	$ python mattermost.py '#alerts' PROBLEM 'Oh no! Something is wrong!'

Alerting a specific user name results in the message actually coming from the "mattermostbot" user using a sort-of "spoofed" user name within the message. A channel alert is sent as you would normally expect from whatever user name you specify in "mattermost.py":

More Information
----------------
* [Mattermost incoming web-hook functionality](https://docs.mattermost.com/developer/webhooks-incoming.html)
* [Zabbix 2.2 custom alertscripts documentation](https://www.zabbix.com/documentation/2.2/manual/config/notifications/media/script)
* [Zabbix 2.4 custom alertscripts documentation](https://www.zabbix.com/documentation/2.4/manual/config/notifications/media/script)
* [Zabbix 3.x custom alertscripts documentation](https://www.zabbix.com/documentation/3.0/manual/config/notifications/media/script)
* [Original repository muokata/zabbix-mattermost-alertscript](https://github.com/muokata/zabbix-mattermost-alertscript)