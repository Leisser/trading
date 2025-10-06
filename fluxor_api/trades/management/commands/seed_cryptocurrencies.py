"""
Django management command to seed cryptocurrency data from JSON file.
"""
import json
import os
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from trades.models import Cryptocurrency


class Command(BaseCommand):
    help = 'Seed cryptocurrency data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='cryptocurrency_data.json',
            help='Path to the JSON file containing cryptocurrency data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing cryptocurrency data before seeding'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing cryptocurrencies with new data'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # If relative path, look in the fluxor_api directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.BASE_DIR, file_path)
        
        if not os.path.exists(file_path):
            raise CommandError(f'File "{file_path}" does not exist.')
        
        try:
            with open(file_path, 'r') as f:
                crypto_data = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON in file "{file_path}": {e}')
        
        if options['clear']:
            self.stdout.write('Clearing existing cryptocurrency data...')
            Cryptocurrency.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared cryptocurrency data.')
            )
        
        created_count = 0
        updated_count = 0
        
        for crypto in crypto_data:
            try:
                # Parse percentage changes
                def parse_percentage(change_str):
                    if change_str is None:
                        return Decimal('0')
                    if isinstance(change_str, str) and change_str.endswith('%'):
                        return Decimal(change_str[:-1])
                    return Decimal(str(change_str))
                
                # Create or update cryptocurrency
                crypto_obj, created = Cryptocurrency.objects.get_or_create(
                    symbol=crypto['symbol'],
                    defaults={
                        'name': crypto['name'],
                        'rank': crypto['rank'],
                        'current_price': Decimal(str(crypto['price_usd'])),
                        'market_cap': Decimal(str(crypto['market_cap_usd'])),
                        'volume_24h': Decimal(str(crypto['volume_24h_usd'])),
                        'circulating_supply': Decimal(str(crypto['circulating_supply'])),
                        'total_supply': Decimal(str(crypto.get('total_supply', 0))),
                        'price_change_1h': parse_percentage(crypto.get('change_1h')),
                        'price_change_24h': parse_percentage(crypto.get('change_24h')),
                        'price_change_7d': parse_percentage(crypto.get('change_7d')),
                        'price_change_30d': parse_percentage(crypto.get('change_30d')),
                        'categories': crypto.get('categories', []),
                        'is_stablecoin': crypto.get('is_stablecoin', False),
                        'is_featured': crypto.get('is_featured', False),
                        'blockchain_network': crypto.get('blockchain_network', ''),
                        'is_active': True,
                        'is_tradeable': True,
                        'data_source': 'manual_seed'
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {crypto_obj.symbol} - {crypto_obj.name}')
                elif options['update']:
                    # Update existing cryptocurrency
                    crypto_obj.name = crypto['name']
                    crypto_obj.rank = crypto['rank']
                    crypto_obj.current_price = Decimal(str(crypto['price_usd']))
                    crypto_obj.market_cap = Decimal(str(crypto['market_cap_usd']))
                    crypto_obj.volume_24h = Decimal(str(crypto['volume_24h_usd']))
                    crypto_obj.circulating_supply = Decimal(str(crypto['circulating_supply']))
                    crypto_obj.total_supply = Decimal(str(crypto.get('total_supply', 0)))
                    crypto_obj.price_change_1h = parse_percentage(crypto.get('change_1h'))
                    crypto_obj.price_change_24h = parse_percentage(crypto.get('change_24h'))
                    crypto_obj.price_change_7d = parse_percentage(crypto.get('change_7d'))
                    crypto_obj.price_change_30d = parse_percentage(crypto.get('change_30d'))
                    crypto_obj.categories = crypto.get('categories', [])
                    crypto_obj.is_stablecoin = crypto.get('is_stablecoin', False)
                    crypto_obj.is_featured = crypto.get('is_featured', False)
                    crypto_obj.blockchain_network = crypto.get('blockchain_network', '')
                    crypto_obj.save()
                    updated_count += 1
                    self.stdout.write(f'Updated: {crypto_obj.symbol} - {crypto_obj.name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {crypto.get("symbol", "unknown")}: {e}')
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding completed!\n'
                f'Created: {created_count} cryptocurrencies\n'
                f'Updated: {updated_count} cryptocurrencies\n'
                f'Total processed: {len(crypto_data)} cryptocurrencies'
            )
        )
