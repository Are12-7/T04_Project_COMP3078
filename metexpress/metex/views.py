from django.shortcuts import render, redirect
from .models import Village, Debate, Message
from .forms import VillageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# REGISTER PAGE
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,
                           '''
                           Your password can’t be too similar to your other personal information.\n
                           Your password must contain at least 8 characters.\n
                           Your password can’t be a commonly used password.\n
                           Your password can’t be entirely numeric.
                           ''')

    return render(request, 'metex/registration.html', {'form': form})


# LOGIN PAGE
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # Check if user exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # Authenticating username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Does not exist
            messages.error(request, 'User email or Password Incorrect')

    data = {'page': page}
    return render(request, 'metex/registration.html', data)


# LOGOUT USER
def logoutUser(request):
    logout(request)
    return redirect('home')


# HOME PAGE
def home(request):
    # q = query for search option
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # find by name,
    villages = Village.objects.filter(
        Q(thread__topic__contains=q) |
        Q(description__icontains=q) |
        Q(title__icontains=q)
    )
    debates = Debate.objects.all()[:5]
    # Villages available
    village_count = villages.count()
    # Filtering discussions to be displayed when corresponds.
    village_discussions = Message.objects.filter(
        Q(village__thread__topic__icontains=q))

    data = {'villages': villages, 'debates': debates,
            'village_count': village_count, 'village_discussions': village_discussions}
    return render(request, 'metex/home.html', data)


# VILLAGE PAGE
def village(request, id):
    village = Village.objects.get(id=id)
    # get all messages associated with a village
    village_discussions = village.message_set.all()
    # Retrieving all sophists
    sophists = village.sophists.all()
    if request.method == 'POST':
        discussions = Message.objects.create(
            user=request.user,
            village=village,
            content=request.POST.get('content')
        )
        village.sophists.add(request.user)
        return redirect('village', id=village.id)

    data = {'village': village,
            'village_discussions': village_discussions, 'sophists': sophists}
    return render(request, 'metex/village.html', data)


# CREATE VILLAGE
@login_required(login_url='login')
def createVillage(request):
    form = VillageForm()
    if request.method == 'POST':
        form = VillageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    data = {'form': form}
    return render(request, 'metex/village_form.html', data)


# UPDATE VILLAGE
@login_required(login_url='login')
def updateVillage(request, id):
    village = Village.objects.get(id=id)
    form = VillageForm(instance=village)

    # Error message when a different user is trying to update other's user village
    if request.user != village.host:
        return HttpResponse('Sorry, you can not edit this village')

    if request.method == 'POST':
        form = VillageForm(request.POST, instance=village)
        if form.is_valid():
            form.save()
            return redirect('home')
    data = {'form': form}
    return render(request, 'metex/village_form.html', data)


# DELETE VILLAGE
@login_required(login_url='login')
def deleteVillage(request, id):
    village = Village.objects.get(id=id)
    # Error message when a different user is trying to delete other's user village
    if request.user != village.host:
        return HttpResponse('Sorry, you can not delete this village')

    if request.method == 'POST':
        village.delete()
        return redirect('home')
    return render(request, 'metex/delete.html', {'element': village})


# DELETE DISCUSSION/COMMENT/MESSAGE
# only authenticated users can delete
@login_required(login_url='login')
def deleteDiscussion(request, id):
    village_discussions = Message.objects.get(id=id)

    # Error message when a different user is trying to delete other's user village
    if request.user != village_discussions.user:
        return HttpResponse('Sorry, you can not delete this message')

    if request.method == 'POST':
        village_discussions.delete()
        return redirect('home')
    return render(request, 'metex/delete.html', {'obj': village_discussions})
