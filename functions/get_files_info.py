from google.genai import types
import os

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory):
        return f"Error: Invalid working directory {working_directory}"
    if directory:
        directory = os.path.abspath(os.path.join(working_directory, directory))
        if not os.path.isdir(directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not directory:
        directory = working_directory

    if not directory.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    output = ""
    for name in os.listdir(directory):
        path = directory + "/" + name
        output += f"- {name}: "
        size = os.path.getsize(path)
        output += f"file_size={size} bytes, "
        output += f"is_dir={os.path.isdir(path)}"
        output += "\n"

    return output

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT, properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
