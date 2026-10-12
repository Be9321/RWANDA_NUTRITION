from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ChildForm, HouseholdForm
from .models import Child, Household


# ---------- Child ----------
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


# ---------- Household ----------
class HouseholdListView(LoginRequiredMixin, ListView):
    model = Household
    template_name = 'households/household_list.html'
    context_object_name = 'households'

    def get_queryset(self):
        return Household.objects.select_related('sector__district')


class HouseholdDetailView(LoginRequiredMixin, DetailView):
    model = Household
    template_name = 'households/household_detail.html'


class HouseholdCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household registered successfully.'
    extra_context = {'heading': 'Register a household',
                     'cancel_url': reverse_lazy('households:household_list')}


class HouseholdUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household updated successfully.'
    extra_context = {'heading': 'Edit household',
                     'cancel_url': reverse_lazy('households:household_list')}


class HouseholdDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Household
    template_name = 'crud_confirm_delete.html'
    success_url = reverse_lazy('households:household_list')
    success_message = 'Household deleted.'
    extra_context = {'heading': 'Delete household',
                     'warning': 'All children in this household and their measurements will also be deleted.',
                     'cancel_url': reverse_lazy('households:household_list')}