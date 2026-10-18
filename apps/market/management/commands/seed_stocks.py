from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.market.models import Stock
from apps.market.services import DEFAULT_STOCK_UNIVERSE

class Command(BaseCommand):
    help = 'Seeds the database with curated stocks from Indian NSE, US markets, ETFs, and default demo user.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Stock Universe & Demo Accounts...'))
        
        # 1. Ensure Demo Trader Account Exists
        demo_user, created_user = User.objects.get_or_create(
            username='demo_trader',
            defaults={
                'email': 'trader@stocksense.ai',
                'first_name': 'Demo',
                'last_name': 'Trader',
                'is_staff': True,
                'is_active': True,
            }
        )
        if created_user:
            demo_user.set_password('StockSense@2026')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user: 'demo_trader' / 'StockSense@2026'"))
        else:
            self.stdout.write(self.style.NOTICE("Demo user 'demo_trader' already exists."))

        # 2. Seed / Update Stock Universe
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
