from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ChildForm, HouseholdForm
from .models import Child, Household


class HouseholdListView(LoginRequiredMixin, ListView):
    model = Household
    template_name = 'households/household_list.html'
    context_object_name = 'households'

    def get_queryset(self):
        return Household.objects.select_related('sector__district__province').order_by('household_code')


class HouseholdDetailView(LoginRequiredMixin, DetailView):
    model = Household
    template_name = 'households/household_detail.html'


class HouseholdCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'households/household_form.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household registered successfully.'


class HouseholdUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'households/household_form.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household updated successfully.'


class HouseholdDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Household
    template_name = 'households/household_confirm_delete.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household deleted.'


class ChildListView(LoginRequiredMixin, ListView):
    model = Child
    template_name = 'households/child_list.html'
    context_object_name = 'children'

    def get_queryset(self):
        return Child.objects.select_related('household__sector__district')


class ChildDetailView(LoginRequiredMixin, DetailView):
    model = Child
    template_name = 'households/child_detail.html'


class ChildCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Child
    form_class = ChildForm
    template_name = 'households/child_form.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child registered successfully.'


class ChildUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Child
    form_class = ChildForm
    template_name = 'households/child_form.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child updated successfully.'


class ChildDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Child
    template_name = 'households/child_confirm_delete.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child deleted.'