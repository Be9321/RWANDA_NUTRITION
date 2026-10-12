from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from households.models import Child
from .forms import GrowthMeasurementForm, ProgramForm, ReferralForm
from .models import GrowthMeasurement, Program, Referral


class GrowthMeasurementListView(LoginRequiredMixin, ListView):
    model = GrowthMeasurement
    template_name = 'nutrition/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        return GrowthMeasurement.objects.select_related('child__household__sector__district').order_by('-measurement_date')


class GrowthMeasurementDetailView(LoginRequiredMixin, DetailView):
    model = GrowthMeasurement
    template_name = 'nutrition/measurement_detail.html'


class GrowthMeasurementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = GrowthMeasurement
    form_class = GrowthMeasurementForm
    template_name = 'nutrition/measurement_form.html'
    success_url = reverse_lazy('nutrition:measurement_list')
    success_message = 'Measurement saved successfully.'


class GrowthMeasurementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GrowthMeasurement
    form_class = GrowthMeasurementForm
    template_name = 'nutrition/measurement_form.html'
    success_url = reverse_lazy('nutrition:measurement_list')
    success_message = 'Measurement updated successfully.'


class GrowthMeasurementDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = GrowthMeasurement
    template_name = 'nutrition/measurement_confirm_delete.html'
    success_url = reverse_lazy('nutrition:measurement_list')
    success_message = 'Measurement deleted.'


class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'nutrition/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.prefetch_related('children').order_by('-start_date')


class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    template_name = 'nutrition/program_detail.html'


class ProgramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'nutrition/program_form.html'
    success_url = reverse_lazy('nutrition:program_list')
    success_message = 'Program created successfully.'


class ProgramUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'nutrition/program_form.html'
    success_url = reverse_lazy('nutrition:program_list')
    success_message = 'Program updated successfully.'


class ProgramDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Program
    template_name = 'nutrition/program_confirm_delete.html'
    success_url = reverse_lazy('nutrition:program_list')
    success_message = 'Program deleted.'


class ReferralListView(LoginRequiredMixin, ListView):
    model = Referral
    template_name = 'nutrition/referral_list.html'
    context_object_name = 'referrals'

    def get_queryset(self):
        return Referral.objects.select_related('child__household__sector__district', 'facility__sector__district').order_by('-referral_date')


class ReferralDetailView(LoginRequiredMixin, DetailView):
    model = Referral
    template_name = 'nutrition/referral_detail.html'


class ReferralCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Referral
    form_class = ReferralForm
    template_name = 'nutrition/referral_form.html'
    success_url = reverse_lazy('nutrition:referral_list')
    success_message = 'Referral created successfully.'


class ReferralUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Referral
    form_class = ReferralForm
    template_name = 'nutrition/referral_form.html'
    success_url = reverse_lazy('nutrition:referral_list')
    success_message = 'Referral updated successfully.'


class ReferralDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Referral
    template_name = 'nutrition/referral_confirm_delete.html'
    success_url = reverse_lazy('nutrition:referral_list')
    success_message = 'Referral deleted.'


def dashboard(request):
    today = timezone.localdate()

    latest = GrowthMeasurement.objects.filter(child=OuterRef('pk')).order_by('-measurement_date', '-id')
    children = Child.objects.select_related('household__sector__district').annotate(
        latest_z=Subquery(latest.values('height_for_age_z')[:1])
    )
    assessed = [c for c in children if c.latest_z is not None]
    stunted = [c for c in assessed if c.latest_z < -2]

    prevalence = round(len(stunted) * 100 / len(assessed), 1) if assessed else 0

    totals = {}
    for c in assessed:
        name = c.household.sector.district.name
        t = totals.setdefault(name, [0, 0])
        t[0] += 1
        if c.latest_z < -2:
            t[1] += 1
    labels = sorted(totals)
    rates = [round(totals[d][1] * 100 / totals[d][0], 1) for d in labels]

    context = {
        'child_count': len(children),
        'prevalence': prevalence,
        'measured_this_month': GrowthMeasurement.objects.filter(
            measurement_date__year=today.year, measurement_date__month=today.month).count(),
        'open_referrals': Referral.objects.filter(status='open').count(),
        'high_risk': sorted(stunted, key=lambda c: c.latest_z)[:10],
        'chart_labels': labels,
        'chart_rates': rates,
    }
    return render(request, 'dashboard.html', context)