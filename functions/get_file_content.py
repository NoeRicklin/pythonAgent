from google.genai import types
import os

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory):
        return f"Error: Invalid working directory {working_directory}"
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
 
    MAXCHARS = 10_000
    with open(file_path) as f:
        text = f.read(MAXCHARS)
        if f.read(1) != "":
            text += f'[...File "{file_path}" truncated at 10000 characters]'

    return text

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file. Files longer than 10000 characters are truncated and marked at the end. The file_path is given relative to the working directory, which is expected to be the root of the project.",
    parameters=types.Schema(
        type=types.Type.OBJECT, properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to retrieve the content from. The path is assumed to be relative to the root of the project by the program",
            ),
        },
    ),
)
