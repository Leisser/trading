from django.shortcuts import render
from django.http import JsonResponse

def order_list(request):
    return JsonResponse({'message': 'Order list endpoint'})

def order_detail(request, pk):
    return JsonResponse({'message': f'Order detail {pk}'})
