from decimal import Decimal
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.market.models import Stock, HistoricalPrice
from apps.market.services import DEFAULT_STOCK_UNIVERSE

class Command(BaseCommand):
    help = 'Seeds the database with curated stocks from Indian NSE, US markets, ETFs, demo user, and baseline price records.'

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

        # 2. Seed / Update Stock Universe with Baseline Market Quotes
        created_count = 0
        updated_count = 0
        now = timezone.now()

        for symbol, info in DEFAULT_STOCK_UNIVERSE.items():
            base_price = Decimal(str(info.get('price', 100.0)))
            base_change = Decimal(str(info.get('change', 0.0)))
            base_change_pct = Decimal(str(info.get('change_pct', 0.0)))
            day_high = Decimal(str(info.get('high', float(base_price) * 1.01)))
            day_low = Decimal(str(info.get('low', float(base_price) * 0.99)))
            volume = int(info.get('volume', 1000000))

            stock, created = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': info['name'],
                    'sector': info['sector'],
                    'exchange': info['exchange'],
                    'country': info['country'],
                    'currency': info['currency'],
                    'last_price': base_price,
                    'last_change': base_change,
                    'last_change_pct': base_change_pct,
                    'day_high': day_high,
                    'day_low': day_low,
                    'volume': volume,
                    'last_updated': now,
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

            # Seed 45 days of baseline historical daily bars if none exist
            if stock.historical_prices.count() < 30:
                history_records = []
                current_p = float(base_price)
                today = now.date()
                for day_idx in range(45, 0, -1):
                    bar_date = today - datetime.timedelta(days=day_idx)
                    # Skip weekends
                    if bar_date.weekday() >= 5:
                        continue
                    # Slight organic variance
                    pct = ((day_idx * 7 + 13) % 9 - 4) * 0.004
                    bar_close = round(current_p * (1.0 + pct), 2)
                    bar_open = round(bar_close * 0.997, 2)
                    bar_high = round(max(bar_open, bar_close) * 1.006, 2)
                    bar_low = round(min(bar_open, bar_close) * 0.994, 2)
                    history_records.append(HistoricalPrice(
                        stock=stock,
                        date=bar_date,
                        open_price=Decimal(str(bar_open)),
                        high_price=Decimal(str(bar_high)),
                        low_price=Decimal(str(bar_low)),
                        close_price=Decimal(str(bar_close)),
                        volume=volume,
                        source='Curated Baseline Snapshot'
                    ))
                HistoricalPrice.objects.bulk_create(history_records, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded stocks: {created_count} created, {updated_count} updated with live baseline snapshots.'
            )
        )
