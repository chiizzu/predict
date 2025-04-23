from django.shortcuts import render
from . import get
from . import utils
from django.http import JsonResponse
import json

def index(request):
    harga = get.real_time_price
    prediksi = utils.predicted_price
    print(harga)
    context = {
        'harga' : harga,
        'predict' : prediksi,
        'trend': 'Initial',
        'initialPrice' : get.price
    }
    return render(request, 'index.html', context)

def Prediksi(request):
    prediksi = float(utils.predicted_price)
    prediksi = json.dumps(prediksi)
    return JsonResponse({'prediction': prediksi})
    

