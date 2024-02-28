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
    link_pattern = re.compile(r"\((s\d+, s\d+)\) |\((s\d+, h\d+)\)")
    ping_test_pattern = re.compile(r"\*\*\* Ping: testing ping reachability\n(.+?)\n\*\*\*")
    warning_pattern = re.compile(r"\*\*\* Warning: (.+)")
    performance_pattern = re.compile(r"completed in ([\d.]+) seconds")
    
    # Extract information
    hosts_match = host_pattern.search(output)
    switches_match = switch_pattern.search(output)
    links_matches = link_pattern.findall(output)
    ping_test_match = ping_test_pattern.search(output)
    warnings = warning_pattern.findall(output)
    performance_match = performance_pattern.search(output)

    # Process and structure information
    if hosts_match:
        structured_data["network_setup"]["hosts"] = [host.strip() for host in hosts_match.group(1).split()]
    if switches_match:
        structured_data["network_setup"]["switches"] = [switch.strip() for switch in switches_match.group(1).split()]
    if links_matches:
        structured_data["network_setup"]["links"] = [f"({link[0].strip()})" if link[0] else f"({link[1].strip()})" for link in links_matches]
    if ping_test_match:
        structured_data["execution_details"]["ping_test"] = ping_test_match.group(1).strip()
    if warnings:
        structured_data["execution_details"]["warnings"] = warnings
    if performance_match:
        structured_data["execution_details"]["performance"] = f"{performance_match.group(1)} seconds"

    return structured_data


