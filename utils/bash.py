import os
import subprocess
import sys


class Shell:

    def __init__(self, base_working_dir):
        self.home_path = base_working_dir
        self.dir = base_working_dir
        self.is_linux = sys.platform == "linux"

    def _check_directory_change(self, args_list):
        if args_list[0] == "cd":
            if len(args_list) == 1:
                # go back to working directory
                self.dir = self.home_path
            elif args_list[1] == "..":
                # go up one level
                tree = self.get_tree_from_path(self.dir)
                new_tree = tree[:-1]
                self.dir = self.build_path_from_tree(new_tree)
            elif args_list[1][0] == "\\" or args_list[1][0] == "/":
                # go to absolute path
                if self.is_linux:
                    new_dir = args_list[1]
                else:
                    new_dir = args_list[1][1:]
                if os.path.isdir(new_dir):
                    self.dir = new_dir
                else:
                    return "The specified path does not exist"
            else:
                # go down one level
                sub_folders = [f.name for f in os.scandir(self.dir) if f.is_dir()]
                if args_list[1] in sub_folders:
                    self.dir += args_list[1]
                else:
                    return f"There is no folder named \"{args_list[1]}\" in the current path"
            return self.dir
        return None

    def get_tree_from_path(self, path):
        cleaned_tree = []
        if not self.is_linux:
            tree = path.split("\\")
        else:
            tree = path.split("/")
        for branch in tree:
            if branch != "":
                cleaned_tree.append(branch)
        return cleaned_tree

    def build_path_from_tree(self, tree):
        if not self.is_linux:
            path = ""
            for branch in tree:
                path += branch + "\\"
        else:
            path = "/"
            for branch in tree:
                path += branch + "/"
        return path

    def execute_command(self, command):
        try:
            """ execute a command on the shell """
            args_list = command.split(" ")
            cd = self._check_directory_change(args_list)
            if cd is not None:
                return cd
            out = subprocess.run(
                args_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                cwd=self.dir
            )
            stdout, stderr = out.stdout, out.stderr
            try:
                stdout, stderr = stdout.decode(), stderr.decode()
            except UnicodeDecodeError:
                pass
            if stderr is not None:
                return self._format_output(f"stdout:\n{stdout}\n\nstderr:\n{stderr}")
            return self._format_output(f"stdout:\n{stdout}")
        except OSError as e:
            return str(e)

    def _format_output(self, string):
        if self.is_linux:
            return string
        return string.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
