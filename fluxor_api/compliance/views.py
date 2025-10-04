from django.shortcuts import render
from django.http import JsonResponse

def compliance_list(request):
    return JsonResponse({'message': 'Compliance list endpoint'})

def compliance_detail(request, pk):
    return JsonResponse({'message': f'Compliance detail {pk}'})
