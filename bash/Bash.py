import subprocess


def execute_command(command):
    args_list = command.split(" ")
    out = subprocess.Popen(
        args_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = out.communicate()
    print(stdout, stderr)
    if stderr is not None:
        return stdout + stderr
    return stdout
