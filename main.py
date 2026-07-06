import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import MAX_LOOPS


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("'OPENROUTER_API_KEY' missing from .env file")

CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    return response

# TODO: use the app to fix the calculator precedence, i'm rate limited

def main():

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    for _ in range(MAX_LOOPS):
        response = generate_content(CLIENT, messages)

        if response.usage is None:
            raise RuntimeError("the usage property is missing, this is likely caused by a failed api request")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise RuntimeError("content from tool call is missing")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            break
        if message.content:
            print(f"{message.content}")
    if message.tool_calls:
        print(f"handling process exceeded the {MAX_LOOPS} iterations")
    if message.content:
        print(f"Final response:\n{message.content}")
    
        


if __name__ == "__main__":
    main()
