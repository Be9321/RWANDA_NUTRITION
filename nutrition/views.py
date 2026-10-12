from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from households.models import Child
from .forms import MeasurementForm, ProgramForm, EnrollmentForm, ReferralForm
from .models import GrowthMeasurement, Program, Enrollment, Referral


# ---------- Dashboard ----------
@login_required
def dashboard(request):
    today = timezone.localdate()

    # Latest height-for-age z-score of each child (subquery)
    latest = GrowthMeasurement.objects.filter(child=OuterRef('pk')).order_by('-measurement_date', '-id')
    children = Child.objects.select_related('household__sector__district').annotate(
        latest_z=Subquery(latest.values('height_for_age_z')[:1])
    )
    assessed = [c for c in children if c.latest_z is not None]
    stunted = [c for c in assessed if c.latest_z < -2]

    prevalence = round(len(stunted) * 100 / len(assessed), 1) if assessed else 0

    # Stunting rate per district (for the chart)
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


# ---------- Measurements ----------
class MeasurementListView(LoginRequiredMixin, ListView):
    model = GrowthMeasurement
    template_name = 'nutrition/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        return GrowthMeasurement.objects.select_related('child', 'measured_by')


class MeasurementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = GrowthMeasurement
    form_class = MeasurementForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('measurement_list')
    success_message = 'Measurement recorded successfully.'
    extra_context = {'heading': 'Record a growth measurement',
                     'cancel_url': reverse_lazy('measurement_list')}

    def form_valid(self, form):
        form.instance.measured_by = self.request.user
        return super().form_valid(form)


class MeasurementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GrowthMeasurement
    form_class = MeasurementForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('measurement_list')
    success_message = 'Measurement updated successfully.'
    extra_context = {'heading': 'Edit measurement',
                     'cancel_url': reverse_lazy('measurement_list')}


class MeasurementDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = GrowthMeasurement
    template_name = 'crud_confirm_delete.html'
    success_url = reverse_lazy('measurement_list')
    success_message = 'Measurement deleted.'
    extra_context = {'heading': 'Delete measurement',
                     'warning': 'This cannot be undone.',
                     'cancel_url': reverse_lazy('measurement_list')}


# ---------- Programs ----------
class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'nutrition/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.annotate(n_children=Count('enrollments'))


class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    template_name = 'nutrition/program_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.select_related('child__household')
        return context


class ProgramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('program_list')
    success_message = 'Program created successfully.'
    extra_context = {'heading': 'Add a nutrition program',
                     'cancel_url': reverse_lazy('program_list')}


class ProgramUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('program_list')
    success_message = 'Program updated successfully.'
    extra_context = {'heading': 'Edit program',
                     'cancel_url': reverse_lazy('program_list')}


class ProgramDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Program
    template_name = 'crud_confirm_delete.html'
    success_url = reverse_lazy('program_list')
    success_message = 'Program deleted.'
    extra_context = {'heading': 'Delete program',
                     'warning': 'All enrolments in this program will also be deleted.',
                     'cancel_url': reverse_lazy('program_list')}


# ---------- Enrolments (the many-to-many link) ----------
class EnrollmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'crud_form.html'
    success_message = 'Child enrolled successfully.'

    def get_program(self):
        return get_object_or_404(Program, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['program'] = self.get_program()
        return kwargs

    def form_valid(self, form):
        form.instance.program = self.get_program()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('program_detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.get_program()
        context['heading'] = f'Enroll a child in {program.name}'
        context['cancel_url'] = reverse('program_detail', args=[program.pk])
        return context


class EnrollmentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Enrollment
    template_name = 'crud_confirm_delete.html'
    success_message = 'Enrolment removed.'

    def get_success_url(self):
        return reverse('program_detail', args=[self.object.program_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Remove enrolment'
        context['warning'] = 'The child stays registered and keeps their measurements.'
        context['cancel_url'] = reverse('program_detail', args=[self.object.program_id])
        return context


# ---------- Referrals ----------
class ReferralListView(LoginRequiredMixin, ListView):
    model = Referral
    template_name = 'nutrition/referral_list.html'
    context_object_name = 'referrals'

    def get_queryset(self):
        return Referral.objects.select_related('child', 'facility')


class ReferralCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Referral
    form_class = ReferralForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('referral_list')
    success_message = 'Referral recorded successfully.'
    extra_context = {'heading': 'Refer a child to a health facility',
                     'cancel_url': reverse_lazy('referral_list')}

    def form_valid(self, form):
        form.instance.referred_by = self.request.user
        return super().form_valid(form)


class ReferralUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Referral
    form_class = ReferralForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('referral_list')
    success_message = 'Referral updated successfully.'
    extra_context = {'heading': 'Edit referral',
                     'cancel_url': reverse_lazy('referral_list')}


class ReferralDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Referral
    template_name = 'crud_confirm_delete.html'
    success_url = reverse_lazy('referral_list')
    success_message = 'Referral deleted.'
    extra_context = {'heading': 'Delete referral',
                     'warning': 'This cannot be undone.',
                     'cancel_url': reverse_lazy('referral_list')}


@login_required
@require_POST
def referral_set_status(request, pk, status):
    referral = get_object_or_404(Referral, pk=pk)
    if status not in dict(Referral.STATUS):
        messages.error(request, 'Unknown status.')
    else:
        referral.status = status
        referral.save(update_fields=['status'])
        messages.success(request, f'Referral marked as {referral.get_status_display().lower()}.')
    return redirect('referral_list')