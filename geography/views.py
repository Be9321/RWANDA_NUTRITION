import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from households.models import Child
from nutrition.models import GrowthMeasurement
from .models import District


DEMO_DISTRICT_COORDINATES = {
    'Gasabo': (-1.90, 30.13), 'Kicukiro': (-2.00, 30.10),
    'Nyarugenge': (-1.95, 30.05), 'Burera': (-1.45, 29.75),
    'Gakenke': (-1.70, 29.78), 'Gicumbi': (-1.70, 30.08),
    'Musanze': (-1.50, 29.63), 'Rulindo': (-1.66, 29.99),
    'Gisagara': (-2.58, 29.75), 'Huye': (-2.60, 29.74),
    'Kamonyi': (-2.00, 29.88), 'Muhanga': (-2.08, 29.75),
    'Nyamagabe': (-2.48, 29.58), 'Nyanza': (-2.35, 29.75),
    'Nyaruguru': (-2.62, 29.57), 'Ruhango': (-2.23, 29.78),
    'Bugesera': (-2.20, 30.10), 'Gatsibo': (-1.65, 30.45),
    'Kayonza': (-1.80, 30.50), 'Kirehe': (-2.25, 30.65),
    'Ngoma': (-2.00, 30.40), 'Nyagatare': (-1.30, 30.33),
    'Rwamagana': (-1.95, 30.43), 'Karongi': (-2.05, 29.35),
    'Ngororero': (-1.87, 29.56), 'Nyabihu': (-1.62, 29.53),
    'Nyamasheke': (-2.35, 29.10), 'Rubavu': (-1.68, 29.27),
    'Rusizi': (-2.48, 28.90), 'Rutsiro': (-1.90, 29.32),
}


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
    points = []
    for d in District.objects.select_related('province'):
        stat = stats.get(d.pk)
        fallback_lat, fallback_lng = DEMO_DISTRICT_COORDINATES.get(d.name, (-1.95, 29.9))
        points.append({
            'name': d.name,
            'province': d.province.name,
            'lat': float(d.latitude) if d.latitude is not None else fallback_lat,
            'lng': float(d.longitude) if d.longitude is not None else fallback_lng,
            'rate': stat['rate'] if stat else None,
            'assessed': stat['assessed'] if stat else 0,
            'photo': d.photo.url if d.photo else '',
            'url': reverse('geography:district_detail', args=[d.pk]),
        })
    return render(request, 'geography/map.html', {'points': points, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


