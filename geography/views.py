import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from households.models import Child
from nutrition.models import GrowthMeasurement
from .models import District


def district_stats():
    """Stunting rate per district, from each child's latest z-score."""
    latest = GrowthMeasurement.objects.filter(child=OuterRef('pk')).order_by('-measurement_date', '-id')
    children = Child.objects.select_related('household__sector').annotate(
        latest_z=Subquery(latest.values('height_for_age_z')[:1]))
    counts = {}
    for c in children:
        if c.latest_z is None:
            continue
        d = c.household.sector.district_id
        entry = counts.setdefault(d, [0, 0])
        entry[0] += 1
        if c.latest_z < -2:
            entry[1] += 1
    stats = {}
    for d, (assessed, stunted) in counts.items():
        rate = round(stunted * 100 / assessed, 1)
        # prevalence bands: 30% or more very high, 20 to 30% high, below 20% lower
        badge = 'danger' if rate >= 30 else 'warning' if rate >= 20 else 'success'
        stats[d] = {'assessed': assessed, 'stunted': stunted, 'rate': rate, 'badge': badge}
    return stats


@login_required
def district_list(request):
    stats = district_stats()
    districts = District.objects.select_related('province')
    rows = [(d, stats.get(d.pk)) for d in districts]
    return render(request, 'geography/district_list.html', {'rows': rows})


@login_required
def district_detail(request, pk):
    district = get_object_or_404(District.objects.select_related('province'), pk=pk)
    context = {
        'district': district,
        'stats': district_stats().get(pk),
        'sectors': district.sectors.annotate(n_households=Count('households')),
    }
    return render(request, 'geography/district_detail.html', context)


@login_required
def district_map(request):
    stats = district_stats()
    data = {}
    for d in District.objects.select_related('province'):
        s = stats.get(d.pk)
        key = re.sub('[^a-z]', '', d.name.lower())
        data[key] = {
            'name': d.name,
            'province': d.province.name,
            'rate': s['rate'] if s else None,
            'assessed': s['assessed'] if s else 0,
            'photo': d.photo.url if d.photo else '',
            'url': reverse('geography:district_detail', args=[d.pk]),
        }
    return render(request, 'geography/map.html', {'district_data': data})