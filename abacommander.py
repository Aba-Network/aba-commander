# 
# Chat w/ functional calling a.i. LLM running locally on port 1234, which can start/stop an Aba blockchain node

import os
import datetime
import json
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    chain = os.environ["CHAIN"]
except KeyError:
    chain = "aba"  # Default value if not found in the environment

permitted_values = {"aba", "chia"}
if chain not in permitted_values:
    raise ValueError(f"Invalid chain value. Allowed values are {permitted_values}")

try:
    activate_dir = os.environ["ACTIVATE_DIR"]
except KeyError:
    activate_dir = "~/aba-blockchain"

# Query Gorilla server
def get_gorilla_response(prompt="", model="gorilla-openfunctions-v1", functions=[]):
  api_key = "EMPTY"
  api_base = "http://localhost:1234/v1"
  try:
    prompt = f'<<question>> {prompt} <<function>> {json.dumps(functions)}'
    client = OpenAI(api_key = api_key, base_url = api_base)
    completion = client.chat.completions.create(
      model="gorilla-openfunctions-v1",
      temperature=0.5,
      messages=[{"role": "user", "content": prompt}],
      functions=functions,
    )
    return completion.choices[0].message.content
  except Exception as e:
    print(e, model, prompt)


def nowdate():
    now = datetime.datetime.now()
    return("Current local time and date: " + now.strftime("%Y-%m-%d %H:%M:%S"))

def run_command(subcommand, output=True):
    print(subcommand)
    """
    Executes a aba CLI command and returns its output.
    
    Parameters:
        subcommand (str): The aba CLI command to execute.
        
    Returns:
        str: The output of the aba CLI command.
    """

    # set up env to use the dev version of aba etc
    command = f". {activate_dir}/activate; {subcommand}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #process = subprocess.Popen(subcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print("running process")
    if output:
        output, error = process.communicate()
        if error:
            print("Error:", error.decode())
        return output.decode()
    else:
        return True

def check_cmd(name, input):
    if (input.startswith(name + "(") and input.endswith(")")):
        return True
    return False

def parse_response(response):
    """
    Parses an aba CLI response and calls the appropriate command based on the response string.
    
    Parameters:
        response (str): The aba CLI response to parse.
        
    Returns:
        None
    """
    if check_cmd(chain + "_show", response): #response == "aba show -s":
        return run_command(chain + " show -s")
    elif check_cmd(chain + "_start_all", response):
        return run_command(chain + " start all", output=False)
    elif check_cmd(chain + "_stop_all", response):
        return run_command(chain + " stop all", output=False)
    elif check_cmd(chain + "_wallet_show", response):
        return run_command(chain + " wallet show")
    elif (response.startswith("nowdate(") and response.endswith(")")):
        return nowdate()
    else:
        print("Invalid function call:", response)

def goodbye():
    """Function to print a goodbye message"""
    print("Goodbye!")

functions = [    
{
    "name": chain + "_show",
    "api_call": chain + "_show",
    "description": "show the status of the aba node and network"
},
{
    "name": chain + "_start_all",
    "api_call": chain + "_start_all",
    "description": "start aba running, including all its processes"
},
        {
    "name": chain + "_stop_all",
    "api_call": chain + "_stop_all",
    "description": "stop aba, including all aba processes"
},
{
    "name": chain + "_wallet_show",
    "api_call": chain + "_wallet_show",
    "description": "show the general details of the aba wallet, including public keys and balance and info"
},
{
    "name": "nowdate",
    "api_call": "nowdate",
    "description": "display date and time"
}
]
while True:
    print()
    print("ABA Blockchain Commander, from www.aba.ooo")
    print()
    print("Type in your question or 'q' or 'quit' to exit: ")
    print()
    query = input(">")    
    if query == "quit" or query == "q":
        goodbye()
        break
    else:

        print(parse_response(get_gorilla_response(query, functions=functions)))
