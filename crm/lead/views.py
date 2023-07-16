from typing import Any, Dict
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .forms import AddCommentForm
from .models import Lead

from team.models import Team


from client.models import Client

class LeadListView(ListView):
    model = Lead
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()

        return queryset.filter(created_by=self.request.user,converted_to_clients=False)

class LeadDetailView(DetailView):
    model = Lead
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()

        return context
    
    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Edit lead'
        return context
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add lead'
        return context

    def form_valid(self, form):
       
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()
        
        return redirect(self.get_success_url())

class ConvertToClientView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]

        client = Client.objects.create(
        name = lead.name,
        email = lead.email,
        description = lead.description,
        created_by=request.user,
        team=team,
    )
        lead.converted_to_clients = True
        lead.save()
        messages.success(request, 'The lead was converted to client.')

        return redirect('leads:list')

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)