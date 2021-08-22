# Tesla EDD Checker
#Requirements:
* Python 3.9
* Chrome browser with the appropriate chromedriver for your OS and Chrome version
    * Add the chromedriver to your system's path 
* The following system environment variables:
    * TESLA_USERNAME: your tesla website username
    * TESLA_PASSWORD: your tesla website password
    * ALERT_WEBHOOK: Discord webhook for alerting you of an EDD change
    * STATUS_WEBHOOK: Discord webhook for simply letting you know the script ran when there is no EDD change
  
If you don't want to use Discord notifications, just comment out/delete the discord portions of the code. 
I find discord alerts to be the easiest way to get notified immediately on my phone for free.

If you do want to use Discord alerts, I'd suggest setting up a new Discord server and creating the two webhooks. 
Have the status webhook set up so that it won't alert you on new messages. 

How to create a Discord server: https://www.howtogeek.com/318890/how-to-set-up-your-own-discord-chat-server/

How to create webhooks: https://www.socialoomph.com/help/view/help_discord_webhook_how/

# Install python libraries
* pip install -r requirements.txt

