from django.shortcuts import render

def home(request):
    return render(request, 'recipes/pages/home.html', status=200)

def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', status=200)

