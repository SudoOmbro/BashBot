import subprocess


def execute_command(command):
    """ execute a command on the shell """
    args_list = command.split(" ")
    out = subprocess.Popen(
        args_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = out.communicate()
    if stderr is not None:
        return f"stdout:{stdout}\n\nstderr:{stderr}"
    return f"stdout:{stdout}"
