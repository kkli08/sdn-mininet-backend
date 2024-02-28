from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import subprocess

def process_mininet_parameters(request, depth, fanout):
    # Construct the command with the parameters
    command = f"sudo mn --switch ovs --controller ovsc --topo tree,depth={depth},fanout={fanout} --test pingall"
    
    # Execute the command and capture the output
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        command_output = result.stdout
    except subprocess.CalledProcessError as e:
        # If the command fails, capture the error output instead
        command_output = e.output

    # Construct the response data
    response_data = {
        'depth': depth,
        'fanout': fanout,
        'command_output': command_output
    }

    return JsonResponse(response_data)

