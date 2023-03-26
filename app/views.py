from django.shortcuts import render

def caronas_disp(request):
    return render(request, 'app/caronas_disp.html', {})
