from django.shortcuts import render
from django.http import JsonResponse

def blockchain_list(request):
    return JsonResponse({'message': 'Blockchain list endpoint'})

def blockchain_detail(request, pk):
    return JsonResponse({'message': f'Blockchain detail {pk}'})
