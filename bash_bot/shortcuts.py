class Shortcut:

    def __init__(self, command, args, description):
        self.command = command
        self.args = args
        self.description = description

    def __str__(self):
        text = "/" + self.command + " "
        for arg in self.args:
            text += "[" + arg + "] "
        text += "- " + self.description
