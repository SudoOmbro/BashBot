# BashBot
_a bot that lets you access your server from telegram_

**DISCLAIMER**

This is still a very early version, it's basically just a proof of concept at this point

#features

* control the remote server on which the bot is located with the same commands you'd use on a shell
* seamlessly upload/download files to/from the machine with built in bot commands
* whitelist
* scripts (WIP)
* options screen to add/remove users to/from the whitelist and to edit all the scripts

# Notes

* When uploading a file through the bot, make sure to send it as file, even it it's an image.
* when using the "cd" command, note that "cd ~" won't work, use just "cd" instead
* when using the "cd" command, adding a "\\" as the first character will mark that path as absolute, even on Windows.

# How to setup
* clone the repository
* duplicate the config_template.json file and call it config.json
* fill in all the required fields in config.json (the whitelist isn't required)

_the whitelist, if not left empty, should be an array of Telegram User IDs_