import csv, io,datetime
from .forms import MsgForm, MemberForm
from django.shortcuts import render, redirect
from django.views.generic import (View, ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from . import models

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class IndexView(ListView):
    template_name = 'nursesApp/index.html'
    context_object_name = 'members'
    model = models.Member

    def get_queryset(self):
        return models.Member.objects.all()

class NurseshomeView(ListView):
    template_name = 'nursesApp/nurses.html'
    context_object_name = 'members'
    model = models.Member

    def get_queryset(self):
        return models.Member.objects.all()

class ContributorView(ListView):
    template_name = 'nursesApp/contributors.html'
    context_object_name = 'contributors'
    model = models.Contributor
    paginate_by = 100

    def get_queryset(self):
       return models.Contributor.objects.filter().order_by('-t')


class MemberView(ListView):
    template_name = 'nursesApp/members.html'
    context_object_name = 'members'
    model = models.Member
    paginate_by = 100

class WinnerView(TemplateView):
    template_name = 'nursesApp/winners.html'

class WinnerView(ListView):
    template_name = 'nursesApp/winners.html'
    context_object_name = 'winners'

    def get_queryset(self):
        return models.Contributor.objects.filter().order_by('-y')

class MemberUpdateView(UpdateView):
    model = models.Member
    form_class = MemberForm
    template_name='nursesApp/member_update.html'

class MemberDeleteView(DeleteView):
    model = models.Member
    success_url = reverse_lazy("nursesApp:members")


class MemberDetailView(DetailView):
    model = models.Member
    context_object_name = 'member_detail'
    template_name='nursesApp/member_detail.html'

    def get_context_data(self, *args, **kwargs):
        data = super(MemberDetailView,self).get_context_data(*args,**kwargs)
        getMember = data['member_detail']
        contrib = models.Contributor.objects.filter(name__iexact=getMember.name)
        if contrib.count() > 0:
            data['contrib'] = contrib[0]
            data['membe'] = models.Member.objects.filter(added_by=data['contrib'])
        return data

class CreatememberView(CreateView):
    template_name = 'nursesApp/create_member.html'
    form_class = MemberForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.save()
        return render(request,self.template_name,{'form':form,'message':'Submitted'})

class MsgView(CreateView):
    template_name = 'nursesApp/contactus.html'
    form_class = MsgForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.save()
        return render(request,self.template_name,{'form':form,'message':'Submitted'})


def member_upload(request):
    template = "nursesApp/member_upload.html"

    prompt = {
        'order': ''
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_str = io.StringIO(data_set)
    next(io_str)
    for column in csv.reader(io_str, delimiter=',', quotechar="|"):
        getDate = datetime.datetime.strptime(column[1], "%d-%m-%y").date()
        try:
            getContrib = models.Contributor.objects.get(name=column[2])
            models.Member.objects.create(
                name=column[0],
                joined_on=getDate,
                added_by=getContrib,
                nurse=column[3],
                position=column[4],
                url=column[5]
            )
        except models.Contributor.DoesNotExist:
            addContrib = models.Contributor.objects.create(name=column[2])
            models.Member.objects.create(
                name=column[0],
                joined_on=getDate,
                added_by=addContrib,
                nurse=column[3],
                position=column[4],
                url=column[5]
            )

    context = {}
    return render(request, template, context)

    def memberSearch(request):
        memberName = request.GET.get('member')
        data = models.Member.objects.filter(name__icontains=memberName)
        print(data)
        sendJson = serializers.serialize('json',data)
        return HttpResponse(sendJson)

    def updateContributorCount(request):
        print('Updating...')
        contributors = models.Contributor.objects.all()
        for contrib in contributors:
            getMembers = models.Member.objects.filter(added_by=contrib.contributor.name).count()
            print('{} added {} members'.format(contrib.contributor.name, getMembers))

        return redirect('/contributors')
