from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.utils import timezone

from households.models import Child
from .models import GrowthMeasurement, Referral


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