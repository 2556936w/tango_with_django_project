from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


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


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # Check registration success
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # User form
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Profile form
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True

        # Else form is invalid
        else:
            print(user_form.errors, profile_form.errors)

    # Else request method is not POST
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render template
    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,})


def user_login(request):
    if request.method == 'POST':
        # Get information from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Log user in
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # Blank dictionary object
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
