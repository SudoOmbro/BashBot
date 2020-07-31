class Script:

    def __init__(self, name, body, description, verbose):
        self.name = name
        self.body = body
        self.description = description
        self.verbose = verbose  # controls if the scripts returns each command's output

    def __str__(self):
        return f"{self.name}:\n{self.description}\n\nbody:\n{self.body}\n\nverbose:{self.verbose}"

    @staticmethod
    def get_scripts_from_json(scripts_json):
        scripts_json_data = scripts_json["scripts"]
        result = []
        for element in scripts_json_data:
            result.append(Script(
                element["name"],
                element["body"],
                element["description"],
                element["verbose"]
            ))
        return result
