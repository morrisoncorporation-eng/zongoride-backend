from django.shortcuts import render

def rapidoc_view(request):
    return render(request, 'rapidoc.html')
