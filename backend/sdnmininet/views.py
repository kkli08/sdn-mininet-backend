from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import subprocess
import re

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

    # Parse the output and organize into a structured format
    structured_output = parse_mininet_output(command_output)

    # Construct the response data
    response_data = {
        'depth': depth,
        'fanout': fanout,
        'structured_output': structured_output
    }

    return JsonResponse(response_data)

def parse_mininet_output(output):
    # Initialize a structured data dictionary
    structured_data = {
        "network_setup": {
            "controllers": [],
            "hosts": [],
            "switches": [],
            "links": []
        },
        "execution_details": {
            "ping_test": "",
            "warnings": [],
            "performance": ""
        }
    }
    
    # Regex patterns for extracting information
    host_pattern = re.compile(r"\*\*\* Adding hosts:\n(.+?)\n")
    switch_pattern = re.compile(r"\*\*\* Adding switches:\n(.+?)\n")
    link_pattern = re.compile(r"\*\*\* Adding links:\n(.+?)\n")
    ping_test_pattern = re.compile(r"\*\*\* Ping: testing ping reachability\n(.+?)\n\*\*\*")
    warning_pattern = re.compile(r"\*\*\* Warning: (.+)")
    performance_pattern = re.compile(r"completed in ([\d.]+) seconds")
    
    # Extract and organize information
    hosts = host_pattern.search(output)
    switches = switch_pattern.search(output)
    links = link_pattern.search(output)
    ping_test = ping_test_pattern.search(output)
    warnings = warning_pattern.findall(output)
    performance = performance_pattern.search(output)

    if hosts:
        structured_data["network_setup"]["hosts"] = [host.strip() for host in hosts.group(1).split()]
    if switches:
        structured_data["network_setup"]["switches"] = [switch.strip() for switch in switches.group(1).split()]
    if links:
        structured_data["network_setup"]["links"] = [link.strip() for link in links.group(1).split(")")]
    if ping_test:
        structured_data["execution_details"]["ping_test"] = ping_test.group(1).strip()
    if warnings:
        structured_data["execution_details"]["warnings"] = warnings
    if performance:
        structured_data["execution_details"]["performance"] = f"{performance.group(1)} seconds"

    return structured_data

