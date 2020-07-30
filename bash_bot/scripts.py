class Script:

    def __init__(self, name, body, description):
        self.name = name
        self.body = body
        self.description = description

    def __str__(self):
        return "{}:\n{}\n\nbody:\n{}".format(self.name, self.description, self.body)
