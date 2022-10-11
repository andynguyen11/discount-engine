# Generated by Django 4.1.2 on 2022-10-11 03:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('active', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type', models.CharField(choices=[('percent', 'Percent off'), ('fixed', 'Dollars off'), ('bogo', 'Buy one get one')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Fixed',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='discounts.discount')),
                ('value', models.IntegerField()),
            ],
            bases=('discounts.discount',),
        ),
        migrations.CreateModel(
            name='Percent',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='discounts.discount')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
            ],
            bases=('discounts.discount',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='discounts.discount')),
                ('bo', models.CharField(max_length=10)),
                ('go', models.CharField(max_length=10)),
            ],
            bases=('discounts.discount',),
        ),
    ]