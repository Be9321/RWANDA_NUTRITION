import csv
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import MeasurementForm
from .ml import model_summary, predict_measurement
from .models import GrowthMeasurement


@login_required
@require_http_methods(['GET'])
def measurement_api(request):
    measurements = GrowthMeasurement.objects.select_related('child__household').order_by('-measurement_date', '-id')[:100]
    results = []
    for measurement in measurements:
        prediction = predict_measurement(measurement)
        results.append({
            'id': measurement.id,
            'child': measurement.child.full_name,
            'measurement_date': measurement.measurement_date.isoformat(),
            'weight_kg': float(measurement.weight_kg),
            'height_cm': float(measurement.height_cm),
            'muac_cm': float(measurement.muac_cm) if measurement.muac_cm is not None else None,
            'height_for_age_z': float(measurement.height_for_age_z) if measurement.height_for_age_z is not None else None,
            'prediction': prediction,
        })
    return JsonResponse({'count': len(results), 'model': model_summary(), 'results': results})


@login_required
@require_http_methods(['POST'])
def measurement_api_create(request):
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    form = MeasurementForm(payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)

    measurement = form.save(commit=False)
    measurement.measured_by = request.user
    measurement.save()
    return JsonResponse({
        'id': measurement.id,
        'message': 'Measurement created and scored successfully.',
        'prediction': predict_measurement(measurement),
    }, status=201)
@login_required
@require_http_methods(['GET'])
def measurement_csv(request):
    response = JsonResponse({}, status=200)
    response = __import__('django.http', fromlist=['HttpResponse']).HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nutrition_measurements.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'child', 'measurement_date', 'weight_kg', 'height_cm', 'muac_cm', 'height_for_age_z', 'predicted_risk', 'risk_probability'])
    measurements = GrowthMeasurement.objects.select_related('child').order_by('-measurement_date', '-id')
    for measurement in measurements:
        prediction = predict_measurement(measurement)
        writer.writerow([
            measurement.id,
            measurement.child.full_name,
            measurement.measurement_date,
            measurement.weight_kg,
            measurement.height_cm,
            measurement.muac_cm or '',
            measurement.height_for_age_z or '',
            prediction['risk_level'],
            prediction['probability'] or '',
        ])
    return response
