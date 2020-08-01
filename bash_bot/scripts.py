import json


class Script:

    def __init__(self, name: str, body: str, description: str, verbose: bool):
        self.name = name
        self.body = body
        self.description = description
        self.verbose = verbose  # controls if the scripts returns each command's output

    def __str__(self):
        return f"*{self.name}:*\n{self.description}\n\n*body:*\n{self.body}\n\n*verbose:* {self.verbose}"

    def save(self, script_list: list):
        if self not in script_list:
            script_list.append(self)

    @staticmethod
    def get_scripts_from_json(scripts_json: json):
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

    @staticmethod
    def get_script_from_name(script_list: list, script_name: str):
        for script in script_list:
            if script.name == script_name:
                return script
        return None

    @staticmethod
    def get_script_list_json(script_list: list):
        dict_list = []
        for script in script_list:
            dict_list.append(script.__dict__)
        return {"scripts": dict_list}
