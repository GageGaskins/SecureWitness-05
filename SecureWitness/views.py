from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Crypto.Hash import SHA256
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Report, User, Document, Group, Comment, Folder
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
    user_folders = list(Folder.objects.filter(owner=user['id']))

    for folder in user_folders:
        for report in list(folder.reports.all()):
            user_reports_list = user_reports_list.exclude(pk=report.id)


    context = {'user_reports_list': user_reports_list, "user": user, 'groups': user_groups, 'folders': user_folders}
    return render(request, 'SecureWitness/user.html', context)


def group(request, group_id):
    curr_group = get_object_or_404(Group, pk=group_id)
    group_info = model_to_dict(curr_group)
    group_reports = curr_group.reports.all()

    user_info = request.session['curr_user']
    curr_user = get_object_or_404(User, pk=user_info['id'])

    share_reports = Report.objects.filter(owner=curr_user)

    for report in group_reports:
        share_reports = share_reports.exclude(pk=report.id)

    group_users = curr_group.users.exclude(pk=user_info['id'])

    add_users = User.objects.all()

    if user_info['admin_status']:
        add_users = add_users.exclude(pk=user_info['id'])

    filter_users = curr_group.users.all()

    for user in filter_users:
        add_users = add_users.exclude(pk=user.id)

    context = {'group': group_info, 'reports': group_reports, 'users': group_users, 'share_reports': share_reports,
               'add_users': add_users}
    return render(request, 'SecureWitness/group.html', context)


def group_share_report(request, group_id, report_id):
    shared_report = get_object_or_404(Report, pk=report_id)
    destination = get_object_or_404(Group, pk=group_id)

    destination.reports.add(shared_report)

    return HttpResponseRedirect(reverse('group', args=(group_id,)))


def group_add_user(request, group_id, user_id):
    new_member = get_object_or_404(User, pk=user_id)
    destination = get_object_or_404(Group, pk=group_id)

    destination.users.add(new_member)
    return HttpResponseRedirect(reverse('group', args=(group_id,)))


def folder_add_report_list(request, folder_id):

    user_info = request.session['curr_user']
    curr_user = User.objects.get(pk=user_info['id'])
    curr_folder = Folder.objects.get(pk=folder_id)
    folder_reports = list(curr_folder.reports.all())
    add_reports = curr_user.report_set.all()

    for folder in folder_reports:
        add_reports = add_reports.exclude(pk=folder.id)

    return render(request, 'SecureWitness/folder_add_report_list.html', {'reports': add_reports, 'folder': model_to_dict(curr_folder)})


def folder_remove_report_list(request, folder_id):
    curr_folder = Folder.objects.get(pk=folder_id)
    folder_reports = curr_folder.reports.all()

    return render(request, 'SecureWitness/folder_remove_report_list.html', {'reports': folder_reports, 'folder': model_to_dict(curr_folder)})


def folder_remove_report(request, folder_id, report_id):
    curr_folder = Folder.objects.get(pk=folder_id)
    removed_report = Report.objects.get(pk=report_id)
    curr_folder.reports.remove(removed_report)
    return HttpResponseRedirect(reverse('folder', args=(folder_id,)))


def folder_add_report(request, folder_id, report_id):

    curr_folder = Folder.objects.get(pk=folder_id)
    added_report = Report.objects.get(pk=report_id)

    curr_folder.reports.add(added_report)

    return HttpResponseRedirect(reverse('folder', args=(folder_id,)))


def folder(request, folder_id):

    folder = get_object_or_404(Folder, pk=folder_id)
    reports = folder.reports.all()

    curr_folder = model_to_dict(folder)
    return render(request, 'SecureWitness/folder.html', {'reports': reports, 'folder': curr_folder})


def manage_folders(request):
    user_info = request.session['curr_user']

    folders = get_object_or_404(User, pk=user_info['id']).folder_set.all()

    return render(request, 'SecureWitness/manage_folders.html', {'folders': folders})


def new_folder(request):
    return render(request, 'SecureWitness/new_folder.html', {})


def create_folder(request):

    user_info = request.session['curr_user']
    folder_name = request.POST['folder_name']
    new_folder = Folder(name=folder_name, owner=User.objects.get(pk=user_info['id']))
    new_folder.save()
    return HttpResponseRedirect(reverse('manage_folders'))


def edit_folder_page(request, folder_id):
    curr_folder = Folder.objects.get(pk=folder_id)

    return render(request, 'SecureWitness/edit_folder_page.html', {'folder': curr_folder})


def update_folder(request, folder_id):
    curr_folder = Folder.objects.get(pk=folder_id)
    curr_folder.name = request.POST['folder_name']
    curr_folder.save()

    return HttpResponseRedirect(reverse('folder', args=(folder_id,)))


def delete_folder(request, folder_id):

    curr_folder = Folder.objects.get(pk=folder_id)
    curr_folder.delete()

    return HttpResponseRedirect(reverse('manage_folders'))


def report(request, report_id):
    current_report = get_object_or_404(Report, pk=report_id)
    report_comments = Comment.objects.filter(report=report_id).order_by('timestamp')

    user = request.session['curr_user']
    context = {"report": current_report, 'user': user, 'comments': report_comments}
    return render(request, 'SecureWitness/report.html', context)


def reports(request):
    user_info = request.session['curr_user']
    curr_user = get_object_or_404(User, pk=user_info['id'])
    if user_info['admin_status']:
        all_reports = list(Report.objects.all())
        return render(request, 'SecureWitness/search.html', {'reports': all_reports})
    else:
        all_reports = list(Report.objects.filter(private=False))

    for report in list(curr_user.report_set.all()):
        if report not in all_reports:
            all_reports.append(report)

    for group in curr_user.group_set.all():
        for report in group.reports.all():
            if report not in all_reports:
                all_reports.append(report)

    return render(request, 'SecureWitness/search.html', {'reports': all_reports})


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

def delete_report(request, report_id):
    targetreport = get_object_or_404(Report, pk=report_id)
    targetreport.delete()
    return HttpResponseRedirect(reverse('user'))

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


def doc_list(request):
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

def manage_groups(request):

    all_groups = Group.objects.all()

    return render(request, 'SecureWitness/manage_groups.html', {'groups': all_groups})

def new_group(request):

    return render(request, 'SecureWitness/new_group.html', {})

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        new_group = Group(name=group_name)
        new_group.save()

        return HttpResponseRedirect(reverse('manage_groups'))
    return HttpResponseRedirect(reverse('manage_groups'))


def logout(request):
    request.session.flush()

    return HttpResponseRedirect(reverse('index'))

