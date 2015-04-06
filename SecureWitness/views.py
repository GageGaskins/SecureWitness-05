from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from .models import Report, User

# Create your views here.


def index(request):
    return render(request, 'SecureWitness/index.html', {})


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        user_reports_list = Report.objects.get(pk=user_id)
    except:
        user_reports_list = None
    context = {'user_reports_list': user_reports_list, "user": user}
    return render(request, 'SecureWitness/user.html', context)


def report(request, report_id):
    return render(request, 'SecureWitness/report.html',{})


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        verify = request.POST['verify_password']

        if password != verify:
            return render(request, 'SecureWitness/index.html', {'error_message': 'Passwords did not match.'})
        else:
            new_user = User(name=name, email='email@email.com', password=password)
            new_user.save()
            return HttpResponseRedirect(reverse('user', args=(new_user.id,)))