from django.core.management.base import BaseCommand
from apps.market.models import Stock
from apps.market.services import DEFAULT_STOCK_UNIVERSE

class Command(BaseCommand):
    help = 'Seeds the database with curated stocks from Indian NSE, US markets, and ETFs.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Stock Universe...'))
        created_count = 0
        updated_count = 0

        for symbol, info in DEFAULT_STOCK_UNIVERSE.items():
            stock, created = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': info['name'],
                    'sector': info['sector'],
                    'exchange': info['exchange'],
                    'country': info['country'],
                    'currency': info['currency'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded stocks: {created_count} created, {updated_count} updated.'
            )
        )
