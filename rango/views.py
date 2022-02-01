from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

def index(request):
    # Query database for a list of all categories currently stored sorted by number of likes (descending), pick top 5
    category_list = Category.objects.order_by('-likes')[:5]

    # Create context dictionary containing the query results
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage' : 'This tutorial has been put together by Timo'}
    return render(request, 'rango/about.html', context=context_dict)
