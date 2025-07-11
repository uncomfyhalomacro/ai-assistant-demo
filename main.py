import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def call_function(function_call_part, verbose=False):
    if not isinstance(function_call_part, types.FunctionCall):
        return "Error: are you sure your AI is running?"
    output_for_function_call_part = (
        f"Calling function: {function_call_part.name}({function_call_part.args})"
        if verbose
        else f" - Calling function: {function_call_part.name}"
    )
    print(output_for_function_call_part)
    result = ""
    if function_call_part.name not in [
        "get_files_info",
        "get_file_content",
        "write_file",
        "run_python_file",
    ]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    if function_call_part.name == "get_files_info":
        result = get_files_info("./calculator/", **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        result = get_file_content("./calculator/", **function_call_part.args)
    elif function_call_part.name == "write_file":
        result = write_file("./calculator/", **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        result = run_python_file("./calculator/", **function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )


def main():
    if len(sys.argv) <= 1:
        sys.exit(1)
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    function_calls = response.function_calls
    if function_calls:
        for function_call_part in function_calls:
            function_call_result = call_function(
                function_call_part, "--verbose" in sys.argv
            )
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if __name__ == "__main__":
    main()
