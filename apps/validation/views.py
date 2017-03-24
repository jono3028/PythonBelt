from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
# from django.forms.models import model_to_dict
from models import User
# Create your views here.
'''Landing page w/ 2 forms (login and registration)'''
def index(request):
    return render(request, 'validation/index.html')

'''Call method to creat a new user or login user and enter session'''
def validateUser(request, route):
    if request.method == 'POST':
        if route == 'reg':
            print request.POST
            newUser = User.objects.newUser(request.POST)
        else:
            newUser = User.objects.validateUser(request.POST)
            print newUser
        if not newUser[1]:
            for x in range(len(newUser[0])):
                messages.error(request, newUser[0][x])
            return redirect(reverse('validation:login'))
        else:
            request.session['user'] =newUser[0].id
            return redirect(reverse('wishlist:home'))
    else:
        return redirect(reverse('validation:login'))

'''Call method to exit session'''
def logOut (request):
    request.session.clear()
    return redirect(reverse('validation:login'))
