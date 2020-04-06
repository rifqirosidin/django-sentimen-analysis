from django.shortcuts import render
from . import scraping as process
from django.http import JsonResponse


def index(request):

    return render(request, 'index.html')


def store(request):
    if(request.method == "POST"):
        data = request.POST['value']               
        proses = process.sentimenAnalysis()
        dataScrapping = proses.scrappingData(data=data)
  
    response = dataScrapping.to_dict()   
    return JsonResponse(response, safe=False)


