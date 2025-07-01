from google.genai import types
import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory):
        return f"Error: Invalid working directory {working_directory}"
    if not os.path.isfile(os.path.join(working_directory, file_path)):
        return f'Error: File "{file_path}" not found.'
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        result = subprocess.run(["uv", "run", file_path] + args, capture_output=True, cwd=working_directory, timeout=30, encoding="utf-8") 

        output = ""
        if result.stdout != "":
            output = f"STDOUT: {result.stdout}"
        if result.stderr != "":
            output += f"STDERR: {result.stderr}"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if output != "":
            return output
        return "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified python program and returns its output along with any errors. There is a timeout of 30s for each program.",
    parameters=types.Schema(
        type=types.Type.OBJECT, properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be executed. Anything other than a .py file or an invalid path will return an error message."),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments for the program"),
        },
    ),
)
