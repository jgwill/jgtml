# Minimal wrapper for jgtml/jgtapp.py commands as Langchain/Langgraph tools.


import subprocess
import json
import os
import sys
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.errors import GraphRecursionError
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools.shell import ShellTool

from langchain_ollama import OllamaLLM

import warnings
#

# Suppress the specific UserWarning
warnings.filterwarnings("ignore", category=UserWarning, message="The shell tool has no safeguards by default. Use at your own risk.")


@tool
def get_indicator_data(request_data: dict) -> str:
    """
    Fetch indicator data from the JGTrading API.
    """
    cmd = ["jgtcli", "ids", json.dumps(request_data)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def add_order(order_details: dict) -> str:
    """
    Submit a new trading order.
    """
    cmd = ["jgtcli", "fxaddorder", json.dumps(order_details)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def move_stop(order_id: str, new_stop: float) -> str:
    """
    Adjust the stop level of an existing order.
    """
    cmd = ["jgtcli", "fxmvstop", order_id, str(new_stop)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def remove_order(order_id: str) -> str:
    """
    Cancel an existing order.
    """
    cmd = ["jgtcli", "fxrmorder", order_id]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def remove_trade(trade_id: str) -> str:
    """
    Remove a trade from the system.
    """
    cmd = ["jgtcli", "fxrmtrade", trade_id]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def execute_trade(trade_details: dict) -> str:
    """
    Execute a trade with specified parameters.
    """
    cmd = ["jgtcli", "fxtr", json.dumps(trade_details)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

@tool
def entry_validate(order_id: str, timeframe: str, demo: bool=False) -> str:
    """
    Validate entry order in reference to timeframe and remove if invalid.
    """
    demo_arg = '--demo' if demo else '--real'
    cmd = ["jgtcli", "entryvalidate", order_id, timeframe, demo_arg]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def get_input() -> str:
    print("----------------------")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)

def build_agent(model, recursion_limit=10):
    base_model="llama3"
    host="localhost"
    model = OllamaLLM(model=base_model, base_url=host if host else None)
    #selected_tools = ["terminal"]
    #terminal_tool = load_tools("terminal",llm=model)
    
    tools = [
        add_order,
        move_stop,
        remove_order,
        remove_trade,
        execute_trade,
        entry_validate
    ]
    tools.append("terminal")
    tools.append("human")
    loaded_tools = load_tools(tools, llm=model,allow_dangerous_tools=True, input_func=get_input)
    
    agent = create_react_agent(model, tools=loaded_tools)
    agent.config = agent.config or {}
    agent.config["recursion_limit"] = recursion_limit
    return agent

def print_stream(stream):
    for s in stream:
        try:
            # Skip Langfuse internal state messages and size limit warnings
            if isinstance(s, dict) and ('keep_alive' in s or 'states' in s):
                continue
            if isinstance(s, str) and ('Item exceeds size limit' in s or 'pending_switch_proposals' in s):
                continue
                
            # Handle different response formats
            if isinstance(s, dict) and "messages" in s:
                message = s["messages"][-1]
            else:
                message = s
                
            if isinstance(message, tuple):
                print(message)
            elif hasattr(message, 'content'):
                print(message.content)
            else:
                print(s)
        except Exception as e:
            print(s)

if __name__ == "__main__":
    # Example usage through CLI for demonstration:
    # python jgtml_agent.py add_order '{"symbol":"EURUSD","quantity":1000,"price":1.2345}'
    # python jgtml_agent.py entry_validate "ORD123" "M15" true
    # if len(sys.argv) < 2:
    #     print("Usage: jgtml_agent.py <command> [arguments...]")
    #     sys.exit(1)

    # command = sys.argv[1]
    # args = sys.argv[2:]

    # Dummy model usage, adapt as needed for local or remote LLM
    model = None  
    graph = build_agent(model)
    graph.config["recursion_limit"] = 35
    system_instructions="You are interacting using the human tool addressing carefully what the user is asking."
    user_input="You assist in various trading actions and decisions. Interact with the user using the human tool"
    inputs = {"messages": [("system", system_instructions),("user", user_input)]}
    # Simple direct invocation of the tools without extra prompting:
    # if command not in graph.tools_dict:
    #     print(f"Command '{command}' not recognized by agent.")
    #     sys.exit(1)

    # Convert last arguments from JSON if it's a dict,
    # or parse booleans if needed (entry_validate uses that).
    try:
        print_stream(graph.stream(inputs))
        # result = graph.tools_dict[command](*args)
        # print(result)
    except GraphRecursionError:
        print("Recursion limit reached.")
    except Exception as e:
        print(f"Error executing '{command}': {e}")