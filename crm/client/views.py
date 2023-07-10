from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Client

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    context = {'clients': clients}

    return render(request, 'clients/clients_list.html',{
        'clients': clients
    })