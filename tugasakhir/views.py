from django.shortcuts import render

def index(request):

    return render(request, 'index.html')


def store(request):

    if(request.method == "POST"):
        data = request.POST['data1']
        print(data)

        return render(request, 'index.html')  
