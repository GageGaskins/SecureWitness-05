from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Crypto.Hash import SHA256
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Report, User, Document, Group, Comment
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

    user_groups = User.objects.get(pk=user['id']).group_set.all()

    context = {'user_reports_list': user_reports_list, "user": user, 'groups': user_groups}
    return render(request, 'SecureWitness/user.html', context)


def group(request, group_id):
    curr_group = get_object_or_404(Group, pk=group_id)
    group_info = model_to_dict(curr_group)
    group_reports = curr_group.reports.all()

    curr_user = request.session['curr_user']

    share_reports = Report.objects.all()

    for report in group_reports:
        share_reports = share_reports.exclude(pk=report.id)

    group_users = curr_group.users.exclude(pk=curr_user['id'])

    add_users = User.objects.all()
    filter_users = curr_group.users.all()

    for user in filter_users:
        add_users = add_users.exclude(pk=user.id)

    context = {'group': group_info, 'reports': group_reports, 'users': group_users, 'share_reports': share_reports,
               'add_users': add_users}
    return render(request, 'SecureWitness/group.html', context)


def group_share_report(request, group_id, report_id):
    shared_report = get_object_or_404(Report, pk=report_id)
    print(shared_report)
    destination = get_object_or_404(Group, pk=group_id)

    print(destination)

    destination.reports.add(shared_report)

    return HttpResponseRedirect(reverse('group', args=(group_id,)))


def group_add_user(request, group_id, user_id):
    new_member = get_object_or_404(User, pk=user_id)
    destination = get_object_or_404(Group, pk=group_id)

    destination.users.add(new_member)
    return HttpResponseRedirect(reverse('group', args=(group_id,)))

def add_to_folder(request, folder_id, report_id):
    filedreport = get_object_or_404(Report, pk=report_id)
    destination = get_object_or_404(Folder, pk=folder_id)

    filedreport.folder = destination
    return render(request, 'SecureWitness/user.html', {'create_error': 'Error in creating report'})


def report(request, report_id):
    current_report = get_object_or_404(Report, pk=report_id)
    report_comments = Comment.objects.filter(report=report_id).order_by('timestamp')

    user = request.session['curr_user']
    context = {"report": current_report, 'user': user, 'comments': report_comments}
    return render(request, 'SecureWitness/report.html', context)


def edit_report_page(request, report_id):
    current_report = get_object_or_404(Report, pk=report_id)

    return render(request, 'SecureWitness/edit_report_page.html', {'report': current_report})


def update_report(request, report_id):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        short = request.POST['short_description']
        long = request.POST['long_description']
        location = request.POST.get('location', "")
        keywords = request.POST.get('keywords', "")
        report_date = request.POST.get('report_date', "")
        private = False

        if 'private' in request.POST:
            private = request.POST['private']

        updated_report = Report.objects.get(pk=report_id)

        updated_report.title = title
        updated_report.author = author
        updated_report.short_description = short
        updated_report.long_description = long
        updated_report.location = location
        updated_report.keywords = keywords
        updated_report.report_date = report_date
        updated_report.private = private
        updated_report.save()

        return HttpResponseRedirect(reverse('report', args=(report_id,)))

    return HttpResponseRedirect(reverse('report', args=(report_id,)))


def make_comment(request, report_id):
    if request.method == "POST":
        comment_text = request.POST['comment_text']

        user_info = request.session['curr_user']
        curr_id = user_info['id']

        commenter = get_object_or_404(User, pk=curr_id)
        curr_report = get_object_or_404(Report, pk=report_id)

        comment = Comment(text=comment_text, report=curr_report, owner=commenter)
        comment.save()

        return HttpResponseRedirect(reverse('report', args=(report_id,)))

    return HttpResponseRedirect(reverse('report', args=(report_id,)))


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
            user_info = model_to_dict(new_user)
            request.session['curr_user'] = user_info
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
        else:
            return render(request, 'SecureWitness/index.html', {'login_error_message': "Invalid login."})


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
        query = request.POST['search'].lower()
        terms = query.split(" ")
        all_reports = Report.objects.all()
        returned_reports = []

        for report in all_reports:
            title = report.title.split(" ")
            title = [x.lower() for x in title]
            if set(terms).intersection(title):
                returned_reports.append(report)

    return render(request, 'SecureWitness/search.html', {'reports': returned_reports})


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

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


def make_admin_list(request):
    users = User.objects.filter(admin_status=False)
    return render(request, 'SecureWitness/make_admin_list.html', {'users': users})


def make_admin(request, user_id):
    new_admin = get_object_or_404(User, pk=user_id)
    print(new_admin.name)
    new_admin.admin_status = True
    new_admin.save()

    return HttpResponseRedirect(reverse('user'))


def logout(request):
    request.session.flush()

    return HttpResponseRedirect(reverse('index'))

