from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ChildForm
from .models import Child


class ChildListView(ListView):
    model = Child
    template_name = 'households/child_list.html'
    context_object_name = 'children'

    def get_queryset(self):
        return Child.objects.select_related('household__sector__district')


class ChildDetailView(DetailView):
    model = Child
    template_name = 'households/child_detail.html'


class ChildCreateView(SuccessMessageMixin, CreateView):
    model = Child
    form_class = ChildForm
    template_name = 'households/child_form.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child registered successfully.'


class ChildUpdateView(SuccessMessageMixin, UpdateView):
    model = Child
    form_class = ChildForm
    template_name = 'households/child_form.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child updated successfully.'


class ChildDeleteView(SuccessMessageMixin, DeleteView):
    model = Child
    template_name = 'households/child_confirm_delete.html'
    success_url = reverse_lazy('households:child_list')
    success_message = 'Child deleted.'