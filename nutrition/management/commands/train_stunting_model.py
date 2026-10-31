from django.core.management.base import BaseCommand, CommandError

from nutrition.ml import train_and_save_model


class Command(BaseCommand):
    help = 'Train and save the stunting-risk prediction model from growth measurements.'

    def handle(self, *args, **options):
        try:
            bundle = train_and_save_model()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Trained model on {bundle['sample_count']} measurements; "
            f"validation accuracy: {bundle['accuracy']}%."
        ))