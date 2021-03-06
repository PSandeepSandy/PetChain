# Generated by Django 2.0.7 on 2018-08-05 02:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex='^[1-9][0-9]{5}$')])),
                ('locality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('West Bengal', 'West Bengal'), ('Maharashtra', 'Maharashtra')], max_length=50)),
                ('landmark', models.CharField(blank=True, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('coins', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('age', models.IntegerField(blank=True)),
                ('weight', models.IntegerField(blank=True)),
                ('quantity', models.IntegerField(blank=True, default=1)),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ItemAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('attr_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.AttributeType')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Item')),
            ],
            options={
                'verbose_name_plural': 'ItemAtrributes',
            },
        ),
        migrations.CreateModel(
            name='ItemAttributeValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('attr_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.AttributeType')),
            ],
            options={
                'verbose_name_plural': 'ItemAttributeValues',
            },
        ),
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('image_1', models.CharField(blank=True, max_length=20)),
                ('image_2', models.CharField(blank=True, max_length=20)),
                ('image_3', models.CharField(blank=True, max_length=20)),
                ('image_4', models.CharField(blank=True, max_length=20)),
                ('image_5', models.CharField(blank=True, max_length=20)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Item')),
            ],
            options={
                'verbose_name_plural': 'ItemImages',
            },
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField()),
                ('total_price', models.IntegerField()),
                ('invoice', models.FileField(upload_to='')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Buyer')),
                ('buyer_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('APR', 'Approved'), ('SHP', 'Shipped'), ('DLV', 'Delivered')], default='APR', max_length=3)),
                ('invoice', models.FileField(upload_to='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Item')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Order')),
                ('seller_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Address')),
            ],
        ),
        migrations.AddField(
            model_name='itemattributevalues',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.Seller'),
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_market.ItemType'),
        ),
    ]
