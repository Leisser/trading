from django.shortcuts import render
from django.http import JsonResponse

def wallet_list(request):
    return JsonResponse({'message': 'Wallet list endpoint'})

def wallet_detail(request, pk):
    return JsonResponse({'message': f'Wallet detail {pk}'})
