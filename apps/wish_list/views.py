
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Item
from ..validation.models import User

# Create your views here.
'''Display the wishlist home page'''
def home(request):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    user_id = int(request.session['user'])
    context = {
        'currentUser': User.objects.get(id=user_id),
        'userList': Item.objects.getUsersItems(user_id),
        'availItems': Item.objects.getAvailableItems(user_id)
    }
    return render(request, 'wish_list/index.html', context)

'''Calls method to add item from DB '''
def addItem(request):
    if request.method == 'POST':
        valItem = Item.objects.checkItem(request.POST)
        if valItem:
            item = Item.objects.makeItem(request.POST)
            print item.id
            Item.objects.addToList(request.POST['user_id'],item.id)
            return redirect(reverse('wishlist:home'))
        else:
            messages.error(request, 'Item must be two or more characters in length')
            return redirect(reverse('wishlist:create'))
    else:
        return redirect(reverse('wishlist:home'))

'''Calls metho to delete item from DB'''
def deleteItem (request, id):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    Item.objects.deleteItem(id)
    return redirect(reverse('wishlist:home'))

'''Calls method to add item to wishList'''
def addToList(request, id):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    Item.objects.addToList(request.session['user'], id)
    return redirect(reverse('wishlist:home'))

'''Calls method to add item to wishList'''
def removeFromList(request, id):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    Item.objects.removeFromList(request.session['user'], id)
    return redirect(reverse('wishlist:home'))

'''Renders page displaying item info'''
def item(request, id):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    context = {
        'users': Item.objects.getUsers(id)
    }
    return render(request, 'wish_list/item.html', context)

''''Renders page with form to add new item (POST --> editItem/add)'''
def create(request):
    try:
        request.session['user']
    except KeyError:
        messages.error(request, 'Must be logged in to view')
        return redirect(reverse('validation:login'))
    return render(request, 'wish_list/create.html')
