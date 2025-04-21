from django.shortcuts import render
from .models import Pharmacy, Medicine, InventoryMed, MedList, ListItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import (
    login, logout, authenticate
)
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    context = {
        "user": request.user
    }
    return render(request, 'pmap/index.html', context)

# locate pharmacies
@login_required
def pharmacies(request):
    return render(request, 'pmap/pharmacies.html')

# manage medicines
@login_required
def medicines(request):
    return render(request, 'pmap/medicines.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'pmap/login_view.html')
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )
        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)
        login(request, user_object)
        return redirect('index')
    