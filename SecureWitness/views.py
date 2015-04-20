from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Crypto.Hash import SHA256
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Report, User, Document
from .forms import DocumentForm

# Create your views here.


def index(request):
    return render(request, 'SecureWitness/index.html', {})


def user(request):
    user = request.session['curr_user']
    try:
        user_reports_list = Report.objects.filter(owner=user['id'])
    except:
        user_reports_list = None

    context = {'user_reports_list': user_reports_list, "user": user}
    return render(request, 'SecureWitness/user.html', context)


def report(request, report_id):

    current_report = get_object_or_404(Report, pk=report_id)

    return render(request, 'SecureWitness/report.html', {"report": current_report})


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
            request.session['curr_user'] = new_user
            return HttpResponseRedirect(reverse('user'))


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        hash_pass = SHA256.new(str.encode(password)).hexdigest()

        try:
            temp_user = User.objects.get(email=email)
        except:
            return render(request, 'SecureWitness/index.html', {'login_error_message': "Invalid login."})

        if temp_user.password == hash_pass:
            user_info = model_to_dict(temp_user)
            request.session['curr_user'] = user_info
            return HttpResponseRedirect(reverse('user'))

        return render(request, 'SecureWitness/index.html', {})


def new_report(request):

    return render(request, 'SecureWitness/new_report.html', {})


def create_report(request):

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        short = request.POST['short_description']
        long = request.POST['long_description']
        location = request.POST.get('location', "")
        keywords = request.POST.get('keywords', "")
        report_date = request.POST.get('report_date', "")
        private = False

        if 'private' in request.POST:
            private = True

        user_info = request.session['curr_user']
        curr_id = user_info['id']
        user = User.objects.get(pk=curr_id)

        report_new = Report(title=title, author=author, short_description=short, long_description=long, private=private,
                            location=location, keywords=keywords, report_date=report_date, owner=user)
        report_new.save()

        return HttpResponseRedirect(reverse('user'))

    return render(request, 'SecureWitness/user.html', {'create_error': 'Error in creating report'})


def search(request):
    if request.method == 'POST':
        query = request.POST['search']
        terms = query.split(" ")
        all_reports = Report.objects.all()
        returned_reports = []

        for report in all_reports:
            title = report.title.split(" ")
            if set(terms).intersection(title):
                returned_reports.append(report)

    return render(request, 'SecureWitness/search.html', {'reports': returned_reports})

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'SecureWitness/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def get_doc(request, docname):

    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + docname
    return response