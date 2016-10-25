from django.shortcuts import render


def index(request):
    context = {

    }
    return render(request, 'projects/photo/index.html', context)