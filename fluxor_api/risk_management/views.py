from django.shortcuts import render
from django.http import JsonResponse

def risk_list(request):
    return JsonResponse({'message': 'Risk list endpoint'})

def risk_detail(request, pk):
    return JsonResponse({'message': f'Risk detail {pk}'})
