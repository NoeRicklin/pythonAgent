import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

verbose = False

if len(sys.argv) < 2:
    print("Usage: main.py [Your Prompt]")
    exit(1)

if len(sys.argv) >= 3:
    if sys.argv[2] == "--verbose":
        verbose = True

prompt = sys.argv[1]

messages = [
        types.Content(role="user",
                      parts=[types.Part(text=prompt)]
                      )
        ]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose:
    print("User prompt: {prompt}")
print(f"Response:\n{response.text}")
if verbose:
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
