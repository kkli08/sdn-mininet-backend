from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

def process_mininet_parameters(request, depth, fanout):
    # Example operation (replace with your actual logic)
    result = depth * fanout  # Replace this with the operation you want to perform

    # Construct the response data
    response_data = {
        'depth': depth,
        'fanout': fanout,
        'result': result
    }

    return JsonResponse(response_data)

