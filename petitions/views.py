# petitions/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import PetitionForm
from .models import Petition, PetitionVote

class PetitionListView(ListView):
    model = Petition
    template_name = 'petitions/list.html'
    context_object_name = 'petitions'

class PetitionDetailView(DetailView):
    model = Petition
    template_name = 'petitions/detail.html'
    context_object_name = 'petition'

class PetitionCreateView(LoginRequiredMixin, CreateView):
    model = Petition
    form_class = PetitionForm
    template_name = 'petitions/create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('petitions:detail', args=[self.object.pk])

@login_required
def vote_yes(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    PetitionVote.objects.get_or_create(petition=petition, voter=request.user)
    return redirect('petitions:detail', pk=petition.pk)
