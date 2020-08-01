# BashBot
_a bot that lets you access and interact with your server from Telegram_

**DISCLAIMER**

This in an early version, there may be some bugs.

# features

* **control** the remote server on which the bot is located with the same commands you'd use on a shell
* **upload/download** files to/from the machine with built in bot commands
* **whitelist**
* **scripts**
* **options** screen to add/remove users to/from the whitelist
* runtime **script editor**

# Notes

* When uploading a file through the bot, make sure to send it as file, even it it's an image.
* when using the "cd" command, note that "cd ~" won't work, use just "cd" instead.
* when using the "cd" command, adding a "\\" as the first character will mark that path as absolute, even on Windows.
* when adding a user to an empty whitelist, you'll be added as well.

# How to setup
* clone the repository
* duplicate the config_template.json file and call it config.json
* fill in all the required fields in config.json (the whitelist isn't required)

_the whitelist, if not left empty, should be an array of Telegram User IDs_