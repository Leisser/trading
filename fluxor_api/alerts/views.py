from django.shortcuts import render
from django.http import JsonResponse

def alert_list(request):
    return JsonResponse({'message': 'Alert list endpoint'})

def alert_detail(request, pk):
    return JsonResponse({'message': f'Alert detail {pk}'})
