from django.shortcuts import render

def home(request):
    return render(request, 'recipes/pages/home.html', status=200, context={
        'name': 'Jamal',
    })

