from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'pmap/index.html')

# locate pharmacies
def pharmacies(request):
    return render(request, 'pmap/pharmacies.html')

# manage medicines
def medicines(request):
    return render(request, 'pmap/medicines.html')