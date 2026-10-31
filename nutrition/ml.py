"""Training and inference helpers for the stunting-risk model."""

from datetime import date
from functools import lru_cache
from pathlib import Path

import joblib
from django.conf import settings

MODEL_PATH = Path(settings.BASE_DIR) / 'model_artifacts' / 'stunting_risk.joblib'
FEATURE_NAMES = (
    'age_months', 'weight_kg', 'height_cm', 'muac_cm',
    'sex_female', 'food_security_risk', 'sanitation_risk',
    'water_risk', 'income_risk',
)

FOOD_SECURITY_RISK = {'secure': 0, 'mild': 1, 'severe': 2}
SANITATION_RISK = {'improved': 0, 'basic': 1, 'none': 2}
WATER_RISK = {'piped': 0, 'unprotected': 1}
INCOME_RISK = {'high': 0, 'middle': 1, 'lower_mid': 2, 'low': 3}


def _age_in_months(date_of_birth, reference_date=None):
    today = reference_date or date.today()
    months = (today.year - date_of_birth.year) * 12 + today.month - date_of_birth.month
    if today.day < date_of_birth.day:
        months -= 1
    return max(months, 0)


def measurement_features(measurement):
    child = measurement.child
    household = child.household
    return [
        _age_in_months(child.date_of_birth, measurement.measurement_date),
        float(measurement.weight_kg),
        float(measurement.height_cm),
        float(measurement.muac_cm) if measurement.muac_cm is not None else -1.0,
        1 if child.sex == 'F' else 0,
        FOOD_SECURITY_RISK.get(household.food_security, 1),
        SANITATION_RISK.get(household.sanitation, 1),
        WATER_RISK.get(household.water_source, 1),
        INCOME_RISK.get(household.income_category, 2),
    ]


def training_rows():
    from .models import GrowthMeasurement

    measurements = GrowthMeasurement.objects.select_related('child__household').exclude(
        height_for_age_z__isnull=True
    )
    rows = []
    for measurement in measurements:
        rows.append((measurement_features(measurement), int(measurement.height_for_age_z < -2)))
    return rows


def _risk_label(probability):
    if probability >= 0.7:
        return 'High'
    if probability >= 0.4:
        return 'Moderate'
    return 'Low'


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def clear_model_cache():
    load_model.cache_clear()


def predict_measurement(measurement):
    bundle = load_model()
    if bundle is None:
        return {
            'available': False,
            'risk_level': 'Unavailable',
            'probability': None,
            'model_version': None,
        }

    probability = float(bundle['pipeline'].predict_proba([measurement_features(measurement)])[0][1])
    return {
        'available': True,
        'risk_level': _risk_label(probability),
        'probability': round(probability * 100, 1),
        'model_version': bundle.get('trained_at'),
    }


def model_summary():
    bundle = load_model()
    if bundle is None:
        return {
            'available': False,
            'accuracy': None,
            'sample_count': 0,
            'trained_at': None,
        }
    return {
        'available': True,
        'accuracy': bundle.get('accuracy'),
        'sample_count': bundle.get('sample_count', 0),
        'trained_at': bundle.get('trained_at'),
    }


def train_and_save_model():
    from datetime import datetime, timezone

    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    rows = training_rows()
    if len(rows) < 10:
        raise ValueError('At least 10 labelled growth measurements are required to train the model.')
    labels = [label for _, label in rows]
    if len(set(labels)) < 2:
        raise ValueError('Training data must contain both stunted and non-stunted examples.')

    features = [features for features, _ in rows]
    stratify = labels if min(labels.count(0), labels.count(1)) >= 2 else None
    if len(rows) >= 20 and stratify is not None:
        x_train, x_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.25, random_state=42, stratify=stratify
        )
    else:
        x_train, x_test, y_train, y_test = features, features, labels, labels

    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)),
    ])
    pipeline.fit(x_train, y_train)
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    predictions = pipeline.predict(x_test)

    metrics = {'accuracy': round(float(accuracy_score(y_test, predictions)) * 100, 1)}
    if len(set(y_test)) == 2:
        metrics['roc_auc'] = round(float(roc_auc_score(y_test, probabilities)), 3)

    bundle = {
        'pipeline': pipeline,
        'features': FEATURE_NAMES,
        'accuracy': metrics['accuracy'],
        'roc_auc': metrics.get('roc_auc'),
        'sample_count': len(rows),
        'trained_at': datetime.now(timezone.utc).isoformat(),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_PATH)
    clear_model_cache()
    return bundle