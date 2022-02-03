from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import CategoryForm


def index(request):
    # Query database for a list of all categories currently stored sorted by number of likes (descending), pick top 5
    category_list = Category.objects.order_by('-likes')[:5]
    # Top 5 viewed pages
    page_list = Page.objects.order_by('-views')[:5]

    # Create context dictionary containing the query results
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage' : 'This tutorial has been put together by Timo'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Try to find a slug with the given name
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve the associated pages
        pages = Page.objects.filter(category=category)
        # Add result list to template context
        context_dict['pages'] = pages
        # Add category objet from db into context
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If specified category not found, do nothing
        context_dict['pages'] = None
        context_dict['category'] = None
    # Return rendered response
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # If form is valid, save to db
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        # If form is invalid
        else:
            print(form.errors)

    # render
    return render(request, 'rango/add_category.html', {'form' : form})
