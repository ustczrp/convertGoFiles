import os
import time
from datetime import datetime
import json
import fileAccess
import httpx
from dotenv import load_dotenv
from openai import AzureOpenAI


def init():
    load_dotenv()

    api_key = os.getenv("API_KEY")
    api_version = os.getenv("API_VERSION")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        http_client=httpx.Client(verify=False)
    )
    return client


outputFunction = [
    {
        "type": "function",
        "function": {
                "name": "extract_source_file",
                "description": "Return a source code file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "string",
                            "description": "the actualt name of the source file",
                        },
                        "source": {
                            "type": "string",
                            "description": "the genereated source code file"
                        },
                    },
                    "required": ["source"],
                }
        }
    }
]


def execute_prompt(prompt, taskName, client):

    temperature = float(os.getenv("LLM_TEMPERATURE"))
    top_p = float(os.getenv("LLM_TOP_P"))

    model = os.getenv("MODEL")
    start_time = time.time()
    messages = [{"role": "user", "content": prompt}]

    fileAccess.trace(taskName+"Prompt", prompt)

    print(f'Start executing prompt ({taskName}) at: {datetime.now()}')

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        timeout=3000,
        tools=outputFunction,
        tool_choice="auto"
    )

    end_time = time.time()
    # print(f'Duration of chat_with_gpt4 for prompt ({taskName}): {
    #       end_time - start_time:.4f} seconds')

    return response


def process_llm_response(llmResponse):
    response_message = llmResponse.choices[0].message
    if response_message.tool_calls:
        if response_message.tool_calls[0]:
            try:
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                # strict=False allows for parsing java code in the arguments
                function_args = json.loads(
                    tool_call.function.arguments, strict=False)
                print(f"Function call: {function_name}")
                print(f"Function arguments: {function_args}")

                if function_name == "extract_source_file":
                    function_response = extract_source_file(request=function_args.get(
                        "request"), source=function_args.get("source"), tool_call=tool_call)
                else:
                    function_response = json.dumps(
                        {"error": "Unknown function"})
                    return function_response
            except Exception as e:
                print(f"Error processing function call: {e}")
                print(f"tool arguments: {tool_call.function.arguments}")
                function_response = json.dumps(
                    {
                        "error": f"Error processing function call: {e}",
                        "arguments": tool_call.function.arguments
                    })
                return function_response

        print(f"Function response:", function_response)
        return function_response.get("source")
    else:
        print("No tool calls were made by the model.")


def extract_source_file(request, source, tool_call):
    function_response = {
        "tool_call_id": tool_call.id,
        "role": "tool",
                "source": source,
                "request": request,
    }
    return function_response
