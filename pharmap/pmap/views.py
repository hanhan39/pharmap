from django.shortcuts import render
from .models import Pharmacy, Medicine, InventoryMed, MedList, ListItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import (
    login, logout, authenticate
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now

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
    if request.method == 'GET':
        medlists = MedList.objects.filter(user=request.user)
        context = {
            "medlists": medlists,
            "user": request.user
        }
        return render(request, 'pmap/pharmacies.html', context)
    if request.method == 'POST':
        medlist_id = request.POST.get('medlist_id')
        return redirect(f"{reverse('results')}?medlist_id={medlist_id}")

@login_required
def results(request):
    medlist_id = request.GET.get('medlist_id')

    medicine_ids = set(
        ListItem.objects.filter(medlist_id=medlist_id).values_list('medicine_id', flat=True)
    )
    pharmacies = Pharmacy.objects.prefetch_related('inventorymed_set__medicine')
    results = []

    for pharmacy in pharmacies:
        matched_meds = [f"{item.medicine.brand} ({item.medicine.generic}) - PHP {item.price}" for item in pharmacy.inventorymed_set.all() if item.medicine_id in medicine_ids]

        if matched_meds:
            results.append({
                'pharmacy': pharmacy,
                'matched_medicines': matched_meds,
                'match_count': len(matched_meds),
            })

    context = {
        "user": request.user,
        "results": results,
    }

    return render(request, 'pmap/results.html', context)

@login_required
def medicines(request):
    if request.method == 'GET':
        medicines = Medicine.objects.all()
        medlists = MedList.objects.filter(user=request.user).prefetch_related('listitem_set__medicine')

        userdata = []

        for medlist in medlists:
            items = [item.medicine for item in medlist.listitem_set.all()]
            userdata.append({
                'medlist': medlist,
                'medicines': items,
            })

        context = {
            "user": request.user,
            "medicines": medicines,
            "medlists": userdata,
        }
        return render(request, 'pmap/medicines.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        medicine_ids = request.POST.getlist('medicines')

        if len(medicine_ids) == 0:
            return render(request, 'pmap/medicines.html', {
                'error': 'Please select at least one medicine',
                'medicines': Medicine.objects.all()
            })
        
        medlist = MedList.objects.create(
            name=name,
            user=request.user,
            created_at=now()
        )

        for med_id in medicine_ids:
            ListItem.objects.create(medlist=medlist, medicine_id=med_id)

        return redirect('pharmacies')

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

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'pmap/signup_view.html')
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_email = request.POST['email']
        submitted_password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if submitted_password != confirm_password:
            messages.add_message(request, messages.INFO, 'Passwords are not identical.')
            return redirect(request.path_info)
        elif User.objects.filter(username=submitted_username).exists() | User.objects.filter(email=submitted_email).exists():
            messages.add_message(request, messages.INFO, 'Invalid sign up. Username or email already exists.')
            return redirect(request.path_info)
        else:
            user = User.objects.create_user(submitted_username, submitted_email, submitted_password)
            user.save()
            return redirect('login_view')