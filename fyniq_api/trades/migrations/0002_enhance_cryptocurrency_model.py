# Generated migration for enhanced cryptocurrency model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0001_initial'),
    ]

    operations = [
        # Update existing fields
        migrations.AlterField(
            model_name='cryptocurrency',
            name='symbol',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='current_price',
            field=models.DecimalField(decimal_places=12, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='market_cap',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='volume_24h',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='price_change_24h',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        
        # Add new fields
        migrations.AddField(
            model_name='cryptocurrency',
            name='coin_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='rank',
            field=models.PositiveIntegerField(db_index=True, default=999),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='circulating_supply',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=30),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='total_supply',
            field=models.DecimalField(blank=True, decimal_places=8, default=0, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='max_supply',
            field=models.DecimalField(blank=True, decimal_places=8, default=0, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='price_change_1h',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='price_change_7d',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='price_change_30d',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='price_change_1y',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='volume_change_24h',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='market_cap_change_24h',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='rsi_14',
            field=models.DecimalField(blank=True, decimal_places=2, default=50, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='ma_20',
            field=models.DecimalField(blank=True, decimal_places=12, default=0, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='ma_50',
            field=models.DecimalField(blank=True, decimal_places=12, default=0, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='blockchain_network',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='contract_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='decimals',
            field=models.PositiveIntegerField(blank=True, default=18, null=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='categories',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='tags',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='is_tradeable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='is_stablecoin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='data_source',
            field=models.CharField(default='coinmarketcap', max_length=50),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='last_updated_external',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]