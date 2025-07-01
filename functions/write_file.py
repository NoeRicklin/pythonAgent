from google.genai import types
import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory):
        return f"Error: Invalid working directory {working_directory}"
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_path.startswith(working_directory):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        os.makedirs(os.path.split(file_path)[0], exist_ok=True)
        f = open(file_path, "x")
        f.close()

    with open(file_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the contents of a file with the passed content.",
    parameters=types.Schema(
        type=types.Type.OBJECT, properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be overwritten.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The new script to be written to the specified file.",
            ),
        },
    ),
)
