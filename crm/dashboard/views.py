from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lead.models import Lead
from client.models import Client
from team.models import Team

@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)[0]

    lead = Lead.objects.filter(team=team, converted_to_clients=False).order_by('-created_at')[0:5]
    client = Client.objects.filter(team=team).order_by('-created_at')[0:5]

    return render(request, 'dashboard/dashboard.html', {
        'leads' : lead,
        'clients' : client,
    })