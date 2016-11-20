Zabbix Mattermost AlertScript
========================


About
-----
This is simply a Bash script that uses the custom alert script functionality within [Zabbix](http://www.zabbix.com/) along with the incoming web-hook feature of [Mattermost](https://mattermost.com/).

#### Versions
This works with Zabbix 1.8.x or greater - including 2.2, 2.4 and 3.x!

#### Huge thanks and appreciation to:

* [Eric OC](https://github.com/ericoc) where this was originally forked from (https://github.com/ericoc/zabbix-slack-alertscript)
* [Paul Reeves](https://github.com/pdareeves/) for the hint that Mattermost changed their API/URLs!
* [Igor Shishkin](https://github.com/teran) for the ability to message users as well as channels!
* Leslie at AspirationHosting for confirming that this script works on Zabbix 1.8.2!
* [Hiromu Yakura](https://github.com/hiromu) for escaping quotation marks in the fields received from Zabbix to have valid JSON!
* [Devlin Gonçalves](https://github.com/devlinrcg), [tkdywc](https://github.com/tkdywc), [damaarten](https://github.com/damaarten), and [lunchables](https://github.com/lunchables) for Zabbix 3.0 AlertScript documentation, suggestions and testing!

Installation
------------

### The script itself

This [`mattermost.sh` script](https://raw.githubusercontent.com/muokata/zabbix-mattermost-alertscript/master/mattermost.sh) needs to be placed in the `AlertScriptsPath` directory that is specified within the Zabbix servers' configuration file (`zabbix_server.conf`) and must be executable by the user running the zabbix_server binary (usually "zabbix") on the Zabbix server before restarting the Zabbix server software:

	[root@zabbix ~]# grep AlertScriptsPath /etc/zabbix/zabbix_server.conf
	### Option: AlertScriptsPath
	AlertScriptsPath=/usr/lib/zabbix/alertscripts

	[root@zabbix ~]# ls -lh AlertScriptsPath=/usr/lib/zabbix/alertscriptsmattermost.sh
	-rwxr-xr-x 1 root root 1.6K Nov 19 20:04 /usr/lib/zabbix/alertscripts/mattermost.sh

Configuration
-------------

### mattermost web-hook

An incoming web-hook integration must be created within your Mattermost account which can be done at https://<your mattermost uri>/chattr/integrations/incoming_webhooks:


the incoming web-hook URL would be something like:

	https://<your mattermost uri>/hooks/ere5h9gfbbbk8gdxsdsduwuicsd

Make sure that you specify your correct Mattermost incoming web-hook URL and feel free to edit the sender user name at the top of the script:

	# Mattermost incoming web-hook URL and user name
	url='https://<your mattermost uri>/hooks/ere5h9gfbbbk8gdxsdsduwuicsd'
	username='zabbix'


### Within the Zabbix web interface

When logged in to the Zabbix servers web interface with super-administrator privileges, navigate to the "Administration" tab, access the "Media Types" sub-tab, and click the "Create media type" button.

You need to create a media type as follows:

* **Name**: Mattermost
* **Type**: Script
* **Script name**: mattermost.sh

...and ensure that it is enabled before clicking "Save".

<!-- ![Zabbix Media Type](https://pictures.ericoc.com/github/zabbix-mediatype.png "Zabbix Media Type") -->

However, on Zabbix 3.x and greater, media types are configured slightly differently and you must explicity define the parameters sent to the `mattermost.sh` script. On Zabbix 3.x, three script parameters should be added as follows:

* `{ALERT.SENDTO}`
* `{ALERT.SUBJECT}`
* `{ALERT.MESSAGE}`

<!--  ...as shown here:

![Zabbix 3.x Media Type](https://pictures.ericoc.com/github/zabbix3-mediatype.png "Zabbix 3.x Media Type") -->

Then, create a "Mattermost" user on the "Users" sub-tab of the "Administration" tab within the Zabbix servers web interface and specify this users "Media" as the "Mattermost" media type that was just created with the Mattermost.com channel ("#alerts" in the example) or user name (such as "@ericoc") that you want messages to go to in the "Send to" field as seen below:

<!--  ![Zabbix User](https://pictures.ericoc.com/github/zabbix-user.png "Zabbix User") -->

Finally, an action can then be created on the "Actions" sub-tab of the "Configuration" tab within the Zabbix servers web interface to notify the Zabbix "Mattermost" user ensuring that the "Subject" is "PROBLEM" for "Default message" and "RECOVERY" should you choose to send a "Recovery message".

Keeping the messages short is probably a good idea; use something such as the following for the contents of each message:

	{TRIGGER.NAME} - {HOSTNAME} ({IPADDRESS})

Additionally, you can have multiple different Zabbix users each with "Mattermost" media types that notify unique Mattermost users or channels upon different triggered Zabbix actions.


Testing
-------
Assuming that you have set a valid Mattermost web-hook URL within your "mattermost.sh" file, you can execute the script manually (as opposed to via Zabbix) from Bash on a terminal:

	$ bash mattermost.sh '#alerts' PROBLEM 'Oh no! Something is wrong!'

Alerting a specific user name results in the message actually coming from the "mattermostbot" user using a sort-of "spoofed" user name within the message. A channel alert is sent as you would normally expect from whatever user name you specify in "mattermost.sh":

<!--  ![Mattermost Testing](https://pictures.ericoc.com/github/mattermost-example.png "Mattermost Testing") -->


More Information
----------------
* [Mattermost incoming web-hook functionality](https://docs.mattermost.com/developer/webhooks-incoming.html)
* [Zabbix 2.2 custom alertscripts documentation](https://www.zabbix.com/documentation/2.2/manual/config/notifications/media/script)
* [Zabbix 2.4 custom alertscripts documentation](https://www.zabbix.com/documentation/2.4/manual/config/notifications/media/script)
* [Zabbix 3.x custom alertscripts documentation](https://www.zabbix.com/documentation/3.0/manual/config/notifications/media/script)
