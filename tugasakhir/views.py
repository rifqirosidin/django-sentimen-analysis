from django.shortcuts import render
from . import scraping as process

def index(request):

    return render(request, 'index.html')


def store(request):
    if(request.method == "POST"):
        data = request.POST['value']               
        proses = process.sentimenAnalysis()
        proses.scrappingData(data=data)

    return render(request, 'store.html')  
    # return JsonResponse(data)


