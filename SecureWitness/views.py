from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Crypto.Hash import SHA256
from django.contrib.auth import authenticate
from django.template import RequestContext, loader

from .models import Report, User

# Create your views here.


def index(request):
    return render(request, 'SecureWitness/index.html', {})


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        user_reports_list = Report.objects.filter(owner=user_id)
    except:
        user_reports_list = None
    context = {'user_reports_list': user_reports_list, "user": user}
    return render(request, 'SecureWitness/user.html', context)


def report(request, report_id):
    return render(request, 'SecureWitness/report.html', {})


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        verify = request.POST['verify_password']

        if password != verify:
            return render(request, 'SecureWitness/index.html', {'error_message': 'Passwords did not match.'})
        else:
            password = SHA256.new(b'password').hexdigest()
            new_user = User(name=name, email=email, password=password)
            new_user.save()
            return HttpResponseRedirect(reverse('user', args=(new_user.id,)))


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        hash_pass = SHA256.new(str.encode(password)).hexdigest()

        try:
            temp_user = User.objects.get(email=email)
            print("got user")
        except:
            print("wrong")
            return render(request, 'SecureWitness/index.html', {'error_message': "Invalid login."})

        if temp_user.password == hash_pass:
            print("logging in as " + temp_user.name)
            return HttpResponseRedirect(reverse('user', args=(temp_user.id,)))

        return render(request, 'SecureWitness/index.html', {})


def new_report(request, user_id):

    print(user_id)

    return render(request, 'SecureWitness/new_report.html', {'user_id': user_id})

def create_report(request, user_id):

    print(user_id)

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        short = request.POST['short_description']
        long = request.POST['long_description']
        private = False

        if 'private' in request.POST:
            private = request.POST['private']

        user = get_object_or_404(User, pk=user_id)

        try:
            user_reports_list = Report.objects.filter(owner=user_id)
        except:
            user_reports_list = None

        report_new = Report(title=title, author=author, short_description=short, long_description=long, private=private, owner=user)
        report_new.save()

        context = {'user_reports_list': user_reports_list, "user": user}

        return render(request, 'SecureWitness/user.html', context)

    return render(request, 'SecureWitness/user.html', {'create_error': 'Error in creating report'})