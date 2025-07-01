import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

verbose = False

if len(sys.argv) < 2:
    print("Usage: main.py [Your Prompt]")
    exit(1)

if len(sys.argv) >= 3:
    if sys.argv[2] == "--verbose":
        verbose = True

prompt = sys.argv[1]

messages = [types.Content(role="user",
                      parts=[types.Part(text=prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

prompt_tokens = 0
response_tokens = 0

if verbose:
    print(f"User prompt:\n{prompt}")

for i in range(20):
    ai_response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]))

    prompt_tokens += ai_response.usage_metadata.prompt_token_count
    response_tokens += ai_response.usage_metadata.candidates_token_count

    for candidate in ai_response.candidates:
        messages.append(candidate.content)

    if ai_response.function_calls:
        for function_call_part in ai_response.function_calls:
            try:
                result = call_function(function_call_part, verbose)
                messages.append(result)
                response = result.parts[0].function_response.response["result"]
                if verbose:
                    print(f"-> {response}")
            except:
                raise Exception("Invalid return value from call_function")
    else:
        print(f"Response:\n{ai_response.text}")
        exit()
    if True:
        print(f"Response:\n{ai_response.text}")

if verbose:
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
